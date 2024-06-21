from aiogram import types, Dispatcher
from bot import bot
import commands.entertaining.earnings.generator.db as db
from commands.db import url_name, get_balance, get_name
from commands.main import win_luser
from assets import kb
from assets.antispam import new_earning_msg, antispam, antispam_earning


@antispam
async def generator_list(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    await message.answer(f'''{url}, с данного момента ты можешь сам построить свой генератор и улучшать его. Это очень весело и облегчит тебе работу.

🪓 Для начала тебе нужно будет создать свой генератор, он будет стоять как и прежде 2.000 материи. Введите команду "Построить генератор" и после через команду "Мой генератор" вы сможете настраивать его и улучшать повышая свою прибыль.

📎 Чтобы узнать все команды генератора введите команду "Помощь" и выберите соответствующую кнопку.''')


@antispam
async def my_generator(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgenerator(user_id)

    if not data:
        await message.answer(f'{url}, у вас нет своего генератора {rloser}')
        return

    dox = int((data[0] + 1) * 20)
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format((int(data[2]))).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашем "Генератор материи":
💷 Доход: {dox} материи/час
💼 Турбины: {data[0]} шт.
🆙 для следующего уровня: 2000 🌌

💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance} материи''', reply_markup=kb.generator(user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def edit_generator_msg(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await url_name(user_id)
    data = await db.getgenerator(user_id)

    if not data:
        return

    dox = int((data[0] + 1) * 20)
    balance = '{:,}'.format(int(data[1])).replace(',', '.')
    nalogs = '{:,}'.format((int(data[2]))).replace(',', '.')
    dox = '{:,}'.format(dox).replace(',', '.')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашем "Генератор материи":
💷 Доход: {dox} материи/час
💼 Турбины: {data[0]} шт.
🆙 для следующего уровня: 2000 🌌

💸 Налоги: {nalogs}$/5.000.000$
💰 На счету: {balance} материи''', reply_markup=kb.generator(user_id))


@antispam
async def buy_generator(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getgenerator(user_id)

    if data:
        await message.answer(f'{url}, у вас уже есть построенный генератор. Чтобы узнать подробнее, введите "Мой генератор" {rloser}')
        return

    balance = await db.getonlimater(user_id)
    if balance < 2000:
        await message.answer(f'{url}, у вас недостаточно материи для постройки генератора. Его стоимость 2.000 материи {rloser}')
    else:
        await db.buy_generator_db(user_id)
        await message.answer(f'{url}, вы успешно построили генератор для подробностей введите "Мой генератор" {rwin}')


@antispam_earning
async def buy_turbine(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(user_id)

    if not gen:
        return

    if gen[0] >= 10:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас уже куплено максимальное количество турбин {rloser}')
        return

    ch = 2000  # стоимость 1 турбины
    balance = await db.getonlimater(user_id)

    if balance < ch:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег для покупки турбины. Её стоимость 2.000 материи {rloser}')
        return

    ch2 = '{:,}'.format(ch).replace(',', '.')
    await db.buy_turbine_db(user_id)
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно купили турбину за {ch2}🌌 {rwin}')
    await edit_generator_msg(call)


@antispam_earning
async def snyt_pribl(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(user_id)

    if not gen:
        return

    if gen[1] <= 0:
        await bot.answer_callback_query(call.id, text=f'{url}, на данный момент на балансе вашего генератора нет прибыли {rloser}')
        return

    balance2 = '{:,}'.format(gen[1]).replace(',', '.')
    await db.snyt_pribl_gen_db(user_id, gen[1])
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно сняли {balance2}🌌 с баланса вашего генератора {rwin}')
    await edit_generator_msg(call)


@antispam_earning
async def oplata_nalogov(call):
    user_id = call.from_user.id
    url = await get_name(user_id)
    rwin, rloser = await win_luser()
    gen = await db.getgenerator(user_id)

    if not gen:
        return

    balance = await get_balance(user_id)
    if balance < gen[2]:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас недостаточно денег чтоб оплатить налоги {rloser}')
        return

    if gen[2] == 0:
        await bot.answer_callback_query(call.id, text=f'{url}, у вас нет налогов чтобы их оплатить {rwin}')
        return

    nalogs2 = '{:,}'.format(gen[2]).replace(',', '.')
    await db.oplata_nalogs_gen_db(user_id, gen[2])
    await bot.answer_callback_query(call.id, text=f'{url}, вы успешно оплатили налоги на сумму {nalogs2}$ с вашего игрового баланса {rwin}')
    await edit_generator_msg(call)


def reg(dp: Dispatcher):
    dp.register_message_handler(my_generator, lambda message: message.text.lower().startswith('мой генератор'))
    dp.register_message_handler(generator_list, lambda message: message.text.lower().startswith('генератор'))
    dp.register_message_handler(buy_generator, lambda message: message.text.lower().startswith('построить генератор'))
    dp.register_callback_query_handler(snyt_pribl, text_startswith='generator-sobrat')
    dp.register_callback_query_handler(buy_turbine, text_startswith='generator-buy-turb')
    dp.register_callback_query_handler(oplata_nalogov, text_startswith='generator-nalog')
