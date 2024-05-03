from commands.db import conn, cursor

async def getbusiness(id):
    cursor.execute('SELECT business, balance, nalogs, territory, bsterritory FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()
    business, balance, nalogs, territory, bsterritory = i
    return business, balance, nalogs, territory, bsterritory

async def getbusiness1(id):
    cursor.execute('SELECT business FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def buy_business_db(id):
    cursor.execute('UPDATE business SET business = 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - 500000000 WHERE user_id = ?', (id,))
    conn.commit()

async def getterritory(id):
    cursor.execute('SELECT territory FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def getbsterritory(id):
    cursor.execute('SELECT bsterritory FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def buy_territory_db(id, ch):
    cursor.execute('UPDATE business SET territory = territory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def buy_bsterritory_db(id, ch):
    cursor.execute('UPDATE business SET bsterritory = bsterritory + 1 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def get_business_balance(id):
    cursor.execute('SELECT balance FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def snyt_pribl_bs_db(id, ch):
    cursor.execute('UPDATE business SET balance = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def get_business_nalogs(id):
    cursor.execute('SELECT nalogs FROM business WHERE user_id = ?', (id,))
    i = cursor.fetchone()[0]
    return i

async def oplata_nalogs_bs_db(id, ch):
    cursor.execute('UPDATE business SET nalogs = 0 WHERE user_id = ?', (id,))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (ch, id))
    conn.commit()

async def autobusiness():
    cursor.execute('UPDATE business SET balance = balance + ROUND((90000000 * bsterritory) / 15) WHERE business = 1 AND nalogs < 5000000')
    cursor.execute('UPDATE business SET nalogs = nalogs + 200000 WHERE business = 1 AND nalogs < 5000000')
    conn.commit()