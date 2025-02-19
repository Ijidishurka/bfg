from commands.db import conn, cursor
from decimal import Decimal
from bot import bot


async def buy_garden(user_id: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal('1000000000')

    cursor.execute('INSERT INTO garden (user_id, balance, nalogs, tree, water) VALUES (?, ?, ?, ?, ?)', (user_id, 0, 0, 0, 100))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def payment_taxes(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE garden SET nalogs = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def withdraw_profit(user_id: int, ch: int) -> None:
    cursor.execute('UPDATE garden SET balance = 0 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET corn = corn + ? WHERE user_id = ?', (ch, user_id))
    conn.commit()


async def buy_tree(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) - Decimal(ch)

    cursor.execute('UPDATE garden SET tree = tree + 1 WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def buy_postion(summ: int, st: int, user_id: int) -> None:
    cursor.execute('UPDATE users SET corn = corn - ? WHERE user_id = ?', (st, user_id))
    cursor.execute('UPDATE users SET energy = energy + ? WHERE user_id = ?', (summ, user_id))
    conn.commit()


async def sell_garden(user_id: int, ch: int) -> None:
    balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
    summ = Decimal(balance) + Decimal(ch)
    
    cursor.execute('DELETE FROM garden WHERE user_id = ?', (user_id,))
    cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(summ), user_id))
    conn.commit()


async def autogarden() -> None:
    cursor.execute('UPDATE garden SET balance = balance + ((tree + 1) * 3) WHERE nalogs < 5000000')
    cursor.execute('UPDATE garden SET water = water - 10 WHERE water >= 10')
    cursor.execute('UPDATE garden SET nalogs = nalogs + 200000 WHERE nalogs < 5000000')
    conn.commit()
    await garden_driedup()


async def garden_driedup() -> None:
    users = cursor.execute('SELECT user_id FROM garden WHERE water < 10').fetchall()
    for user_id in users:

        text = '''😔 Сожалеем, но вы забыли полить сад и он засох.
Штат отобрал вашу территорию.

Вы можете построить новый сад ещё раз, но не забывайте вовремя поливать его.'''

        try:
            await bot.send_message(chat_id=user_id[0], text=text)
        except:
            pass

        cursor.execute('DELETE from garden WHERE user_id = ?', (user_id[0],))
        conn.commit()
