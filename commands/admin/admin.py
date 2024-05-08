from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from commands.db import register_users, getname, getads, getonlibalance, getstatus, getidname, getstatus
from commands.admin.admin_db import *
from commands.main import geturl
from commands.main import win_luser
import config as cfg
from commands.admin.loger import new_log
from bot import bot, dp


class new_ads_state(StatesGroup):
    txt = State()


async def give_money(message):
    user_id = message.from_user.id
    status = await getstatus(user_id)
    if user_id not in cfg.admin and status == 0:
        return await message.answer('👮‍♂️ Вы не являетесь администратором бота чтобы использовать данную команду.\nДля покупки введи команду "Донат"')

    user_name = await getidname(user_id)
    rwin, rloser = await win_luser()
    url = await geturl(user_id, user_name)

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_user_name = await getidname(r_user_id)
        r_url = await geturl(r_user_id, r_user_name)
    except:
        return await message.answer(f'{url}, чтобы выдать деньги нужно ответить на сообщение пользователя {rloser}')

    try:
        su = message.text.split()[1]
        su = (su).replace('к', '000').replace('м', '000000').replace('.', '')
        summ = int(su)
        summ2 = '{:,}'.format(summ).replace(',', '.')
    except:
        return await message.answer(f'{url}, вы не ввели сумму которую хотите выдать {rloser}')

    if user_id in cfg.admin:
        await give_money_db(user_id, r_user_id, summ, 'rab')
        await message.answer(f'{url}, вы выдали {summ2}$ пользователю {r_url}  {rwin}')
    else:
        res = await give_money_db(user_id, r_user_id, summ, 'adm')
        if res == 'limit':
            return await message.answer(f'{url}, вы достигли лимита на выдачу денег  {rloser}')

        await message.answer(f'{url}, вы выдали {summ2}$ пользователю {r_url}  {rwin}')
    await new_log(f'#выдача\nПользователь {user_name} ({user_id})\nСумма: {summ2}$\nПользователю {r_user_name} ({r_user_id})', 'issuance_money')


async def give_bcoins(message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    user_name = await getidname(user_id)
    rwin, rloser = await win_luser()
    url = await geturl(user_id, user_name)

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_user_name = await getidname(r_user_id)
        r_url = await geturl(r_user_id, r_user_name)
    except:
        return await message.answer(f'{url}, чтобы выдать деньги нужно ответить на сообщение пользователя {rloser}')

    try:
        su = message.text.split()[1]
        su = (su).replace('к', '000').replace('м', '000000').replace('.', '')
        summ = int(su)
        summ2 = '{:,}'.format(summ).replace(',', '.')
    except:
        return await message.answer(f'{url}, вы не ввели сумму которую хотите выдать {rloser}')

    await give_bcoins_db(r_user_id, summ)
    await message.answer(f'{url}, вы выдали {summ2}💳 пользователю {r_url}  {rwin}')
    await new_log(f'#бкоин-выдача\nАдмин {user_name} ({user_id})\nСумма: {summ2}$\nПользователю {r_user_name} ({r_user_id})', 'issuance_bcoins')


async def new_ads(message, state: FSMContext, type=0):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if type == 0:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))
        await message.answer("⚙️ Введите новый текст рекламы ('-' чтобы удалить)\n\n<i>Вы можете использовать HTML-теги для форматирования текста.</i>", reply_markup=keyboard)
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


async def unloading(message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.chat.type != 'private':
        return

    time = datetime.now().strftime("%Y-%m-%d в %H:%M:%S")
    with open('users.db', 'rb') as file:
        await bot.send_document(message.chat.id, file, caption=f'🛡 Копия бд создана <blockquote>{time}</blockquote>')


async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='📍 Рассылка'), types.KeyboardButton(text='🕹 Управление')],
            [types.KeyboardButton(text='✨ Промокоды'), types.KeyboardButton(text='📥 Выгрузка')],
            [types.KeyboardButton(text='⚙️ Изменить текст рекламы')]
        ],
        resize_keyboard=True
    )

    await message.answer('<b>👮‍♂️ Админ меню:</b>', reply_markup=keyboard)


@dp.message_handler(commands='adm')
async def admin_menu_s(message: types.Message):
    await admin_menu(message)


@dp.message_handler(lambda message: message.text.lower().startswith('бдать'))
async def give_bcoins_s(message: types.Message):
    await give_bcoins(message)


@dp.message_handler(lambda message: message.text == '📥 Выгрузка')
async def unloading_s(message: types.Message):
    await unloading(message)


@dp.message_handler(lambda message: message.text == '⚙️ Изменить текст рекламы')
async def edit_ads_s(message: types.Message, state: FSMContext):
    await new_ads(message, state=state)


@dp.message_handler(state=new_ads_state.txt)
async def edit_ads_s(message: types.Message, state: FSMContext):
    await new_ads(message, state=state, type=1)