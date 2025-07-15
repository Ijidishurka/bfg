import asyncio
from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters.custom import TextIn
from states.admin import NewAdvState, MailingState
from commands.admin import keyboards as kb
from assets.antispam import admin_only
from commands.admin.db import *
from bot import bot


@admin_only(private=True)
async def new_ads(message: types.Message, state: FSMContext, action=0):
    if action == 0:
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text="Отмена"))
        keyboard = builder.as_markup(resize_keyboard=True)

        await message.answer(
            text="⚙️ Введите новый текст рекламы ('-' чтобы удалить)\n\n"
                 "<i>Вы можете использовать HTML-теги для форматирования текста.</i>",
            reply_markup=keyboard
        )

        await NewAdvState.txt.set()
        return

    if message.text == "Отмена":
        await state.clear()
        await admin_menu_cmd(message)
        return

    message.text = "" if message.text == "-" else message.text
    try:
        ads = message.text.replace(r"\n", "\n")
        text = "⚙️ Реклама в сообщениях удалена" if message.text == "" else "⚙️ Установлен новый текст рекламы:\n\n" + ads
        await message.answer(text=text, disable_web_page_preview=True)
        await upd_ads(message.text)
    except:
        await message.answer(text="❌ Ошибка в разметке HTML")

    await state.clear()
    await admin_menu_cmd(message)
    

@admin_only(private=True)
async def unloading_cmd(message: types.Message):
    await message.answer(text="<b>⚠️ Выберите файл для выгрузки:</b>", reply_markup=kb.unloading_menu())


@admin_only(private=True)
async def unloading_db_cmd(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open("users.db", "rb") as file:
        await bot.send_document(chat_id=message.chat.id, document=file, caption=f"🛡 Копия бд создана <blockquote>{time}</blockquote>")
        

@admin_only(private=True)
async def unloading_errors_cmd(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open("bot_errors.txt", "rb") as file:
        await bot.send_document(chat_id=message.chat.id, document=file, caption=f"‼️ Ошибки бота на момент <blockquote>{time}</blockquote>")


@admin_only(private=True)
async def unloading_logs_cmd(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open("logs.txt", "rb") as file:
        await bot.send_document(chat_id=message.chat.id, document=file, caption=f"📋 Логи бота на момент <blockquote>{time}</blockquote>")


@admin_only(private=True)
async def admin_menu_cmd(message: types.Message):
    await message.answer(text="<b>👮‍♂️ Админ меню:</b>", reply_markup=kb.admin_menu())


@admin_only(private=True)
async def close_menu_cmd(message: types.Message):
    await message.answer(text="✅ <b>Админ меню закрыто!</b>", reply_markup=ReplyKeyboardRemove())
    

@admin_only(private=True)
async def ads_menu_cmd(message: types.Message):
    await message.answer(text="<b>😇 Меню рекламы:</b>", reply_markup=kb.ads_menu())


@admin_only(private=True)
async def mailing_cmd(message: types.Message):
    await MailingState.mailing_text.set()
    await message.answer(text="📂 Пришлите мне готовое сообщение для рассылки:", reply_markup=kb.cancel())


async def process_mailing(message, state: FSMContext):
    if message.text == "Отмена":
        await state.clear()
        await message.answer("Отменено.")
        await admin_menu_cmd(message)
        return

    inline_keyboard = None
    if message.reply_markup and message.reply_markup.inline_keyboard:
        inline_keyboard = message.reply_markup.inline_keyboard
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(text=message.text, inline_keyboard=inline_keyboard)
    await message.answer(text="✅ Сообщение сохранено.\nВы уверены что хотите начать рассылку? (да/нет)")
    await MailingState.mailing_conf.set()


async def process_mailing_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    if message.text.lower() != "да":
        await message.answer("Рассылка отменена.")
        return

    users, chats = await get_users_chats()

    ucount, uerror = 0, 0,
    ucount2, uerror2 = 0, 0

    await message.answer("✨ Рассылка запущена!")
    await admin_menu_cmd(message)

    for user_id in users:
        try:
            await bot.send_message(chat_id=user_id[0], text=data["text"], reply_markup=data["inline_keyboard"])
            await asyncio.sleep(0.025)
            ucount += 1
        except:
            uerror += 1

    for chat_id in chats:
        try:
            await bot.send_message(chat_id=chat_id[0], text=data["text"], reply_markup=data["inline_keyboard"])
            await asyncio.sleep(0.025)
            ucount2 += 1
        except:
            uerror2 += 1

    await message.answer(text=f"""📡 <b>Рассылка завершена.</b>
    
<i>Личные сообщения:</i>
  Получено: {ucount:,}
  Не получено: {uerror:,}

<i>Чаты:</i>
  Получено: {ucount2:,}
  Не получено: {uerror2:,}""")


def reg(dp: Dispatcher):
    dp.message.register(admin_menu_cmd, Command("adm"))
    dp.message.register(admin_menu_cmd, TextIn("🔙 Назад"))
    dp.message.register(close_menu_cmd, TextIn("🔙 Закрыть меню"))

    
    dp.message.register(unloading_cmd, TextIn("📥 Выгрузка"))
    dp.message.register(unloading_logs_cmd, TextIn("📋 Логи"))
    dp.message.register(unloading_errors_cmd, TextIn("❗️ Ошибки"))
    dp.message.register(unloading_db_cmd, TextIn("💾 Бд"))
    
    dp.message.register(ads_menu_cmd, TextIn("📣 Реклама"))
    dp.message.register(new_ads, TextIn("🪪 Текст рекламы"))
    dp.message.register(lambda message, state: new_ads(message, state, action=1), NewAdvState.txt)
    dp.message.register(mailing_cmd, TextIn("📍 Рассылка"))
    dp.message.register(process_mailing, MailingState.mailing_text)
    dp.message.register(process_mailing_2, MailingState.mailing_conf)
