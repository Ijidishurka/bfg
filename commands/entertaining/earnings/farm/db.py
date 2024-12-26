from commands.db import conn, cursor
from decimal import Decimal


async def buy_ferma(user_id: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('500000000')

    cursor.execute('INSERT INTO ferma (user_id, balance, nalogs, cards) VALUES (?, ?, ?, ?)', (user_id, 0, 0, 0))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def buy_cards(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE ferma SET cards = cards + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def withdraw_profit(user_id: int, ch: int) -> None:
    cursor.execute('UPDATE ferma SET balance = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET btc = btc + ? WHERE user_id = ?', (ch, user_id))
    conn.commit()


async def pay_taxes(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE ferma SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def sell_ferma(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)

    cursor.execute('DELETE FROM ferma WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()
    

async def autoferma() -> None:
    cursor.execute(f'UPDATE ferma SET balance = balance + 3000 WHERE nalogs < 5000000 AND cards = 0')
    cursor.execute('UPDATE ferma SET balance = balance + ROUND(3000 * POWER(cards, 2.5)) WHERE nalogs < 5000000 AND cards > 0')
    cursor.execute('UPDATE ferma SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()