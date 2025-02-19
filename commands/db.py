from datetime import datetime
from decimal import Decimal
import sqlite3

from user import BFGconst
import config as cfg
from bot import bot


conn = sqlite3.connect('users.db')
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER,
    name TEXT,
    balance TEXT,
    btc TEXT DEFAULT '0',
    bank TEXT DEFAULT '0',
    depozit TEXT DEFAULT '0',
    timedepozit NUMERIC DEFAULT '0',
    exp INTEGER DEFAULT '10',
    energy INTEGER DEFAULT '10',
    case1 INTEGER DEFAULT '0',
    case2 INTEGER DEFAULT '0',
    case3 INTEGER DEFAULT '0',
    case4 INTEGER DEFAULT '0',
    rating INTEGER DEFAULT '0',
    games INTEGER DEFAULT '0',
    ecoins INTEGER DEFAULT '0',
    per TEXT DEFAULT '0',
    dregister NUMERIC,
    corn INTEGER DEFAULT '0',
    status INTEGER DEFAULT '0',
    issued NUMERIC DEFAULT '0',
    game_id INTEGER,
    yen TEXT DEFAULT '0',
    perlimit TEXT DEFAULT '0'
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ban_list (
    user_id INTEGER,
    time INTEGER,
    reason INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS mine (
    user_id INTEGER,
    iron INTEGER DEFAULT '0',
    gold INTEGER DEFAULT '0',
    diamond INTEGER DEFAULT '0',
    amestit INTEGER DEFAULT '0',
    aquamarine INTEGER DEFAULT '0',
    emeralds INTEGER DEFAULT '0',
    matter INTEGER DEFAULT '0',
    plasma INTEGER DEFAULT '0',
    nickel INTEGER DEFAULT '0',
    titanium INTEGER DEFAULT '0',
    cobalt INTEGER DEFAULT '0',
    ectoplasm INTEGER DEFAULT '0',
    biores INTEGER DEFAULT '0',
    palladium INTEGER DEFAULT '0'
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS ferma (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    cards INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS generator (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    turbine INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS garden (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    tree INTEGER,
    water INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS business (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    territory INTEGER,
    bsterritory INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS tree (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    territory INTEGER,
    tree INTEGER,
    yen INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS quarry (
    user_id INTEGER,
    balance NUMERIC,
    nalogs INTEGER,
    territory INTEGER,
    bur INTEGER,
    lvl INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo (
    name TEXT,
    summ TEXT,
    activ INTEGER,
    data TEXT
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS promo_activ (
    user_id INTEGER,
    name TEXT
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS sett (
    ads TEXT,
    kursbtc INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS wedlock (
    user1 INTEGER,
    user2 NUMERIC,
    rtime INTEGER
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS clans (
    clan_id INTEGER PRIMARY KEY,
    balance TEXT,
    name TEXT,
    inv INT,
    kick INT,
    ranks INT,
    kazna INT,
    robbery INT,
    war INT,
    upd_name INT,
    type INT,
    shield INT,
    ratting INT,
    win INT,
    lose INT
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS clan (
    user_id INTEGER,
    clan_id INTEGER,
    rank INT
)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS chats (
    chat_id INTEGER,
    users INTEGER
)''')
conn.commit()


cursor.execute('''CREATE TABLE IF NOT EXISTS property (
    user_id INTEGER,
    helicopter INTEGER DEFAULT '0',
    car INTEGER DEFAULT '0',
    yahta INTEGER DEFAULT '0',
    phone INTEGER DEFAULT '0',
    house INTEGER DEFAULT '0',
    plane INTEGER DEFAULT '0'
)''')


current_kurs = cursor.execute('SELECT kursbtc FROM sett').fetchone()
if current_kurs is None:
    cursor.execute('INSERT INTO sett (ads, kursbtc) VALUES (?, ?)', ('', 65000))
    
    
async def get_user_info(user_id: int) -> tuple:
    user = cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
    mine = cursor.execute("SELECT * FROM mine WHERE user_id = ?", (user_id,)).fetchone()
    property = cursor.execute("SELECT * FROM property WHERE user_id = ?", (user_id,)).fetchone()
    ferma = cursor.execute("SELECT * FROM ferma WHERE user_id = ?", (user_id,)).fetchone()
    business = cursor.execute("SELECT * FROM business WHERE user_id = ?", (user_id,)).fetchone()
    garden = cursor.execute("SELECT * FROM garden WHERE user_id = ?", (user_id,)).fetchone()
    generator = cursor.execute("SELECT * FROM generator WHERE user_id = ?", (user_id,)).fetchone()
    quarry = cursor.execute("SELECT * FROM quarry WHERE user_id = ?", (user_id,)).fetchone()
    tree = cursor.execute("SELECT * FROM tree WHERE user_id = ?", (user_id,)).fetchone()
    
    clan = None
    cinfo = cursor.execute("SELECT clan_id, rank FROM clan WHERE user_id = ?", (user_id,)).fetchone()
    rank = cinfo[1] if cinfo else 0
    
    if cinfo:
        clan = cursor.execute("SELECT * FROM clans WHERE clan_id = ?", (cinfo[0],)).fetchone()
    
    return user, mine, property, ferma, business, garden, generator, quarry, tree, clan, rank


async def sql_zapros(sql: str, summ: int, user_id: int) -> None:
    cursor.execute(sql, (summ, user_id))
    conn.commit()


async def get_new_id() -> int:
    cursor.execute("SELECT COUNT(*) FROM users")
    new_id = 100 + cursor.fetchone()[0]
    
    while cursor.execute("SELECT user_id FROM users WHERE game_id = ?", (new_id,)).fetchone():
        new_id += 1
        
    return new_id


async def reg_user(user_id: int) -> None:
    ex = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()
    if not ex:
        dt = int(datetime.now().timestamp())
        nid = await get_new_id()
        cursor.execute('INSERT INTO users (user_id, name, balance, dregister, game_id)' 'VALUES (?, ?, ?, ?, ?)', (user_id, 'Игрок', cfg.start_money, dt, nid))
        cursor.execute('INSERT INTO mine (user_id) VALUES (?)', (user_id,))
        cursor.execute('INSERT INTO property (user_id) VALUES (?)', (user_id,))
        conn.commit()


async def getperevod(perevod: int | str, user_id: int, reply_user_id: int) -> None:
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
    
    
async def url_name(user_id: int) -> str:
    name = cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    return f'<a href="tg://user?id={user_id}">{name}</a>'


async def getpofildb(user_id: int) -> tuple:
    data = cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()

    ferma = cursor.execute('SELECT user_id FROM ferma WHERE user_id = ?', (user_id,)).fetchone()
    business = cursor.execute('SELECT user_id FROM business WHERE user_id = ?', (user_id,)).fetchone()
    garden = cursor.execute('SELECT user_id FROM garden WHERE user_id = ?', (user_id,)).fetchone()
    generator = cursor.execute('SELECT user_id FROM generator WHERE user_id = ?', (user_id,)).fetchone()

    property = cursor.execute('SELECT * FROM property WHERE user_id = ?', (user_id,)).fetchone()

    return data, (ferma, business, garden, generator), property


async def top_db(user_id: int, st: str, table='users') -> tuple:
    cursor.execute(f"SELECT * FROM {table} ORDER BY CAST({st} AS REAL) DESC LIMIT 1000")
    top_players = cursor.fetchall()

    cursor.execute(f"SELECT * FROM {table} WHERE user_id = ?", (user_id,))
    userinfo = cursor.fetchone()
    return userinfo, top_players


async def top_clans_db(user_id: int) -> tuple:
    top_clans = cursor.execute(f"SELECT * FROM clans ORDER BY CAST(ratting AS REAL) DESC LIMIT 1000").fetchall()
    claninfo = cursor.execute(f"SELECT * FROM clan WHERE user_id = ?", (user_id,)).fetchone()
    return claninfo, top_clans


async def get_colvo_users() -> tuple:
    users = cursor.execute(f"SELECT COUNT(*) FROM users").fetchone()[0]
    chats = cursor.execute(f"SELECT COUNT(*) FROM chats").fetchone()[0]
    uchats = cursor.execute("SELECT SUM(users) FROM chats").fetchone()[0]
    return users, chats, uchats


async def getban(user_id: int) -> tuple:
    return cursor.execute(f"SELECT * FROM ban_list WHERE user_id = ?", (user_id,)).fetchone()


async def upd_chat_db(chat_id: int) -> None:
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


async def chek_user(user_id: int) -> str:
    return cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()


async def reset_limit() -> None:
    cursor.execute('UPDATE users SET per = 0')
    conn.commit()
    
    
async def setname(name: str, user_id: int) -> None:
    cursor.execute('UPDATE users SET name = ? WHERE user_id = ?', (name, user_id))
    conn.commit()
    
    
async def get_name(user_id: int) -> str:
    return cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]


async def update_ads_const() -> None:
    ads = cursor.execute("SELECT ads FROM sett").fetchone()[0]
    ads = ads.replace(r'\n', '\n')
    BFGconst.ads = ads
    