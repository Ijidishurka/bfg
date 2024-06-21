from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from commands.admin.admin import admin_menu
from commands.db import getads, url_name
from commands.admin.db import *
from commands.main import win_luser
from commands.admin.loger import new_log
from assets.antispam import antispam


class new_promo_state(StatesGroup):
    name = State()
    summ = State()
    activ = State()
    txt = State()


class dell_promo_state(StatesGroup):
    name = State()


class promo_info_state(StatesGroup):
    name = State()


async def promo_menu(message: types.Message):
    if message.chat.type != 'private':
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📖 Создать промо"), types.KeyboardButton("🗑 Удалить промо"))
    keyboard.add(types.KeyboardButton("ℹ️ Промо инфо"))
    keyboard.add(types.KeyboardButton("👮 Вернуться в админ меню"))
    await message.answer('👾 Выберите действие:', reply_markup=keyboard)


async def new_promo(message, state: FSMContext, type='name'):
    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))

        await message.answer("😄 Введите название промо", reply_markup=keyboard)
        await new_promo_state.txt.set()
        return

    if type == 'txt':
        await state.update_data(name=message.text.split()[0])
        await message.answer("📟 Введите валюту которую будет выдавать промокод (таблица/столбик эмодзи)\n\n"
                             "Пример для промо на йены: <code>users/yen 💴</code>\n\n"
                             "<i>Для создания промокода на деньги используйте '-'</i>")
        await new_promo_state.name.set()
        return

    if type == 'summ':
        txt = 'users/balance $' if message.text == '-' else message.text
        await state.update_data(txt=txt)
        await message.answer("😃 Введите сумму $ за активацию")
        await new_promo_state.summ.set()
        return

    try:
        summ = message.text.split()[0].replace('е', 'e')
        summ = int(float(summ))
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

    data2 = (data['name'], data['summ'], data['activ'], data['txt'])
    if (await new_promo_db(data2)):
        await message.answer("⚠️ Промокод с таким названием уже существует.")
        await admin_menu(message)
        return

    summ = '{:,}'.format(data['summ']).replace(',', '.')
    summ2 = '{:,}'.format(data['summ'] * data['activ']).replace(',', '.')
    activ = '{:,}'.format(data['activ']).replace(',', '.')
    emj = ' '.join(data['txt'].split()[1:])

    await message.answer(f'''🎰 Вы успешно создали промокод:\n
Название: <code>{data['name']}</code>
Сумма: {summ}{emj}
Активаций: {activ}\n
Общая сумма: {summ2}{emj}''')
    await admin_menu(message)


async def promo_info(message, state: FSMContext, type='name'):
    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Отмена"))

        await message.answer("💻 Введите название промо", reply_markup=keyboard)
        await promo_info_state.name.set()
        return

    name = message.text.split()[0]
    res = await promo_info_db(name)
    if not res:
        await message.answer(f"❌ Промокод <b>{name}</b> не найден.")
    else:
        summ = '{:,}'.format(int(res[1])).replace(',', '.')
        emj = ' '.join(res[3].split()[1:])
        await message.answer(f'''🎰 Информация о промокоде:

Название: <code>{res[0]}</code>
Сумма: {summ}{emj}
Осталось активаций: {res[2]}''')
    await state.finish()
    await promo_menu(message)


async def dell_promo(message, state: FSMContext, type='name'):
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


def get_summ(summ):
    if len(str(summ)) > 45:
        return "{:.0e}".format(summ)
    else:
        return '{:,}'.format(summ).replace(',', '.')


@antispam
async def activ_promo(message: types.Message):
    url = await url_name(message.from_user.id)
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
        await message.answer(f'Данный промокод уже активирован {rloser}\n\n{ads}', disable_web_page_preview=True)
        return

    if res == 'used':
        await message.answer(f'Вы уже активировали этот промокод {rloser}\n\n{ads}', disable_web_page_preview=True)
        return

    summ = get_summ(int(res[1]))
    emj = ' '.join(res[3].split()[1:])

    await new_log(f'#промоактив\nИгрок: {message.from_user.id}\nПромо: {name}\nСумма: {summ}{emj}', 'promo')  # new log
    await message.answer(f"{url}, вы активировали промокод <b>{res[0]}</b>!\nПолучено: <b>{summ}</b>{emj} {rwin}")


def reg(dp: Dispatcher):
    dp.register_message_handler(promo_menu, lambda message: message.text == '✨ Промокоды', is_admin=True)
    dp.register_message_handler(admin_menu, lambda message: message.text == '👮 Вернуться в админ меню', is_admin=True)
    dp.register_message_handler(promo_info, lambda message: message.text == 'ℹ️ Промо инфо', is_admin=True)
    dp.register_message_handler(lambda message, state: promo_info(message, state, type='finish'), state=promo_info_state.name)

    dp.register_message_handler(new_promo, lambda message: message.text == '📖 Создать промо', is_admin=True)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='txt'), state=new_promo_state.txt)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='summ'), state=new_promo_state.name)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='activ'), state=new_promo_state.summ)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='finish'), state=new_promo_state.activ)

    dp.register_message_handler(dell_promo, lambda message: message.text == '🗑 Удалить промо', is_admin=True)
    dp.register_message_handler(lambda message, state: dell_promo(message, state, type='finish'), state=dell_promo_state.name)
    dp.register_message_handler(activ_promo, lambda message: message.text.lower().startswith('промо'))
