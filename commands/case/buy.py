from commands.case.db import *
from commands.db import register_users, getname, getonlibalance, getidname, getads
from commands.main import geturl
from commands.main import win_luser


async def buy_case(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    result = await win_luser()
    rwin, rloser = result
    try:
        case = int(message.text.split()[2])
        arg = int(message.text.split()[3])
    except:
        await message.answer(f'''{url}, вы ввели не числовые данные для покупки кейсов {rloser}''', parse_mode='html')
        return

    if arg > 1000:
        return

    if case in [1, 2]:
        await buy_case_1_2(message, result)


async def buy_case_1_2(message, result):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    balance = await getonlibalance(message)
    rwin, rloser = result
    try:
        case_n = int(message.text.split()[2])
        case = int(message.text.split()[3])
    except:
        await message.answer(f'''{url}, вы ввели не числовые данные для покупки кейсов {rloser}''', parse_mode='html')
        return

    if case_n == 1:
        v, summ, summ2, name = 'case1', 750_000_000_000_000_000, '750 квдр', "Обычный кейс"
    else:
        v, summ, summ2, name = 'case2', 5_000_000_000_000_000_000, '750 квнт', "Золотой кейс"

    summ = summ * case

    if summ > balance:
        await message.answer(f'''{url}, у вас недостаточно средств для покупки данного кейса {rloser}''', parse_mode='html')
        return

    await buy_case_db_12(user_id, v, summ, case)
    await message.answer(f'{url}, вы успешно купили «{name}» за {summ2}$ ✅', parse_mode='html')