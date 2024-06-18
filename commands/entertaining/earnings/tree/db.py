from commands.db import conn, cursor
from decimal import Decimal


async def gettree(id):
    return cursor.execute('SELECT balance, nalogs, territory, tree, yen FROM tree WHERE user_id = ?', (id,)).fetchone()


async def getonlibiores(id):
    return cursor.execute('SELECT biores FROM mine WHERE user_id = ?', (id,)).fetchone()[0]


async def buy_tree_db(id):
    cursor.execute('INSERT INTO tree (user_id, balance, nalogs, territory, tree, yen) VALUES (?, ?, ?, ?, ?, ?)', (id, 0, 0, 5, 1, 0))
    cursor.execute('UPDATE mine SET biores = biores - 500000000 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_ter_db(id, summ):
    cursor.execute('UPDATE mine SET biores = biores - ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE tree SET territory = territory + 1 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_tree_ter_db(id, summ):
    cursor.execute('UPDATE mine SET biores = biores - ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE tree SET tree = tree + 1 WHERE user_id = ?', (id,))
    conn.commit()


async def snyt_pribl_db(id, summ, summ2):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = int(Decimal(balance) + Decimal(summ))

    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    cursor.execute('UPDATE users SET yen = yen + ? WHERE user_id = ?', (summ2, id))
    cursor.execute('UPDATE tree SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE tree SET yen = 0 WHERE user_id = ?', (id,))
    conn.commit()


async def oplata_nalogs_db(id, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (id,)).fetchone()[0]
    summ = int(Decimal(balance) - Decimal(ch))

    cursor.execute('UPDATE tree SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), id))
    conn.commit()


async def autotree():
    cursor.execute('UPDATE tree SET balance = balance + ROUND(5000 * POWER(tree, 3.8)) WHERE nalogs < 5000000')
    cursor.execute('UPDATE tree SET yen = yen + ROUND(tree * 5) WHERE nalogs < 5000000')
    cursor.execute('UPDATE tree SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()