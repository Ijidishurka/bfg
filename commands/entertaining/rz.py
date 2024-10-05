import random
import re
from aiogram import Dispatcher
from assets.antispam import antispam
from commands.db import url_name, setname, bonus_db, get_colvo_users, getstatus, get_name
from commands.main import win_luser
from assets.gettime import bonustime, kaznatime, lucktime
from assets.transform import transform_int as tr
import config as cfg


@antispam
async def shar_cmd(message):
    list = ["Мой ответ - нет", "Мне кажется - да", "Сейчас нельзя предсказать", "Мне кажется - нет",
            "Знаки говорят - нет", "Да", "Нет", "Можешь быть уверен в этом"]
    await message.answer(random.choice(list))


@antispam
async def vibor_cmd(message):
    list = ["Первый варинат лучше", "Однозначно первый", "Второй варинат лучше", "Однозначно второй"]
    await message.answer(random.choice(list))


@antispam
async def shans_cmd(message):
    r = random.randint(1, 100)
    await message.answer(f'Шанс этого - {r}%')


@antispam
async def setname_cmd(message):
    user_id = message.from_user.id
    rwin, rloser = await win_luser()
    url = await url_name(user_id)
    try:
        name = " ".join(message.text.split()[2:])
    except:
        await message.answer(f'{url}, ваш ник не может быть короче 5 символов {rloser}')
        return

    status_limits = {0: 20, 1: 25, 2: 30, 3: 45, 4: 50}
    status = await getstatus(message.from_user.id)
    climit = status_limits.get(status, status_limits[0])

    if re.search(r'<|>|@|t\.me|http', name):
        await message.answer(f'{url}, ваш ник содержит запрещённые символы {rloser}')
        return

    if len(name) < 5:
        await message.answer(f'{url}, ваш ник не может быть короче 5 символов {rloser}')
        return

    if len(name) > climit:
        await message.answer(f'{url}, ваш ник не может быть длиннее {climit} символов {rloser}')
        return

    await setname(name, user_id)
    await message.answer(f'Ваш ник изменён на «{name}»')


@antispam
async def kazna_cmd(message):
    await message.answer(f'💰 На данный момент казна штата составляет 98.894.419.531.599.545$')


@antispam
async def ogr_kazna(message):
    user_id = message.from_user.id
    url = await url_name(user_id)

    bt, left = await kaznatime(user_id)
    if bt == 1:
        await message.answer(f'{url}, вы уже грабили казну сегодня. Бегите скорее, полиция уже в пути 🚫')
        return

    i = random.randint(1, 3)
    if i == 1:
        await message.answer(f'{url}, к сожалению вам не удалось ограбить казну ❎')
        return

    summ = random.randint(100000000, 400000000)

    await bonus_db(user_id, 'users', 'balance', summ)
    await message.answer(f'{url}, вы успешно ограбили казну. На ваш баланс зачислено {tr(summ)} ✅')


@antispam
async def try_luck(message):
    user_id = message.from_user.id
    url = await url_name(user_id)

    bt, left = await lucktime(user_id)
    if bt == 1:
        hours = left // 3600
        minutes = (left % 3600) // 60
        txt = f'{hours}ч {minutes}м' if hours > 0 else f'{minutes}м'
        await message.answer(f'{url}, ты уже испытывал свою удачу, следующий раз ты сможешь через {txt}')
        return

    summ = random.randint(10_000_000, 900_000_000)

    await bonus_db(user_id, 'mine', 'biores', summ)
    await message.answer(f'✅ Вы успешно испытали удачу и получили {tr(summ)}кг биоресурса ☣️')


@antispam
async def bonus_cmd(message):
    user_id = message.from_user.id
    url = await url_name(user_id)

    bt, left = await bonustime(user_id)
    if bt == 1:
        hours = left // 3600
        minutes = (left % 3600) // 60
        txt = f'{hours}ч {minutes}м' if hours > 0 else f'{minutes}м'
        await message.answer(
            f'{url}, ты уже получал(-а) ежедневный бонус, следующий бонус ты сможешь получить через {txt}')
        return

    i = random.randint(1, 4)
    if i == 1:
        table, v = 'users', 'balance'
        summ = random.randint(1000000, 4000000)
        txt = f'{tr(summ)}$ 💰'
    elif i == 2:
        table, v = 'users', 'rating'
        summ = random.randint(100, 950)
        txt = f'{summ} рейтинга 👑'
    elif i == 3:
        table, v = 'users', 'case1'
        summ = random.randint(1, 10)
        txt = f'обычный кейс  - {summ} 📦'
    else:
        table, v = 'mine', 'matter'
        summ = random.randint(1, 10)
        txt = f'{summ} материи 🌌'

    await bonus_db(user_id, table, v, summ)
    await message.answer(f'{url}, вам был выдан ежедневный бонус в размере {txt}')


@antispam
async def stats_cmd(message):
    users, chats, uchats = await get_colvo_users()

    await message.answer(f'''📊 Кол-во пользователей бота: {users:,}
📊 Общее кол-во чатов: {chats:,}
📊 Общее кол-во игроков в беседах: {uchats:,}'''.replace(',', '.'))


@antispam
async def chat_list(message):
    await message.answer(f'''💭 Официальная беседа бота: {cfg.chat}
💭 Официальный канал разработки: {cfg.chanell}
🏆 Официальный чат с розыгрышами: ...''', disable_web_page_preview=True)


@antispam
async def my_name(message):
    name = await get_name(message)
    await message.answer(f'🗂 Ваш ник - «{name}»')


def reg(dp: Dispatcher):
    dp.register_message_handler(shar_cmd, lambda message: message.text.lower().startswith('шар '))
    dp.register_message_handler(vibor_cmd, lambda message: message.text.lower().startswith('выбери '))
    dp.register_message_handler(shans_cmd, lambda message: message.text.lower().startswith('шанс '))
    dp.register_message_handler(setname_cmd, lambda message: message.text.lower().startswith('сменить ник'))
    dp.register_message_handler(kazna_cmd, lambda message: message.text.lower().startswith('казна'))
    dp.register_message_handler(stats_cmd, lambda message: message.text.lower().startswith('статистика бота'))
    dp.register_message_handler(bonus_cmd, lambda message: message.text.lower().startswith('ежедневный бонус'))
    dp.register_message_handler(try_luck, lambda message: message.text.lower().startswith('испытать удачу'))
    dp.register_message_handler(ogr_kazna, lambda message: message.text.lower().startswith(('ограбить казну', 'ограбить мерию')))
    dp.register_message_handler(my_name, lambda message: message.text.lower().startswith('мой ник'))
    dp.register_message_handler(chat_list, lambda message: message.text.lower().startswith('!беседа'))