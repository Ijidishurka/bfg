from aiogram import types, Dispatcher

import commands.entertaining.earnings.generator.db as db
from assets.transform import transform_int as tr
from assets import keyboards as kb
from assets.antispam import new_earning, antispam, antispam_earning
from filters.custom import TextIn, StartsWith
from user import BFGuser, BFGconst


@antispam
async def generator_list_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'''{user.url}, с данного момента ты можешь сам построить свой генератор и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свой генератор, он будет стоять как и прежде 2.000 материи. Введите команду "Построить генератор" и после через команду "Мой генератор" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды генератора введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_generator_cmd(message: types.Message, user: BFGuser):
    generator = user.generator
    win, lose = BFGconst.emj()

    if not generator:
        await message.answer(f'{user.url}, у вас нет своего генератора {lose}')
        return
    
    await edit_generator_msg(message, user, 'send')


async def edit_generator_msg(call: types.CallbackQuery | types.Message, user: BFGuser, action='edit') -> None:
    generator = user.generator
    
    if action == 'edit':
        await user.update()

    dox = int((generator.turbine.get() + 1) * 20)

    txt = f'''{user.url}, информация о вашем "Генератор материи":
💷 Доход: {dox} материи/час
💼 Турбины: {generator.turbine} шт.
🆙 для следующего уровня: 2000 🌌

💸 Налоги: {generator.nalogs.tr()}$/5.000.000$
💰 На счету: {generator.balance.tr()} материи'''
    
    try:
        if action == 'edit':
            await call.message.edit_text(text=txt, reply_markup=kb.generator(user.id))
        else:
            msg = await call.answer(text=txt, reply_markup=kb.generator(user.id))
            await new_earning(msg)
    except:
        return


@antispam
async def buy_generator_cmd(message: types.Message, user: BFGuser):
    generator = user.generator
    win, lose = BFGconst.emj()
    
    if generator:
        await message.answer(f'{user.url}, у вас уже есть построенный генератор. Чтобы узнать подробнее, введите "Мой генератор" {lose}')
        return

    if int(user.mine.matter) < 2000:
        await message.answer(f'{user.url}, у вас недостаточно материи для постройки генератора. Его стоимость 2.000 материи {lose}')
        return

    await db.buy_generator(user.id)
    await message.answer(f'{user.url}, вы успешно построили генератор для подробностей введите "Мой генератор" {win}')


@antispam_earning
async def buy_turbine_cmd(call: types.CallbackQuery, user: BFGuser):
    generator = user.generator
    win, lose = BFGconst.emj()

    if not generator:
        return

    if int(generator.turbine) >= 10:
        await call.answer(f'{user.name}, у вас уже куплено максимальное количество турбин {lose}')
        return

    ch = 2000  # стоимость 1 турбины

    if int(user.mine.matter) < ch:
        await call.answer(f'{user.name}, у вас недостаточно денег для покупки турбины. Её стоимость 2.000 материи {lose}')
        return

    await db.buy_turbine(user.id)
    await call.answer(f'{user.name}, вы успешно купили турбину за {tr(ch)}🌌 {win}')
    await edit_generator_msg(call, user)


@antispam_earning
async def withdraw_profit_cmd(call: types.CallbackQuery, user: BFGuser):
    generator = user.generator
    win, lose = BFGconst.emj()
    
    if not generator:
        return

    if int(generator.balance) <= 0:
        await call.answer(f'{user.name}, на данный момент на балансе вашего генератора нет прибыли {lose}')
        return

    await db.withdraw_profit(user.id, generator.balance.get())
    await call.answer(f'{user.name}, вы успешно сняли {generator.balance.tr()}🌌 с баланса вашего генератора {win}')
    await edit_generator_msg(call, user)


@antispam_earning
async def payment_taxes_cmd(call: types.CallbackQuery, user: BFGuser):
    generator = user.generator
    win, lose = BFGconst.emj()

    if not generator:
        return

    if int(user.balance) < int(generator.nalogs):
        await call.answer(f'{user.name}, у вас недостаточно денег чтоб оплатить налоги {lose}')
        return

    if int(generator.nalogs) == 0:
        await call.answer(f'{user.name}, у вас нет налогов чтобы их оплатить {win}')
        return

    await db.payment_taxes(user.id, generator.nalogs.get())
    await call.answer(f'{user.name}, вы успешно оплатили налоги на сумму {generator.nalogs.tr()}$ с вашего игрового баланса {win}')
    await edit_generator_msg(call, user)


@antispam
async def sell_generator_cmd(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    generator = user.generator
    
    if not generator:
        await message.answer(f'{user.url}, у вас нет своего генератора {lose}')
        return
    
    summ = (1000 * generator.turbine.get()) + 1000  # Половина стоимости генератора + турбин
    
    await db.sell_generator(user.id, summ)
    await message.answer(f'{user.url}, Вы успешно продали свой генератор за {tr(summ)}🌌 {win}')


def reg(dp: Dispatcher):
    dp.message.register(generator_list_cmd, TextIn("генератор"))
    dp.message.register(my_generator_cmd, TextIn("мой генератор"))
    dp.message.register(buy_generator_cmd, TextIn("построить генератор"))
    dp.callback_query.register(withdraw_profit_cmd, StartsWith("generator-sobrat"))
    dp.callback_query.register(buy_turbine_cmd, StartsWith("generator-buy-turb"))
    dp.callback_query.register(payment_taxes_cmd, StartsWith("generator-nalog"))
    dp.message.register(sell_generator_cmd, TextIn("продать генератор"))
