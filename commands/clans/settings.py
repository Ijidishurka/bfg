from aiogram import Dispatcher, types
from assets.antispam import antispam
from commands.db import url_name, get_balance
from commands.main import win_luser
from commands.clans.db import *
import commands.clans.clan
from bot import bot
from assets import kb
import re


@antispam
async def clan_dell(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if not data:
		await message.answer(f'{url}, вы не состоите в клане {lose}')
		return

	if data[2] != 4:
		await message.answer(f'{url}, вы не можете удалить данный клан так как не являетесь создателем клана {lose}')
		return

	d, _, _ = await clan_full_info(data[1])

	await message.answer(f'''<b>[Внимание]</b>
😔 Вы действительно хотите удалить клан <b>[{d[2]}]</b>
✅ Для подтверждения нажмите кнопку ниже''', reply_markup=kb.dell_clan(user_id, data[1]))


async def clan_dell_call(call: types.CallbackQuery):
	error = False
	cdata = call.data.split('|')
	zap = cdata[0].split('_')[1]
	uid, cid = int(cdata[1]), int(cdata[2])
	user_id = call.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if uid != user_id:
		return

	if not data or data[2] != 4 or data[1] != cid:
		error = True

	try: await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	except: return

	if zap == 'false' or error:
		return

	res = await clan_dell_db(data[1])
	await call.message.answer(f'{url}, вы успешно удалили клан <b>[{res}]</b> {win}')


@antispam
async def clan_name(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if not data:
		await message.answer(f'{url}, вы не состоите в клане {lose}')
		return

	try:
		name = " ".join(message.text.split()[2:])
	except:
		await message.answer(f'{url}, вы не ввели название клана на которое хотите поменять {lose}')
		return

	if len(name) < 5:
		await message.answer(f'{url}, название клана не может быть меньше чем 5 символов {lose}')
		return

	if len(name) > 25:
		await message.answer(f'{url}, название клана не может быть длинее чем 25 символов {lose}')
		return

	if re.search(r'<|>|@|t\.me|http', name):
		await message.answer(f'{url}, название вашего клана содержит запрещённые символы {lose}')
		return

	res = await new_name_clan_db(name, data[1], data[2])

	if res == '<small rank':
		await message.answer(f'{url}, ваш ранг слишком мал, для того чтобы изменить название клана {lose}')
	else:
		await message.answer(f'<b>[Внимание]</b>\n✏️ Вы успешно изменили название клана на <b>[{name}]</b>')


@antispam
async def clan_new_owner(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if not data:
		await message.answer(f'{url}, вы не состоите в клане {lose}')
		return

	try:
		uid = int(message.text.split()[2])
	except:
		await message.answer(f'{url}, вы не указали ID игрока которому хотите передать клан {lose}')
		return

	if data[2] != 4:
		await message.answer(f'{url}, к сожалению Вы не можете передать клан так как не являетесь его основателем {lose}')
		return

	if user_id == uid:
		await message.answer(f'{url}, вы не можете передать клан самому себе {lose}')
		return

	r_data = await clan_info(user_id)
	d, _, _ = await clan_full_info(data[1])

	if r_data and r_data[1] == data[1]:
		await message.answer(f'''<b>⚠️ ВАЖНОЕ УВЕДОМЛЕНИЕ ⚠️</b>
<b>Передача клана "{d[2]}"</b>
🔴 <b>Внимание:</b> Это действие является окончательным и <u>не может быть отменено</u> после подтверждения.
❗ Пожалуйста, убедитесь в своем решении перед подтверждением.
✅ Если вы полностью уверены в своем решении и готовы передать клан, нажмите кнопку ниже для подтверждения.''', reply_markup=kb.new_own_clan(uid, data[1], user_id))
	else:
		await message.answer(f'{url}, данный игрок не находиться в вашем клане, вы не можете передать ему клан {lose}')


async def clan_new_owner_call(call: types.CallbackQuery):
	error = False
	cdata = call.data.split('|')
	zap = cdata[0].split('_')[1]
	uid, cid, uid2 = int(cdata[1]), int(cdata[2]), int(cdata[3])
	user_id = call.from_user.id
	url = await url_name(user_id)
	data = await clan_info(user_id)
	data2 = await clan_info(uid)

	if uid2 != user_id:
		return

	if not data or not data2 or data[2] != 4 or data[1] != cid or data2[1] != data[1]:
		error = True

	try: await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	except: return

	if zap == 'false' or error:
		return

	name = await new_owner_db(uid, cid, user_id)
	await call.message.answer(f'{url}, вы успешно передали клан <b>[{name}]</b> игроку с ID: {uid}')


@antispam
async def clan_setting_type(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if not data:
		await message.answer(f'{url}, вы не состоите в клане {lose}')
		return

	d, _, _ = await clan_full_info(data[1])

	try:
		type = message.text.lower().split()[3]
	except:
		await message.answer(f'{url}, вы не указали тип клана, который хотите установить.\nДоступные типы: [закрытый, открытый] {lose}')
		return

	if data[2] != 4:
		await message.answer(f'{url}, вы не можете изменять настройки данного клана так как не являетесь создателем клана {lose}')
		return

	if type == 'закрытый':
		u = 0
	elif type == 'открытый':
		u = 1
	else:
		await message.answer(f'{url}, неизвестный тип клана. Доступные типы: [закрытый, открытый] {lose}')
		return

	await upd_settings_type_db(u, data[1])
	await message.answer(f'<b>[Внимание]</b>\n📥 Вы успешно изменили тип клана <b>[{d[2]}]</b> на {type}')


@antispam
async def clan_settings(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	url = await url_name(user_id)
	data = await clan_info(user_id)

	if not data:
		await message.answer(f'{url}, вы не состоите в клане {lose}')
		return

	d, _, _ = await clan_full_info(data[1])

	try:
		msg = message.text.lower().split()[2]
		u = int(message.text.split()[3])
	except:
		if 'msg' not in locals():
			await message.answer('<b>[Внимание]</b>\n❌ Данной настройки не существует. Проверьте название и введите ещё раз')
		else:
			await message.answer(f'{url}, вы не ввели ранг на который хотите изменить данную настройку [1-4] {lose}')
		return

	if u not in range(1, 5):
		await message.answer(f'{url}, вы не можете поставить ранг выше 4 {lose}')
		return

	if data[2] != 4:
		await message.answer(f'{url}, вы не можете изменять настройки данного клана так как не являетесь создателем клана {lose}')
		return

	mlist = {
		'приглашение': ('приглашения на вход в клан', 'inv'),
		'кик': ('на кик с клана', 'kick'),
		'ранги': ('изменения рангов в клане', 'ranks'),
		'казна': ('снятия денег с казны клана', 'kazna'),
		'ограбление': ('начала ограбление в клане', 'robbery'),
		'война': ('начала войны в клане', 'war'),
		'название': ('изменение названия клана', 'upd_name')
	}

	if msg in mlist:
		txt, st = mlist[msg]
	else:
		await message.answer(f'<b>[Внимание]</b>\n❌ Данной настройки не существует. Проверьте название и введите ещё раз')
		return

	await upd_settings(st, data[1], u)
	await message.answer(f'<b>[Внимание]</b>\n📥 Вы успешно изменили настройки {txt} <b>[{d[2]}]</b>')


def reg(dp: Dispatcher):
	dp.register_message_handler(clan_dell, lambda message: message.text.lower().startswith('клан удалить'))
	dp.register_callback_query_handler(clan_dell_call, text_startswith='clan-dell')
	dp.register_message_handler(clan_name, lambda message: message.text.lower().startswith('клан название'))
	dp.register_message_handler(clan_new_owner, lambda message: message.text.lower().startswith('клан передать'))
	dp.register_callback_query_handler(clan_new_owner_call, text_startswith='clan-new-owner')
	dp.register_message_handler(clan_setting_type, lambda message: message.text.lower().startswith('клан настройки тип'))
	dp.register_message_handler(clan_settings, lambda message: message.text.lower().startswith('клан настройки '))