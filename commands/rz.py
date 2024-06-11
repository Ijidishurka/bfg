import random
from assets.antispam import antispam
from commands.db import url_name, setname, bonus_db, getads, top_db, get_colvo_users, getstatus
from commands.main import win_luser
from assets.gettime import bonustime, kaznatime, lucktime
from commands.assets.transform import transform


async def shar_cmd(message):
    list = ["Мой ответ - нет", "Мне кажется - да", "Сейчас нельзя предсказать", "Мне кажется - нет", "Знаки говорят - нет", "Да", "Нет", "Можешь быть уверен в этом"]
    await message.answer(random.choice(list))


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

    name = name.replace('<', '').replace('>', '').replace('@', '').replace('t.me', '').replace('http', '')
    if len(name) < 5:
        await message.answer(f'{url}, ваш ник не может быть короче 5 символов {rloser}')
        return
    if len(name) > climit:
        await message.answer(f'{url}, ваш ник не может быть длиннее {climit} символов {rloser}')
        return
    await setname(name, user_id)
    await message.answer(f'Ваш ник изменён на «{name}»')


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
    summ2 = '{:,}'.format(summ).replace(',', '.')

    await bonus_db(user_id, 'users', 'balance', summ)
    await message.answer(f'{url}, вы успешно ограбили казну. На ваш баланс зачислено {summ2} ✅')


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
    summ2 = '{:,}'.format(summ).replace(',', '.')

    await bonus_db(user_id, 'mine', 'biores', summ)
    await message.answer(f'✅ Вы успешно испытали удачу и получили {summ2}кг биоресурса ☣️')


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
        table = 'users'
        v = 'balance'
        summ = random.randint(1000000, 4000000)
        summ2 = '{:,}'.format(summ).replace(',', '.')
        txt = f'в размере {summ2}$ 💰'
    elif i == 2:
        table = 'users'
        v = 'rating'
        summ = random.randint(100, 950)
        txt = f'в размере {summ} рейтинга 👑'
    elif i == 3:
        table = 'users'
        v = 'case1'
        summ = random.randint(1, 10)
        txt = f'в размере обычный кейс  - {summ} 📦'
    else:
        table = 'mine'
        v = 'matter'
        summ = random.randint(1, 10)
        txt = f'в размере {summ} материи 🌌'

    await bonus_db(user_id, table, v, summ)
    await message.answer(f'{url}, вам был выдан ежедневный бонус {txt}')


@antispam
async def stats_cmd(message):
    users, chats, uchats = await get_colvo_users()

    users = '{:,}'.format(users).replace(',', '.')
    chats = '{:,}'.format(chats).replace(',', '.')
    uchats = '{:,}'.format(uchats).replace(',', '.')

    await message.answer(f'''📊 Кол-во пользователей бота: {users}
📊 Общее кол-во чатов: {chats}
📊 Общее кол-во игроков в беседах: {uchats}''')


@antispam
async def top_command(message):
    userinfo, top_players = await top_db(message)
    user_id = message.from_user.id
    ads = await getads(message)
    url = await url_name(user_id)

    user_position = None
    for i, player in enumerate(top_players, start=1):
        if player[0] == user_id:
            user_position = i
            break

    top_message = f"{url}, топ 10 игроков:\n"
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    for i, player in enumerate(top_players[:10], start=1):
        tb = await transform(player[2])
        position_emoji = emojis[i - 1]
        top_message += f"{position_emoji} {player[1]} — 👑{player[13]} | {tb}\n"

    top_message += f"—————————————————\n"

    if user_position is not None and user_position <= 10:
        tb = await transform(userinfo[2])
        position_emoji = emojis[user_position - 1]
        top_message += f"{position_emoji} {userinfo[1]} — 👑{userinfo[13]} | {tb}"
    else:
        tb = await transform(userinfo[2])
        top_message += f"➡️1️⃣0️⃣0️⃣ {userinfo[1]} — 👑{userinfo[13]} | {tb}"

    top_message += f'\n\n{ads}'

    await message.answer(top_message, disable_web_page_preview=True)