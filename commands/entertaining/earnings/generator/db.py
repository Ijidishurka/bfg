from commands.db import conn, cursor
from decimal import Decimal


async def buy_generator_db(user_id: int) -> None:
    cursor.execute('INSERT INTO generator (user_id, balance, nalogs, turbine) VALUES (?, ?, ?, ?)', (user_id, 0, 0, 0))
    cursor.execute('UPDATE mine SET matter = matter - 2000 WHERE user_id = ?', (user_id,))
    conn.commit()


async def buy_turbine_db(user_id: int) -> None:
    cursor.execute('UPDATE mine SET matter = matter - 2000 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE generator SET turbine = turbine + 1 WHERE user_id = ?', (user_id,))
    conn.commit()


async def withdraw_profit_db(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE mine SET matter = matter + ? WHERE user_id = ?', (summ, user_id))
    cursor.execute('UPDATE generator SET balance = balance - ? WHERE user_id = ?', (summ, user_id))
    conn.commit()


async def payment_taxes_db(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) - Decimal(ch))

    cursor.execute('UPDATE generator SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def sell_generator(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)
    
    cursor.execute('DELETE FROM generator WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def autogen() -> None:
    cursor.execute('UPDATE generator SET balance = balance + ROUND(20 * (turbine + 1)) WHERE nalogs < 5000000')
    cursor.execute('UPDATE generator SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()