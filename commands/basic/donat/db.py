import time
from decimal import Decimal

from commands.db import conn, cursor


async def buy_status_db(user_id: int, summ: int, status: int) -> None:
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (summ, user_id))
    cursor.execute(f"UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
    conn.commit()


async def exchange_value_db(user_id: int, summ: int | str, price: int) -> None:
    balance = cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]

    balance = int(Decimal(balance) + Decimal(summ))

    cursor.execute(f"UPDATE users SET balance = ? WHERE user_id = ?", (str(balance), user_id))
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (price, user_id))
    conn.commit()


async def buy_limit_db(user_id: int, summ: int | str, price: int) -> None:
    doplimit = cursor.execute("SELECT perlimit FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    doplimit = int(Decimal(doplimit) + Decimal(summ))

    cursor.execute(f"UPDATE users SET perlimit = ? WHERE user_id = ?", (str(doplimit), user_id))
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (price, user_id))
    conn.commit()
    

async def buy_energy_db(user_id: int, price: int, amount: int) -> None:
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (price, user_id))
    cursor.execute(f"UPDATE users SET energy = energy + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()


async def new_pay(user_id: int, amount: int, transaction_id: str) -> None:
    cursor.execute(
        "INSERT INTO donat (user_id, amount, transaction_id, time, refund) VALUES (?, ?, ?, ?, ?)",
        (user_id, amount, transaction_id, int(time.time()), 0)
    )
    cursor.execute(f"UPDATE users SET ecoins = ecoins + ? WHERE user_id = ?", (amount, user_id))
    conn.commit()


async def get_transactions_to_refund(user_id: int) -> list:
    return cursor.execute("SELECT * FROM donat WHERE user_id = ? AND time >= ? AND refund = 0", (user_id, int(time.time()-86400))).fetchall()


async def get_transaction(donat_id: int) -> tuple:
    return cursor.execute("SELECT * FROM donat WHERE id = ?", (donat_id,)).fetchone()


async def new_refund(user_id: int, amount: int, donat_id: int) -> None:
    cursor.execute(f"UPDATE users SET ecoins = ecoins - ? WHERE user_id = ?", (amount, user_id))
    cursor.execute(f"UPDATE donat SET refund = 1 WHERE id = ?", (donat_id,))
    conn.commit()
