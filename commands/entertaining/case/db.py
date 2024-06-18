from commands.db import conn, cursor
from decimal import Decimal


async def getcase(message):
    user_id = message.from_user.id
    data = cursor.execute('SELECT case1, case2, case3, case4 FROM users WHERE user_id = ?', (user_id,)).fetchone()
    return data[0], data[1], data[2], data[3]


async def open_case_db(user_id, summ, u, table='users'):
    if u == 'balance':
        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        summ = Decimal(balance) + Decimal(summ)

        cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    else:
        cursor.execute(f"UPDATE {table} SET {u} = {u} + ? where user_id = ?", (summ, user_id))
    conn.commit()


async def open_case2_db(user_id, colvo, v):
    cursor.execute(f"UPDATE users SET {v} = {v} - ? where user_id = ?", (colvo, user_id))
    conn.commit()


async def buy_case_db_12(user_id, v, summ, case):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(summ)

    cursor.execute(f"UPDATE users SET {v} = {v} + ? WHERE user_id = ?", (case, user_id))
    cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    conn.commit()


async def get_mine(user_id):
    data = cursor.execute("SELECT titanium, matter FROM mine WHERE user_id = ?", (user_id,)).fetchone()
    return data[0], data[1]


async def buy_case_db_3(user_id, summ, case):
    cursor.execute(f"UPDATE users SET case3 = case3 + ? WHERE user_id = ?", (case, user_id))
    cursor.execute(f"UPDATE mine SET titanium = titanium - ? WHERE user_id = ?", (summ, user_id))
    conn.commit()


async def buy_case_db_4(user_id, summ, case):
    cursor.execute(f"UPDATE users SET case4 = case4 + ? WHERE user_id = ?", (case, user_id))
    cursor.execute(f"UPDATE mine SET matter = matter - ? WHERE user_id = ?", (summ, user_id))
    conn.commit()