from commands.case.db import *
from commands.db import register_users, getname, getonlibalance, getidname, getads
from commands.main import geturl
from commands.main import win_luser


async def buy_case(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    try:
        case = int(message.text.split()[2])
        arg = int(message.text.split()[3])
    except:
        await message.answer(f'''{url}, вы ввели не числовые данные для покупки кейсов {rloser}''', parse_mode='html',
                             disable_web_page_preview=True)
        return

    if arg > 10000:
        return

    if case == 1 or case == 2:
        await buy_case_1_2(message)


async def buy_case_1_2(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    balance = await getonlibalance(message)
    result = await win_luser()
    rwin, rloser = result
    try:
        case_n = int(message.text.split()[2])
        case = int(message.text.split()[3])
    except:
        await message.answer(f'''{url}, вы ввели не числовые данные для покупки кейсов {rloser}''', parse_mode='html',
                             disable_web_page_preview=True)
        return

    if case_n == 1:
        v = 'case1'
        summ = 750000000000000000
        summ2 = '750 квдр'
        name = "Обычный кейс"
    else:
        v = 'case2'
        summ = 5000000000000000000
        summ2 = '750 квнт'
        name = "Золотой кейс"

    summ = summ * case

    if summ < balance:
        await message.answer(f'''{url}, у вас недостаточно средств для покупки данного кейса {rloser}''', parse_mode='html', disable_web_page_preview=True)
        return

    await buy_case_db_12(user_id, v, summ, case)
    await message.answer(
        f'{url}, вы успешно купили «{name}» за {summ2}$ ✅',
        parse_mode='html')

