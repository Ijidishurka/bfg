from commands.db import conn, cursor


async def getecoins(id):
    cursor.execute('SELECT ecoins FROM users WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

