from commands.db import conn, cursor
from decimal import Decimal


async def buy_tree(user_id: int) -> None:
    cursor.execute('INSERT INTO tree (user_id, balance, nalogs, territory, tree, yen) VALUES (?, ?, ?, ?, ?, ?)', (user_id, 0, 0, 5, 1, 0))
    cursor.execute('UPDATE mine SET biores = biores - 500000000 WHERE user_id = ?', (user_id,))
    conn.commit()


async def buy_ter(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE mine SET biores = biores - ? WHERE user_id = ?', (summ, user_id))
    cursor.execute('UPDATE tree SET territory = territory + 1 WHERE user_id = ?', (user_id,))
    conn.commit()


async def buy_tree_ter(user_id: int, summ: int) -> None:
    cursor.execute('UPDATE mine SET biores = biores - ? WHERE user_id = ?', (summ, user_id))
    cursor.execute('UPDATE tree SET tree = tree + 1 WHERE user_id = ?', (user_id,))
    conn.commit()


async def withdraw_profit(user_id: int, summ: int, summ2: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) + Decimal(summ))

    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute('UPDATE users SET yen = yen + ? WHERE user_id = ?', (summ2, user_id))
    cursor.execute('UPDATE tree SET balance = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE tree SET yen = 0 WHERE user_id = ?', (user_id,))
    conn.commit()


async def pay_taxes(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) - Decimal(ch))

    cursor.execute('UPDATE tree SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def sell_tree(user_id: int, summ: int) -> None:
    cursor.execute('DELETE FROM garden WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE mine SET biores = biores + ? WHERE user_id = ?', (int(summ), user_id))
    conn.commit()


async def autotree() -> None:
    cursor.execute('UPDATE tree SET balance = balance + ROUND(5000 * POWER(tree, 3.8)) WHERE nalogs < 5000000')
    cursor.execute('UPDATE tree SET yen = yen + ROUND(tree * 5) WHERE nalogs < 5000000')
    cursor.execute('UPDATE tree SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()
