from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from commands.admin.admin import admin_menu
from commands.db import getads
from commands.admin.admin_db import *
from commands.main import win_luser
import config as cfg
from commands.admin.loger import new_log
from bot import dp
from assets.antispam import antispam


class new_promo_state(StatesGroup):
    name = State()
    summ = State()
    activ = State()


class dell_promo_state(StatesGroup):
    name = State()


async def promo_menu(message: types.message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📖 Создать промо"), types.KeyboardButton("🗑 Удалить промо"))
    keyboard.add(types.KeyboardButton("ℹ️ Промо инфо"))
    keyboard.add(types.KeyboardButton("👮 Вернуться в админ меню"))
    await message.answer('👾 Выберите действие:', reply_markup=keyboard)


async def new_promo(message, state: FSMContext, type='name'):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))

        await message.answer("😄 Введите название промо", reply_markup=keyboard)
        await new_promo_state.name.set()
        return

    if type == 'summ':
        await state.update_data(name=message.text.split()[0])
        await message.answer("😃 Введите сумму $ за активацию")
        await new_promo_state.summ.set()
        return

    try:
        summ = message.text.split()[0]
        summ = (summ).replace('к', '000').replace('м', '000000').replace('.', '')
        summ = int(summ)
    except:
        await message.answer("😔 Значение должно быть числом...")
        return

    if type == 'activ':
        await state.update_data(summ=summ)
        await message.answer("😊 Введите количество активаций")
        await new_promo_state.activ.set()
        return

    await state.update_data(activ=summ)
    data = await state.get_data()
    await state.finish()

    data2 = (data['name'], data['summ'], data['activ'])
    if (await new_promo_db(data2)):
        await message.answer("⚠️ Промокод с таким названием уже существует.")
        await admin_menu(message)
        return

    summ = '{:,}'.format(data['summ']).replace(',', '.')
    summ2 = '{:,}'.format(data['summ'] * data['activ']).replace(',', '.')
    activ = '{:,}'.format(data['activ']).replace(',', '.')

    await message.answer(f'''🎰 Вы успешно создали промокод:\n
Название: <code>{data['name']}</code>
Сумма: {summ}$
Активаций: {activ}\n
Общая сумма: {summ2}$''')
    await admin_menu(message)


async def dell_promo(message, state: FSMContext, type='name'):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))

        await message.answer("🗑 Введите название промо который вы хотите удалить", reply_markup=keyboard)
        await dell_promo_state.name.set()
        return

    name = message.text.split()[0]
    res = await dell_promo_db(name)
    if res:
        await message.answer(f"❌ Промокод <b>{name}</b> не найден.")
    else:
        await message.answer(f"✅ Промокод <b>{name}</b> успешно удалён!")
    await state.finish()
    await promo_menu(message)


@antispam
async def activ_promo(message: types.Message):
    rwin, rloser = await win_luser()
    ads = await getads()
    if len(message.text.split()) < 2:
        await message.answer(f"Вы не ввели промокод {rloser}")
        return

    name = message.text.split()[1]
    res = await activ_promo_db(name, message.from_user.id)

    if res == 'no promo':
        await message.answer(f'Данного промокода не существует {rloser}\n\n{ads}', disable_web_page_preview=True)
        return

    if res == 'activated':
        await message.answer(f'Данный промокд уже активирован {rloser}\n\n{ads}', disable_web_page_preview=True)
        return

    if res == 'used':
        await message.answer(f'Вы уже активировали этот промокод {rloser}\n\n{ads}', disable_web_page_preview=True)
        return

    summ = '{:,}'.format(res).replace(',', '.')
    await new_log(f'#промоактив\nИгрок: {message.from_user.id}\nПромо: {name}\nСумма: {summ}$', 'promo')
    await message.answer(f"Вы активировали промокод на сумму {summ}$ {rwin}")


@dp.message_handler(lambda message: message.text == '✨ Промокоды')
async def promo_menu_s(message: types.Message):
    await promo_menu(message)


@dp.message_handler(lambda message: message.text == '👮 Вернуться в админ меню')
async def backto_adm_menu(message: types.Message):
    await admin_menu(message)


@dp.message_handler(lambda message: message.text == '📖 Создать промо')
async def new_promo_s(message: types.Message, state: FSMContext):
    await new_promo(message, state=state)


@dp.message_handler(state=new_promo_state.name)
async def new_promo_s(message: types.Message, state: FSMContext):
    await new_promo(message, state=state, type='summ')


@dp.message_handler(state=new_promo_state.summ)
async def new_promo_s(message: types.Message, state: FSMContext):
    await new_promo(message, state=state, type='activ')


@dp.message_handler(state=new_promo_state.activ)
async def new_promo_s(message: types.Message, state: FSMContext):
    await new_promo(message, state=state, type='finish')


@dp.message_handler(lambda message: message.text == '🗑 Удалить промо')
async def dell_promo_s(message: types.Message, state: FSMContext):
    await dell_promo(message, state=state)


@dp.message_handler(state=dell_promo_state.name)
async def dell_promo_s(message: types.Message, state: FSMContext):
    await dell_promo(message, state=state, type='finish')


@dp.message_handler(lambda message: message.text.lower().startswith('промо'))
async def activ_promo_s(message: types.Message):
    await activ_promo(message)