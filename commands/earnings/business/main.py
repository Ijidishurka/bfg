from aiogram import Dispatcher, types
from commands.earnings.business.db import *
from commands.db import getonlibalance, url_name, get_name
from commands.main import win_luser
import commands.assets.kb as kb
from assets.antispam import antispam_earning, new_earning_msg, antispam
from bot import bot


@antispam
async def business_list(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    await message.answer(f'''{url}, теперь ты можешь принимать решения сам и влиять на свой бизнес.

🪓 Для начала я проведу тебе маленький инструктаж по поводу данных бизнесов, ты не можешь просто купить бизнес и начать зарабатывать на нём. Теперь вам предоставлена возможность самому влиять на доход, увеличить территорию бизнеса, закупать продукты и платить налоги в казну штата.

🏗 Для начала вам потребуется построить площадку для того чтобы возвести на ней свой бизнес. Для этого используйте команду "Построить бизнес", после этого вами будет куплена маленькая территория под бизнес.

💫 Далее вы можете при помощи команд управлять бизнесом, увеличивать его доход, покупать улучшения и прочее. Чтобы узнать все команды введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_business(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if not data:
        return await message.answer(f'{url}, у вас нет своего бизнеса чтобы построить введите команду "Построить бизнес" {rloser}')

    dox = int(90000000 * data[4] / 15)
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format(int(data[2])).replace(',', '.')
    territory = '{:,}'.format(data[3]).replace(',', '.')
    bsterritory = '{:,}'.format(data[4]).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    ch = int(22000000 * (1 + 0.15) ** (data[3] - 4))
    ch = '{:,}'.format(ch).replace(',', '.')

    ch2 = int(22000000 * (1 + 0.15) ** (data[4] - 1))
    ch2 = '{:,}'.format(ch2).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашем бизнесе "Бизнес":
🧱 Территория: {territory} м²
🆙 для следующего уровня: {ch}$
🏢 Территория бизнеса: {bsterritory} м²
🆙 для следующего уровня: {ch2}$

💷 Доход: {dox}$
💸 Налоги: {nalogs}$/5.000.000$
💰 Прибыль: {balance}$''', reply_markup=kb.business(user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def upd_business_text(call: types.CallbackQuery):
    uid = call.from_user.id
    url = await url_name(uid)
    data = await getbusiness(uid)
    if not data:
        return

    dox = int(90000000 * data[4] / 15)
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format(int(data[2])).replace(',', '.')
    territory = '{:,}'.format(data[3]).replace(',', '.')
    bsterritory = '{:,}'.format(data[4]).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    ch = int(22000000 * (1 + 0.15) ** (data[3] - 4))
    ch = '{:,}'.format(ch).replace(',', '.')

    ch2 = int(22000000 * (1 + 0.15) ** (data[4] - 1))
    ch2 = '{:,}'.format(ch2).replace(',', '.')

    try: await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашем бизнесе "Бизнес":
🧱 Территория: {territory} м²
🆙 для следующего уровня: {ch}$
🏢 Территория бизнеса: {bsterritory} м²
🆙 для следующего уровня: {ch2}$

💷 Доход: {dox}$
💸 Налоги: {nalogs}$/5.000.000$
💰 Прибыль: {balance}$''', reply_markup=kb.business(uid))
    except: pass


@antispam
async def buy_business(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if data:
        return await message.answer(f'{url}, у вас уже есть построенная территория под бизнес. Чтобы узнать подробнее, введите "Мой бизнес" {rloser}')
    else:
        balance = await getonlibalance(message)
        if balance < 500000000:
            await message.answer(f'{url}, у вас недостаточно денег для постройки территории бизнеса. Её стоимость 500 млн$ {rloser}')
        else:
            await buy_business_db(user_id)
            await message.answer(f'{url}, вы успешно построили свой бизнес для подробностей введите "Мой бизнес" {rwin}')


@antispam_earning
async def buy_territory(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нету своего бизнеса чтобы увеличивать его территорию {rloser}')
    else:
        ch = int(22000000 * (1 + 0.15) ** (data[3] - 4))
        ch2 = '{:,}'.format(ch).replace(',', '.')
        balance = await getonlibalance(call)
        if balance < ch:
            await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег на балансе чтобы увеличить территорию бизнеса {rloser}')
        else:
            await buy_territory_db(user_id, ch)
            await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили территорию бизнеса на 1 м² за {ch2}$ {rwin}')
            await upd_business_text(call)


@antispam_earning
async def buy_bsterritory(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего бизнеса чтобы увеличить бизнес {rloser}')
        return

    if data[3] <= data[4]:
        await bot.answer_callback_query(call.id, text=f'{url}, чтобы увеличить бизнес для начала увеличьте его территорию {rloser}')
        return

    ch = int(22000000 * (1 + 0.15) ** (data[4] - 1))
    ch2 = '{:,}'.format(ch).replace(',', '.')
    balance = await getonlibalance(call)
    if balance < ch:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег на балансе чтобы увеличить бизнес {rloser}')
    else:
        await buy_bsterritory_db(user_id, ch)
        await bot.answer_callback_query(call.id, text=f'{url}, вы успешно увеличили бизнес на 1 м² за {ch2}$ {rwin}')
        await upd_business_text(call)


@antispam_earning
async def snyt_pribl_business(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего бизнеса чтобы собирать с него приыбль {rloser}')
        return

    if data[1] == 0:
        await bot.answer_callback_query(call.id, text=f'{url}, на данный момент на балансе вашего бизнеса нет прибыли {rloser}')
    else:
        balance2 = '{:,}'.format(data[1]).replace(',', '.')
        await snyt_pribl_bs_db(user_id, data[1])
        await bot.answer_callback_query(call.id, text=f'{url}, вы успешно сняли {balance2}$ с баланса вашего бизнеса {rwin}')
        await upd_business_text(call)


@antispam_earning
async def oplata_nalogov_business(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    data = await getbusiness(user_id)
    if not data:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет своего бизнеса чтобы платить за него налоги {rloser}')
        return

    nalogs2 = '{:,}'.format(data[2]).replace(',', '.')
    balance = await getonlibalance(call)

    if balance < data[2]:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
        return

    if data[2] == 0:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        return

    await oplata_nalogs_bs_db(user_id, data[2])
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
    await upd_business_text(call)


def reg(dp: Dispatcher):
    dp.register_message_handler(my_business, lambda message: message.text.lower().startswith('мой бизнес'))
    dp.register_message_handler(business_list, lambda message: message.text.lower().startswith('бизнес'))
    dp.register_message_handler(buy_business, lambda message: message.text.lower().startswith('построить бизнес'))
    dp.register_callback_query_handler(snyt_pribl_business, text_startswith='business-sobrat')
    dp.register_callback_query_handler(buy_territory, text_startswith='business-ter')
    dp.register_callback_query_handler(buy_bsterritory, text_startswith='business-bis')
    dp.register_callback_query_handler(oplata_nalogov_business, text_startswith='business-nalog')
