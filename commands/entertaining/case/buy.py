from aiogram import Dispatcher, types
import commands.entertaining.case.db as db
from commands.db import url_name, get_balance
from commands.main import win_luser
from assets.transform import transform as tr
from assets.antispam import antispam


@antispam
async def buy_case(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    win, lose = await win_luser()

    try:
        case = int(message.text.split()[2])
        arg = int(message.text.split()[3])
    except:
        await message.answer(f'''{url}, вы ввели не числовые данные для покупки кейсов {lose}''')
        return

    if arg > 1000 or arg <= 0:
        return

    if case in [1, 2]:
        return await buy_case_1_2(message)

    if case == 3:
        return await buy_case_3(message)

    if case == 4:
        return await buy_case_4(message)


async def buy_case_1_2(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    balance = await get_balance(user_id)
    win, lose = await win_luser()

    try:
        case_n = int(message.text.split()[2])
        case = int(message.text.split()[3])
    except:
        case = 1

    if case_n == 1:
        v, summ, name = 'case1', 750_000_000_000_000_000, "Обычный кейс"
    else:
        v, summ, name = 'case2', 5_000_000_000_000_000_000, "Золотой кейс"

    summ = summ * case

    if summ > balance:
        await message.answer(f'{url}, у вас недостаточно средств для покупки данного кейса {lose}')
        return

    await db.buy_case_db_12(user_id, v, summ, case)
    await message.answer(f'{url}, вы успешно купили {case} «{name}» за {tr(summ)}$ ✅')


async def buy_case_3(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    win, lose = await win_luser()
    titanium, matter = await db.get_mine(user_id)

    try:
        case = int(message.text.split()[3])
    except:
        case = 1

    v, summ = 'case3', 50
    summ = summ * case

    if summ > titanium:
        await message.answer(f'{url}, у вас недостаточно средств для покупки данного кейса {lose}')
        return

    await db.buy_case_db_3(user_id, summ, case)
    await message.answer(f'{url}, вы успешно купили {case} «Рудный кейс» за {summ}⚙️ ✅')


async def buy_case_4(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    win, lose = await win_luser()
    titanium, matter = await db.get_mine(user_id)

    try:
        case = int(message.text.split()[3])
    except:
        case = 1

    v, summ = 'case4', 200
    summ = summ * case

    if summ > matter:
        await message.answer(f'{url}, у вас недостаточно средств для покупки данного кейса {lose}')
        return

    await db.buy_case_db_4(user_id, summ, case)
    await message.answer(f'{url}, вы успешно купили {case} «Материальный кейс» за {summ}🌌 ✅')


def reg(dp: Dispatcher):
    dp.register_message_handler(buy_case, lambda message: message.text.lower().startswith('купить кейс'))