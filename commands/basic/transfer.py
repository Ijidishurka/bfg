from decimal import Decimal

from aiogram import types, Dispatcher

from commands.db import getperevod, url_name
from commands.admin.db import give_bcoins_db, give_money_db
from filters.custom import TextIn, StartsWith
from user import BFGuser, BFGconst
from assets.transform import transform_int as tr
from commands.admin.loger import new_log
from assets.antispam import antispam, admin_only
import config as cfg


def get_limit_cmd(status: int) -> int:
    """Получить лимит на дневную передачу"""
    if status == 1:
        return 300_000_000_000_000
    elif status == 2:
        return 750_000_000_000_000
    elif status == 3:
        return 1_000_000_000_000_000
    elif status == 4:
        return 30_000_000_000_000_000
    return 150_000_000_000_000  # Для статуса "игрок" (0)


@antispam
async def transfer_cmd(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    win, lose = BFGconst.emj()
    limit = get_limit_cmd(user.status)

    try:
        reply_user_id = message.reply_to_message.from_user.id
        url2 = await url_name(reply_user_id)
    except:
        await message.reply(f'{user.url}, чтобы передать деньги нужно ответить на сообщение пользователя {lose}')
        return

    if user_id == reply_user_id:
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.reply(f'{user.url}, вы не ввели сумму которую хотите передать игроку {lose}')
        return

    limit = Decimal(str(limit)) + Decimal(int(user.perlimit))
    d_per = Decimal(int(user.per)) + Decimal(str(summ))

    if d_per > limit:
        await message.reply(f'{user.url}, вы уже исчерпали свой дневной лимит передачи денег')
        return

    if summ > 0:
        if int(user.balance) >= summ:
            await message.answer(f'Вы передали {tr(summ)}$ игроку {url2} {win}')
            await getperevod(summ, user_id, reply_user_id)
            await new_log(f'#перевод\n{user_id}\nСумма: {tr(summ)}\nПередал: {reply_user_id}', 'money_transfers')
        else:
            await message.reply(f'{user.url}, вы не можете передать больше чем у вас есть на балансе {lose}')

    else:
        await message.reply(f'{user.url}, вы не можете передать отрицательное число игроку {lose}')


@antispam
async def limit_cmd(message: types.Message, user: BFGuser):
    limit = get_limit_cmd(user.status)

    limit = int(limit) + int(user.perlimit)
    per = int(user.per)
    ost = limit - per

    await message.reply(f'''{user.url}, здесь ваш лимит на сегодня: {tr(limit)}$
💫 Вы уже передали: {tr(per)}$
🚀 У вас осталось: {tr(ost)}$ для передачи!''')


@antispam
async def give_money(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    if not (user.user_id in cfg.admin or user.status == 4):
        await message.answer(
            '👮‍♂️ Вы не являетесь администратором бота чтобы использовать данную команду.\n'
            'Для покупки введи команду "Донат"')
        return

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_url = await url_name(r_user_id)
    except:
        await message.answer(f'{user.url}, чтобы выдать деньги нужно ответить на сообщение пользователя {lose}')
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.answer(f'{user.url}, вы не ввели сумму которую хотите выдать {lose}')
        return

    if user.user_id in cfg.admin:
        await give_money_db(user.user_id, r_user_id, summ, 'rab')
        await message.answer(f'{user.url}, вы выдали {tr(summ)}$ пользователю {r_url}  {win}')
    else:
        res = await give_money_db(user.user_id, r_user_id, summ, 'adm')
        if res == 'limit':
            await message.answer(f'{user.url}, вы достигли лимита на выдачу денег  {lose}')
            return

        await message.answer(f'{user.url}, вы выдали {tr(summ)}$ пользователю {r_url}  {win}')

    await new_log(f'#выдача\nИгрок {user.user_id}\nСумма: {tr(summ)}$\nИгроку {r_user_id}', 'issuance_money')  # new log


@admin_only()
async def give_bcoins(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    win, lose = BFGconst.emj()

    try:
        r_user_id = message.reply_to_message.from_user.id
        r_url = await url_name(user_id)
    except:
        await message.answer(f'{user.url}, чтобы выдать деньги нужно ответить на сообщение пользователя {lose}')
        return

    try:
        summ = message.text.split()[1].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.answer(f'{user.url}, вы не ввели сумму которую хотите выдать {lose}')
        return

    await give_bcoins_db(r_user_id, summ)
    await message.answer(f'{user.url}, вы выдали {tr(summ)}💳 пользователю {r_url}  {win}')
    await new_log(f'#бкоин-выдача\nАдмин {user_id}\nСумма: {tr(summ)}$\nПользователю {r_user_id}', 'issuance_bcoins')


def reg(dp: Dispatcher):
    dp.message.register(limit_cmd, TextIn("мой лимит"))
    dp.message.register(transfer_cmd, StartsWith("дать"))
    dp.message.register(give_money, StartsWith("выдать"))
    dp.message.register(give_bcoins, StartsWith("бдать"))
