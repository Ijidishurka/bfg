from decimal import Decimal
from commands.db import conn, cursor
from datetime import datetime


game_time = dict()


async def gametime(id):
    nd = 5
    ct = datetime.now()
    ld = game_time.get(id)

    if not ld:
        game_time[id] = ct
        ld = datetime.fromtimestamp(0)
    if ld:
        delta_seconds = (ct - ld).total_seconds()
        sl = int(nd - delta_seconds)

        if sl > 0:
            left1 = sl
            return 1
        else:
            game_time[id] = ct
            return 0


async def upgames(user_id):
    cursor.execute(f'UPDATE users SET games = games + 1 WHERE user_id = ?', (user_id,))
    conn.commit()


async def gXX(user_id, summ, c):
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = (Decimal(balance) - Decimal(summ)) + Decimal(c)

    cursor.execute("UPDATE users SET balance = ? where user_id = ?", (str(int(summ)), user_id))
    cursor.execute("UPDATE users SET games = games + 1 where user_id = ?", (user_id,))
    conn.commit()