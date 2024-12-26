from aiogram import Dispatcher, types
from assets.antispam import antispam_earning, new_earning, antispam
from commands.db import url_name, top_db, get_name, top_clans_db
from commands.clans.db import clan_full_info
from assets import kb
from user import BFGuser, BFGconst


def get_num_user(num: list, user_position: int | None) -> str:
	if user_position is not None and user_position <= 999:
		emojis = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
		return ''.join(emojis[int(digit)] for digit in num)
	return '➡️9️⃣9️⃣9️⃣'


async def get_user_position(top_players: list, user_id) -> int | None:
	for i, player in enumerate(top_players, start=1):
		if i > 999:
			break
		if player[0] == user_id:
			return i
	return None


def transform(summ: int) -> str:
	summ = int(summ)
	if summ > 100_000_000_000_000:
		return "{:.2e}".format(float(summ))
	return "{:,}".format(summ).replace(',', '.')


async def get_username(tab: str, data: tuple) -> str:
	if tab != 'users':
		return await get_name(data[0])
	return data[1]


async def handle_top(call, tab, st, index, top, top_emj) -> None:
	user_id = call.from_user.id
	userinfo, top_players = await top_db(user_id, st, tab)

	user_position = await get_user_position(top_players, user_id)
	url = await url_name(user_id)

	top_message = f"{url}, топ 10 игроков бота по {top}:\n"
	emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "1️⃣0️⃣"]

	for i, player in enumerate(top_players[:10], start=1):
		emj = emojis[i - 1]
		value = transform(player[index])
		name = await get_username(tab, player)
		top_message += f"{emj} {name} — {value}{top_emj}\n"

	top_message += f"—————————————————\n"

	emoji = get_num_user(str(user_position), user_position)
	value = transform(userinfo[index])
	name = await get_username(tab, userinfo)
	top_message += f"{emoji} {name} — {value}{top_emj}"

	await call.message.edit_text(text=top_message, reply_markup=kb.top(user_id, st), disable_web_page_preview=True)


async def handle_top_earning(call, tab, st, index, top, top_emj) -> None:
	user_id = call.from_user.id
	userinfo, top_players = await top_db(user_id, st, tab)
	url = await url_name(user_id)

	top_message = f"{url}, топ 10 игроков бота по {top}:\n"
	emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "1️⃣0️⃣"]

	for i, player in enumerate(top_players[:10], start=1):
		emj = emojis[i - 1]
		value = transform(player[index])
		name = await get_username(tab, player)
		top_message += f"{emj} {name} — {value}{top_emj}\n"

	if userinfo:
		user_position = await get_user_position(top_players, user_id)
		emoji = get_num_user(str(user_position), user_position)
		value = transform(userinfo[index])
		name = await get_username(tab, userinfo)

		top_message += f"—————————————————\n"
		top_message += f"{emoji} {name} — {value}{top_emj}"

	await call.message.edit_text(text=top_message, reply_markup=kb.top(user_id, st), disable_web_page_preview=True)


@antispam
async def top(message: types.Message, user: BFGuser):
	msg = await message.answer(f'{user.url}, выберите ниже топ который хотите открыть', reply_markup=kb.top(user.user_id, 'None'))
	await new_earning(msg)


@antispam_earning
async def top_call(call: types.CallbackQuery, user: BFGuser):
	tab = call.data.split('-')[1].split('|')[0]
	type = call.data.split('|')[2]
	
	if tab == type:
		return

	if tab == 'rating':
		await handle_top(call, 'users', 'rating', 13, 'рейтингу', '👑')
	elif tab == 'balance':
		await handle_top(call, 'users', 'balance', 2, 'балансу', '💲')
	elif tab == 'exp':
		await handle_top(call, 'users', 'exp', 7, 'опыту', '🏆')
	elif tab == 'yen':
		await handle_top(call, 'users', 'yen', 22, 'йенам', '💴')
	elif tab == 'case1':
		await handle_top(call, 'users', 'case1', 9, 'обычным кейсам', '📦')
	elif tab == 'case2':
		await handle_top(call, 'users', 'case2', 10, 'золотым кейсам', '🏵')
	elif tab == 'case3':
		await handle_top(call, 'users', 'case3', 11, 'рудным кейсам', '🏺')
	elif tab == 'case4':
		await handle_top(call, 'users', 'case4', 12, 'материальным кейсам', '🌌')
	elif tab == 'cards':
		await handle_top_earning(call, 'ferma', 'cards', 3, 'фермам', '🧰')
	elif tab == 'bsterritory':
		await handle_top_earning(call, 'business', 'bsterritory', 4, 'бизнесам', '🗄')


@antispam
async def top_clans(message: types.Message, user: BFGuser):
	claninfo, top_clans = await top_clans_db(user.user_id)
	user_position = None
	
	if claninfo:
		d, _, _ = await clan_full_info(claninfo[1])
		user_position = await get_user_position(top_clans, d[0])

	top_message = f"{user.url}, топ 10 кланов:\n"
	emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

	for i, clan in enumerate(top_clans[:10], start=1):
		position_emoji = emojis[i - 1]
		top_message += f"{position_emoji} {clan[2]} — {clan[12]}👑\n"

	if user_position is not None:
		top_message += f"—————————————————\n"
		emoji = get_num_user(str(user_position), user_position)
		top_message += f"{emoji} {d[2]} — {d[12]}👑"

	top_message += f'\n\n{BFGconst.ads}'

	await message.answer(top_message, disable_web_page_preview=True)


def reg(dp: Dispatcher):
	dp.register_message_handler(top, lambda message: message.text.lower() == 'топ')
	dp.register_callback_query_handler(top_call, text_startswith='top-')
	dp.register_message_handler(top_clans, lambda message: message.text.lower() == 'клан топ')