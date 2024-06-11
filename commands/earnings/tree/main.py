from aiogram import types, Dispatcher
from bot import bot
from commands.earnings.tree import db
from commands.db import url_name, getonlibalance, get_name
from commands.main import win_luser
import commands.assets.kb as kb
from assets.antispam import new_earning_msg, antispam, antispam_earning


@antispam
async def my_tree(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if not data:
        await message.answer(f'{url}, у вас нет своего участка денежного дерева {rloser}')
        return

    dox = int(3000 * (data[3] ** 3.8))
    tre_price = int(5000 * (data[3] ** 3.8))
    ter_price = int(5000 * (data[2] ** 3.8))

    balance = '{:,}'.format(int(data[0])).replace(',', '.')
    nalogs = '{:,}'.format((int(data[1]))).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')
    tre_price = '{:,}'.format(tre_price).replace(',', '.')
    ter_price = '{:,}'.format(ter_price).replace(',', '.')
    yen = '{:,}'.format(data[4]).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашем участке "Денежное дерево":
🏡 Участок: {data[2]} м²
🆙 для следующего уровня: {ter_price} ☣️
🌳 Размер дерева: {data[3]} м
🆙 для следующего уровня: {tre_price} ☣️

💷 Доход: {dox}$
💸 Налоги: {nalogs}$/5.000.000$
💰 Прибыль: {balance}$
💴 Йены: {yen}¥''', reply_markup=kb.tree(user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def edit_tree_msg(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await url_name(user_id)
    data = await db.gettree(user_id)
    if not data:
        return

    dox = int(3000 * (data[3] ** 3.8))
    tre_price = int(5000 * (data[3] ** 3.8))
    ter_price = int(5000 * (data[2] ** 3.8))

    balance = '{:,}'.format(int(data[0])).replace(',', '.')
    nalogs = '{:,}'.format((int(data[1]))).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')
    tre_price = '{:,}'.format(tre_price).replace(',', '.')
    ter_price = '{:,}'.format(ter_price).replace(',', '.')
    yen = '{:,}'.format(data[4]).replace(',', '.')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашем участке "Денежное дерево":
🏡 Участок: {data[2]} м²
🆙 для следующего уровня: {ter_price} ☣️
🌳 Размер дерева: {data[3]} м
🆙 для следующего уровня: {tre_price} ☣️

💷 Доход: {dox}$
💸 Налоги: {nalogs}$/5.000.000$
💰 Прибыль: {balance}$
💴 Йены: {yen}¥''', reply_markup=kb.tree(user_id))


@antispam
async def buy_tree(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if data:
        await message.answer(f'{url}, у вас уже есть свой участок. Для подробностей введите "Моё дерево" {rwin}')
    else:
        balance = await db.getonlibiores(user_id)
        if balance < 500_000_000:
            await message.answer(f'{url}, у вас недостаточно биоресурсов для постройки участка денежного дерева. '
                                 f'Его стоимость 500.000.000 кг биоресурса {rloser}')
            return

        await db.buy_tree_db(user_id)
        await message.answer(f'{url}, вы успешно построили свой участок для подробностей введите "Моё дерево" {rwin}')


@antispam_earning
async def snyt_pribl(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if not data:
        return

    if data[0] <= 0 and data[4] <= 0:
        await bot.answer_callback_query(call.id, text=f'{url}, на данный момент на балансе вашего участка нет прибыли {rloser}')
        return

    balance2 = '{:,}'.format(data[0]).replace(',', '.')
    yen2 = '{:,}'.format(data[4]).replace(',', '.')

    await db.snyt_pribl_db(user_id, data[0], data[4])
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно сняли {balance2}$ и {yen2}¥ с баланса вашего участка {rwin}')
    await edit_tree_msg(call)


@antispam_earning
async def oplata_nalogov(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if not data:
        return

    balance = await getonlibalance(call)
    if balance < data[1]:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
        return

    if data[1] <= 0:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        return

    nalogs2 = '{:,}'.format(data[2]).replace(',', '.')
    await db.oplata_nalogs_db(user_id, data[1])
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
    await edit_tree_msg(call)


@antispam_earning
async def buy_ter(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if not data:
        return

    balance = await db.getonlibiores(user_id)
    summ = int(5000 * (data[2] ** 3.8))

    if balance < summ:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно биоресурсов {rloser}')
        return

    summ2 = '{:,}'.format(summ).replace(',', '.')
    await db.buy_ter_db(user_id, summ)
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили участок за {summ2}$ {rwin}')
    await edit_tree_msg(call)


@antispam_earning
async def buy_tree_call(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.gettree(user_id)
    if not data:
        return

    balance = await db.getonlibiores(user_id)
    summ = int(5000 * (data[3] ** 3.8))

    if balance < summ:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно биоресурсов {rloser}')
        return

    if data[2] <= data[3]:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно места {rloser}')
        return

    summ2 = '{:,}'.format(summ).replace(',', '.')
    await db.buy_tree_ter_db(user_id, summ)
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили дерево за {summ2}$ {rwin}')
    await edit_tree_msg(call)


def reg(dp: Dispatcher):
    dp.register_message_handler(my_tree, lambda message: message.text.lower().startswith('моё дерево'))
    dp.register_message_handler(buy_tree, lambda message: message.text.lower().startswith('построить участок'))
    dp.register_callback_query_handler(snyt_pribl, text_startswith='tree-sobrat')
    dp.register_callback_query_handler(oplata_nalogov, text_startswith='tree-nalog')
    dp.register_callback_query_handler(buy_tree_call, text_startswith='tree-tree')
    dp.register_callback_query_handler(buy_ter, text_startswith='tree-ter')