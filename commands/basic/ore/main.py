from decimal import Decimal

from aiogram import Dispatcher, types

from assets.antispam import antispam
from commands.basic.ore import db
import commands.basic.ore.dig
from assets.transform import transform_int as tr
from user import BFGuser, BFGconst


@antispam
async def sell_btc_cmd(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        summ_btc = int(message.text.split()[2])
    except:
        summ_btc = user.btc
        
    summ_btc = Decimal(str(summ_btc))
    btc = Decimal(str(user.btc))

    kurs = await db.getkurs()
    summ = summ_btc * kurs
    
    if btc < summ_btc:
        await message.answer(f'{user.url}, вы не можете продать столько BTC {lose}')
        return
    
    if summ_btc <= 0:
        await message.answer(f'{user.url}, нельзя продавать отрицательно или же нулевое количество BTC {lose}')
        return
        
    await message.answer(f'{user.url}, вы успешно продали {tr(summ_btc)} BTC за {tr(summ)}$ {win}')
    await user.btc.upd(summ_btc, '-')
    await user.balance.upd(summ, '+')


@antispam
async def buy_btc_cmd(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    
    try:
        summ_btc = int(message.text.split()[2])
    except:
        await message.answer(f'{user.url}, вы не ввели количество BTC которое хотите купить {lose}')
        return

    summ_btc = Decimal(summ_btc)

    kurs = await db.getkurs()
    summ = summ_btc * kurs

    if Decimal(str(user.balance)) < summ:
        await message.answer(f'{user.url}, у вас недостаточно денег для покупки BTC {lose}')
        return
        
    if summ_btc <= 0:
        await message.answer(f'{user.url}, нельзя покупать отрицательно или же нулевое количество BTC {lose}')
        return

    await message.answer(f'{user.url}, вы успешно купили {tr(summ_btc)} BTC за {tr(summ)}$ {win}')
    await user.btc.upd(summ_btc, '+')
    await user.balance.upd(summ, '-')


@antispam
async def price_btc_cmd(message: types.Message, user: BFGuser):
    kurs = await db.getkurs()
    await message.answer(f'{user.url}, на данный момент курс 1 BTC составляет - {tr(kurs)}$ 🌐\n\n{BFGconst.ads}', disable_web_page_preview=True)


@antispam
async def rating_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'''{user.url}, ваш рейтинг {user.rating.tr()}👑\n\n{BFGconst.ads}''', disable_web_page_preview=True)


@antispam
async def sell_rating_cmd(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        summ_r = int(message.text.split()[2])
    except:
        summ_r = user.rating

    summ_r = Decimal(summ_r)

    kurs = 100_000_000  # сумма за 1 рейтинг
    summ = summ_r * kurs
    rating = Decimal(str(user.rating))

    if rating < summ_r:
        await message.answer(f'{user.url}, у вас недостаточно рейтинга для его продажи {lose}')
        return
    
    if rating - summ_r < 0 and summ_r <= 0:
        await message.answer(f'{user.url}, вы неправильно ввели число рейтинга которое хотите продать {lose}')
        return

    await message.answer(f'{user.url}, вы понизили количество вашего рейтинга на {tr(summ_r)}👑 за {tr(summ)}$ {win}')
    await user.rating.upd(summ_r, '-')
    await user.balance.upd(summ, '+')


@antispam
async def buy_ratting_cmd(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    
    try:
        r_summ = int(message.text.split()[1])
    except:
        await message.answer(f'{user.url},  вы неправильно ввели число рейтинга которое хотите купить {lose}')
        return

    r_summ = Decimal(r_summ)
    kurs = 150_000_000  # стоимость 1 рейтинга
    summ = r_summ * kurs
    
    if Decimal(str(user.balance)) < summ:
        await message.answer(f'{user.url}, у вас недостаточно денег для покупки рейтинга {lose}')
        return
    
    if r_summ <= 0:
        await message.answer(f'{user.url}, вы неправильно ввели число рейтинга которое хотите купить {lose}')
        return

    await message.answer(f'{user.url}, вы повысили количество вашего рейтинга на {tr(r_summ)}👑 за {tr(summ)}$ {win}')
    await user.rating.upd(r_summ, '+')
    await user.balance.upd(summ, '-')


def reg(dp: Dispatcher):
    dp.register_message_handler(sell_btc_cmd, lambda message: message.text.lower().startswith(('продать биткоин', 'биткоин продать')))
    dp.register_message_handler(buy_btc_cmd, lambda message: message.text.lower().startswith(('купить биткоин', 'биткоин купить')))
    dp.register_message_handler(price_btc_cmd, lambda message: message.text.lower() in ['курс биткоина', 'курс биткоин', 'биткоин курс'])
    dp.register_message_handler(rating_cmd, lambda message: message.text.lower() == 'рейтинг')
    dp.register_message_handler(buy_ratting_cmd, lambda message: message.text.lower().startswith('рейтинг'))
    dp.register_message_handler(sell_rating_cmd, lambda message: message.text.lower().startswith('продать рейтинг'))

    commands.basic.ore.dig.reg(dp)
