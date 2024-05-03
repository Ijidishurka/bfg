from commands.earnings.farm.db import *
from commands.db import register_users, getname, getonlibalance, getidname
from commands.main import geturl
from commands.main import win_luser
from commands.assets.kb import help_fermaKB

async def ferma_list(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    await register_users(message)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свою ферму и улучшать её. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свою ферму, цена постройки 500.000.000$. Введите команду "Построить ферму" и после через команду "Моя ферма" вы сможете настраивать её и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды ферм введите команду "Помощь" и выберите соответствующую кнопку.''', parse_mode='html')

async def my_ferma(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    result = await win_luser()
    rwin, rloser = result
    ferma, balance, nalogs, cards = await getferm(id)
    if cards != 0:
        dox = 3000 * (cards ** 2.5)
        dox = int(dox)
    else:
        dox = 3000
    balance = int(balance)
    nalogs = int(nalogs)
    balance = '{:,}'.format(balance).replace(',', '.')
    nalogs = '{:,}'.format(nalogs).replace(',', '.')
    cards = '{:,}'.format(cards).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')
    await register_users(message)
    if ferma == 0:
        await message.answer(f'{url}, у вас нет своей фермы чтобы построить введите команду "Построить ферму" {rloser}', parse_mode='html')
    else:
        await message.answer(f'''{url}, информация о вашей "Майнинг ферма":
💷 Доход: {dox}฿/час
📝 Видеокарты: {cards} шт./♾️ шт.
💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance}฿''', parse_mode='html', reply_markup=help_fermaKB)

async def buy_ferma(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    ferm = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if ferm == 1:
        await message.answer(f'{url}, у вас уже есть построенная ферма. Чтобы узнать подробнее, введите "Моя ферма" {rloser}', parse_mode='html')
    else:
        balance = await getonlibalance(message)
        if balance < 500000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки фермы. Её стоимость 500.000.000$ {rloser}', parse_mode='html')
        else:
            await buy_ferma_db(id)
            await message.answer(f'{url}, вы успешно купили ферму для подробностей введите "Моя ферма" {rwin}', parse_mode='html')

async def buy_cards(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    ferm = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if ferm == 0:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы увеличить её видеокарты {rloser}', parse_mode='html')
    else:
        cards = await gercards(id)
        ch = 500000000 * (1 + 0.15) ** (cards - 1)
        ch = int(ch)
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await call.message.answer(f'{url}, у вас недостаточно денег для увеличения видеокарт. Её стоимость {ch2}$ {rloser}', parse_mode='html')
        else:
            await buy_cards_db(id, ch)
            await call.message.answer(f'{url}, вы успешно увеличили количество видеокарт в ферме за {ch2}$ {rwin}', parse_mode='html')

async def snyt_pribl_ferma(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    ferm = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if ferm == 0:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы собрать с неё приыбль {rloser}', parse_mode='html')
    else:
        balance = await get_ferma_balance(id)
        balance2 = '{:,}'.format(balance).replace(',', '.')
        if balance == 0:
            await call.message.answer(f'{url}, на данный момент на балансе вашей фермы нет прибыли {rloser}', parse_mode='html')
        else:
            await snyt_pribl_ferma_db(id, balance)
            await call.message.answer(f'{url}, вы успешно сняли {balance2}฿ с баланса вашей фермы {rwin}', parse_mode='html')

async def oplata_nalogov_ferma(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    ferm = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if ferm == 0:
        await call.message.answer(f'{url}, у вас нет своей фермы чтобы платить за неё налоги {rloser}', parse_mode='html')
    else:
        nalogs = await get_ferma_nalogs(id)
        nalogs2 = '{:,}'.format(nalogs).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < nalogs:
            await call.message.answer(f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}', parse_mode='html')
            return
        if nalogs == 0:
            await call.message.answer(f'{url}, у вас нет налогов чтобы их оплатить {rwin}', parse_mode='html')
        else:
            await oplata_nalogs_ferma_db(id, nalogs)
            await call.message.answer(f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}', parse_mode='html')
