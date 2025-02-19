from datetime import datetime

from aiogram import Dispatcher, types

from assets.antispam import antispam, antispam_earning, new_earning
from commands.db import get_name
from commands.clans import db
from assets import kb
from user import BFGuser, BFGconst


async def get_clan_text(user: BFGuser) -> str:
	data, colvo, glovo = await db.clan_full_info(user.clan.id)

	clan_type = 'открытый' if data[10] == 1 else 'закрытый'
	stime = "➖"

	if datetime.now() <= datetime.fromtimestamp(data[11]):
		seconds = int(data[11]) - int(datetime.now().timestamp())
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60

		stime = f"{hours:02}:{minutes:02}:{seconds:02}"

	text = f'''{user.url}, информация о Вашем клане:
	✏️️ Название: "{data[2]}"
	🗂 ID клана: {data[0]}
	🔓 Тип клана: {clan_type}
	👤 Глава: {glovo}
	👥 Участников: {colvo}

	👑 Рейтинг: {data[12]}
	💰 В казне клана: {data[1]}$
	🏹 Действие щита: {stime}

	🔥 Побед: {data[13]}, поражений: {data[14]}
	🗡 На вас нападало: {data[13] + data[14]} кланов'''
	
	return text


@antispam
async def my_clan(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	txt = await get_clan_text(user)
	msg = await message.answer(txt, reply_markup=kb.clan(user.id))
	await new_earning(msg)


@antispam_earning
async def my_clan_call(call: types.CallbackQuery, user: BFGuser):
	udata = await db.clan_info(user.id)

	if not udata:
		return

	try:
		txt = await get_clan_text(user)
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.id))
	except:
		...


@antispam_earning
async def clan_users(call: types.CallbackQuery, user: BFGuser):
	if not user.clan:
		return
	
	emojis = {
		1: ("👤", "Участник"),
		2: ("👀", "Модератор"),
		3: ("💎", "Заместитель"),
		4: ("👑", "Глава")
	}

	data = await db.get_user_list(user.clan.id)
	txt = f'{user.url}, участники клана:\n'
	
	for player in data:
		name = await get_name(player[0])
		d = emojis.get(int(player[2]), emojis[1])
		txt += f'[{d[0]}] | [{name} ({player[0]})] - [{d[1]}]\n'

	try:
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.id))
	except:
		...


@antispam_earning
async def clan_settings(call: types.CallbackQuery, user: BFGuser):
	if not user.clan:
		return

	emojis = {
		1: '[👤] Участник',
		2: '[👀] Модер',
		3: '[💎] Зам',
		4: '[👑] Глава'
	}

	d = user.clan.settings

	txt = f'''{user.url}, текущие настройки клана:
[📥] Приглашение в клан: {emojis[d['inv']]}
[💢] Кикать могут: {emojis[d['kick']]}
[🔰] Повышать/понижать могут: {emojis[d['ranks']]}
[💵] Снимать с казны могут: {emojis[d['kazna']]}
[💰] Начинать ограбление могут: {emojis[d['robbery']]}
[⚔️] Начинать войну могут: {emojis[d['war']]}
[✏️] Изменять название могут: {emojis[d['upd_name']]}'''

	try:
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.id))
	except:
		...


def reg(dp: Dispatcher):
	dp.register_message_handler(my_clan, lambda message: message.text.lower() == 'мой клан')
	dp.register_callback_query_handler(my_clan_call, text_startswith='clan-info')
	dp.register_callback_query_handler(clan_users, text_startswith='clan-users')
	dp.register_callback_query_handler(clan_settings, text_startswith='clan-settings')
