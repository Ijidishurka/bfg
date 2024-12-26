from decimal import Decimal
from commands.db import conn, cursor


async def buy_property(user_id: int, num: int, u: str, summ: int | str) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) - Decimal(summ))

    cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    cursor.execute(f"UPDATE property SET {u} = ? WHERE user_id = ?", (num, user_id))
    conn.commit()


async def sell_property(user_id: int, u: str, summ: int | str) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) + Decimal(summ))

    cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    cursor.execute(f"UPDATE property SET {u} = ? WHERE user_id = ?", (0, user_id))
    conn.commit()