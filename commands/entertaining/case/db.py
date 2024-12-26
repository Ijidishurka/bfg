from commands.db import conn, cursor
from decimal import Decimal


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