from commands.db import conn, cursor
from decimal import Decimal


async def getbankdb(message):
    user_id = message.from_user.id
    cursor.execute('SELECT depozit, timedepozit, bank FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    depozit, timedepozit, bank = i
    return depozit, timedepozit, bank


async def putbank_db(summ, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ2 = Decimal(balance) - Decimal(summ)

    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (str(summ2), user_id))
    cursor.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def takeoffbank_db(summ, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ2 = Decimal(balance) + Decimal(summ)

    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (str(summ2), user_id))
    cursor.execute("UPDATE users SET bank = bank - ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def putdep_db(summ2, user_id, dt, summ):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(summ)

    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    cursor.execute("UPDATE users SET depozit = depozit + ? WHERE user_id = ?", (summ2, user_id))
    cursor.execute("UPDATE users SET timedepozit = ? WHERE user_id = ?", (dt, user_id))
    conn.commit()


async def getdepost(ost, user_id):
    cursor.execute("UPDATE users SET depozit = depozit - ? WHERE user_id = ?", (ost, user_id))
    cursor.execute("UPDATE users SET bank = bank + ? WHERE user_id = ?", (ost, user_id))
    conn.commit()


async def sndep_db(summ, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)

    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
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
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.06) WHERE depozit > 0 AND status = 0')
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.08) WHERE depozit > 0 AND status = 1')
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.1) WHERE depozit > 0 AND status = 2')
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.12) WHERE depozit > 0 AND status = 3')
    cursor.execute('UPDATE users SET depozit = depozit + ROUND(depozit * 0.15) WHERE depozit > 0 AND status = 4')
    conn.commit()
