from commands.db import conn, cursor
from decimal import Decimal


async def buy_business(user_id: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('500000000')

    cursor.execute('INSERT INTO business (user_id, balance, nalogs, territory, bsterritory) VALUES (?, ?, ?, ?, ?)', (user_id, 0, 0, 5, 1))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def buy_territory(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET territory = territory + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def buy_bsterritory(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET bsterritory = bsterritory + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def withdraw_profit(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)

    cursor.execute('UPDATE business SET balance = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def payment_taxes(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE business SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def sell_business(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)

    cursor.execute('DELETE FROM business WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def autobusiness() -> None:
    cursor.execute('UPDATE business SET balance = balance + ROUND((90000000 * bsterritory) / 15) WHERE nalogs < 5000000')
    cursor.execute('UPDATE business SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()
