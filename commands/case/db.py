from commands.db import conn, cursor


async def getcase(message):
    user_id = message.from_user.id
    cursor.execute('SELECT case1, case2, case3, case4 FROM users WHERE user_id = ?', (user_id,))
    i = cursor.fetchone()
    case1, case2, case3, case4 = i
    return case1, case2, case3, case4


async def open_case_db(user_id, table, v, summ, case, case_summ):
    cursor.execute(f"UPDATE {table} SET {v} = {v} + ? WHERE user_id = ?", (summ, user_id))
    cursor.execute(f"UPDATE users SET {case} = {case} - ? WHERE user_id = ?", (case_summ, user_id))
    conn.commit()


async def buy_case_db_12(user_id, v, summ, case):
    cursor.execute(f"UPDATE users SET {v} = {v} + ? WHERE user_id = ?", (case, user_id))
    cursor.execute(f"UPDATE users SET balance = balance - ? WHERE user_id = ?", (summ, user_id))
    conn.commit()