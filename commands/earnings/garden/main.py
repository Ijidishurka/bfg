from commands.earnings.garden.db import *
from commands.db import getname, getonlibalance, getidname
from commands.main import geturl
from commands.main import win_luser
from commands.assets.kb import helpGarden_kb

async def harden_list(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свой сад и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет построить свой сад, цена постройки 1.000.000.000$. Введите команду "Построить сад" и после через команду "Мой сад" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды садов введите команду "Помощь" и выберите соответствующую кнопку.''', parse_mode='html')


async def my_garden(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    result = await win_luser()
    rwin, rloser = result
    water, tree, nalogs, balance, garden = await getgarden(id)
    dox = (tree + 1) * 3
    balance = int(balance)
    nalogs = int(nalogs)
    balance = '{:,}'.format(balance).replace(',', '.')
    nalogs = '{:,}'.format(nalogs).replace(',', '.')
    if garden == 0:
        await message.answer(f'{url}, у вас нет своего сада. Введите команду "Построить сад" {rloser}', parse_mode='html')
    else:
        await message.answer(f'''{url}, информация о вашем "Сад":
🥜 Доход: {dox} зёрен/час
🌳 Деревья: {tree} шт./10 шт.
💦 Воды: {water}/100
💸 Налоги: {nalogs}$/5.000.000$
🧺 На счету: {balance} зёрен

⭐ Не забывайте поливать дерево иначе оно засохнет.''', parse_mode='html', reply_markup=helpGarden_kb)


async def buy_garden(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 1:
        await message.answer(f'{url}, у вас уже есть построенный сад. Чтобы узнать подробнее, введите "Мой сад" {rloser}', parse_mode='html')
    else:
        balance = await getonlibalance(message)
        if balance < 1000000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки Сада. Его стоимость 1.00.000.000$ {rloser}', parse_mode='html')
        else:
            await buy_garden_db(id)
            await message.answer(f'{url}, вы успешно купили сад для подробностей введите "Мой сад" {rwin}', parse_mode='html')


async def buy_tree(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 0:
        await call.message.answer(f'{url}, у вас нет своего сада чтобы покупать деревья {rloser}', parse_mode='html')
    else:
        tree = await gettree(id)
        if tree == 10:
            await call.message.answer(f'{url}, у вас уже куплено максимальное количество деревьев {rloser}', parse_mode='html')
            return
        ch = 1000000000 * (1 + 0.15) ** (tree + 1)
        ch = int(ch)
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await call.message.answer(f'{url}, у вас недостаточно денег для покупки дерева. Её стоимость {ch2}$ {rloser}', parse_mode='html')
        else:
            await buy_tree_db(id, ch)
            await call.message.answer(f'{url}, вы успешно увеличили количество деревьев в вашем саду за {ch2}$ {rwin}', parse_mode='html')


async def snyt_pribl_garden(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 0:
        await call.message.answer(f'{url}, у вас нет своего сада чтобы собирать с него приыбль {rloser}', parse_mode='html')
    else:
        balance = await getgardenbalance(id)
        balance2 = '{:,}'.format(balance).replace(',', '.')
        if balance == 0:
            await call.message.answer(f'{url}, на данный момент на балансе вашего сада нет прибыли {rloser}', parse_mode='html')
        else:
            await snyt_pribl_garden_db(id, balance)
            await call.message.answer(f'{url}, вы успешно сняли {balance2} зёрен с баланса вашего сада {rwin}', parse_mode='html')


async def polit_dereva_garden(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 0:
        await call.message.answer(f'{url}, у вас нет своего сада чтобы поливать деревья {rloser}', parse_mode='html')
    else:
        water = await getwater(id)
        if water == 200:
            await call.message.answer(f'{url}, вы уже полили свой сад {rloser}', parse_mode='html')
        else:
            await politderevo(id)
            await call.message.answer(f'{url}, вы успешно полили свой сад {rwin}', parse_mode='html')


async def polit_dereva_garden_2(message):
    id = message.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 0:
        await message.answer(f'{url}, у вас нет своего сада чтобы поливать деревья {rloser}', parse_mode='html')
    else:
        water = await getwater(id)
        if water == 200:
            await message.answer(f'{url}, вы уже полили свой сад {rloser}', parse_mode='html')
        else:
            await politderevo(id)
            await message.answer(f'{url}, вы успешно полили свой сад {rwin}', parse_mode='html')


async def oplata_nalogov_garden(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    garden = await getogarden(id)
    result = await win_luser()
    rwin, rloser = result
    if garden == 0:
        await call.message.answer(f'{url}, у вас нет своего сада чтобы платить за него налоги {rloser}', parse_mode='html')
    else:
        nalogs = await get_garden_nalogs(id)
        nalogs2 = '{:,}'.format(nalogs).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < nalogs:
            await call.message.answer(f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}', parse_mode='html')
            return
        if nalogs == 0:
            await call.message.answer(f'{url}, у вас нет налогов чтобы их оплатить {rwin}', parse_mode='html')
        else:
            await oplata_nalogs_garden_db(id, nalogs)
            await call.message.answer(f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}', parse_mode='html')