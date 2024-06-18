from aiogram import Dispatcher, types
from commands.entertaining.earnings.farm.db import *
from commands.db import getonlibalance, url_name, get_name
from commands.main import win_luser
from assets import kb
from assets.antispam import antispam_earning, new_earning_msg, antispam
from bot import bot


@antispam
async def ferma_list(message):
    id = message.from_user.id
    url = await url_name(id)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свою ферму и улучшать её. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свою ферму, цена постройки 500.000.000$. Введите команду "Построить ферму" и после через команду "Моя ферма" вы сможете настраивать её и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды ферм введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_ferma(message):
    uid = message.from_user.id
    url = await url_name(uid)
    rwin, rloser = await win_luser()
    data = await getferm(uid)
    if not data:
        return await message.answer(f'{url}, у вас нет своей фермы чтобы построить введите команду "Построить ферму" {rloser}')

    if data[3] != 0: dox = int(3000 * (data[3] ** 2.5))
    else: dox = 3000
    ch = int(500000000 * (1 + 0.15) ** (data[3]))
    ch2 = '{:,}'.format(ch).replace(',', '.')
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format(int(data[2])).replace(',', '.')
    cards = '{:,}'.format(data[3]).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашей "Майнинг ферма":
💷 Доход: {dox}฿/час
📝 Видеокарты: {cards} шт./♾️ шт.
🆙 для следующего уровня: {ch2}$

💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance}฿''', reply_markup=kb.ferma(uid))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def upd_ferma_text(call: types.CallbackQuery):
    uid = call.from_user.id
    url = await url_name(uid)
    data = await getferm(uid)
    if not data:
        return

    if data[3] != 0: dox = int(3000 * (data[3] ** 2.5))
    else: dox = 3000

    ch = int(500000000 * (1 + 0.15) ** (data[3] - 1))
    ch2 = '{:,}'.format(ch).replace(',', '.')
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format(int(data[2])).replace(',', '.')
    cards = '{:,}'.format(data[3]).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    try: await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашей "Майнинг ферма":
💷 Доход: {dox}฿/час
📝 Видеокарты: {cards} шт./♾️ шт.
🆙 для следующего уровня: {ch2}$

💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance}฿''', reply_markup=kb.ferma(uid))
    except: pass


@antispam
async def buy_ferma(message):
    id = message.from_user.id
    url = await url_name(id)
    data = await getferm(id)
    rwin, rloser = await win_luser()
    if data:
        await message.answer(f'{url}, у вас уже есть построенная ферма. Чтобы узнать подробнее, введите "Моя ферма" {rloser}')
    else:
        balance = await getonlibalance(message)
        if balance < 500000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки фермы. Её стоимость 500.000.000$ {rloser}')
        else:
            await buy_ferma_db(id)
            await message.answer(f'{url}, вы успешно купили ферму для подробностей введите "Моя ферма" {rwin}')


@antispam_earning
async def buy_cards(call: types.CallbackQuery):
    id = call.from_user.id
    url = await get_name(id)
    data = await getferm(id)
    rwin, rloser = await win_luser()
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своей фермы чтобы увеличить её видеокарты {rloser}', parse_mode='html')
    else:
        ch = int(500000000 * (1 + 0.15) ** (data[3] - 1))
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег для увеличения видеокарт. Её стоимость {ch2}$ {rloser}')
        else:
            await buy_cards_db(id, ch)
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили количество видеокарт в ферме за {ch2}$ {rwin}')
            await upd_ferma_text(call)


@antispam_earning
async def snyt_pribl_ferma(call):
    id = call.from_user.id
    url = await get_name(id)
    data = await getferm(id)
    rwin, rloser = await win_luser()
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своей фермы чтобы собрать с неё приыбль {rloser}')
    else:
        if data[1] == 0:
            await bot.answer_callback_query(call.id, text=f'{url}, на данный момент на балансе вашей фермы нет прибыли {rloser}')
        else:
            balance2 = '{:,}'.format(data[1]).replace(',', '.')
            await snyt_pribl_ferma_db(id, data[1])
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно сняли {balance2}฿ с баланса вашей фермы {rwin}')
            await upd_ferma_text(call)


@antispam_earning
async def oplata_nalogov_ferma(call):
    id = call.from_user.id
    url = await get_name(id)
    data = await getferm(id)
    rwin, rloser = await win_luser()
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своей фермы чтобы платить за неё налоги {rloser}')
    else:
        nalogs2 = '{:,}'.format(data[2]).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < data[2]:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
            return
        if data[2] == 0:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        else:
            await oplata_nalogs_ferma_db(id, data[2])
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
            await upd_ferma_text(call)


def reg(dp: Dispatcher):
    dp.register_message_handler(my_ferma, lambda message: message.text.lower().startswith('моя ферма'))
    dp.register_message_handler(ferma_list, lambda message: message.text.lower().startswith(('ферма', 'фермы')))
    dp.register_message_handler(buy_ferma, lambda message: message.text.lower().startswith('построить ферму'))
    dp.register_callback_query_handler(buy_cards, text_startswith='ferma-bycards')
    dp.register_callback_query_handler(snyt_pribl_ferma, text_startswith='ferma-sobrat')
    dp.register_callback_query_handler(oplata_nalogov_ferma, text_startswith='ferma-nalog')
