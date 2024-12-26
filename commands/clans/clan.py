from aiogram import Dispatcher, types
from assets.antispam import antispam, antispam_earning, new_earning
from commands.db import url_name, get_name
from commands.clans.db import *
from assets import kb
from user import BFGuser, BFGconst


async def get_clan_text(udata, url):
	data, colvo, glovo = await clan_full_info(udata[1])

	type = 'открытый' if data[10] == 1 else 'закрытый'

	if datetime.now() > datetime.fromtimestamp(data[11]):
		stime = "➖"
	else:
		seconds = int(data[11]) - int(datetime.now().timestamp())
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60

		stime = f"{hours:02}:{minutes:02}:{seconds:02}"

	return f'''{url}, информация о Вашем клане:
	✏️️ Название: "{data[2]}"
	🗂 ID клана: {data[0]}
	🔓 Тип клана: {type}
	👤 Глава: {glovo}
	👥 Участников: {colvo}

	👑 Рейтинг: {data[12]}
	💰 В казне клана: {data[1]}$
	🏹 Действие щита: {stime}

	🔥 Побед: {data[13]}, поражений: {data[14]}
	🗡 На вас нападало: {data[13] + data[14]} кланов'''


@antispam
async def my_clan(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()
	udata = await clan_info(user.user_id)

	if not udata:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	txt = await get_clan_text(udata, user.url)
	msg = await message.answer(txt, reply_markup=kb.clan(user.user_id))
	await new_earning(msg)


@antispam_earning
async def my_clan_call(call: types.CallbackQuery, user: BFGuser):
	udata = await clan_info(user.user_id)

	if not udata:
		return

	try:
		txt = await get_clan_text(udata, user.url)
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.user_id))
	except:
		pass


@antispam_earning
async def clan_users(call: types.CallbackQuery, user: BFGuser):
	udata = await clan_info(user.user_id)

	if not udata:
		return

	emojis = {
		1: ("👤", "Участник"),
		2: ("👀", "Модератор"),
		3: ("💎", "Заместитель"),
		4: ("👑", "Глава")
	}

	data = await get_user_list(udata[1])

	txt = f'{user.url}, участники клана:\n'
	for user in data:
		name = await get_name(user[0])
		d = emojis.get(int(user[2]), emojis[1])
		txt += f'[{d[0]}] | [{name} ({user[0]})] - [{d[1]}]\n'

	try:
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.user_id))
	except:
		pass


@antispam_earning
async def clan_settings(call: types.CallbackQuery, user: BFGuser):
	user_id = call.from_user.id
	url = await url_name(user_id)
	udata = await clan_info(user_id)

	if not udata:
		return

	emojis = {
		1: '[👤] Участник',
		2: '[👀] Модер',
		3: '[💎] Зам',
		4: '[👑] Глава'
	}

	d, _, _ = await clan_full_info(udata[1])

	txt = f'''{url}, текущие настройки клана:
[📥] Приглашение в клан: {emojis[d[3]]}
[💢] Кикать могут: {emojis[d[4]]}
[🔰] Повышать/понижать могут: {emojis[d[5]]}
[💵] Снимать с казны могут: {emojis[d[6]]}
[💰] Начинать ограбление могут: {emojis[d[7]]}
[⚔️] Начинать войну могут: {emojis[d[8]]}
[✏️] Изменять название могут: {emojis[d[9]]}'''

	try:
		await call.message.edit_text(text=txt, reply_markup=kb.clan(user.user_id))
	except:
		pass


def reg(dp: Dispatcher):
	dp.register_message_handler(my_clan, lambda message: message.text.lower().startswith('мой клан'))
	dp.register_callback_query_handler(my_clan_call, text_startswith='clan-info')
	dp.register_callback_query_handler(clan_users, text_startswith='clan-users')
	dp.register_callback_query_handler(clan_settings, text_startswith='clan-settings')