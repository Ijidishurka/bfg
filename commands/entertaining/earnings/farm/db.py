from commands.db import conn, cursor
from decimal import Decimal


async def getferm(id):
    data = cursor.execute('SELECT * FROM ferma WHERE user_id = ?', (id,)).fetchone()
    if data: return data
    else: return False


async def buy_ferma_db(id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('500000000')

    cursor.execute('INSERT INTO ferma (user_id, balance, nalogs, cards) VALUES (?, ?, ?, ?)', (id, 0, 0, 0))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def buy_cards_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE ferma SET cards = cards + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def snyt_pribl_ferma_db(id, ch):
    cursor.execute('UPDATE ferma SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET btc = btc + ? WHERE user_id = ?', (ch, id))
    conn.commit()


async def oplata_nalogs_ferma_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE ferma SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def autoferma():
    cursor.execute(f'UPDATE ferma SET balance = balance + {3000} WHERE nalogs < 5000000 AND cards = 0')
    cursor.execute('UPDATE ferma SET balance = balance + ROUND(3000 * POWER(cards, 2.5)) WHERE nalogs < 5000000 AND cards > 0')
    cursor.execute('UPDATE ferma SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()