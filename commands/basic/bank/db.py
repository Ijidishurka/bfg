from commands.db import conn, cursor
from decimal import Decimal, getcontext

getcontext().prec = 320  # Decimial будет округлять все после 320 знаков


async def putdep_db(user_id: int, time: int) -> None:
    cursor.execute("UPDATE users SET timedepozit = ? WHERE user_id = ?", (time, user_id))
    conn.commit()


async def autobank() -> None:
    climit = {1: 0.08, 2: 0.1, 3: 0.12, 4: 0.15}
    users = cursor.execute('SELECT user_id, depozit, status FROM users WHERE depozit > 0').fetchall()
    
    for user in users:
        p = climit.get(user[2], 0.06)
        summ = int(Decimal(user[1]) + (Decimal(user[1])) * Decimal(p))
        summ = "{:.0f}".format(summ)
        cursor.execute('UPDATE users SET depozit = ? WHERE user_id = ?', (summ, user[0]))
    conn.commit()
