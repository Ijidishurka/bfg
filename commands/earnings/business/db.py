from commands.db import conn, cursor


async def getbusiness(id):
    data = cursor.execute('SELECT * FROM business WHERE user_id = ?', (id,)).fetchone()
    if data: return data
    else: return False


async def buy_business_db(id):
    cursor.execute('INSERT INTO business (user_id, balance, nalogs, territory, bsterritory) VALUES (?, ?, ?, ?, ?)', (id, 0, 0, 5, 1))
    cursor.execute('UPDATE users SET balance = balance - 500000000 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_territory_db(id, ch):
    cursor.execute('UPDATE business SET territory = territory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def buy_bsterritory_db(id, ch):
    cursor.execute('UPDATE business SET bsterritory = bsterritory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def snyt_pribl_bs_db(id, ch):
    cursor.execute('UPDATE business SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def oplata_nalogs_bs_db(id, ch):
    cursor.execute('UPDATE business SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def autobusiness():
    cursor.execute('UPDATE business SET balance = balance + ROUND((90000000 * bsterritory) / 15) WHERE business = 1 AND nalogs < 5000000')
    cursor.execute('UPDATE business SET nalogs = nalogs + 200000 WHERE business = 1 AND nalogs < 5000000')
    conn.commit()