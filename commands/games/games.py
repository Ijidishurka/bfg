from _decimal import Decimal

from commands.earnings.farm.db import *
from commands.db import register_users, getname, getonlibalance, getidname
from commands.main import geturl
from commands.main import win_luser
from commands.games.gdb import *


async def darts_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    result = await win_luser()
    rwin, rloser = result
    balance = await getonlibalance(message)
    url = await geturl(user_id, user_name)

    try:
        su = message.text.split()[1]
        su2 = (su).replace('к', '000')
        su3 = (su2).replace('м', '000000')
        su4 = (su3).replace('.', '')
        su5 = float(su4)
        summ = int(su5)
    except:
        await message.answer(f'{url}, вы не ввели ставку для игры {rloser}', parse_mode='html')
        return
    if balance >= summ:
        if summ >= 10:
            gt = await gametime(user_id)
            if gt == 1:
                await message.answer(f'{url}, играть можно каждые 5 секунд. Подождите немного {rloser}', parse_mode='html')  # {round(left1)}
                return
            rx1 = await message.reply_dice(emoji="🎯")
            rx = rx1.dice.value

            if int(rx) == 5:
                await message.answer(f'{url}, вы были на волоске от победы! 🎯\n💰 Ваши средства в безопасности! (х1)', parse_mode='html')
            elif int(rx) == 6:
                c = Decimal(summ * 2)
                c2 = round(c)
                c2 = '{:,}'.format(c2)
                await gX2(balance, summ, user_id)
                await message.answer(f'Игрок, в яблочко! 🎯\n💰 Ваш приз: {c2}$!',parse_mode='html')
            else:
                await gX0(balance, summ, user_id)
                await message.answer(f'{rloser} | К сожалению Ваша победа ускользнула от Вас! 🎯️', parse_mode='html')

        else:
            await message.answer(f'{url}, ваша ставка не может быть меньше 10 {rloser}', parse_mode='html')
    else:
        await message.answer(f'{url}, ваша ставка не может быть больше вашего баланса {rloser}', parse_mode='html')

async def kybik_game_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    result = await win_luser()
    rwin, rloser = result
    balance = await getonlibalance(message)
    url = await geturl(user_id, user_name)

    try:
        ch1 = message.text.split()[1]
        ch = int(ch1)
        su = message.text.split()[2]
        su2 = (su).replace('к', '000')
        su3 = (su2).replace('м', '000000')
        su4 = (su3).replace('.', '')
        su5 = float(su4)
        summ = int(su5)
        summ2 = '{:,}'.format(summ).replace(',', '.')
    except:
        await message.answer(f'{rloser} | Ошибка. Вы не ввели ставку для игры.')
        return
    if ch >= 1 and ch <= 6:
        if balance >= summ:
            if summ >= 10:
                gt = await gametime(user_id)
                if gt == 1:
                    await message.answer(f'{url}, играть можно каждые 5 секунд. Подождите немного {rloser}', parse_mode='html')  # {round(left1)}
                    return
                rx1 = await message.reply_dice(emoji="🎲")
                rx = rx1.dice.value

                if int(rx) == ch:
                    c = Decimal(summ * 4)
                    c2 = round(c)
                    c2 = '{:,}'.format(c2).replace(',', '.')
                    await gX4(balance, summ, user_id)
                    await message.answer(f'{rwin} | Поздравляю! Вы угадали число. Ваш выигрыш составил - {c2}$', parse_mode='html')
                    return
                else:
                    await gX0(balance, summ, user_id)
                    await message.answer(f'{rwin} | К сожалению вы не угадали число! 🎲', parse_mode='html')
                    return

            else:
                await message.answer(f'{rloser} | Ваша ставка не может быть меньше 10.', parse_mode='html')
        else:
            await message.answer(f'{rloser} | Недостаточно средств.', parse_mode='html')
    else:
        if ch < 1:
            t = 'меньше 0'
        else:
            t = 'больше 6'
        await message.answer(f'{rloser} | Ошибка. Вы не можете поставить на число {t}.', parse_mode='html')

async def basketbol_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    result = await win_luser()
    rwin, rloser = result
    balance = await getonlibalance(message)
    url = await geturl(user_id, user_name)
    user_id = message.from_user.id
    try:
        su = message.text.split()[1]
        su2 = (su).replace('к', '000')
        su3 = (su2).replace('м', '000000')
        su4 = (su3).replace('.', '')
        su5 = float(su4)
        summ = int(su5)
    except:
        await message.reply(f'{url}, вы не ввели ставку для игры 😞')
        return
    if balance < summ:
        await message.answer(f'{url}, ваша ставка не может быть больше вашего баланса 😕')
        return
    if summ >= 10:
        rx1 = await message.reply_dice(emoji="🏀")
        rx = rx1.dice.value

        if int(rx) == 5:
            c = Decimal(summ * 2)
            c2 = round(c)
            c2 = '{:,}'.format(c2)
            await gX2(balance, summ, user_id)
            await message.answer(f'{url}, мяч в кольце, ура! 🏀\n💰 Ваш приз: {c2}$!', parse_mode='html')

        elif int(rx) == 4:
            await message.answer(f'{url}, бросок оказался на грани фола! 🏀\n💰 Ваши средства в безопасности! (х1)', parse_mode='html')
        else:
            await gX0(balance, summ, user_id)
            await message.answer(f'{rwin} | К сожалению вы не попали в кольцо! 🏀', parse_mode='html')
    else:
        await message.answer(f'{url}, ваша ставка не может быть меньше 10 {rloser}', parse_mode='html')

async def bowling_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    result = await win_luser()
    rwin, rloser = result
    balance = await getonlibalance(message)
    url = await geturl(user_id, user_name)
    user_id = message.from_user.id
    try:
        su = message.text.split()[1]
        su2 = (su).replace('к', '000')
        su3 = (su2).replace('м', '000000')
        su4 = (su3).replace('.', '')
        su5 = float(su4)
        summ = int(su5)
    except:
        await message.reply(f'{url}, вы не ввели ставку для игры 😞')
        return
    if balance < summ:
        await message.answer(f'{url}, ваша ставка не может быть больше вашего баланса 😕')
        return
    if summ >= 10:
        rx1 = await message.reply_dice(emoji="🎳️")
        rx = rx1.dice.value

        if int(rx) == 6:
            c = Decimal(summ * 2)
            c2 = round(c)
            c2 = '{:,}'.format(c2)
            await gX2(balance, summ, user_id)
            await message.answer(f'{url}, страйк! Полная победа! 🎳️\n💰 Ваш приз: {c2}$!', parse_mode='html')

        elif int(rx) == 5:
            await message.answer(f'{url}, так близко к победе! 🎳\n💰 Ваши средства в безопасности! (х1)', parse_mode='html')
        else:
            await gX0(balance, summ, user_id)
            await message.answer(f'{rwin} | К сожалению мимо всех кеглей! 🎳', parse_mode='html')
    else:
        await message.answer(f'{url}, ваша ставка не может быть меньше 10 {rloser}', parse_mode='html')
