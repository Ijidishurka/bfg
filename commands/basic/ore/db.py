import random
from decimal import Decimal
from commands.db import conn, cursor
from pycoingecko import CoinGeckoAPI


api = CoinGeckoAPI()


async def get_rate() -> int:
    i = cursor.execute("SELECT kursbtc FROM sett").fetchone()
    if i is None:
        cursor.execute("INSERT INTO sett (ads, kursbtc) VALUES (?, ?)", ("", 40000))
        conn.commit()
        return 100000
    return i[0]


async def dig_ore(i: int, user_id: int, r: str, op: int) -> None:
    cursor.execute("UPDATE users SET exp = exp + ? WHERE user_id = ?", (int(op), user_id))
    cursor.execute(f"UPDATE mine SET {r} = {r} + ? WHERE user_id = ?", (int(i), user_id))
    cursor.execute("UPDATE users SET energy = energy - 1 WHERE user_id = ?", (user_id,))
    conn.commit()


async def sell_ore(i: int | str, user_id: int, r: str, kolvo: int) -> None:
    cursor.execute(f"UPDATE mine SET {r} = {r} - ? WHERE user_id = ?", (int(kolvo), user_id))
    balance = cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(i)
    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (str(summ), user_id))
    conn.commit()


async def auto_energy() -> None:
    cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE energy < 10 AND status = 0")
    cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE energy < 25 AND status = 1")
    cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE energy < 50 AND status = 2")
    cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE energy < 75 AND status = 3")
    cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE energy < 100 AND status = 4")
    conn.commit()


async def auto_rate_btc() -> None:  # Не используется (актуальный курс - auto_rate_btc_new())
    cursor.execute("SELECT kursbtc FROM sett")
    current_kurs = cursor.fetchone()
    if current_kurs is None:
        cursor.execute("INSERT INTO sett (ads, kursbtc) VALUES (?, ?)", ("", 40000))
        current_kurs = 100000
    else:
        current_kurs = current_kurs[0]

    random_change = random.randint(1, 3)
    s = random.choice([-1, 1])
    new_kurs = current_kurs + (s * random_change)

    cursor.execute("UPDATE sett SET kursbtc = ?", (new_kurs,))
    conn.commit()


async def auto_rate_btc_new() -> None:
    try:
        new_kurs = api.get_price(ids="bitcoin", vs_currencies="usd")["bitcoin"]["usd"]
        cursor.execute("UPDATE sett SET kursbtc = ?", (int(new_kurs),))
        conn.commit()
    except Exception as e:
        print(f"Error update btc price - {e}")
    