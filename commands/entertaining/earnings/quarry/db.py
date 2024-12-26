from commands.db import conn, cursor
from decimal import Decimal


async def buy_quarry_db(user_id: int) -> None:
    cursor.execute('INSERT INTO quarry (user_id, balance, nalogs, territory, bur, lvl) VALUES (?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 1, 1, 1))
    cursor.execute('UPDATE mine SET palladium = palladium - 25 WHERE user_id = ?', (user_id,))
    conn.commit()


async def buy_ter_db(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE mine SET cobalt = cobalt - ? WHERE user_id = ?', (summ, user_id))
    cursor.execute('UPDATE quarry SET territory = territory + 1 user_id = ?', (user_id,))
    conn.commit()


async def buy_bur_db(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE mine SET titanium = titanium - ? WHERE user_id = ?', (summ, user_id))
    cursor.execute('UPDATE quarry SET bur = bur + 1 user_id = ?', (user_id,))
    conn.commit()


async def withdraw_profit_db(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE quarry SET balance = 0 user_id = ?', (user_id,))
    cursor.execute('UPDATE mine SET palladium = palladium + ? WHERE user_id = ?', (summ, user_id))
    conn.commit()


async def payment_taxes_db(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE quarry SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


# async def sell_quarry(user_id: int, ch: int) -> None:
#     balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
#     summ = Decimal(balance) + Decimal(ch)
#
#     cursor.execute('DELETE FROM generator WHERE user_id = ?', (user_id,))
#     cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
#     conn.commit()