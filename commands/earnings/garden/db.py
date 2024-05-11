from commands.db import conn, cursor
from decimal import Decimal


async def getgarden(id):
    cursor.execute('SELECT water, tree, nalogs, balance FROM garden WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        water, tree, nalogs, balance = result
        return water, tree, nalogs, balance, 1
    else:
        return 0, 0, 0, 0, 0


async def getogarden(id):
    cursor.execute('SELECT balance FROM garden WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        return 1
    else:
        return 0


async def buy_garden_db(id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('1000000000')

    cursor.execute('INSERT INTO garden (user_id, balance, nalogs, tree, water) VALUES (?, ?, ?, ?, ?)', (id, 0, 0, 0, 200))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def getgardenbalance(id):
    cursor.execute('SELECT balance FROM garden WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def get_garden_nalogs(id):
    cursor.execute('SELECT nalogs FROM garden WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def oplata_nalogs_garden_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE garden SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def snyt_pribl_garden_db(id, ch):
    cursor.execute('UPDATE garden SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET corn = corn + ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def gettree(id):
    cursor.execute('SELECT tree FROM garden WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def getwater(id):
    cursor.execute('SELECT water FROM garden WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def buy_tree_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE garden SET tree = tree + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def politderevo(id):
    cursor.execute('UPDATE garden SET water = 200 WHERE user_id = ?', (id,))
    conn.commit()


async def getcorn(id):
    cursor.execute('SELECT corn FROM users WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i


async def buy_postion_db(summ, st, id):
    cursor.execute('UPDATE users SET corn = corn - ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE users SET energy = energy + ? WHERE user_id = ?', (st, id))
    conn.commit()


async def autogarden():
    cursor.execute('UPDATE garden SET balance = balance + ((tree + 1) * 3) WHERE nalogs < 5000000')
    cursor.execute('UPDATE garden SET water = water - 10 WHERE nalogs < 5000000')
    cursor.execute('UPDATE garden SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()