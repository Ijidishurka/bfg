from commands.db import conn, cursor


async def getgenertor(id):
    cursor.execute('SELECT turbine, balance, nalogs FROM generator WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        turbine, balance, nalogs = result
        return turbine, balance, nalogs, 1
    else:
        return 0, 0, 0, 0, 0


async def getonlimater(id):
    cursor.execute('SELECT matter FROM main WHERE user_id = ?', (id,))
    result = cursor.fetchone()[0]
    return result


async def getturbine(id):
    cursor.execute('SELECT turbine FROM users WHERE user_id = ?', (id,))
    result = cursor.fetchone()[0]
    return result


async def getgenertor2(id):
    cursor.execute('SELECT turbine FROM generator WHERE user_id = ?', (id,))
    result = cursor.fetchone()

    if result:
        return  1
    else:
        return 0


async def buy_garden_db(id):
    cursor.execute('INSERT INTO generator (user_id, balance, nalogs, turbine) VALUES (?, ?, ?, ?)', (id, 0, 0, 0))
    cursor.execute('UPDATE mine SET matter = matter - 2000 WHERE user_id = ?', (id,))
    conn.commit()


async def buy_turbine_db(id):
    cursor.execute('UPDATE users SET matter = matter - 2000 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE generator SET turbine = turbine + 1 WHERE user_id = ?', (id,))
    conn.commit()