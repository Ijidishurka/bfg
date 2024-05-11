import sqlite3
from datetime import datetime
import config as cfg
from bot import bot
from decimal import Decimal


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, balance TEXT, btc INTEGER, 
bank INTEGER, depozit INTEGER, timedepozit NUMERIC, exp INTEGER, energy INTEGER, case1 INTEGER, case2 INTEGER, 
case3 INTEGER, case4 INTEGER, rating INTEGER, games INTEGER, ecoins INTEGER, per TEXT, dregister NUMERIC, corn INTEGER,
status INTEGER, issued NUMERIC, ban NUMERIC)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS mine (user_id INTEGER, iron INTEGER, gold INTEGER, diamond INTEGER, 
amestit INTEGER, aquamarine INTEGER, emeralds INTEGER, matter INTEGER, plasma INTEGER, nickel INTEGER, 
titanium INTEGER, cobalt INTEGER, ectoplasm INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ferma
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, cards INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS generator
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, turbine INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS garden
                (user_id INTEGER, balance NUMERIC, nalogs INTEGER, tree INTEGER, water INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS business (user_id INTEGER, balance NUMERIC, 
nalogs INTEGER, territory INTEGER, bsterritory INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo (name TEXT, summ TEXT, activ INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo_activ (user_id INTEGER, name TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS sett (ads TEXT, kursbtc INTEGER)''')
conn.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER, users INTEGER)''')
conn.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS property (user_id INTEGER, helicopter INTEGER, 
car INTEGER, yahta INTEGER, phone INTEGER, house INTEGER, plane INTEGER)''')


async def reg_user(user_id):
    ex = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not ex:
        dt = int(datetime.now().timestamp())
        cursor.execute('INSERT INTO users (user_id, name, balance, btc, bank, depozit, timedepozit, exp, energy, case1,'
                       'case2, case3, case4, rating, games, ecoins, per, dregister, corn, status)'
                       'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 'Игрок', cfg.start_money, 200, 0, 0, dt, 5000000, 10, 0, 0, 0, 0, 0, 0, 0, 0, dt, 0, 0))

        cursor.execute('INSERT INTO mine (user_id, iron, gold, diamond, amestit, aquamarine, emeralds, matter, '
                       'plasma, nickel, titanium, cobalt, ectoplasm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

        cursor.execute('INSERT INTO property (user_id, helicopter, car, yahta, phone, house, plane) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 0, 0, 0, 0))

        conn.commit()


async def getperevod(perevod, user_id, reply_user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    r_balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (reply_user_id,)).fetchone()[0]
    per = cursor.execute('SELECT per FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

    balance = int(Decimal(balance) - Decimal(perevod))
    r_balance = int(Decimal(r_balance) + Decimal(perevod))
    per = int(Decimal(per) + Decimal(perevod))

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), user_id))
    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(r_balance), reply_user_id))
    cursor.execute(f'UPDATE users SET per = ? WHERE user_id = ?', (str(per), user_id))
    conn.commit()


async def getname(message):
    user_id = message.from_user.id
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    try:
        ex = cursor.fetchone()[0]
    except:
        ex = 'Игрок'
    return ex


async def getidname(user_id):
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    try:
        ex = cursor.fetchone()[0]
    except:
        ex = 'Игрок'
    return ex


async def getinlinename(callback_query):
    user_id = callback_query.from_user.id
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    try:
        ex = cursor.fetchone()[0]
    except:
        ex = 'Игрок'
    return ex


async def getbalance(user_id):
    data = cursor.execute('SELECT name, balance, btc, bank FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return data[0], int(data[1]), data[2], data[3]


async def getpofildb(user_id):
    data = cursor.execute('SELECT balance, btc, bank, ecoins, energy, exp, games, rating, dregister FROM users WHERE user_id = ?', (user_id,)).fetchone()

    ferma = cursor.execute('SELECT user_id FROM ferma WHERE user_id = ?', (user_id,)).fetchone()
    business = cursor.execute('SELECT user_id FROM business WHERE user_id = ?', (user_id,)).fetchone()
    garden = cursor.execute('SELECT user_id FROM garden WHERE user_id = ?', (user_id,)).fetchone()
    generator = cursor.execute('SELECT user_id FROM generator WHERE user_id = ?', (user_id,)).fetchone()

    return data, (ferma, business, garden, generator)


async def getonlibalance(message):
    user_id = message.from_user.id
    i = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return int(i)


async def get_balance(user_id):
    i = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return int(i)


async def getlimitdb(message):
    user_id = message.from_user.id
    i = cursor.execute('SELECT per FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return int(i)


async def getads(message=None):
    ads = cursor.execute("SELECT ads FROM sett").fetchone()[0]
    ads = ads.replace(r'\n', '\n')
    return ads


async def setname(name, id):
    cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, id))
    conn.commit()


async def bonus_db(user_id, table, v, summ):
    if table == 'users' and v == 'balance':
        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        summ = Decimal(balance) + Decimal(summ)
        cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    else:
        cursor.execute(f"UPDATE {table} SET {v} = {v} + ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def top_db(message):
    id = message.from_user.id

    cursor.execute("SELECT * FROM users ORDER BY rating DESC LIMIT 100")
    top_players = cursor.fetchall()

    cursor.execute("SELECT * FROM users WHERE user_id = ?", (id,))
    userinfo = cursor.fetchone()
    return userinfo, top_players


async def get_colvo_users():
    users = cursor.execute(f"SELECT COUNT(*) FROM users").fetchone()[0]
    chats = cursor.execute(f"SELECT COUNT(*) FROM chats").fetchone()[0]
    uchats = cursor.execute("SELECT SUM(users) FROM chats").fetchone()[0]
    return users, chats, uchats


async def getstatus(id):
    return cursor.execute(f"SELECT status FROM users WHERE user_id = ?", (id,)).fetchone()[0]


async def getban(id):
    return cursor.execute(f"SELECT ban FROM users WHERE user_id = ?", (id,)).fetchone()[0]


async def upd_chat_db(chat_id):
    res = cursor.execute(f"SELECT users FROM chats WHERE chat_id = ?", (chat_id,)).fetchone()
    if not res:
        cursor.execute('INSERT INTO chats (chat_id, users) VALUES (?, ?)', (chat_id, 0))
        conn.commit()
        res = 0
    else:
        res = res[0]

    count = await bot.get_chat_members_count(chat_id)
    if res != count:
        cursor.execute("UPDATE chats SET users = ? WHERE chat_id = ?", (count, chat_id))
        conn.commit()


async def url_name(user_id):
    name = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def chek_user(user_id):
    return cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,)).fetchone()