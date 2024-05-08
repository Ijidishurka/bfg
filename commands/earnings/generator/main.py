from commands.earnings.generator.db import *
from commands.db import register_users, getname, getonlibalance, getidname
from commands.main import geturl
from commands.main import win_luser
from commands.assets.kb import help_generatorKB


async def generator_list(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    await register_users(message)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свой генератор и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свой генератор, он будет стоять как и прежде 2.000 материи. Введите команду "Построить генератор" и после через команду "Мой генератор" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды генератора введите команду "Помощь" и выберите соответствующую кнопку.''', parse_mode='html')


async def my_generator(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    result = await win_luser()
    rwin, rloser = result
    turbine, balance, nalogs, gen = await getgenerator(id)
    dox = (turbine + 1) * 20
    dox = int(dox)
    balance = int(balance)
    nalogs = int(nalogs)
    balance = '{:,}'.format(balance).replace(',', '.')
    nalogs = '{:,}'.format(nalogs).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')
    await register_users(message)
    if gen == 0:
        await message.answer(f'{url}, у вас нет своего генератора {rloser}', parse_mode='html')
    else:
        await message.answer(f'''{url}, информация о вашем "Генератор материи":
💷 Доход: {dox} материи/час
💼 Турбины: {turbine} шт.
💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance} материи''', parse_mode='html', reply_markup=help_generatorKB)


async def buy_generator(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    gen = await getgenertor2(id)
    result = await win_luser()
    rwin, rloser = result
    if gen == 1:
        await message.answer(f'{url}, у вас уже есть построенный генератор. Чтобы узнать подробнее, введите "Мой генератор" {rloser}', parse_mode='html')
    else:
        balance = await getonlimater(id)
        if balance < 2000:
            await message.answer(f'{url}, у вас недостаточно материи для постройки генератора. Его стоимость 2.000 материи {rloser}', parse_mode='html')
        else:
            await buy_generator_db(id)
            await message.answer(f'{url}, вы успешно построили генератор для подробностей введите "Мой генератор" {rwin}', parse_mode='html')


async def buy_turbine(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    gen = await getgenertor2(id)
    result = await win_luser()
    rwin, rloser = result
    if gen == 0:
        await call.message.answer(f'{url}, у вас нет своего генератора чтобы купить турбины {rloser}', parse_mode='html')
    else:
        turbine = await getturbine(id)
        if turbine >= 10:
            return await call.message.answer(
                f'{url}, у вас уже куплено максимальное количество турбин {rloser}',
                parse_mode='html')
        ch = 2000
        balance = await getonlimater(id)
        if balance < ch:
            return await call.message.answer(f'{url}, у вас недостаточно денег для покупки турбины. Её стоимость 2.000 материи {rloser}', parse_mode='html')
        else:
            ch2 = '{:,}'.format(ch).replace(',', '.')
            await buy_turbine_db(id)
            await call.message.answer(f'{url}, вы успешно купили турбину за {ch2}$ {rwin}', parse_mode='html')


async def snyt_pribl_generator(call):
    id = call.from_user.id
    name = await getidname(id)
    url = await geturl(id, name)
    ferm = await getferm(id)
    result = await win_luser()
    rwin, rloser = result
    if ferm == 0:
        await call.message.answer(f'{url}, у вас нет свое фермы чтобы собрать с неё приыбль {rloser}', parse_mode='html')
    else:
        balance = await get_ferma_balance(id)
        balance2 = '{:,}'.format(balance).replace(',', '.')
        if balance == 0:
            await call.message.answer(f'{url}, на данный момент на балансе вашей фермы нет прибыли {rloser}', parse_mode='html')
        else:
            await snyt_pribl_ferma_db(id, balance)
            await call.message.answer(f'{url}, вы успешно сняли {balance2}฿ с баланса вашей фермы {rwin}', parse_mode='html')


async def oplata_nalogov_generator(call):
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
