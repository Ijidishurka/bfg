from decimal import Decimal
from datetime import datetime, timedelta

from commands.db import conn, cursor


async def clan_info(user_id: int) -> tuple:
	return cursor.execute('SELECT * FROM clan WHERE user_id = ?', (user_id,)).fetchone()


async def new_clan_db(user_id: int, name) -> None:
	balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
	balance = int(Decimal(balance) - Decimal('250000000000'))
	cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), user_id))

	dt = int((datetime.now() + timedelta(hours=24)).timestamp())

	cursor.execute('INSERT INTO clans (balance, name, inv, kick, ranks, kazna, robbery, war, upd_name, type, shield,'
				   ' ratting, win, lose) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				   (0, name, 4, 4, 4, 1, 4, 4, 4, 1, dt, 0, 0, 0))

	clan_id = cursor.lastrowid
	cursor.execute('INSERT INTO clan (user_id, clan_id, rank) VALUES (?, ?, ?)', (user_id, clan_id, 4))
	conn.commit()


async def clan_full_info(cid: int) -> tuple:
	data = cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (cid,)).fetchone()
	colvo = cursor.execute('SELECT COUNT(*) FROM clan WHERE clan_id = ?', (cid,)).fetchone()[0]
	glovo = cursor.execute('SELECT user_id FROM clan WHERE clan_id = ? AND rank = 4', (cid,)).fetchone()[0]
	glovo = cursor.execute('SELECT name FROM users WHERE user_id = ?', (glovo,)).fetchone()[0]
	return data, colvo, glovo


async def get_user_list(cid: int) -> list:
	return cursor.execute('SELECT * FROM clan WHERE clan_id = ?', (cid,)).fetchall()


async def join_clan_db(user_id: int, cid: int) -> str:
	data = cursor.execute('SELECT * FROM clans WHERE clan_id = ?', (cid,)).fetchone()
	if not data:
		return '<no_clan>'

	if data[10] == 0:
		return '<private>'

	cursor.execute('INSERT INTO clan (user_id, clan_id, rank) VALUES (?, ?, ?)', (user_id, cid, 1))
	conn.commit()
	return data[2]


async def leave_clan_db(user_id: int) -> None:
	cursor.execute('DELETE FROM clan WHERE user_id = ?', (user_id,))
	conn.commit()


async def clan_dell_db(cid: int) -> None:
	cursor.execute('DELETE FROM clan WHERE clan_id = ?', (cid,))
	cursor.execute('DELETE FROM clans WHERE clan_id = ?', (cid,))
	conn.commit()


async def clan_kick_db(user_id: int, cid: int, rank: int) -> str:
	data = cursor.execute('SELECT * FROM clan WHERE user_id = ?', (user_id,)).fetchone()
	kick_rank = cursor.execute('SELECT kick FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	if not data or data[1] != cid:
		return '<no user>'

	if data[2] >= rank or kick_rank > rank:
		return '<small rank>'

	cursor.execute('DELETE FROM clan WHERE user_id = ?', (user_id,))
	conn.commit()


async def clan_kazna_up_db(user_id: int, summ: int, cid: int) -> None:
	balance = cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]
	clan = cursor.execute('SELECT balance FROM clans WHERE clan_id = ?', (cid,)).fetchone()[0]

	balance = int(Decimal(balance) - Decimal(summ))
	clan = int(Decimal(clan) + Decimal(summ))

	cursor.execute(f'UPDATE users SET balance = ? WHERE user_id = ?', (str(balance), user_id))
	cursor.execute(f'UPDATE clans SET balance = ? WHERE clan_id = ?', (str(clan), cid))
	conn.commit()


async def new_name_clan_db(name: str, cid: int) -> None:
	cursor.execute('UPDATE clans SET name = ? WHERE clan_id = ?', (name, cid))
	conn.commit()


async def new_owner_db(user_id: int, cid: int, new_id: int):
	cursor.execute('UPDATE clan SET rank = 4 WHERE clan_id = ? AND user_id = ?', (cid, new_id))
	cursor.execute('UPDATE clan SET rank = 3 WHERE clan_id = ? AND user_id = ?', (cid, user_id))
	conn.commit()


async def clan_up_rank(user_id: int) -> None:
	cursor.execute('UPDATE clan SET rank = rank + 1 WHERE user_id = ?', (user_id,))
	conn.commit()


async def clan_down_rank(user_id: int) -> None:
	cursor.execute('UPDATE clan SET rank = rank - 1 WHERE user_id = ?', (user_id,))
	conn.commit()


async def upd_settings(column: str, cid: int, rank: int) -> None:
	cursor.execute(f'UPDATE clans SET {column} = ? WHERE clan_id = ?', (rank, cid))
	conn.commit()


async def upd_settings_type_db(new_type: int, cid: int) -> None:
	cursor.execute(f'UPDATE clans SET type = ? WHERE clan_id = ?', (new_type, cid))
	conn.commit()
