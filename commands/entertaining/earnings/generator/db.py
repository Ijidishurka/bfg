from commands.db import conn, cursor
from decimal import Decimal


async def getgenerator(id):
    return cursor.execute('SELECT turbine, balance, nalogs FROM generator WHERE user_id = ?', (id,)).fetchone()


async def getonlimater(id):
    cursor.execute('SELECT matter FROM mine WHERE user_id = ?', (id,))
    result = cursor.fetchone()[0]
    return result


async def buy_generator_db(id):
    cursor.execute('INSERT INTO generator (user_id, balance, nalogs, turbine) VALUES (?, ?, ?, ?)', (id, 0, 0, 0))
    cursor.execute('UPDATE mine SET matter = matter - 2000 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_turbine_db(id):
    cursor.execute('UPDATE mine SET matter = matter - 2000 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE generator SET turbine = turbine + 1 WHERE user_id = ?', (id,))
    conn.commit()


async def snyt_pribl_gen_db(id, summ):
    cursor.execute('UPDATE mine SET matter = matter + ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE generator SET balance = balance - ? WHERE user_id = ?', (summ, id))
    conn.commit()


async def oplata_nalogs_gen_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = int(Decimal(balance) - Decimal(ch))

    cursor.execute('UPDATE generator SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def autogen():
    cursor.execute('UPDATE generator SET balance = balance + ROUND(20 * (turbine + 1)) WHERE nalogs < 5000000')
    cursor.execute('UPDATE generator SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()