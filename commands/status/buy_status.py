from aiogram import Dispatcher, types
from commands.db import get_name, getstatus, url_name, getstatus
from commands.status.db import *
import config as cfg
from commands.main import win_luser


async def buy_status(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()
    status = await getstatus(user_id)

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{url}, вы не ввели число имущества или привелегии которое хотите купить {rloser}')
        return

    sttaus_list = {
        1: ("Standart VIP", 250),
        2: ("Gold VIP", 500),
        3: ("Platinum VIP", 750),
        4: ("Admin Status", 1500)
    }

    data = sttaus_list.get(u, 'no')
    if data == 'no':
        await message.answer(f'{url}, данного доната не существует. Проверьте введеную вами цифру.')
        return

    if ecoins < data[1]:
        await message.answer(f'{url},к сожалению у вас недостаточно B-Coins для покупки данной привелегии, '
                             f'чтобы пополнить напишите команду "Донат" {rloser}')
        return

    if status > u:
        await message.answer(f'{url}, у вас уже есть этот или более высокий статус {rwin}.')
        return

    await buy_status_db(user_id, data[1], u)
    await message.answer(f'{url}, вы успешко купили статус "{data[0]}" за {data[1]} B-Coins {rwin}.')


async def exchange_value(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()

    try:
        u = int(message.text.split()[1])
    except:
        u = 1

    if u > 1000 or u <= 0:
        return

    if ecoins < u:
        await message.answer(f'На твоём счету {ecoins} B-Coins, чтобы пополнить введите - Донат {rloser}')
        return

    summ = u * 2000000000000000  # сумма денег за 1 B-Coin
    summ2 = '{:,}'.format(summ).replace(',', '.')

    await exchange_value_db(user_id, summ, u)
    await message.answer(f'{url}, вы обменяли {u} B-Coins на {summ2}$ {rwin}')


async def buy_limit(message: types.Message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    ecoins = await getecoins(user_id)
    rwin, rloser = await win_luser()

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{url}, вы не ввели число имущества или привелегии которое хотите купить {rloser}')
        return

    # номер лимита: (лимит, стоимость)
    limit_list = {
        1: (350000000000000, 100),
        2: (3000000000000000000, 1000),
        3: (100000000000000000000, 3000),
        4: (2000000000000000000000, 6500),
    }

    data = limit_list.get(u, 'no')

    if data == 'no':
        return

    if ecoins < data[1]:
        await message.answer(
            f'{url}, к сожалению у вас недостаточно B-Coins для покупки лимита, чтобы пополнить напишите команду "Донат" {rloser}')
        return

    summ2 = '{:,}'.format(data[0]).replace(',', '.')

    await buy_limit_db(user_id, data[0], data[1])
    await message.answer(f'{url}, вы увеличили свой лимит передачи на {summ2}$ за {data[1]} B-Coins {rwin}')


def reg(dp: Dispatcher):
    dp.register_message_handler(buy_status, lambda message: message.text.lower().startswith('купить привилегию'))
    dp.register_message_handler(exchange_value, lambda message: message.text.lower().startswith('обменять'))
    dp.register_message_handler(buy_limit, lambda message: message.text.lower().startswith('купить лимит'))