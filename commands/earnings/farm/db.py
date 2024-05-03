from commands.db import conn, cursor

async def getferm(id):
    cursor.execute('SELECT ferma, balance, nalogs, cards FROM ferma WHERE user_id = ?', (id,))
    i = cursor.fetchone()
    ferma, balance, nalogs, cards = i
    return ferma, balance, nalogs, cards

async def getferm1(id):
    cursor.execute('SELECT ferma FROM ferma WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def buy_ferma_db(id):
    cursor.execute('UPDATE ferma SET ferma = 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - 500000000 WHERE user_id = ?', (id,))
    conn.commit()

async def buy_cards_db(id, ch):
    cursor.execute('UPDATE ferma SET cards = cards + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def gercards(id):
    cursor.execute('SELECT cards FROM ferma WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def get_ferma_balance(id):
    cursor.execute('SELECT balance FROM ferma WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def snyt_pribl_ferma_db(id, ch):
    cursor.execute('UPDATE ferma SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET btc = btc + ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def get_ferma_nalogs(id):
    cursor.execute('SELECT nalogs FROM ferma WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def oplata_nalogs_ferma_db(id, ch):
    cursor.execute('UPDATE ferma SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def autoferma():
    cursor.execute(f'UPDATE ferma SET balance = balance + {3000} WHERE ferma = 1 AND nalogs < 5000000 AND cards = 0')
    cursor.execute('UPDATE ferma SET balance = balance + ROUND(3000 * POWER(cards, 2.5)) WHERE ferma = 1 AND nalogs < 5000000 AND cards > 0')
    cursor.execute('UPDATE ferma SET nalogs = nalogs + 200000 WHERE ferma = 1 AND nalogs < 5000000')
    conn.commit()