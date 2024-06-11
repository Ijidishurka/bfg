from commands.db import conn, cursor
from decimal import Decimal


async def getquarry(id):
    return cursor.execute('SELECT balance, nalogs, territory, bur, lvl FROM quarry WHERE user_id = ?', (id,)).fetchone()


async def getonlipalladium(id):
    return cursor.execute('SELECT palladium FROM mine WHERE user_id = ?', (id,)).fetchone()[0]


async def getonlicobalt(id):
    return cursor.execute('SELECT cobalt FROM mine WHERE user_id = ?', (id,)).fetchone()[0]


async def getonlititanium(id):
    return cursor.execute('SELECT titanium FROM mine WHERE user_id = ?', (id,)).fetchone()[0]


async def buy_quarry_db(id):
    cursor.execute('INSERT INTO quarry (user_id, balance, nalogs, territory, bur, lvl) VALUES (?, ?, ?, ?, ?, ?)', (id, 0, 0, 1, 1, 1))
    cursor.execute('UPDATE mine SET palladium = palladium - 25 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_ter_db(id, summ):
    cursor.execute('UPDATE mine SET cobalt = cobalt - ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE quarry SET territory = territory + 1 user_id = ?', (id,))
    conn.commit()


async def buy_bur_db(id, summ):
    cursor.execute('UPDATE mine SET titanium = titanium - ? WHERE user_id = ?', (summ, id))
    cursor.execute('UPDATE quarry SET bur = bur + 1 user_id = ?', (id,))
    conn.commit()