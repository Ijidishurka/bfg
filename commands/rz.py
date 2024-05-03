import random
from datetime import datetime
from commands.db import register_users, getname, setname, bonus_db, getpofildb, getads, top_db, get_colvo_users, getstatus
from commands.main import geturl
from commands.main import win_luser
from commands.gettime import bonustime, kaznatime
from commands.assets.transform import transform


async def shar_cmd(message):
    list = ["Мой ответ - нет", "Мне кажется - да", "Сейчас нельзя предсказать", "Мне кажется - нет", "Знаки говорят - нет", "Да", "Нет", "Можешь быть уверен в этом"]
    q = random.choice(list)
    await message.answer(f"{q}")


async def setname_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    result = await win_luser()
    rwin, rloser = result
    url = geturl(user_id, user_name)
    try:
        name = " ".join(message.text.split()[2:])
    except:
        await message.answer(f'{url}, ваш ник не может быть короче 5 символов {rloser}', parse_mode='html')
        return

    name = name.replace('<', '').replace('>', '')
    if len(name) < 5:
        await message.answer(f'{url}, ваш ник не может быть короче 5 символов {rloser}', parse_mode='html')
        return
    if len(name) > 20:
        await message.answer(f'{url}, ваш ник не может быть длиннее 20 символов {rloser}', parse_mode='html')
        return
    await setname(name, user_id)
    await message.answer(f'Ваш ник изменён на «{name}»', parse_mode='html')


async def kazna_cmd(message):
    await message.answer(
        f'💰 На данный момент казна штата составляет 98.894.419.531.599.545$',
        parse_mode='html')


async def ogr_kazna(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)

    bt, left = await kaznatime(user_id)
    if bt == 1:
        await message.answer(
            f'{url}, вы уже грабили казну сегодня. Бегите скорее, полиция уже в пути 🚫',
            parse_mode='html')
        return

    i = random.randint(1, 3)
    if i == 1:
        await message.answer(
            f'{url}, к сожалению вам не удалось ограбить казну ❎',
            parse_mode='html')

    summ = random.randint(100000000, 400000000)
    summ2 = '{:,}'.format(summ).replace(',', '.')

    await bonus_db(user_id, 'users', 'balance', summ)
    await message.answer(
        f'{url}, вы успешно ограбили казну. На ваш баланс зачислено {summ2} ✅',
        parse_mode='html')


async def bonus_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)

    bt, left = await bonustime(user_id)
    if bt == 1:
        hours = left // 3600
        minutes = (left % 3600) // 60
        if hours > 0:
            await message.answer(
                f'{url}, ты уже получал(-а) ежедневный бонус, следующий бонус ты сможешь получить через {hours}ч {minutes}м',
                parse_mode='html')
        else:
            await message.answer(
                f'{url}, ты уже получал(-а) ежедневный бонус, следующий бонус ты сможешь получить через {minutes}м',
                parse_mode='html')
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
    await message.answer(
        f'{url}, вам был выдан ежедневный бонус {txt}',
        parse_mode='html')

async def profil_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    balance, btc, bank, ecoins, energy, exp, games, rating, dregister = await getpofildb(message)
    btc = await transform(btc)
    bank = await transform(bank)
    energy = await transform(energy)
    exp = await transform(exp)
    games = await transform(games)
    rating = await transform(rating)
    balance = await transform(balance)
    status = await getstatus(user_id)

    if status == 0:
        st = "Обычный"
    elif status == 1:
        st = "Standart VIP"
    elif status == 2:
        st = "Gold VIP"
    elif status == 3:
        st = "Platinum VIP"
    elif status == 4:
        st = "Администратор"

    dregister = datetime.strptime(dregister, '%Y-%m-%d %H:%M:%S.%f')
    dregister = dregister.strftime('%Y-%m-%d в %H:%M:%S')

    await message.answer(f'''{url}, ваш профиль:
🔎 ID: {user_id}
🏆 Статус: {st}
💰 Денег: {balance}$
🏦 В банке: {bank}$
💳 B-Coins: {ecoins}
💽 Биткоины: {btc}฿
🏋 Энергия: {energy}
👑 Рейтинг: {rating}
🌟 Опыт: {exp}
🎲 Всего сыграно игр: {games}

📦 Имущество:
 💼 Бизнес: Бизнес
 🔋 Ферма: Майнинг ферма

📅 Дата регистрации:
{dregister}''', parse_mode='html')


async def stats_cmd(message):
    users = await get_colvo_users()
    users = '{:,}'.format(users).replace(',', '.')

    await message.answer(f'''📊 Кол-во пользователей бота: {users}
📊 Общее кол-во чатов: ???
📊 Общее кол-во игроков в беседах: ???''', parse_mode='html')


async def top_command(message):
    userinfo, top_players = await top_db(message)
    user_id = message.from_user.id
    ads = await getads(message)
    user_name = await getname(message)
    url = await geturl(user_id, user_name)

    user_position = None
    for i, player in enumerate(top_players, start=1):
        if player[0] == user_id:
            user_position = i
            break

    top_message = f"{url}, топ 10 игроков:\n"
    emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

    # Ограничим количество выводимых игроков до топ-10
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

    await message.answer(top_message, parse_mode='html', disable_web_page_preview=True)




