from aiogram import Dispatcher, types
from assets.antispam import antispam
from commands.db import url_name, get_name
from commands.entertaining.db import *
from commands.main import win_luser
from bot import bot
from assets import kb


def get_ptime(dt):
	dt = datetime.fromtimestamp(dt)
	current_time = datetime.now()
	delta = current_time - dt
	days = delta.days
	hours = delta.seconds // 3600
	minutes = (delta.seconds % 3600) // 60

	def pluralize(number, one, few, many):
		if number % 10 == 1 and number % 100 != 11:
			return one
		elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
			return few
		else:
			return many

	if days > 0:
		return f"{days} {pluralize(days, 'день', 'дня', 'дней')}"
	elif hours > 0:
		return f"{hours} {pluralize(hours, 'час', 'часа', 'часов')}"
	else:
		return f"{minutes} {pluralize(minutes, 'минута', 'минуты', 'минут')}"


@antispam
async def my_wedlock(message: types.message):
	user_id = message.from_user.id
	data = await get_wedlock(user_id)
	win, lose = await win_luser()
	name = await url_name(user_id)
	if not data:
		await message.answer(f'{name}, к сожалению вы не женаты {lose}')
		return

	name1 = await get_name(data[0])
	name2 = await get_name(data[1])

	name1 = f'<a href="tg://openmessage?user_id={data[0]}">{name1}</a>'
	name2 = f'<a href="tg://openmessage?user_id={data[1]}">{name2}</a>'

	dt = datetime.fromtimestamp(data[2]).strftime('%d.%m.%y в %H:%M:%S')
	dt_delta = get_ptime(data[2])

	await message.answer(f'''Брак между {name1} и {name2}:
🗓 Зарегестрирован: {dt}
👩‍❤️‍👨 Существует: {dt_delta}''')


@antispam
async def wedlock(message: types.message):
	user_id = message.from_user.id
	win, lose = await win_luser()
	name = await url_name(user_id)

	try:
		r_id = message.reply_to_message.from_user.id
		rname = await url_name(r_id)
	except:
		await message.answer(f'{name}, вы не ответили на сообщение партнёра на котором вы хотите пожениться {lose}')
		return

	if user_id == r_id:
		await message.answer(f'{name}, к сожалению вы не можете жениться на самому себе {lose}')
		return

	res = await get_new_wedlock(user_id, r_id)

	if res == 'u_not':
		await message.answer(f'{name}, вы уже находитесь в браке {lose}')
	elif res == 'u_not':
		await message.answer(f'{name}, ваш партнёр уже находиться в браке {lose}')
	else:
		await message.answer(f'''💍 {rname}, минуту внимания!
💓 {name} сделал вам предложение руки и сердца.
😍 Принять решение можно кнопками внизу.''', reply_markup=kb.wedlock(user_id, r_id))


async def wedlock_call(call: types.CallbackQuery):
	data = call.data.split('-')[1].split('|')
	type, r_id, u_id = data[0], int(data[1]), int(data[2])
	user_id = call.from_user.id

	if type == 'false' and user_id == u_id:
		try:
			await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		except:
			pass
		return

	if user_id != r_id:
		await bot.answer_callback_query(call.id, text='⚠️ Вы не можете нажать эту кнопку.')
		return

	try: await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	except: return

	name1 = await url_name(u_id)
	name2 = await url_name(r_id)

	if type == 'true':
		res = await new_wedlock(u_id, r_id)
		if res == 'error': return
		await call.message.answer(f'💍 Вы успешно приняли предложение о браке\n'
								  f'👰👨‍⚖ С сегодняшнего дня {name1} и {name2} состоят в браке!\n'
								  f'Поздравим молодоженов 🎉')
	else:
		await call.message.answer(f'💔 {name1}, cожалеем, но {name2} отклонил ваше предложение о бракосочетании.')


@antispam
async def divorce(message: types.message):
	user_id = message.from_user.id
	data = await get_wedlock(user_id)
	win, lose = await win_luser()
	name = await url_name(user_id)
	if not data:
		await message.answer(f'{name}, к сожалению вы не женаты {lose}')
		return

	await message.answer(f'📝 Убедитесь что вы согласны разводится.\nЧтобы развестись, нажмите на кнопку ниже',
						 reply_markup=kb.divorce(user_id))


async def divorce_call(call: types.CallbackQuery):
	type = call.data.split('-')[1].split('|')[0]
	uid = int(call.data.split('|')[1])
	user_id = call.from_user.id
	win, lose = await win_luser()

	if user_id != uid:
		await bot.answer_callback_query(call.id, text='⚠️ Вы не можете нажать эту кнопку.')
		return

	name = await url_name(user_id)
	data = await get_wedlock(user_id)

	if not data:
		return

	try: await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
	except: return

	if type == 'true':
		await divorce_db(uid)
		dt_delta = get_ptime(data[2])
		name1 = await url_name(data[0])
		name2 = await url_name(data[1])
		await call.message.answer(f'💔 Брак между {name1} и {name2} расторгнут.\nОн просуществовал {dt_delta}')
	else:
		await call.message.answer(f'{name}, вы успешно отказались от развода {win}')


def reg(dp: Dispatcher):
	dp.register_message_handler(my_wedlock, lambda message: message.text.lower() == 'мой брак')
	dp.register_message_handler(wedlock, lambda message: message.text.lower() == 'свадьба')
	dp.register_callback_query_handler(wedlock_call, text_startswith='wedlock-')
	dp.register_message_handler(divorce, lambda message: message.text.lower() == 'развод')
	dp.register_callback_query_handler(divorce_call, text_startswith='divorce-')
