from commands.db import conn, cursor
from decimal import Decimal


async def give_money_db(user_id, r_user_id, summ, st):
    if st == 'adm':
        limit = 150000000000000  # лимит выдачи денег у статуса админ (4)
        per = cursor.execute(f"SELECT issued FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        if (per + summ) < limit: return 'limit'
        cursor.execute(f'UPDATE users SET issued = issued + ? WHERE user_id = ?', (summ, user_id))

    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (r_user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), r_user_id))
    conn.commit()


async def give_bcoins_db(r_user_id, summ):
    cursor.execute(f'UPDATE users SET ecoins = ecoins + ? WHERE user_id = ?', (summ, r_user_id))
    conn.commit()


async def upd_ads(txt):
    cursor.execute(f'UPDATE sett SET ads = ?', (txt,))
    conn.commit()


async def new_promo_db(data):
    res = cursor.execute(f"SELECT name FROM promo WHERE name = ?", (data[0],)).fetchone()
    if res:
        return 'error'

    cursor.execute('INSERT INTO promo (name, summ, activ) VALUES (?, ?, ?)', (data[0], str(data[1]), data[2]))
    conn.commit()


async def dell_promo_db(name):
    res = cursor.execute(f"SELECT name FROM promo WHERE name = ?", (name,)).fetchone()
    if not res:
        return 'error'

    cursor.execute('DELETE from promo WHERE name = ?', (name,))
    cursor.execute('DELETE from promo_activ WHERE name = ?', (name,))
    conn.commit()


async def activ_promo_db(name, user_id):
    data = cursor.execute(f"SELECT * FROM promo WHERE name = ?", (name,)).fetchone()
    if not data:
        return 'no promo'

    if data[2] <= 0:
        return 'activated'

    res = cursor.execute(f"SELECT * FROM promo_activ WHERE name = ? AND user_id = ?", (name, user_id)).fetchone()
    if res:
        return 'used'

    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) + Decimal(int(data[1])))

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    cursor.execute(f'UPDATE promo SET activ = activ - 1 WHERE name = ?', (name,))
    cursor.execute('INSERT INTO promo_activ (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    return int(data[1])