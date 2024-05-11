from commands.db import conn, cursor
from decimal import Decimal


async def getbusiness(id):
    data = cursor.execute('SELECT * FROM business WHERE user_id = ?', (id,)).fetchone()
    if data: return data
    else: return False


async def buy_business_db(id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('500000000')

    cursor.execute('INSERT INTO business (user_id, balance, nalogs, territory, bsterritory) VALUES (?, ?, ?, ?, ?)', (id, 0, 0, 5, 1))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def buy_territory_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET territory = territory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def buy_bsterritory_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET bsterritory = bsterritory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def snyt_pribl_bs_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)

    cursor.execute('UPDATE business SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def oplata_nalogs_bs_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def autobusiness():
    cursor.execute('UPDATE business SET balance = balance + ROUND((90000000 * bsterritory) / 15) WHERE nalogs < 5000000')
    cursor.execute('UPDATE business SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()