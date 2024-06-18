from datetime import datetime, timedelta
from commands.db import conn, cursor
from decimal import Decimal


async def clan_info(uid):
	return cursor.execute('SELECT * FROM clan WHERE user_id = ?', (uid,)).fetchone()


async def new_clan_db(uid, name):
	balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (uid,)).fetchone()[0]
	balance = int(Decimal(balance) - Decimal('250000000000'))
	cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), uid))

	dt = int((datetime.now() + timedelta(hours=24)).timestamp())

	cursor.execute('INSERT INTO clans (balance, name, inv, kick, ranks, kazna, robbery, war, upd_name, type, shield,'
				   ' ratting, win, lose) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				   (0, name, 4, 4, 4, 1, 4, 4, 4, 1, dt, 0, 0, 0))

	clan_id = cursor.lastrowid
	cursor.execute('INSERT INTO clan (user_id, clan_id, rank) VALUES (?, ?, ?)', (uid, clan_id, 4))
	conn.commit()


async def clan_full_info(cid):
	data = cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (cid,)).fetchone()
	colvo = cursor.execute('SELECT COUNT(*) FROM clan WHERE clan_id = ?', (cid,)).fetchone()[0]
	glovo = cursor.execute('SELECT user_id FROM clan WHERE clan_id = ? AND rank = 4', (cid,)).fetchone()[0]
	glovo = cursor.execute('SELECT name FROM users WHERE user_id = ?', (glovo,)).fetchone()[0]
	return data, colvo, glovo


async def get_user_list(cid):
	return cursor.execute('SELECT * FROM clan WHERE clan_id = ?', (cid,)).fetchall()


async def join_clan_db(uid, cid):
	data = cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (cid,)).fetchone()
	if not data:
		return '<no_clan>'

	if data[10] == 0:
		return '<private>'

	cursor.execute('INSERT INTO clan (user_id, clan_id, rank) VALUES (?, ?, ?)', (uid, cid, 1))
	conn.commit()
	return data[2]


async def leave_clan_db(uid, cid):
	name = cursor.execute('SELECT name FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	cursor.execute('DELETE FROM clan WHERE user_id = ?', (uid,))
	conn.commit()

	return name


async def clan_dell_db(cid):
	name = cursor.execute('SELECT name FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	cursor.execute('DELETE FROM clan WHERE clan_id = ?', (cid,))
	cursor.execute('DELETE FROM clans WHERE clan_id = ?', (cid,))
	conn.commit()

	return name


async def clan_kick_db(uid, cid, rank):
	data = cursor.execute('SELECT * FROM clan WHERE user_id = ?', (uid,)).fetchone()
	clan = cursor.execute('SELECT kick, name FROM clans WHERE clan_id = ?', (cid,)).fetchone()

	if not data or data[1] != cid:
		return '<no user>'

	if data[2] >= rank or clan[0] > rank:
		return '<small rank>'

	cursor.execute('DELETE FROM clan WHERE user_id = ?', (uid,))
	conn.commit()

	return clan[1]


async def clan_kazna_up_db(uid, summ, cid):
	balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (uid,)).fetchone()[0]
	clan = cursor.execute('SELECT balance FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	balance = int(Decimal(balance) - Decimal(summ))
	clan = int(Decimal(clan) + Decimal(summ))

	cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), uid))
	cursor.execute(f'UPDATE clans SET balance = ? WHERE clan_id = ?', (str(clan), cid))
	conn.commit()


async def new_name_clan_db(name, cid, rank):
	upd_name = cursor.execute('SELECT upd_name FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	if upd_name > rank:
		return '<small rank>'

	cursor.execute('UPDATE clans SET name = ? WHERE clan_id = ?', (name, cid))
	conn.commit()


async def new_owner_db(uid, cid, user_id):
	name = cursor.execute('SELECT name FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	cursor.execute('UPDATE clan SET rank = 4 WHERE clan_id = ? AND user_id = ?', (cid, uid))
	cursor.execute('UPDATE clan SET rank = 3 WHERE clan_id = ? AND user_id = ?', (cid, user_id))
	conn.commit()

	return name


async def clan_up_rank(uid):
	cursor.execute('UPDATE clan SET rank = rank + 1 WHERE user_id = ?', (uid,))
	conn.commit()


async def clan_down_rank(uid):
	cursor.execute('UPDATE clan SET rank = rank - 1 WHERE user_id = ?', (uid,))
	conn.commit()


async def upd_settings(st, cid, rank):
	cursor.execute(f'UPDATE clans SET {st} = ? WHERE clan_id = ?', (rank, cid))
	conn.commit()


async def upd_settings_type_db(u, cid):
	cursor.execute(f'UPDATE clans SET type = ? WHERE clan_id = ?', (u, cid))
	conn.commit()