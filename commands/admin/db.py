from decimal import Decimal

from commands.db import conn, cursor, update_ads_const


async def give_money_db(user_id: int, r_user_id: int, summ: str, status: str) -> str | None:
    if status == 'adm':
        limit = 150_000_000_000_000  # лимит выдачи денег у статуса админ (4)
        per = cursor.execute(f"SELECT issued FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
        if (per + summ) > limit:
            return 'limit'
        
        cursor.execute(f'UPDATE users SET issued = issued + ? WHERE user_id = ?', (summ, user_id))

    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (r_user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(summ)

    cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), r_user_id))
    conn.commit()


async def give_bcoins_db(r_user_id: int, summ: int) -> None:
    cursor.execute(f'UPDATE users SET ecoins = ecoins + ? WHERE user_id = ?', (summ, r_user_id))
    conn.commit()


async def upd_ads(text: str) -> None:
    cursor.execute('UPDATE sett SET ads = ?', (text,))
    conn.commit()
    await update_ads_const()


async def new_promo_db(data: tuple) -> str | None:
    res = cursor.execute(f"SELECT name FROM promo WHERE name = ?", (data[0],)).fetchone()
    if res:
        return 'error'

    cursor.execute('INSERT INTO promo (name, summ, activ, data) VALUES (?, ?, ?, ?)', (data[0], str(data[1]), data[2], data[3]))
    conn.commit()


async def dell_promo_db(name: str) -> str | None:
    res = cursor.execute(f"SELECT name FROM promo WHERE name = ?", (name,)).fetchone()
    if not res:
        return 'error'

    cursor.execute('DELETE from promo WHERE name = ?', (name,))
    cursor.execute('DELETE from promo_activ WHERE name = ?', (name,))
    conn.commit()


async def activ_promo_db(name: str, user_id: int) -> str | tuple:
    data = cursor.execute(f"SELECT * FROM promo WHERE name = ?", (name,)).fetchone()
    if not data:
        return 'no promo'

    if data[2] <= 0:
        return 'activated'

    res = cursor.execute(f"SELECT * FROM promo_activ WHERE name = ? AND user_id = ?", (name, user_id)).fetchone()
    if res:
        return 'used'

    parts = data[3].split()[0].split('/')
    table, column = parts[0], parts[1]

    balance = cursor.execute(f'SELECT {column} FROM {table} WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = int(Decimal(balance) + Decimal(int(data[1])))

    if table == 'users' and column in ['balance']:
        summ = str(summ)

    cursor.execute(f'UPDATE {table} SET {column} = ? WHERE user_id = ?', (summ, user_id))
    cursor.execute(f'UPDATE promo SET activ = activ - 1 WHERE name = ?', (name,))
    cursor.execute('INSERT INTO promo_activ (user_id, name) VALUES (?, ?)', (user_id, name))
    conn.commit()
    return data


async def promo_info_db(name: str) -> tuple:
    return cursor.execute(f"SELECT * FROM promo WHERE name = ?", (name,)).fetchone()


async def get_users_chats() -> tuple:
    users = cursor.execute(f"SELECT user_id FROM users").fetchall()
    chats = cursor.execute(f"SELECT chat_id FROM chats").fetchall()
    return users, chats


async def zap_sql(query: str) -> str | None:
    try:
        cursor.execute(query)
        conn.commit()
    except Exception as e:
        conn.rollback()
        return e
    
    
async def new_ban(user_id: int, time_s: int, reason: str) -> None:
    user_id = cursor.execute(f"SELECT user_id FROM users WHERE game_id = ?", (user_id,)).fetchone()
    if user_id:
        res = cursor.execute(f"SELECT * FROM ban_list WHERE user_id = ?", (user_id[0],)).fetchone()
        if res:
            cursor.execute('DELETE FROM ban_list WHERE user_id = ?', (user_id[0],))
            conn.commit()
            
        cursor.execute('INSERT INTO ban_list (user_id, time, reason) VALUES (?, ?, ?)', (user_id[0], time_s, reason))
        conn.commit()


async def unban_user(user_id: int) -> None:
    user_id = cursor.execute(f"SELECT user_id FROM users WHERE game_id = ?", (user_id,)).fetchone()
    if user_id:
        cursor.execute('DELETE FROM ban_list WHERE user_id = ?', (user_id[0],))
        conn.commit()
        
    
async def take_the_money(user_id: int, summ: str) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    
    new_balance = Decimal(str(balance)) - Decimal(str(summ))
    new_balance = "{:.0f}".format(new_balance)
    
    cursor.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()


async def reset_the_money(user_id: int) -> None:
    cursor.execute("UPDATE users SET balance = 0, bank = 0, btc = 0, depozit = 0, energy = 10, corn = 0, yen = 0 WHERE user_id = ?", (user_id,))
    cursor.execute("UPDATE mine SET iron = 0, gold = 0, diamond = 0, amestit = 0, aquamarine = 10, emeralds = 0, "
                   "matter = 0, plasma = 0, nickel = 0, titanium = 0, cobalt = 0, ectoplasm = 0, biores = 0, palladium = 0 WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM ferma WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM garden WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM generator WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM quarry WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM tree WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM business WHERE user_id = ?", (user_id,))
    conn.commit()
