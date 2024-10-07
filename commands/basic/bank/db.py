from commands.db import conn, cursor
from decimal import Decimal, getcontext

getcontext().prec = 320  # Decimial будет округлять все после 320 знаков


async def getbankdb(user_id):
    i = cursor.execute('SELECT depozit, timedepozit, bank FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return int(i[0]), int(i[1]), int(i[2])


async def putbank_db(summ, user_id):
    balance, bank = cursor.execute('SELECT balance, bank FROM users WHERE user_id = ?', (user_id,)).fetchone()

    new_balance = Decimal(str(balance)) - Decimal(str(summ))
    new_bank = Decimal(bank) + Decimal(summ)
    new_balance = "{:.0f}".format(new_balance)
    new_bank = "{:.0f}".format(new_bank)

    cursor.execute("UPDATE users SET balance = ?, bank = ? WHERE user_id = ?", (new_balance, new_bank, user_id))
    conn.commit()
    
    
async def takeoffbank_db(summ, user_id):
    balance, bank = cursor.execute('SELECT balance, bank FROM users WHERE user_id = ?', (user_id,)).fetchone()

    new_balance = Decimal(str(balance)) + Decimal(str(summ))
    new_bank = Decimal(str(bank)) - Decimal(str(summ))
    new_balance = "{:.0f}".format(new_balance)
    new_bank = "{:.0f}".format(new_bank)

    cursor.execute("UPDATE users SET balance = ?, bank = ? WHERE user_id = ?", (new_balance, new_bank, user_id))
    conn.commit()


async def putdep_db(summ2, user_id, dt, summ):
    balance, depozit = cursor.execute('SELECT balance, depozit FROM users WHERE user_id = ?', (user_id,)).fetchone()
    
    new_balance = Decimal(balance) - Decimal(summ)
    new_dep = Decimal(depozit) + Decimal(summ2)
    new_balance = "{:.0f}".format(new_balance)
    new_dep = "{:.0f}".format(new_dep)

    cursor.execute("UPDATE users SET balance = ?, depozit = ?, timedepozit = ? WHERE user_id = ?", (new_balance, new_dep, dt, user_id))
    conn.commit()


async def getdepost(ost, user_id):
    bank = cursor.execute('SELECT bank FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    
    new_bank = Decimal(bank) + Decimal(ost)
    new_bank = "{:.0f}".format(new_bank)
    
    cursor.execute("UPDATE users SET depozit = 0, bank = ? WHERE user_id = ?", (new_bank, user_id))
    conn.commit()


async def sndep_db(summ, user_id):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)
    summ = "{:.0f}".format(summ)

    cursor.execute("UPDATE users SET balance = ?, depozit = 0 WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def autobank():
    climit = {1: 0.08, 2: 0.1, 3: 0.12, 4: 0.15}
    users = cursor.execute('SELECT user_id, depozit, status FROM users WHERE depozit > 0').fetchall()
    
    for user in users:
        p = climit.get(user[2], 0.06)
        summ = int(Decimal(user[1]) + (Decimal(user[1])) * Decimal(p))
        summ = "{:.0f}".format(summ)
        cursor.execute('UPDATE users SET depozit = ? WHERE user_id = ?', (summ, user[0]))
    conn.commit()
