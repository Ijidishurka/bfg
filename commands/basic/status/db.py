from commands.db import conn, cursor
from decimal import Decimal


async def buy_status_db(user_id: int, summ: int, u: int) -> None:
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (summ, user_id))
    cursor.execute(f"UPDATE users SET status = ? WHERE user_id = ?", (u, user_id))
    conn.commit()


async def exchange_value_db(user_id: int, summ: int | str, u: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

    balance = int(Decimal(balance) + Decimal(summ))

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), user_id))
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (u, user_id))
    conn.commit()


async def buy_limit_db(user_id: int, summ: int | str, u: int) -> None:
    doplimit = cursor.execute('SELECT perlimit FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    doplimit = int(Decimal(doplimit) + Decimal(summ))

    cursor.execute(f'UPDATE users SET perlimit = ? WHERE user_id = ?', (str(doplimit), user_id))
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (u, user_id))
    conn.commit()
    

async def buy_energy_db(user_id: int, summ: int, u: int) -> None:
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (summ, user_id))
    cursor.execute(f"UPDATE users SET energy = energy + ? WHERE user_id = ?", (u, user_id))
    conn.commit()