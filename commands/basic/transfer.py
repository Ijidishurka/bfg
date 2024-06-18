from aiogram import types
from commands.db import getperevod, getlimitdb, getstatus, url_name, get_balance, get_doplimit
from commands.main import win_luser
from commands.admin.loger import new_log
from assets.antispam import antispam
from decimal import Decimal


async def get_limit_cmd(status):
    if status == 1:
        limit = 300000000000000
    elif status == 2:
        limit = 750000000000000
    elif status == 3:
        limit = 1000000000000000
    elif status == 4:
        limit = 30000000000000000
    else:
        limit = 150000000000000
    return limit


@antispam
async def dat_cmd(message: types.Message):
    user_id = message.from_user.id
    rwin, rloser = await win_luser()
    balance = await get_balance(user_id)
    per = await getlimitdb(message)
    url = await url_name(user_id)
    status = await getstatus(user_id)
    limit = await get_limit_cmd(status)
    doplimit = await get_doplimit(user_id)

    try:
        reply_user_id = message.reply_to_message.from_user.id
        url2 = await url_name(reply_user_id)
    except:
        await message.reply(f'{url}, чтобы передать деньги нужно ответить на сообщение пользователя {rloser}')
        return

    if user_id == reply_user_id:
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
        summ2 = '{:,}'.format(summ).replace(',', '.')
    except:
        await message.reply(f'{url}, вы не ввели сумму которую хотите передать игроку {rloser}')
        return

    limit = Decimal(str(limit)) + Decimal(doplimit)
    d_per = Decimal(per) + Decimal(str(summ))

    if d_per > limit:
        await message.reply(f'{url}, вы уже исчерпали свой дневной лимит передачи денег')
        return

    if summ > 0:
        if int(balance) >= summ:
            await message.answer(f'Вы передали {summ2}$ игроку {url2} {rwin}')
            await getperevod(summ, user_id, reply_user_id)
            await new_log(f'#перевод\n{user_id}\nСумма: {summ2}\nПередал: {reply_user_id}', 'money_transfers')
        else:
            await message.reply(f'{url}, вы не можете передать больше чем у вас есть на балансе {rloser}')

    else:
        await message.reply(f'{url}, вы не можете передать отрицательное число игроку {rloser}')


@antispam
async def limit_cmd(message):
    user_id = message.from_user.id
    per = await getlimitdb(message)
    url = await url_name(user_id)
    status = await getstatus(user_id)
    limit = await get_limit_cmd(status)
    doplimit = await get_doplimit(user_id)

    limit = int(limit) + int(doplimit)
    per = int(per)
    ost = limit - per

    youlimit = '{:,}'.format(limit).replace(',', '.')
    ost = '{:,}'.format(ost).replace(',', '.')
    per2 = '{:,}'.format(per).replace(',', '.')

    await message.reply(f'''{url}, здесь ваш лимит на сегодня: {youlimit}$
💫 Вы уже передали: {per2}$
🚀 У вас осталось: {ost}$ для передачи!''')