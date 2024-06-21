from commands.db import conn, cursor
from decimal import Decimal


async def getquarry(uid):
    return cursor.execute('SELECT balance, nalogs, territory, bur, lvl FROM quarry WHERE user_id = ?', (uid,)).fetchone()


async def getonlipalladium(uid):
    return cursor.execute('SELECT palladium FROM mine WHERE user_id = ?', (uid,)).fetchone()[0]


async def getonlicobalt(uid):
    return cursor.execute('SELECT cobalt FROM mine WHERE user_id = ?', (uid,)).fetchone()[0]


async def getonlititanium(uid):
    return cursor.execute('SELECT titanium FROM mine WHERE user_id = ?', (uid,)).fetchone()[0]


async def buy_quarry_db(uid):
    cursor.execute('INSERT INTO quarry (user_id, balance, nalogs, territory, bur, lvl) VALUES (?, ?, ?, ?, ?, ?)', (uid, 0, 0, 1, 1, 1))
    cursor.execute('UPDATE mine SET palladium = palladium - 25 WHERE user_id = ?', (uid,))
    conn.commit()


async def buy_ter_db(uid, summ):
    cursor.execute('UPDATE mine SET cobalt = cobalt - ? WHERE user_id = ?', (summ, uid))
    cursor.execute('UPDATE quarry SET territory = territory + 1 user_id = ?', (uid,))
    conn.commit()


async def buy_bur_db(uid, summ):
    cursor.execute('UPDATE mine SET titanium = titanium - ? WHERE user_id = ?', (summ, uid))
    cursor.execute('UPDATE quarry SET bur = bur + 1 user_id = ?', (uid,))
    conn.commit()


async def snyt_pribl_quarry_db(uid, summ):
    cursor.execute('UPDATE quarry SET balance = 0 user_id = ?', (uid,))
    cursor.execute('UPDATE mine SET palladium = palladium + ? WHERE user_id = ?', (summ, uid))
    conn.commit()


async def oplata_nalogs_db(uid, ch):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (uid,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE quarry SET nalogs = 0 WHERE user_id = ?', (uid,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), uid))
    conn.commit()