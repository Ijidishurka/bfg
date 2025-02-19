from commands.db import conn, cursor
from datetime import datetime


async def get_wedlock(user_id: int) -> tuple:
    return cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (user_id, user_id)).fetchone()


async def get_new_wedlock(user_id: int, rid: int) -> str:
    if cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (user_id, user_id)).fetchone():
        return 'u_not'
    if cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (rid, rid)).fetchone():
        return 'r_not'


async def new_wedlock(user_id: int, rid: int) -> bool:
    data1 = cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (user_id, user_id)).fetchone()
    data2 = cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (rid, rid)).fetchone()
    if data1 or data2:
        return True

    cursor.execute('INSERT INTO wedlock (user1, user2, rtime) VALUES (?, ?, ?)', (user_id, rid, datetime.now().timestamp()))
    conn.commit()


async def divorce_db(user_id: int) -> None:
    cursor.execute('DELETE FROM wedlock WHERE user1 = ? OR user2 = ?', (user_id, user_id))
    conn.commit()
    