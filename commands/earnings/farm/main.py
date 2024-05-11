from commands.earnings.farm.db import *
from commands.db import getname, getonlibalance, getidname
from commands.main import geturl
from commands.main import win_luser
from commands.assets.kb import help_fermaKB
from assets.antispam import antispam_earning, new_earning_msg


async def ferma_list(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свою ферму и улучшать её. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свою ферму, цена постройки 500.000.000$. Введите команду "Построить ферму" и после через команду "Моя ферма" вы сможете настраивать её и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды ферм введите команду "Помощь" и выберите соответствующую кнопку.''', parse_mode='html')


async def my_ferma(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    result = await win_luser()
    rwin, rloser = result
    data = await getferm(id)
    if not data:
        return await message.answer(f'{url}, у вас нет своей фермы чтобы построить введите команду "Построить ферму" {rloser}', parse_mode='html')

    await new_earning_msg(message.chat.id, message.message_id + 1)
    if data[3] != 0: dox = int(3000 * (data[3] ** 2.5))
    else: dox = 3000
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format(int(data[2])).replace(',', '.')
    cards = '{:,}'.format(data[3]).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    await message.answer(f'''{url}, информация о вашей "Майнинг ферма":
💷 Доход: {dox}฿/час
📝 Видеокарты: {cards} шт./♾️ шт.
💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance}฿''', parse_mode='html', reply_markup=help_fermaKB)


async def buy_ferma(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    data = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if data:
        await message.answer(f'{url}, у вас уже есть построенная ферма. Чтобы узнать подробнее, введите "Моя ферма" {rloser}', parse_mode='html')
    else:
        balance = await getonlibalance(message)
        if balance < 500000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки фермы. Её стоимость 500.000.000$ {rloser}', parse_mode='html')
        else:
            await buy_ferma_db(id)
            await message.answer(f'{url}, вы успешно купили ферму для подробностей введите "Моя ферма" {rwin}', parse_mode='html')


@antispam_earning
async def buy_cards(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    data = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if not data:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы увеличить её видеокарты {rloser}', parse_mode='html')
    else:
        ch = int(500000000 * (1 + 0.15) ** (data[3] - 1))
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await call.message.answer(f'{url}, у вас недостаточно денег для увеличения видеокарт. Её стоимость {ch2}$ {rloser}', parse_mode='html')
        else:
            await buy_cards_db(id, ch)
            await call.message.answer(f'{url}, вы успешно увеличили количество видеокарт в ферме за {ch2}$ {rwin}', parse_mode='html')


@antispam_earning
async def snyt_pribl_ferma(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    data = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if not data:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы собрать с неё приыбль {rloser}', parse_mode='html')
    else:
        if data[1] == 0:
            await call.message.answer(f'{url}, на данный момент на балансе вашей фермы нет прибыли {rloser}', parse_mode='html')
        else:
            balance2 = '{:,}'.format(data[1]).replace(',', '.')
            await snyt_pribl_ferma_db(id, data[1])
            await call.message.answer(f'{url}, вы успешно сняли {balance2}฿ с баланса вашей фермы {rwin}', parse_mode='html')


@antispam_earning
async def oplata_nalogov_ferma(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    data = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if not data:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы платить за неё налоги {rloser}', parse_mode='html')
    else:
        nalogs2 = '{:,}'.format(data[2]).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < data[2]:
            await call.message.answer(f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}', parse_mode='html')
            return
        if data[2] == 0:
            await call.message.answer(f'{url}, у вас нет налогов чтобы их оплатить {rwin}', parse_mode='html')
        else:
            await oplata_nalogs_ferma_db(id, data[2])
            await call.message.answer(f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}', parse_mode='html')