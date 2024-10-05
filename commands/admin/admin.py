import asyncio
import sys
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup
from commands.admin.db import *
import config as cfg
from bot import bot

from assets.antispam import earning_msg
from assets.gettime import bonus_time, kazna_time
from commands.help import help_msg


class new_ads_state(StatesGroup):
    txt = State()


class Mailing(StatesGroup):
    mailing_text = State()
    mailing_conf = State()


async def new_ads(message, state: FSMContext, type=0):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if type == 0:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))
        await message.answer("⚙️ Введите новый текст рекламы ('-' чтобы удалить)\n\n"
                             "<i>Вы можете использовать HTML-теги для форматирования текста.</i>", reply_markup=keyboard)
        await new_ads_state.txt.set()
        return

    txt = message.text
    if txt == 'Отмена':
        await state.finish()
        await admin_menu(message)
        return

    txt = '' if txt == '-' else txt
    try:
        ads = txt.replace(r'\n', '\n')
        msg = '⚙️ Реклама в сообщениях удалена' if txt == '' else '⚙️ Установлен новый текст рекламы:\n\n' + ads
        await message.answer(msg, disable_web_page_preview=True)
        await upd_ads(txt)
    except:
        await message.answer('❌ Ошибка в разметке HTML')

    await state.finish()
    await admin_menu(message)
    

async def unloading(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='💾 Бд'), types.KeyboardButton(text='❗️ Ошибки'), types.KeyboardButton(text='📋 Логи')],
            [types.KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )

    await message.answer('<b>⚠️ Выберите файл для выгрузки:</b>', reply_markup=keyboard)


async def unloading_db(message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.chat.type != 'private':
        return

    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('users.db', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'🛡 Копия бд создана <blockquote>{time}</blockquote>')
        
        
async def unloading_errors(message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.chat.type != 'private':
        return

    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('commands/admin/bot_errors.txt', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'‼️ Ошибки бота на момент <blockquote>{time}</blockquote>')
        
        
async def unloading_logs(message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.chat.type != 'private':
        return

    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('commands/admin/logs.txt', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'📋 Логи бота на момент <blockquote>{time}</blockquote>')


async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='📣 Реклама'), types.KeyboardButton(text='🕹 Управление')],
            [types.KeyboardButton(text='✨ Промокоды'), types.KeyboardButton(text='📥 Выгрузка')],
            [types.KeyboardButton(text='🌟 Модули')]
        ],
        resize_keyboard=True
    )

    await message.answer('<b>👮‍♂️ Админ меню:</b>', reply_markup=keyboard)
    
    
async def ads_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='📍 Рассылка'), types.KeyboardButton(text='🪪 Текст рекламы')],
            [types.KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )

    await message.answer('<b>😇 Меню рекламы:</b>', reply_markup=keyboard)


async def control(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🛡 Пользователи"), types.KeyboardButton("💽 ОЗУ"))
    keyboard.add(types.KeyboardButton("👮 Вернуться в админ меню"))

    await message.answer('<b>🕹️ Меню управления:</b>', reply_markup=keyboard)


def sizeof_fmt(num):
    for unit in ['Б', 'КБ', 'МБ']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%.1f %s" % (num, 'ТБ')


async def RAM_control(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🗑 Очистить все", callback_data="ram-clear"))

    earning = sizeof_fmt(sys.getsizeof(earning_msg))
    help_menu = sizeof_fmt(sys.getsizeof(help_msg))
    bonus = sizeof_fmt(sys.getsizeof(bonus_time))
    kazna = sizeof_fmt(sys.getsizeof(kazna_time))

    await message.answer(f'''💽 Информация о использовании ОЗУ:
💸 Заработок: {earning}
🆘 Помощь: {help_menu}
🎁 Бонусы: {bonus}
💰 Казна: {kazna}''', reply_markup=keyboard)


async def RAM_clear(call: types.CallbackQuery):
    user_id = call.from_user.id
    if user_id not in cfg.admin:
        return

    global earning_msg, help_msg, bonus_time, kazna_time
    earning_msg.clear()
    help_msg.clear()
    bonus_time.clear()
    kazna_time.clear()

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🗑 Очищено!')


async def rassilka(message: types.Message):
    await Mailing.mailing_text.set()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Отмена"))
    await message.answer('📂 Пришлите мне готовое сообщение для рассылки:', reply_markup=keyboard)


async def process_rassilka(message, state: FSMContext):
    text = message.text
    if text == 'Отмена':
        await state.finish()
        await message.answer('Отменено.')
        await admin_menu(message)
        return

    inline_keyboard = None
    if message.reply_markup and message.reply_markup.inline_keyboard:
        inline_keyboard = message.reply_markup.inline_keyboard
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await state.update_data(text=text, inline_keyboard=inline_keyboard)
    await message.answer("✅ Сообщение сохранено.\nВы уверены что хотите начать рассылку? (да/нет)")
    await Mailing.mailing_conf.set()


async def process_rassilka2(message, state: FSMContext):
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

    dp.register_message_handler(control, lambda message: message.text == '🕹 Управление')
    dp.register_message_handler(RAM_control, lambda message: message.text == '💽 ОЗУ')
    dp.register_callback_query_handler(RAM_clear, text='ram-clear')
    
    dp.register_message_handler(ads_menu, lambda message: message.text == '📣 Реклама')
    dp.register_message_handler(new_ads, lambda message: message.text == '🪪 Текст рекламы')
    dp.register_message_handler(lambda message, state: new_ads(message, state, type=1), state=new_ads_state.txt)
    dp.register_message_handler(rassilka, lambda message: message.text == '📍 Рассылка')
    dp.register_message_handler(process_rassilka, state=Mailing.mailing_text)
    dp.register_message_handler(process_rassilka2, state=Mailing.mailing_conf)