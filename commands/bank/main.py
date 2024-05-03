from datetime import datetime, timedelta
from commands.db import register_users, getname, getads, getonlibalance, getstatus
from commands.bank.db import *
from commands.main import geturl
from commands.main import win_luser
from commands.assets.transform import transform


async def bank_pc(status):
    if status == 0:
        p = 6
        c = 5
        st = "Обычный"
    elif status == 1:
        p = 8
        c = 4.5
        st = "Standart VIP"
    elif status == 2:
        p = 10
        c = 3.5
        st = "Gold VIP"
    elif status == 3:
        p = 12
        c = 3
        st = "Platinum VIP"
    elif status == 4:
        p = 15
        c = 2.5
        st = "Администратор"
    return p, c, st

async def bank_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    ads = await getads(message)
    status = await getstatus(user_id)
    p, c, st = await bank_pc(status)
    depozit, timedepozit, bank = await getbankdb(message)
    timedepozit = datetime.strptime(timedepozit, '%Y-%m-%d %H:%M:%S.%f')
    timedepozit = timedepozit + timedelta(days=3)
    timedepozit = timedepozit.strftime('%Y-%m-%d в %H:%M:%S')

    if depozit == 0:
        timedepozit = 'Нет депозита'

    depozit = '{:,}'.format(depozit).replace(',', '.')
    bank = '{:,}'.format(bank).replace(',', '.')

    await message.answer(f'''{url}, ваш банковский счёт:
👫 Владелец: {user_name}
💰 Деньги в банке: {bank}$
💎 Статус: {st}
   〽 Процент под депозит: {p}%
   💱 Комиссия банка: {c}%
   💵 Под депозитом: {depozit}$
   ⏳ Можно снять: {timedepozit}

{ads}''', parse_mode='html', disable_web_page_preview=True)


async def putbank(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    balance = await getonlibalance(message)
    url = await geturl(user_id, user_name)
    result = await win_luser()
    rwin, rloser = result

    try:
        summ = int(message.text.split()[2])
    except:
        return

    summ2 = '{:,}'.format(summ).replace(',', '.')

    if summ <= balance:
        if summ > 0:
            await putbank_db(summ, user_id)
            await message.answer(f'{url}, вы успешно положили на банковский счёт {summ2}$ {rwin}', parse_mode='html')
        else:
            await message.answer(f'{url}, вы не можете положить в банк отрицательную сумму денег {rloser}',
                                 parse_mode='html')
    else:
        await message.answer(f'{url}, вы не можете положить в банк больше чем у вас на балансе {rloser}', parse_mode='html')


async def takeoffbank(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    balance = await getbakbalance_db(message)
    url = await geturl(user_id, user_name)
    result = await win_luser()
    rwin, rloser = result

    try:
        summ = int(message.text.split()[2])
    except:
        try:
            if message.text.split()[2] in ['все', 'всё']:
                summ = balance
        except:
            return

    summ2 = '{:,}'.format(summ).replace(',', '.')

    if summ <= balance:
        if summ > 0:
            await takeoffbank_db(summ, user_id)
            await message.answer(f'{url}, вы успешно сняли с банковского счёта {summ2}$ {rwin}', parse_mode='html')
        else:
            await message.answer(f'{url}, вы не можете снять с банка отрицательную сумму денег {rloser}',
                                 parse_mode='html')
    else:
        await message.answer(f'{url}, вы не можете снять с банка больше чем у вас есть {rloser}', parse_mode='html')


async def dep_comsa(status):
    if status == 0:
        c = 0.05
        p = 5
    elif status == 1:
        c = 0.045
        p = 4.5
    elif status == 2:
        c = 0.035
        p = 3.5
    elif status == 3:
        c = 0.03
        p = 3
    elif status == 4:
        c = 0.025
        p = 2.5
    return c, p


async def pudepozit(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    balance = await getonlibalance(message)
    depozitb = await getdepbakance_db(message)
    url = await geturl(user_id, user_name)
    result = await win_luser()
    rwin, rloser = result

    try:
        summ = int(message.text.split()[2])
    except:
        return

    if summ < 1000:
        await message.answer(f'{url}, ваш взнос не может быть меньше 1000$ {rloser}', parse_mode='html')
        return

    if depozitb != 0:
        await message.answer(f'{url}, у вас уже открыт депозит. Вы не можете дополнить его {rloser}', parse_mode='html')
        return

    comsa = summ * 0.15
    csumm = summ - comsa
    comsa = int(comsa)
    csumm = int(csumm)

    summ2 = '{:,}'.format(csumm).replace(',', '.')
    comsa2 = '{:,}'.format(comsa).replace(',', '.')

    if summ <= balance:
        dt = datetime.now()
        await putdep_db(csumm, user_id, dt, summ)
        await message.answer(f'{url}, вы успешно положили на депозитный счёт {summ2}$ под 6% {rwin}.\n\nВы заплатили '
                             f'комиссию в размере {comsa2}$ (1.5%) за использование банковских услуг.', parse_mode='html')
    else:
        await message.answer(f'{url}, вы не можете положить на депозит больше чем у вас на балансе {rloser}', parse_mode='html')


async def takeoffdepozit(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    balance, timedepozit, bank = await getbankdb(message)
    timedepozit = datetime.strptime(timedepozit, '%Y-%m-%d %H:%M:%S.%f')
    timedepozit = timedepozit + timedelta(days=3)
    dt = datetime.now()
    url = await geturl(user_id, user_name)
    result = await win_luser()
    rwin, rloser = result

    status = await getstatus(user_id)
    c, p = await dep_comsa(status)

    try:
        summ = int(message.text.split()[2])
    except:
        try:
            if message.text.split()[2] in ['все', 'всё']:
                summ = balance
        except:
            return

    if timedepozit > dt:
        await message.answer(f'{url}, у вас уже открыт депозит. Вы не можете снять с него деньги раньше времени {rloser}',
                             parse_mode='html')
        return

    if summ > balance:
        await message.answer(f'{url}, вы не можете снять с депозита больше чем у вас есть {rloser}',
                             parse_mode='html')
        return

    if summ <= 0:
        await message.answer(f'{url}, вы не можете снять с депозита отрицательную сумму денег {rloser}',
                             parse_mode='html')
        return

    if summ < 100:
        await message.answer(f'{url}, вы не можете снять меньше 100$ {rloser}', parse_mode='html')
        return

    if summ < balance:
        ost = balance - summ
        await getdepost(ost, user_id)

    comsa = summ * int(c)
    csumm = summ - comsa
    comsa = int(comsa)
    csumm = int(csumm)

    summ2 = '{:,}'.format(csumm).replace(',', '.')
    comsa2 = '{:,}'.format(comsa).replace(',', '.')

    await sndep_db(csumm, user_id)
    await message.answer(f'''{url}, вы успешно сняли с депозитного счёта {summ2}$ 😁

Учтите, сняв деньги вы закрыли свой депозитный счёт. Чтобы его вновь активировать положите под депозит любую сумму.

Вы заплатили налог в размере {comsa2}$ ({p}%) за снятие денег с депозита.''', parse_mode='html')
