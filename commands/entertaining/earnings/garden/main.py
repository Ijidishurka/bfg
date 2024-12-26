from aiogram import types, Dispatcher
import commands.entertaining.earnings.garden.db as db
from assets.transform import transform_int as tr
from assets import kb
from assets.antispam import antispam_earning, antispam, new_earning
from bot import bot
from user import BFGuser, BFGconst


@antispam
async def garden_info(message: types.Message, user: BFGuser):
    await message.answer(f'''{user.url}, с данного момента ты можешь сам построить свой сад и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет построить свой сад, цена постройки 1.000.000.000$. Введите команду "Построить сад" и после через команду "Мой сад" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды садов введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_garden(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    garden = user.garden

    if not garden:
        await message.answer(f'{user.url}, у вас нет своего сада. Введите команду "Построить сад" {lose}')
        return

    await upd_garden_text(message, user, action='send')


async def upd_garden_text(call: types.CallbackQuery, user: BFGuser, action='edit'):
    garden = user.garden
    
    if action == 'edit':
        await user.update()

    dox = (garden.tree.get() + 1) * 3
    ch = int(1_000_000_000 * (1 + 0.15) ** (garden.tree.get() + 1))

    txt = f'''{user.url}, информация о вашем "Сад":
🥜 Доход: {tr(dox)} зёрен/час
🌳 Деревья: {garden.tree.tr()} шт./10 шт.
🆙 для следующего уровня: {tr(ch)}$

💦 Воды: {garden.water.tr()}/100
💸 Налоги: {garden.nalogs.tr()}$/5.000.000$
🧺 На счету: {garden.balance.tr()} зёрен

⭐ Не забывайте поливать дерево иначе оно засохнет.'''
    
    try:
        if action == 'edit':
            await call.message.edit_text(text=txt, reply_markup=kb.garden(user.user_id))
        else:
            msg = await call.answer(text=txt, reply_markup=kb.garden(user.user_id))
            await new_earning(msg)
    except:
        return


@antispam
async def buy_garden(message: types.Message, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()
    
    if garden:
        await message.answer(f'{user.url}, у вас уже есть построенный сад. Чтобы узнать подробнее, введите "Мой сад" {lose}')
        return

    if int(user.balance) < 1_000_000_000:
        await message.answer(f'{user.url}, у вас недостаточно денег для постройки Сада. Его стоимость 1.00.000.000$ {lose}')
        return

    await db.buy_garden(user.user_id)
    await message.answer(f'{user.url}, вы успешно купили сад для подробностей введите "Мой сад" {win}')


@antispam_earning
async def buy_tree(call: types.CallbackQuery, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()

    if not garden:
        return

    if garden.tree.get() == 10:
        await bot.answer_callback_query(call.id, text=f'{user.name}, у вас уже куплено максимальное количество деревьев {lose}')
        return

    ch = int(1_000_000_000 * (1 + 0.15) ** (garden.tree.get() + 1))

    if int(user.balance) < ch:
        await bot.answer_callback_query(call.id, text=f'{user.name}, у вас недостаточно денег для покупки дерева. Её стоимость {tr(ch)}$ {lose}')
        return
    
    await db.buy_tree(user.user_id, ch)
    await bot.answer_callback_query(call.id, text=f'{user.name}, вы успешно увеличили количество деревьев в вашем саду за {tr(ch)}$ {win}')
    await upd_garden_text(call, user)


@antispam_earning
async def withdraw_profit(call: types.CallbackQuery, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()

    if not garden:
        return

    if int(garden.balance) == 0:
        await bot.answer_callback_query(call.id, text=f'{user.name}, на данный момент на балансе вашего сада нет прибыли {lose}')
        return

    await db.withdraw_profit(user.user_id, garden.balance.get())
    await bot.answer_callback_query(call.id, text=f'{user.name}, вы успешно сняли {garden.balance.tr()} зёрен с баланса вашего сада {win}')
    await upd_garden_text(call, user)


@antispam_earning
async def water_garden_call(call: types.CallbackQuery, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()

    if not garden:
        return

    if int(garden.water) >= 100:
        await bot.answer_callback_query(call.id, text=f'{user.name}, вы уже полили свой сад {lose}')
        return

    await garden.water.upd(100)
    await bot.answer_callback_query(call.id, text=f'{user.name}, вы успешно полили свой сад {win}')
    await upd_garden_text(call, user)


@antispam
async def water_garden(message: types.Message, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()

    if not garden:
        await message.answer(f'{user.url}, у вас нет своего сада чтобы поливать деревья {lose}')
        return

    if int(garden.water) >= 100:
        await message.answer(f'{user.url}, вы уже полили свой сад {lose}')
        return

    await garden.water.upd(100)
    await message.answer(f'{user.url}, вы успешно полили свой сад {win}')


@antispam_earning
async def pay_taxes(call: types.CallbackQuery, user: BFGuser):
    garden = user.garden
    win, lose = BFGconst.emj()

    if not garden:
        return

    if int(user.balance) < int(garden.nalogs):
        await bot.answer_callback_query(call.id, text=f'{user.name}, у вас недостаточно денег чтоб оплатить налоги {lose}')
        return

    if int(garden.nalogs) == 0:
        await bot.answer_callback_query(call.id, text=f'{user.name}, у вас нет налогов чтобы их оплатить {win}')
        return

    await db.payment_taxes(user.user_id, garden.nalogs.get())
    await bot.answer_callback_query(call.id, text=f'{user.name}, вы успешно оплатили налоги на сумму {garden.nalogs.tr()}$ с вашего игрового баланса {win}')
    await upd_garden_text(call, user)


@antispam
async def sell_garden(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    garden = user.garden
    
    if not garden:
        await message.answer(f'{user.url}, у вас нет своего сада. Введите команду "Построить сад" {lose}')
        return
    
    summ = 500_000_000  # Половина стоимости сада
    
    for i in range(1, garden.tree.get() + 1):  # Компенсация за деревья (50%)
        summ += int(1_000_000_000 * (1 + 0.15) ** (i + 1)) // 2

    await db.sell_garden(user.user_id, summ)
    await message.answer(f'{user.url}, Вы успешно продали свой сад за {tr(summ)}$ {win}')


def reg(dp: Dispatcher):
    dp.register_message_handler(water_garden, lambda message: message.text.lower().startswith('сад полить'))
    dp.register_message_handler(garden_info, lambda message: message.text.lower().startswith('сад'))
    dp.register_message_handler(my_garden, lambda message: message.text.lower().startswith('мой сад'))
    dp.register_message_handler(buy_garden, lambda message: message.text.lower().startswith('построить сад'))
    dp.register_callback_query_handler(buy_tree, text_startswith='garden-buy-tree')
    dp.register_callback_query_handler(water_garden_call, text_startswith='garden-polit')
    dp.register_callback_query_handler(withdraw_profit, text_startswith='garden-sobrat')
    dp.register_callback_query_handler(pay_taxes, text_startswith='garden-nalog')
    dp.register_message_handler(sell_garden, lambda message: message.text.lower() == 'продать сад')
