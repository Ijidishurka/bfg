from commands.db import conn, cursor
from datetime import datetime


async def get_wedlock(user_id):
    return cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (user_id, user_id)).fetchone()


async def get_new_wedlock(uid, rid):
    if cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (uid, uid)).fetchone():
        return 'u_not'
    if cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (rid, rid)).fetchone():
        return 'r_not'


async def new_wedlock(uid, rid):
    data1 = cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (uid, uid)).fetchone()
    data2 = cursor.execute('SELECT * FROM wedlock WHERE user1 = ? OR user2 = ?', (rid, rid)).fetchone()
    if data1 or data2:
        return 'error'

    cursor.execute('INSERT INTO wedlock (user1, user2, rtime) VALUES (?, ?, ?)', (uid, rid, datetime.now().timestamp()))
    conn.commit()


async def divorce_db(uid):
    cursor.execute('DELETE FROM wedlock WHERE user1 = ? OR user2 = ?', (uid, uid))
    conn.commit()