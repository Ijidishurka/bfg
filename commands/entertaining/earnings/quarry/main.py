from aiogram import types, Dispatcher
from bot import bot
from commands.entertaining.earnings.quarry import db
from commands.db import url_name
from commands.main import win_luser
from assets import kb
from assets.antispam import new_earning_msg, antispam, antispam_earning


@antispam
async def quarry_list(message):
    await message.answer(f'''Привет! 🚀 Готов покорить мир карьеров?

🛠 Построй свой первый карьер всего за 25 палладия! Для этого напиши "<code>Построить карьер</code>". Палладий можно получить, открыв рудные кейсы.

🌄 Как только карьер будет построен:
1. Начни добычу ресурсов.
2. Улучшай буровые установки, чтобы увеличивать добычу.
3. Расширяй территорию карьера для установки нового оборудования.

📈 Введи "Мой карьер", чтобы посмотреть статистику и доступные улучшения.

❓ Нужна помощь или хочешь узнать все команды? Введи "<code>Помощь</code>" и выбери раздел "<code>Развлекательные</code>".''')


@antispam
async def my_quarry(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getquarry(user_id)
    if not data:
        await message.answer(f'{url}, у вас нет своего карьера. Введите команду "Построить карьер" {rloser}')
        return

    ter_upd = data[2] * 130
    bur_upd = data[2] * 166

    nalogs = '{:,}'.format((int(data[1]))).replace(',', '.')
    ter_upd = '{:,}'.format((int(ter_upd))).replace(',', '.')
    bur_upd = '{:,}'.format((int(bur_upd))).replace(',', '.')

    msg = await message.answer(f'''{url}, информация о вашем карьере "Карьер":
🔧 Уровень: {data[4]}
🧱 Размер территории: {data[2]}м²
🆙 для следующего уровня: {ter_upd} 🧪
🕳 Количество буровых установок: {data[3]}
🆙 для следующего уровня: {bur_upd} ⚙

💸 Налоги: {nalogs}/5.000.000$''', reply_markup=kb.quarry(user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


async def edit_quarry_msg(call: types.CallbackQuery):
    user_id = call.from_user.id
    url = await url_name(user_id)
    data = await db.getquarry(user_id)
    if not data:
        return

    ter_upd = data[2] * 130
    bur_upd = data[2] * 166

    nalogs = '{:,}'.format((int(data[2]))).replace(',', '.')
    ter_upd = '{:,}'.format((int(ter_upd))).replace(',', '.')
    bur_upd = '{:,}'.format((int(bur_upd))).replace(',', '.')

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''
{url}, информация о вашем карьере "Карьер":
🔧 Уровень: {data[5]}
🧱 Размер территории: {data[3]}м²
🆙 для следующего уровня: {ter_upd} 🧪
🕳 Количество буровых установок: {data[4]}
🆙 для следующего уровня: {bur_upd} ⚙

💸 Налоги: {nalogs}/5.000.000$''', reply_markup=kb.quarry(user_id))


@antispam
async def buy_quarry(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    rwin, rloser = await win_luser()
    data = await db.getquarry(user_id)
    if data:
        await message.answer(f'{url}, у вас уже есть построенный карьер. Чтобы узнать подробнее, введите "Мой карьер" {rloser}')
    else:
        balance = await db.getonlipalladium(user_id)
        if balance < 25:
            await message.answer(f'{url}, у вас недостаточно палладия для постройки карьера. Его стоимость 25 палладия {rloser}')
        else:
            await db.buy_quarry_db(user_id)
            await message.answer(f'{url}, вы успешно построили карьер для подробностей введите "Мой карьер" {rwin}')


def reg(dp: Dispatcher):
    dp.register_message_handler(my_quarry, lambda message: message.text.lower().startswith('мой карьер'))
    dp.register_message_handler(quarry_list, lambda message: message.text.lower().startswith('карьер'))
    dp.register_message_handler(buy_quarry, lambda message: message.text.lower().startswith('построить карьер'))
