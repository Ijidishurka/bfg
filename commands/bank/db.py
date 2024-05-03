from commands.db import conn, cursor


async def getbankdb(message):
    user_id = message.from_user.id
    cursor.execute('SELECT depozit, timedepozit, bank FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    depozit, timedepozit, bank = i
    return depozit, timedepozit, bank


async def putbank_db(summ, user_id):
    cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (summ, user_id))
    cursor.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def takeoffbank_db(summ, user_id):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (summ, user_id))
    cursor.execute("UPDATE users SET bank = bank - ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def putdep_db(summ2, user_id, dt, summ):
    cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?", (summ, user_id))
    cursor.execute("UPDATE users SET depozit = depozit + ? WHERE user_id = ?", (summ2, user_id))
    cursor.execute("UPDATE users SET timedepozit = ? WHERE user_id = ?", (dt, user_id))
    conn.commit()


async def getdepost(ost, user_id):
    cursor.execute("UPDATE users SET depozit = depozit - ? WHERE user_id = ?", (ost, user_id))
    cursor.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (ost, user_id))
    conn.commit()


async def sndep_db(summ, user_id):
    cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?", (summ, user_id))
    cursor.execute("UPDATE users SET depozit = 0 WHERE user_id = ?", (user_id,))
    conn.commit()


async def getbakbalance_db(message):
    user_id = message.from_user.id
    cursor.execute('SELECT bank FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def getdepbakance_db(message):
    user_id = message.from_user.id
    cursor.execute('SELECT depozit FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()[0]
    return i


async def autobank():
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.06) WHERE depozit > 0')
    conn.commit()
