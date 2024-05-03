import sqlite3
import datetime


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, name TEXT, balance INTEGER, btc INTEGER, 
bank INTEGER, depozit INTEGER, timedepozit TIMESTAMP, exp INTEGER, energy INTEGER, case1 INTEGER, case2 INTEGER, case3 INTEGER, case4 INTEGER, 
rating INTEGER, games INTEGER, ecoins INTEGER, per INTEGER, dregister TIMESTAMP, corn INTEGER, status INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS mine (user_id INTEGER, iron INTEGER, gold INTEGER, diamond INTEGER, 
amestit INTEGER, aquamarine INTEGER, emeralds INTEGER, matter INTEGER, plasma INTEGER, nickel INTEGER, 
titanium INTEGER, cobalt INTEGER, ectoplasm INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ferma
                (user_id INTEGER, ferma INTEGER, balance INTEGER, nalogs INTEGER, cards INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS generator
                (user_id INTEGER, balance INTEGER, nalogs INTEGER, turbine INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS garden
                (user_id INTEGER, balance INTEGER, nalogs INTEGER, tree INTEGER, water INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS business (user_id INTEGER, business INTEGER, balance INTEGER, 
nalogs INTEGER, territory INTEGER, bsterritory INTEGER)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS sett
                (ads TEXT, kursbtc INTEGER)''')
conn.commit()


async def register_users(message):
    user_id = message.from_user.id

    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    ex = cursor.fetchone()

    if not ex:
        dt = datetime.datetime.now()
        cursor.execute('INSERT INTO users (user_id, name, balance, btc, bank, depozit, timedepozit, exp, energy, case1, case2, case3, '
                       'case4, rating, games, ecoins, per, dregister, corn, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 'Игрок', 6000000000, 200, 0, 0, dt, 5000000, 10, 0, 0, 0, 0, 0, 0, 0, 0, dt, 0, 0))
        cursor.execute('INSERT INTO mine (user_id, iron, gold, diamond, amestit, aquamarine, emeralds, matter, '
                       'plasma, nickel, titanium, cobalt, ectoplasm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        cursor.execute('INSERT INTO ferma (user_id, ferma, balance, nalogs, cards) VALUES (?, ?, ?, ?, ?)',
                       (user_id, 0, 0, 0, 0))
        cursor.execute('INSERT INTO business (user_id, business, balance, nalogs, territory, bsterritory) VALUES (?, '
                       '?, ?, ?, ?, ?)',
                       (user_id, 0, 0, 0, 5, 1))
        conn.commit()


async def getperevod(message, perevod, user_id, reply_user_id):
    user_id = message.from_user.id
    cursor.execute(
        f'UPDATE users SET balance = balance - ? WHERE user_id = ?', (perevod, user_id))
    cursor.execute(
        f'UPDATE users SET balance = balance + ? WHERE user_id = ?', (perevod, reply_user_id))
    cursor.execute(
        f'UPDATE users SET per = per + ? WHERE user_id = ?', (perevod, user_id))
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


async def getbalance(message):
    user_id = message.from_user.id
    cursor.execute('SELECT name, balance, btc, bank FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    name, balance, btc, bank = i
    return name, balance, btc, bank


async def getpofildb(message):
    user_id = message.from_user.id
    cursor.execute('SELECT balance, btc, bank, ecoins, energy, exp, games, rating, dregister FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    balance, btc, bank, ecoins, energy, exp, games, rating, dregister = i
    return balance, btc, bank, ecoins, energy, exp, games, rating, dregister


async def getonlibalance(message):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def getlimitdb(message):
    user_id = message.from_user.id
    cursor.execute('SELECT per FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def getads(message):
    ex = '<b>Не знаешь как сделать юзер бота?</b>\n<a href="https://t.me/userbotik/5">Скорее нажимай на это сообщение😏</a>'
    return ex


async def setname(name, id):
    cursor.execute("UPDATE users SET name = ? WHERE user_id = ?", (name, id))
    conn.commit()


async def bonus_db(user_id, table, v, summ):
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
    cursor.execute(f"SELECT COUNT(*) FROM users")
    i = cursor.fetchone()[0]
    return i


async def getstatus(id):
    cursor.execute(f"SELECT status FROM users WHERE user_id = ?", (id,))
    i = cursor.fetchone()[0]
    return i
