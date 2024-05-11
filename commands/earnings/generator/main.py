import commands.earnings.generator.db as db
from commands.db import url_name, getonlibalance, getidname
from commands.main import win_luser
from commands.assets.kb import help_generatorKB


async def generator_list(message):
    id = message.from_user.id
    url = await url_name(id)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свой генератор и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свой генератор, он будет стоять как и прежде 2.000 материи. Введите команду "Построить генератор" и после через команду "Мой генератор" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды генератора введите команду "Помощь" и выберите соответствующую кнопку.''')


async def my_generator(message):
    id = message.from_user.id
    url = await url_name(id)
    rwin, rloser = await win_luser()
    data = await db.getgenerator(id)
    if not data:
        await message.answer(f'{url}, у вас нет своего генератора {rloser}')
        return

    dox = int((data[0] + 1) * 20)
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format((int(data[2]))).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    await message.answer(f'''{url}, информация о вашем "Генератор материи":
💷 Доход: {dox} материи/час
💼 Турбины: {data[0]} шт.
💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance} материи''', reply_markup=help_generatorKB)


async def buy_generator(message):
    id = message.from_user.id
    url = await url_name(id)
    rwin, rloser = await win_luser()
    data = await db.getgenerator(id)
    if data:
        await message.answer(f'{url}, у вас уже есть построенный генератор. Чтобы узнать подробнее, введите "Мой генератор" {rloser}')
    else:
        balance = await db.getonlimater(id)
        if balance < 2000:
            await message.answer(f'{url}, у вас недостаточно материи для постройки генератора. Его стоимость 2.000 материи {rloser}')
        else:
            await db.buy_generator_db(id)
            await message.answer(f'{url}, вы успешно построили генератор для подробностей введите "Мой генератор" {rwin}')


async def buy_turbine(call):
    id = call.from_user.id
    url = await url_name(id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(id)

    if not gen:
        await call.message.answer(f'{url}, у вас нет своего генератора чтобы купить турбины {rloser}')
    else:
        if gen[0] >= 10:
            return await call.message.answer(f'{url}, у вас уже куплено максимальное количество турбин {rloser}')

        ch = 2000
        balance = await db.getonlimater(id)

        if balance < ch:
            return await call.message.answer(f'{url}, у вас недостаточно денег для покупки турбины. Её стоимость 2.000 материи {rloser}')
        else:
            ch2 = '{:,}'.format(ch).replace(',', '.')
            await db.buy_turbine_db(id)
            await call.message.answer(f'{url}, вы успешно купили турбину за {ch2}🌌 {rwin}')


async def snyt_pribl_generator(call):
    id = call.from_user.id
    url = await url_name(id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(id)
    if not gen:
        await call.message.answer(f'{url}, у вас нет своего генератора чтобы собрать с него приыбль {rloser}')
    else:
        if gen[1] <= 0:
            await call.message.answer(f'{url}, на данный момент на балансе вашего генератора нет прибыли {rloser}')
        else:
            balance2 = '{:,}'.format(gen[1]).replace(',', '.')
            await db.snyt_pribl_gen_db(id, gen[1])
            await call.message.answer(f'{url}, вы успешно сняли {balance2}🌌 с баланса вашей фермы {rwin}')


async def oplata_nalogov_generator(call):
    id = call.from_user.id
    url = await url_name(id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(id)
    if not gen:
        await call.message.answer(f'{url}, у вас нет своего генератора чтобы платить за него налоги {rloser}')
    else:
        balance = await getonlibalance(call)
        if balance < gen[2]:
            await call.message.answer(f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
            return
        if gen[2] == 0:
            await call.message.answer(f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        else:
            nalogs2 = '{:,}'.format(gen[2]).replace(',', '.')
            await db.oplata_nalogs_gen_db(id, gen[2])
            await call.message.answer(f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
