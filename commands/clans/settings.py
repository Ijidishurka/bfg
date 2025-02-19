import re

from aiogram import Dispatcher, types

from assets.antispam import antispam, antispam_earning, new_earning
from user import BFGuser, BFGconst
from commands.clans import db
from assets import kb


@antispam
async def clan_dell(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	if user.clan.rank != 4:
		await message.answer(f'{user.url}, вы не можете удалить данный клан так как не являетесь создателем клана {lose}')
		return

	msg = await message.answer(f'''<b>[Внимание]</b>
😔 Вы действительно хотите удалить клан <b>[{user.clan.name}]</b>
✅ Для подтверждения нажмите кнопку ниже''', reply_markup=kb.dell_clan(user.id, user.clan.id))
	await new_earning(msg)


@antispam_earning
async def clan_dell_call(call: types.CallbackQuery, user: BFGuser):
	zap = call.data.split('|')[0].split('_')[1]
	cid = int(call.data.split('|')[1])
	win, lose = BFGconst.emj()

	if not user.clan or user.clan.rank != 4 or user.clan.id != cid:
		zap = 'false'

	try:
		await call.message.delete()
	except:
		return

	if zap == 'false':
		return

	await db.clan_dell_db(user.clan.id)
	await call.message.answer(f'{user.url}, вы успешно удалили клан <b>[{user.clan.name}]</b> {win}')


@antispam
async def clan_name(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	try:
		name = " ".join(message.text.split()[2:])
	except:
		await message.answer(f'{user.url}, вы не ввели название клана на которое хотите поменять {lose}')
		return
	
	if user.clan.rank < user.clan.settings['upd_name']:
		await message.answer(f'{user.url}, ваш ранг слишком мал, для того чтобы изменить название клана {lose}')
		return

	if len(name) < 5:
		await message.answer(f'{user.url}, название клана не может быть меньше чем 5 символов {lose}')
		return

	if len(name) > 25:
		await message.answer(f'{user.url}, название клана не может быть длинее чем 25 символов {lose}')
		return

	if re.search(r'<|>|@|t\.me|http', name):
		await message.answer(f'{user.url}, название вашего клана содержит запрещённые символы {lose}')
		return

	await message.answer(f'<b>[Внимание]</b>\n✏️ Вы успешно изменили название клана на <b>[{name}]</b>')
	await db.new_name_clan_db(name, user.clan.id)


@antispam
async def clan_new_owner(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	try:
		uid = int(message.text.split()[2])
	except:
		await message.answer(f'{user.url}, вы не указали ID игрока которому хотите передать клан {lose}')
		return

	if user.clan.rank != 4:
		await message.answer(f'{user.url}, к сожалению Вы не можете передать клан так как не являетесь его основателем {lose}')
		return

	if user.id == uid:
		await message.answer(f'{user.url}, вы не можете передать клан самому себе {lose}')
		return

	r_data = await db.clan_info(user.id)

	if r_data and r_data[1] == user.clan.id:
		msg = await message.answer(f'''<b>⚠️ ВАЖНОЕ УВЕДОМЛЕНИЕ ⚠️</b>
<b>Передача клана "{user.clan.name}"</b>
🔴 <b>Внимание:</b> Это действие является окончательным и <u>не может быть отменено</u> после подтверждения.
❗ Пожалуйста, убедитесь в своем решении перед подтверждением.
✅ Если вы полностью уверены в своем решении и готовы передать клан, нажмите кнопку ниже для подтверждения.''',
							 reply_markup=kb.new_own_clan(uid, user.clan.id, user.id))
		await new_earning(msg)
	else:
		await message.answer(f'{user.url}, данный игрок не находиться в вашем клане, вы не можете передать ему клан {lose}')


@antispam_earning
async def clan_new_owner_call(call: types.CallbackQuery, user: BFGuser):
	zap = call.data.split('|')[0].split('_')[1]
	cdata = call.data.split('|')
	rid, cid = int(cdata[1]), int(cdata[2])
	data = await db.clan_info(rid)

	if not user.clan or not data or user.clan.rank != 4 or user.clan.id != cid or data[1] != user.clan.id:
		zap = 'false'

	try:
		await call.message.delete()
	except:
		return

	if zap == 'false':
		return

	await db.new_owner_db(user.id, cid, rid)
	await call.message.answer(f'{user.url}, вы успешно передали клан <b>[{user.clan.name}]</b> игроку с ID: {rid}')


@antispam
async def clan_setting_type(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	try:
		action = message.text.lower().split()[3]
	except:
		await message.answer(f'{user.url}, вы не указали тип клана, который хотите установить.\nДоступные типы: [закрытый, открытый] {lose}')
		return

	if user.clan.rank != 4:
		await message.answer(f'{user.url}, вы не можете изменять настройки данного клана так как не являетесь создателем клана {lose}')
		return

	if action == 'закрытый':
		clan_type = 0
	elif action == 'открытый':
		clan_type = 1
	else:
		await message.answer(f'{user.url}, неизвестный тип клана. Доступные типы: [закрытый, открытый] {lose}')
		return

	await db.upd_settings_type_db(clan_type, user.clan.id)
	await message.answer(f'<b>[Внимание]</b>\n📥 Вы успешно изменили тип клана <b>[{user.clan.name}]</b> на {action}')


@antispam
async def clan_settings(message: types.message, user: BFGuser):
	win, lose = BFGconst.emj()

	if not user.clan:
		await message.answer(f'{user.url}, вы не состоите в клане {lose}')
		return

	try:
		msg = message.text.lower().split()[2]
		u = int(message.text.split()[3])
	except:
		if 'msg' not in locals():
			await message.answer('<b>[Внимание]</b>\n❌ Данной настройки не существует. Проверьте название и введите ещё раз')
		else:
			await message.answer(f'{user.url}, вы не ввели ранг на который хотите изменить данную настройку [1-4] {lose}')
		return

	if u not in range(1, 5):
		await message.answer(f'{user.url}, вы не можете поставить ранг выше 4 {lose}')
		return

	if user.clan.rank != 4:
		await message.answer(f'{user.url}, вы не можете изменять настройки данного клана так как не являетесь создателем клана {lose}')
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

	await db.upd_settings(st, user.clan.id, u)
	await message.answer(f'<b>[Внимание]</b>\n📥 Вы успешно изменили настройки {txt} <b>[{user.clan.name}]</b>')


def reg(dp: Dispatcher):
	dp.register_message_handler(clan_dell, lambda message: message.text.lower().startswith('клан удалить'))
	dp.register_callback_query_handler(clan_dell_call, text_startswith='clan-dell')
	dp.register_message_handler(clan_name, lambda message: message.text.lower().startswith('клан название'))
	dp.register_message_handler(clan_new_owner, lambda message: message.text.lower().startswith('клан передать'))
	dp.register_callback_query_handler(clan_new_owner_call, text_startswith='clan-new-owner')
	dp.register_message_handler(clan_setting_type, lambda message: message.text.lower().startswith('клан настройки тип'))
	dp.register_message_handler(clan_settings, lambda message: message.text.lower().startswith('клан настройки '))
