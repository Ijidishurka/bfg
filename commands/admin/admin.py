import asyncio
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup

from assets.antispam import admin_only
from commands.admin import keyboards as kb
from commands.admin.db import *
from bot import bot


class new_ads_state(StatesGroup):
    txt = State()


class Mailing(StatesGroup):
    mailing_text = State()
    mailing_conf = State()


async def new_ads(message: types.Message, state: FSMContext, action=0):
    if action == 0:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))
        await message.answer("⚙️ Введите новый текст рекламы ('-' чтобы удалить)\n\n"
                             "<i>Вы можете использовать HTML-теги для форматирования текста.</i>", reply_markup=keyboard)
        await new_ads_state.txt.set()
        return

    if message.text == 'Отмена':
        await state.finish()
        await admin_menu(message)
        return

    message.text = '' if message.text == '-' else message.text
    try:
        ads = message.text.replace(r'\n', '\n')
        msg = '⚙️ Реклама в сообщениях удалена' if message.text == '' else '⚙️ Установлен новый текст рекламы:\n\n' + ads
        await message.answer(msg, disable_web_page_preview=True)
        await upd_ads(message.text)
    except:
        await message.answer('❌ Ошибка в разметке HTML')

    await state.finish()
    await admin_menu(message)
    

@admin_only(private=True)
async def unloading(message: types.Message):
    await message.answer('<b>⚠️ Выберите файл для выгрузки:</b>', reply_markup=kb.unloading_menu())


@admin_only(private=True)
async def unloading_db(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('users.db', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'🛡 Копия бд создана <blockquote>{time}</blockquote>')
        

@admin_only(private=True)
async def unloading_errors(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('commands/admin/bot_errors.txt', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'‼️ Ошибки бота на момент <blockquote>{time}</blockquote>')


@admin_only(private=True)
async def unloading_logs(message: types.Message):
    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('commands/admin/logs.txt', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'📋 Логи бота на момент <blockquote>{time}</blockquote>')


@admin_only(private=True)
async def admin_menu(message: types.Message):
    await message.answer('<b>👮‍♂️ Админ меню:</b>', reply_markup=kb.admin_menu())
    

@admin_only(private=True)
async def ads_menu(message: types.Message):
    await message.answer('<b>😇 Меню рекламы:</b>', reply_markup=kb.ads_menu())


@admin_only(private=True)
async def rassilka(message: types.Message):
    await Mailing.mailing_text.set()
    await message.answer('📂 Пришлите мне готовое сообщение для рассылки:', reply_markup=kb.cancel())


async def process_rassilka(message, state: FSMContext):
    if message.text == 'Отмена':
        await state.finish()
        await message.answer('Отменено.')
        await admin_menu(message)
        return

    inline_keyboard = None
    if message.reply_markup and message.reply_markup.inline_keyboard:
        inline_keyboard = message.reply_markup.inline_keyboard
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(text=message.text, inline_keyboard=inline_keyboard)
    await message.answer("✅ Сообщение сохранено.\nВы уверены что хотите начать рассылку? (да/нет)")
    await Mailing.mailing_conf.set()


async def process_rassilka2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()

    if message.text.lower() != 'да':
        await message.answer("Рассылка отменена.")
        return

    users, chats = await get_users_chats()

    ucount, uerror = 0, 0,
    ucount2, uerror2 = 0, 0

    await message.answer("✨ Рассылка запущена!")
    await admin_menu(message)

    for user_id in users:
        try:
            await bot.send_message(user_id[0], data['text'], reply_markup=data['inline_keyboard'])
            await asyncio.sleep(0.05)
            ucount += 1
        except:
            uerror += 1

    for chat_id in chats:
        try:
            await bot.send_message(chat_id[0], data['text'], reply_markup=data['inline_keyboard'])
            await asyncio.sleep(0.05)
            ucount2 += 1
        except:
            uerror2 += 1

    await message.answer(f'''📡 <b>Рассылка завершена.</b>
    
<i>Личные сообщения:</i>
  Получено: {ucount:,}
  Не получено: {uerror:,}

<i>Чаты:</i>
  Получено: {ucount2:,}
  Не получено: {uerror2:,}''')


def reg(dp: Dispatcher):
    dp.register_message_handler(admin_menu, commands='adm')
    dp.register_message_handler(admin_menu, lambda message: message.text == '🔙 Назад')
    
    dp.register_message_handler(unloading, lambda message: message.text == '📥 Выгрузка')
    dp.register_message_handler(unloading_logs, lambda message: message.text == '📋 Логи')
    dp.register_message_handler(unloading_errors, lambda message: message.text == '❗️ Ошибки')
    dp.register_message_handler(unloading_db, lambda message: message.text == '💾 Бд')
    
    dp.register_message_handler(ads_menu, lambda message: message.text == '📣 Реклама')
    dp.register_message_handler(new_ads, lambda message: message.text == '🪪 Текст рекламы')
    dp.register_message_handler(lambda message, state: new_ads(message, state, action=1), state=new_ads_state.txt)
    dp.register_message_handler(rassilka, lambda message: message.text == '📍 Рассылка')
    dp.register_message_handler(process_rassilka, state=Mailing.mailing_text)
    dp.register_message_handler(process_rassilka2, state=Mailing.mailing_conf)