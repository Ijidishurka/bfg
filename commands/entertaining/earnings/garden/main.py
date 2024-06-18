from aiogram import types, Dispatcher
import commands.entertaining.earnings.garden.db as db
from commands.db import url_name, getonlibalance, get_name
from commands.main import win_luser
from assets import kb
from assets.antispam import antispam_earning, antispam, new_earning_msg
from bot import bot


@antispam
async def harden_list(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свой сад и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет построить свой сад, цена постройки 1.000.000.000$. Введите команду "Построить сад" и после через команду "Мой сад" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды садов введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_garden(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await message.answer(f'{url}, у вас нет своего сада. Введите команду "Построить сад" {rloser}')
        return

    water, tree, nalogs, balance = data[0], data[1], data[2], data[3]

    dox = (tree + 1) * 3
    balance = int(balance)
    nalogs = int(nalogs)
    balance = '{:,}'.format(balance).replace(',', '.')
    nalogs = '{:,}'.format(nalogs).replace(',', '.')

    ch = int(1000000000 * (1 + 0.15) ** (tree + 1))
    ch2 = '{:,}'.format(ch).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашем "Сад":
🥜 Доход: {dox} зёрен/час
🌳 Деревья: {tree} шт./10 шт.
🆙 для следующего уровня: {ch2}$

💦 Воды: {water}/100
💸 Налоги: {nalogs}$/5.000.000$
🧺 На счету: {balance} зёрен

⭐ Не забывайте поливать дерево иначе оно засохнет.''', reply_markup=kb.garden(user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def upd_garden_text(call: types.CallbackQuery):
    uid = call.from_user.id
    url = await url_name(uid)
    data = await db.getgarden(uid)
    if not data:
        return

    water, tree, nalogs, balance = data[0], data[1], data[2], data[3]

    dox = (tree + 1) * 3
    balance = int(balance)
    nalogs = int(nalogs)
    balance = '{:,}'.format(balance).replace(',', '.')
    nalogs = '{:,}'.format(nalogs).replace(',', '.')

    ch = int(1000000000 * (1 + 0.15) ** (tree + 1))
    ch2 = '{:,}'.format(ch).replace(',', '.')

    try: await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашем "Сад":
🥜 Доход: {dox} зёрен/час
🌳 Деревья: {tree} шт./10 шт.
🆙 для следующего уровня: {ch2}$

💦 Воды: {water}/100
💸 Налоги: {nalogs}$/5.000.000$
🧺 На счету: {balance} зёрен

⭐ Не забывайте поливать дерево иначе оно засохнет.''', reply_markup=kb.garden(uid))
    except: pass


@antispam
async def buy_garden(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if data:
        await message.answer(f'{url}, у вас уже есть построенный сад. Чтобы узнать подробнее, введите "Мой сад" {rloser}')
    else:
        balance = await getonlibalance(message)
        if balance < 1000000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки Сада. Его стоимость 1.00.000.000$ {rloser}')
        else:
            await db.buy_garden_db(user_id)
            await message.answer(f'{url}, вы успешно купили сад для подробностей введите "Мой сад" {rwin}')


@antispam_earning
async def buy_tree(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего сада чтобы покупать деревья {rloser}')
    else:
        if data[1] == 10:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас уже куплено максимальное количество деревьев {rloser}')
            return
        ch = int(1000000000 * (1 + 0.15) ** (data[1] + 1))
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег для покупки дерева. Её стоимость {ch2}$ {rloser}')
        else:
            await db.buy_tree_db(user_id, ch)
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили количество деревьев в вашем саду за {ch2}$ {rwin}')
            await upd_garden_text(call)


@antispam_earning
async def snyt_pribl_garden(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего сада чтобы собирать с него приыбль {rloser}')
    else:
        if data[3] == 0:
            await bot.answer_callback_query(call.id, text=f'{url}, на данный момент на балансе вашего сада нет прибыли {rloser}')
        else:
            balance2 = '{:,}'.format(data[3]).replace(',', '.')
            await db.snyt_pribl_garden_db(user_id, data[3])
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно сняли {balance2} зёрен с баланса вашего сада {rwin}')
            await upd_garden_text(call)


@antispam_earning
async def polit_dereva_garden(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего сада чтобы поливать деревья {rloser}')
    else:
        if data[0] == 100:
            await bot.answer_callback_query(call.id, text=f'{url}, вы уже полили свой сад {rloser}')
        else:
            await db.politderevo(user_id)
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно полили свой сад {rwin}')
            await upd_garden_text(call)


@antispam
async def polit_dereva_garden_2(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await message.answer(f'{url}, у вас нет своего сада чтобы поливать деревья {rloser}')
    else:
        if data[0] == 100:
            await message.answer(f'{url}, вы уже полили свой сад {rloser}')
        else:
            await db.politderevo(user_id)
            await message.answer(f'{url}, вы успешно полили свой сад {rwin}')


@antispam_earning
async def oplata_nalogov_garden(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgarden(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего сада чтобы платить за него налоги {rloser}')
    else:
        balance = await getonlibalance(call)
        if balance < data[2]:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
            return

        if data[2] == 0:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        else:
            nalogs2 = '{:,}'.format(data[2]).replace(',', '.')
            await db.oplata_nalogs_garden_db(user_id, data[2])
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
            await upd_garden_text(call)


def reg(dp: Dispatcher):
    dp.register_message_handler(polit_dereva_garden_2, lambda message: message.text.lower().startswith('сад полить'))
    dp.register_message_handler(harden_list, lambda message: message.text.lower().startswith('сад'))
    dp.register_message_handler(my_garden, lambda message: message.text.lower().startswith('мой сад'))
    dp.register_message_handler(buy_garden, lambda message: message.text.lower().startswith('построить сад'))
    dp.register_callback_query_handler(buy_tree, text_startswith='garden-buy-tree')
    dp.register_callback_query_handler(polit_dereva_garden, text_startswith='garden-polit')
    dp.register_callback_query_handler(snyt_pribl_garden, text_startswith='garden-sobrat')
    dp.register_callback_query_handler(oplata_nalogov_garden, text_startswith='garden-nalog')
