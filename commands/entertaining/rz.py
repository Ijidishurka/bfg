import random
import re

from aiogram import Dispatcher, types
from assets.antispam import antispam
from commands.db import get_colvo_users, setname
from assets.gettime import bonustime, kaznatime, lucktime
from assets.transform import transform_int as tr
import config as cfg
from filters.custom import StartsWith, TextIn
from user import BFGuser, BFGconst


@antispam
async def shar_cmd(message: types.Message, user: BFGuser):
    list = ["Мой ответ - нет", "Мне кажется - да", "Сейчас нельзя предсказать", "Мне кажется - нет",
            "Знаки говорят - нет", "Да", "Нет", "Можешь быть уверен в этом"]
    await message.answer(random.choice(list))


@antispam
async def vibor_cmd(message: types.Message, user: BFGuser):
    list = ["Первый варинат лучше", "Однозначно первый", "Второй варинат лучше", "Однозначно второй"]
    await message.answer(random.choice(list))


@antispam
async def shans_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'Шанс этого - {random.randint(1, 100)}%')


@antispam
async def set_name_cmd(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    win, lose = BFGconst.emj()
    
    try:
        name = " ".join(message.text.split()[2:])
    except:
        await message.answer(f'{user.url}, ваш ник не может быть короче 5 символов {lose}')
        return

    climit = {0: 20, 1: 25, 2: 30, 3: 45, 4: 50}.get(user.status, 20)

    if re.search(r'<|>|@|t\.me|http', name):
        await message.answer(f'{user.url}, ваш ник содержит запрещённые символы {lose}')
        return

    if len(name) < 5:
        await message.answer(f'{user.url}, ваш ник не может быть короче 5 символов {lose}')
        return

    if len(name) > climit:
        await message.answer(f'{user.url}, ваш ник не может быть длиннее {climit} символов {lose}')
        return

    await setname(name, user_id)
    await message.answer(f'Ваш ник изменён на «{name}»')


@antispam
async def kazna_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'💰 На данный момент казна штата составляет 98.894.419.531.599.545$')


@antispam
async def ogr_kazna(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    bt, left = await kaznatime(user_id)
    
    if bt == 1:
        await message.answer(f'{user.url}, вы уже грабили казну сегодня. Бегите скорее, полиция уже в пути 🚫')
        return

    if random.randint(1, 3) == 1:
        await message.answer(f'{user.url}, к сожалению вам не удалось ограбить казну ❎')
        return

    summ = random.randint(100_000_000, 400_000_000)

    await user.balance.upd(summ, '+')
    await message.answer(f'{user.url}, вы успешно ограбили казну. На ваш баланс зачислено {tr(summ)} ✅')


@antispam
async def try_luck_cmd(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    bt, left = await lucktime(user_id)
    
    if bt == 1:
        hours = left // 3600
        minutes = (left % 3600) // 60
        txt = f'{hours}ч {minutes}м' if hours > 0 else f'{minutes}м'
        await message.answer(f'{user.url}, ты уже испытывал свою удачу, следующий раз ты сможешь через {txt}')
        return

    summ = random.randint(10_000_000, 900_000_000)

    await user.biores.upd(summ, '+')
    await message.answer(f'✅ Вы успешно испытали удачу и получили {tr(summ)}кг биоресурса ☣️')


@antispam
async def bonus_cmd(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    bt, left = await bonustime(user_id)
    
    if bt == 1:
        hours = left // 3600
        minutes = (left % 3600) // 60
        txt = f'{hours}ч {minutes}м' if hours > 0 else f'{minutes}м'
        await message.answer(f'{user.url}, ты уже получал(-а) ежедневный бонус, следующий бонус ты сможешь получить через {txt}')
        return

    i = random.randint(1, 4)
    
    if i == 1:
        summ = random.randint(1_000_000, 4_000_000)
        await user.balance.upd(summ, '+')
        txt = f'{tr(summ)}$ 💰'
    elif i == 2:
        summ = random.randint(100, 950)
        await user.rating.upd(summ, '+')
        txt = f'{summ} рейтинга 👑'
    elif i == 3:
        summ = random.randint(1, 10)
        await user.case[1].upd(summ, '+')
        txt = f'обычный кейс  - {summ} 📦'
    else:
        summ = random.randint(1, 10)
        await user.mine.matter.upd(summ, '+')
        txt = f'{summ} материи 🌌'
        
    await message.answer(f'{user.url}, вам был выдан ежедневный бонус в размере {txt}')


@antispam
async def stats_cmd(message: types.Message, user: BFGuser):
    users, chats, uchats = await get_colvo_users()

    await message.answer(f'''📊 Кол-во пользователей бота: {tr(users)}
📊 Общее кол-во чатов: {tr(chats)}
📊 Общее кол-во игроков в беседах: {tr(uchats)}''')


@antispam
async def chat_list(message: types.Message, user: BFGuser):
    await message.answer(f'''💭 Официальная беседа бота: {cfg.chat}
💭 Официальный канал разработки: {cfg.channel}
🏆 Официальный чат с розыгрышами: ...''', disable_web_page_preview=True)


@antispam
async def my_name(message: types.Message, user: BFGuser):
    await message.answer(f'🗂 Ваш ник - «{user.name}»')


def reg(dp: Dispatcher):
    dp.message.register(shar_cmd, StartsWith("шар "))
    dp.message.register(vibor_cmd, StartsWith("выбери "))
    dp.message.register(shans_cmd, StartsWith("шанс "))
    dp.message.register(set_name_cmd, StartsWith("сменить ник"))
    dp.message.register(kazna_cmd, TextIn("казна"))
    dp.message.register(stats_cmd, TextIn("статистика бота"))
    dp.message.register(bonus_cmd, TextIn("ежедневный бонус"))
    dp.message.register(try_luck_cmd, TextIn("испытать удачу"))
    dp.message.register(ogr_kazna, TextIn("ограбить казну", "ограбить мерию"))
    dp.message.register(my_name, TextIn("мой ник"))
    dp.message.register(chat_list, TextIn("!беседа"))
