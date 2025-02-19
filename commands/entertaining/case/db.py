from commands.db import conn, cursor
from decimal import Decimal


async def open_case_db(user_id: int, summ: str | int, column: str, table: str = 'users') -> None:
    if column == 'balance':
        balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
        summ = Decimal(balance) + Decimal(summ)

        cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    else:
        cursor.execute(f"UPDATE {table} SET {column} = {column} + ? where user_id = ?", (summ, user_id))
    conn.commit()


async def open_case2_db(user_id: int, amount: int, column: str) -> None:
    cursor.execute(f"UPDATE users SET {column} = {column} - ? where user_id = ?", (amount, user_id))
    conn.commit()
