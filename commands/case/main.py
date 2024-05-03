import random

from commands.case.db import *
from commands.db import register_users, getname, getonlibalance, getidname, getads
from commands.main import geturl
from commands.main import win_luser


async def getcase_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    case1, case2, case3, case4 = await getcase(message)
    ads = await getads(message)
    ycase = {
        "case1": {"name": "📦 Обычный кейс", "quantity": case1},
        "case2": {"name": "🏵 Золотой кейс", "quantity": case2},
        "case3": {"name": "🏺 Рудный кейс", "quantity": case3},
        "case4": {"name": "🌌 Материальный кейс", "quantity": case4},
    }

    positive_resources = {name: info for name, info in ycase.items() if info["quantity"] > 0}

    if positive_resources:
        result_message = "\n".join(
            [f'{info["name"]} - {info["quantity"]} шт.' for name, info in positive_resources.items()])
        txt = f"{result_message}\n\n🔐 Для открытия кейсов используйте - «Кейс открыть [1/2/3/4] [кол-во]»"
    else:
        txt = f"\n😕 У вас нету кейсов."

    await message.answer(f'''{url}, доступные кейсы:
🎁 1. Обычный кейс — 750 квдр $
🎁 2. Золотой кейс - 5 квнт $
🎁 3. Рудный кейс - 50 ⚙️
🎁 4. Материальный кейс - 200 🌌
{txt}
🛒 Для покупки введите «Купить кейс [1/2/3] [кол-во]»

{ads}''', parse_mode='html', disable_web_page_preview=True)


async def open_case(message):
    try:
        case = int(message.text.split()[2])
    except:
        return

    if case == 1:
        await open_case_1(message)
    elif case == 2:
        await open_case_2(message)
    elif case == 3:
        await open_case_3(message)
    elif case == 4:
        await open_case_4(message)


async def open_case_1(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    case1, case2, case3, case4 = await getcase(message)
    result = await win_luser()
    rwin, rloser = result
    try:
        summ_case = int(message.text.split()[3])
    except:
        summ_case = 1

    if case1 < summ_case:
        await message.answer(f'''{url}, у вас недостаточно кейсов для открытия {rloser}\n\n{ads}''', parse_mode='html', disable_web_page_preview=True)
        return

    i = random.randint(1, 3)
    if i == 1:
        table = 'users'
        v = 'balance'
        summ = random.randint(100000000, 400000000)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🔥 Итого денег - {summ2}$'
    elif i == 2:
        table = 'users'
        v = 'rating'
        summ = random.randint(10000, 90050)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'👑 Итого рейтинга - {summ2}'
    else:
        table = 'users'
        v = 'exp'
        summ = random.randint(100, 999)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🏆 Итого опыта - {summ2}'

    await open_case_db(user_id, table, v, summ, 'case1', summ_case)
    await message.answer(
        f'{url}, вы открыли {summ_case} обычный кейс:\n\n{txt}\n\n{ads}',
        parse_mode='html')


async def open_case_2(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    case1, case2, case3, case4 = await getcase(message)
    result = await win_luser()
    rwin, rloser = result
    try:
        summ_case = int(message.text.split()[3])
    except:
        summ_case = 1

    if case2 < summ_case:
        await message.answer(f'''{url}, у вас недостаточно кейсов для открытия {rloser}\n\n{ads}''', parse_mode='html', disable_web_page_preview=True)
        return

    i = random.randint(1, 3)
    if i == 1:
        table = 'users'
        v = 'balance'
        summ = random.randint(1000000000, 4000000000)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🔥 Итого денег - {summ2}$'
    elif i == 2:
        table = 'users'
        v = 'rating'
        summ = random.randint(100000, 900050)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'👑 Итого рейтинга - {summ2}'
    else:
        table = 'users'
        v = 'exp'
        summ = random.randint(1000, 9990)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🏆 Итого опыта - {summ2}'

    await open_case_db(user_id, table, v, summ, 'case2', summ_case)
    await message.answer(
        f'{url}, вы открыли {summ_case} золотой кейс:\n\n{txt}\n\n{ads}',
        parse_mode='html')


async def open_case_3(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    case1, case2, case3, case4 = await getcase(message)
    result = await win_luser()
    rwin, rloser = result
    try:
        summ_case = int(message.text.split()[3])
    except:
        summ_case = 1

    if case3 < summ_case:
        await message.answer(f'''{url}, у вас недостаточно кейсов для открытия {rloser}\n\n{ads}''', parse_mode='html', disable_web_page_preview=True)
        return

    i = random.randint(1, 3)
    if i == 1:
        table = 'users'
        v = 'balance'
        summ = random.randint(10000000000, 40000000000)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🔥 Итого денег - {summ2}$'
    elif i == 2:
        table = 'users'
        v = 'rating'
        summ = random.randint(1000000, 9000050)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'👑 Итого рейтинга - {summ2}'
    else:
        table = 'users'
        v = 'exp'
        summ = random.randint(10000, 99900)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🏆 Итого опыта - {summ2}'

    await open_case_db(user_id, table, v, summ, 'case3', summ_case)
    await message.answer(
        f'{url}, вы открыли {summ_case} рудный кейс:\n\n{txt}\n\n{ads}',
        parse_mode='html')


async def open_case_4(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    case1, case2, case3, case4 = await getcase(message)
    result = await win_luser()
    rwin, rloser = result
    try:
        summ_case = int(message.text.split()[3])
    except:
        summ_case = 1

    if case4 < summ_case:
        await message.answer(f'''{url}, у вас недостаточно кейсов для открытия {rloser}\n\n{ads}''', parse_mode='html', disable_web_page_preview=True)
        return

    i = random.randint(1, 3)
    if i == 1:
        table = 'users'
        v = 'balance'
        summ = random.randint(100000000000, 400000000000)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🔥 Итого денег - {summ2}$'
    elif i == 2:
        table = 'users'
        v = 'rating'
        summ = random.randint(10000000, 90000050)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'👑 Итого рейтинга - {summ2}'
    else:
        table = 'users'
        v = 'exp'
        summ = random.randint(10000, 109900)
        summ = summ * summ_case
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'🏆 Итого опыта - {summ2}'

    await open_case_db(user_id, table, v, summ, 'case4', summ_case)
    await message.answer(
        f'{url}, вы открыли {summ_case} материальный кейс:\n\n{txt}\n\n{ads}',
        parse_mode='html')


