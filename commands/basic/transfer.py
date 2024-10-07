from aiogram import types, Dispatcher
from commands.db import getperevod, getlimitdb, getstatus, url_name, get_balance, get_doplimit
from commands.admin.db import give_bcoins_db, give_money_db
from assets.transform import transform_int as tr
from commands.main import win_luser
from commands.admin.loger import new_log
from assets.antispam import antispam, admin_only
from decimal import Decimal
import config as cfg


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
    win, lose = await win_luser()
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
        await message.reply(f'{url}, чтобы передать деньги нужно ответить на сообщение пользователя {lose}')
        return

    if user_id == reply_user_id:
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
        summ2 = '{:,}'.format(summ).replace(',', '.')
    except:
        await message.reply(f'{url}, вы не ввели сумму которую хотите передать игроку {lose}')
        return

    limit = Decimal(str(limit)) + Decimal(doplimit)
    d_per = Decimal(per) + Decimal(str(summ))

    if d_per > limit:
        await message.reply(f'{url}, вы уже исчерпали свой дневной лимит передачи денег')
        return

    if summ > 0:
        if int(balance) >= summ:
            await message.answer(f'Вы передали {summ2}$ игроку {url2} {win}')
            await getperevod(summ, user_id, reply_user_id)
            await new_log(f'#перевод\n{user_id}\nСумма: {summ2}\nПередал: {reply_user_id}', 'money_transfers')
        else:
            await message.reply(f'{url}, вы не можете передать больше чем у вас есть на балансе {lose}')

    else:
        await message.reply(f'{url}, вы не можете передать отрицательное число игроку {lose}')


@antispam
async def limit_cmd(message: types.Message):
    user_id = message.from_user.id
    per = await getlimitdb(message)
    url = await url_name(user_id)
    status = await getstatus(user_id)
    limit = await get_limit_cmd(status)
    doplimit = await get_doplimit(user_id)

    limit = int(limit) + int(doplimit)
    per = int(per)
    ost = limit - per

    await message.reply(f'''{url}, здесь ваш лимит на сегодня: {tr(limit)}$
💫 Вы уже передали: {tr(per)}$
🚀 У вас осталось: {tr(ost)}$ для передачи!''')


async def give_money(message: types.Message):
    user_id = message.from_user.id
    status = await getstatus(user_id)
    win, lose = await win_luser()
    url = await url_name(user_id)

    if not (user_id in cfg.admin or status == 4):
        await message.answer(
            '👮‍♂️ Вы не являетесь администратором бота чтобы использовать данную команду.\n'
            'Для покупки введи команду "Донат"')
        return

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_url = await url_name(user_id)
    except:
        await message.answer(f'{url}, чтобы выдать деньги нужно ответить на сообщение пользователя {lose}')
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.answer(f'{url}, вы не ввели сумму которую хотите выдать {lose}')
        return

    if user_id in cfg.admin:
        await give_money_db(user_id, r_user_id, summ, 'rab')
        await message.answer(f'{url}, вы выдали {tr(summ)}$ пользователю {r_url}  {win}')
    else:
        res = await give_money_db(user_id, r_user_id, summ, 'adm')
        if res == 'limit':
            await message.answer(f'{url}, вы достигли лимита на выдачу денег  {lose}')
            return

        await message.answer(f'{url}, вы выдали {tr(summ)}$ пользователю {r_url}  {win}')

    await new_log(f'#выдача\nИгрок {user_id}\nСумма: {tr(summ)}$\nИгроку {r_user_id}', 'issuance_money')  # new log


@admin_only()
async def give_bcoins(message: types.Message):
    user_id = message.from_user.id
    win, lose = await win_luser()
    url = await url_name(user_id)

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_url = await url_name(user_id)
    except:
        await message.answer(f'{url}, чтобы выдать деньги нужно ответить на сообщение пользователя {lose}')
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.answer(f'{url}, вы не ввели сумму которую хотите выдать {lose}')
        return

    await give_bcoins_db(r_user_id, summ)
    await message.answer(f'{url}, вы выдали {tr(summ)}💳 пользователю {r_url}  {win}')
    await new_log(f'#бкоин-выдача\nАдмин {user_id}\nСумма: {tr(summ)}$\nПользователю {r_user_id}', 'issuance_bcoins')


def reg(dp: Dispatcher):
    dp.register_message_handler(limit_cmd, lambda message: message.text.lower() == 'мой лимит')
    dp.register_message_handler(dat_cmd, lambda message: message.text.lower().startswith('дать'))
    dp.register_message_handler(give_money, lambda message: message.text.lower().startswith('выдать'))
    dp.register_message_handler(give_bcoins, lambda message: message.text.lower().startswith('бдать'))
