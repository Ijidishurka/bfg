from datetime import datetime, timedelta
from aiogram import Dispatcher, types
from assets.antispam import antispam
from commands.db import url_name, getads, get_balance, getstatus, get_name
from commands.basic.bank.db import *
from commands.main import win_luser
from assets.transform import transform_int as tr


async def bank_pc(status):
    status_info = {
        0: {"p": 6, "c": 5, "st": "Обычный"},
        1: {"p": 8, "c": 4.5, "st": "Standart VIP"},
        2: {"p": 10, "c": 3.5, "st": "Gold VIP"},
        3: {"p": 12, "c": 3, "st": "Platinum VIP"},
        4: {"p": 15, "c": 2.5, "st": "Администратор"}
    }

    info = status_info.get(status, status_info[0])
    return info["p"], info["c"], info["st"]


async def dep_comsa(status):
    status_info = {
        0: {"c": 0.05, "p": 5},
        1: {"c": 0.045, "p": 4.5},
        2: {"c": 0.035, "p": 3.5},
        3: {"c": 0.03, "p": 3},
        4: {"c": 0.025, "p": 2.5}
    }

    info = status_info.get(status, {"c": 0, "p": 0})
    return info["c"], info["p"]


async def get_summ(msg, balance):
    if msg[2] in ['все', 'всё']:
        return balance
    else:
        summ = msg[2].replace('е', 'e')
        return int(float(summ))


@antispam
async def bank_cmd(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    user_name = await get_name(user_id)
    ads = await getads()
    status = await getstatus(user_id)
    p, c, st = await bank_pc(status)

    depozit, timedepozit, bank = await getbankdb(user_id)

    if depozit == 0:
        timedepozit = 'Нет депозита'
    else:
        timedepozit = datetime.fromtimestamp(timedepozit)
        timedepozit += timedelta(days=3)
        timedepozit = timedepozit.strftime('%Y-%m-%d в %H:%M:%S')

    await message.answer(f'''{url}, ваш банковский счёт:
👫 Владелец: {user_name}
💰 Деньги в банке: {tr(bank)}$
💎 Статус: {st}
   〽 Процент под депозит: {p}%
   💱 Комиссия банка: {c}%
   💵 Под депозитом: {tr(depozit)}$
   ⏳ Можно снять: {timedepozit}

{ads}''', disable_web_page_preview=True)


@antispam
async def putbank(message: types.Message):
    print(123233)
    user_id = message.from_user.id
    balance = await get_balance(user_id)
    url = await url_name(user_id)
    win, lose = await win_luser()

    try:
        msg = message.text.split()
        if len(msg) < 3:
            return
        summ = await get_summ(msg, balance)
    except:
        return

    summ, balance = Decimal(summ), Decimal(balance)

    if summ > balance:
        await message.answer(f'{url}, вы не можете положить в банк больше чем у вас на балансе {lose}')
        return

    if summ <= 0:
        await message.answer(f'{url}, вы не можете положить в банк отрицательную сумму денег {lose}')
        return

    await putbank_db(summ, user_id)
    await message.answer(f'{url}, вы успешно положили на банковский счёт {tr(summ)}$ {win}')


@antispam
async def takeoffbank(message: types.Message):
    user_id = message.from_user.id
    _, _, balance = await getbankdb(user_id)
    url = await url_name(user_id)
    win, lose = await win_luser()

    try:
        msg = message.text.split()
        if len(msg) < 3:
            return
        summ = await get_summ(msg, balance)
    except:
        return

    summ, balance = int(summ), int(balance)

    if summ < balance:
        await message.answer(f'{url}, вы не можете снять с банка больше чем у вас есть {lose}')
        return

    if summ <= 0:
        await message.answer(f'{url}, вы не можете снять с банка отрицательную сумму денег {lose}')
        return

    await takeoffbank_db(summ, user_id)
    await message.answer(f'{url}, вы успешно сняли с банковского счёта {tr(summ)}$ {win}')


@antispam
async def pudepozit(message: types.Message):
    user_id = message.from_user.id
    balance = await get_balance(user_id)
    depozitb, _, _ = await getbankdb(user_id)
    status = await getstatus(user_id)
    p, c, st = await bank_pc(status)
    url = await url_name(user_id)
    win, lose = await win_luser()

    try:
        msg = message.text.split()
        if len(msg) < 3:
            return
        summ = await get_summ(msg, balance)
    except:
        return

    if summ < 1000:
        await message.answer(f'{url}, ваш взнос не может быть меньше 1000$ {lose}')
        return

    if depozitb != 0:
        await message.answer(f'{url}, у вас уже открыт депозит. Вы не можете дополнить его {lose}')
        return

    if summ > balance:
        await message.answer(f'{url}, вы не можете положить на депозит больше чем у вас на балансе {lose}')
        return

    comsa = int(summ * 0.15)
    csumm = int(summ - comsa)

    dt = int(datetime.now().timestamp())
    await putdep_db(csumm, user_id, dt, summ)
    await message.answer(f'{url}, вы успешно положили на депозитный счёт {tr(summ)}$ под {p}% {win}.\n\n'
                         f'Вы заплатили комиссию в размере {tr(comsa)}$ (1.5%) за использование банковских услуг.')


@antispam
async def takeoffdepozit(message: types.Message):
    user_id = message.from_user.id
    balance, timedepozit, bank = await getbankdb(user_id)
    url = await url_name(user_id)
    win, lose = await win_luser()

    timedepozit = datetime.fromtimestamp(timedepozit)
    timedepozit += timedelta(days=3)
    dt = datetime.now().timestamp()

    status = await getstatus(user_id)
    c, p = await dep_comsa(status)

    try:
        msg = message.text.split()
        if len(msg) < 3:
            return
        summ = await get_summ(msg, balance)
    except:
        return

    if int(timedepozit.timestamp()) > dt:
        await message.answer(f'{url}, у вас уже открыт депозит. Вы не можете снять с него деньги раньше времени {lose}')
        return

    if summ > balance:
        await message.answer(f'{url}, вы не можете снять с депозита больше чем у вас есть {lose}')
        return

    if summ <= 0:
        await message.answer(f'{url}, вы не можете снять с депозита отрицательную сумму денег {lose}')
        return

    if summ < 100:
        await message.answer(f'{url}, вы не можете снять меньше 100$ {lose}')
        return

    if summ < balance:
        ost = balance - summ
        await getdepost(ost, user_id)

    comsa = int(summ * float(c))
    csumm = int(summ - comsa)

    await sndep_db(csumm, user_id)
    await message.answer(f'''{url}, вы успешно сняли с депозитного счёта {tr(summ)}$ 😁

Учтите, сняв деньги вы закрыли свой депозитный счёт. Чтобы его вновь активировать положите под депозит любую сумму.

Вы заплатили налог в размере {tr(comsa)}$ ({p}%) за снятие денег с депозита.''')


def reg(dp: Dispatcher):
    dp.register_message_handler(putbank, lambda message: message.text.lower().startswith('банк положить'))
    dp.register_message_handler(takeoffbank, lambda message: message.text.lower().startswith('банк снять'))
    dp.register_message_handler(pudepozit, lambda message: message.text.lower().startswith('депозит положить'))
    dp.register_message_handler(takeoffdepozit, lambda message: message.text.lower().startswith('депозит снять'))
    dp.register_message_handler(bank_cmd, lambda message: message.text.lower() == 'банк')