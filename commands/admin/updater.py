import time, json, sys, os, shutil, requests, subprocess, tempfile
from assets.antispam import admin_only
from commands.admin import keyboards as kb
from aiogram import types, Dispatcher
import config as cfg
from bot import bot, dp
import asyncio

from assets.antispam import earning_msg
from assets.gettime import bonus_time, kazna_time
from commands.help import help_msg

if_notification = False


async def check_updates():
	if os.path.exists('updates.json'):
		with open('updates.json', 'r') as json_file:
			data = json.load(json_file)
			
		os.remove('updates.json')
		ctime = time.time() - data['time']
		
		if data['type'] == 'update':
			txt = f'<b>🏖 Обновление загружено!</b>\n<i>Обновление заняло {ctime:.1f}сек</i>\n\n<tg-spoiler>Официальный канал разработки бота - @copybfg</tg-spoiler>'
		else:
			txt = f'<b>💫 Бот перезагружен!</b>\n\n<i>Перезагрузка заняла {ctime:.1f}сек</i>'
		
		await bot.edit_message_text(chat_id=data['message'][0], message_id=data['message'][1], text=txt)
	

async def search_update(force=False, check=False):
	global if_notification
	try:
		if not check and if_notification and not force:
			return
		
		response = requests.get("https://raw.githubusercontent.com/Ijidishurka/bfg/refs/heads/main/bot.py")
		response.raise_for_status()
		
		content = response.text
		last_version = content.splitlines()[0].strip().split(": ")[1]
		
		with open('bot.py', 'r', encoding='utf-8') as file:
			version = file.readline().strip().split(": ")[1]
		
		last_version_int = int(last_version.replace('.', ''))
		version_int = int(version.replace('.', ''))

		if last_version_int <= version_int:
			return False
		
		if_notification = True
		
		if check:
			return True
		
		response = requests.get("https://raw.githubusercontent.com/Ijidishurka/bfg/refs/heads/main/update_list.txt")
		
		txt = f'<b>🔍 Доступно обновление 🛎</b>\nЧто нового?\n\n<i>{response.text}</i>'
		
		for admin in cfg.admin:
			try: await bot.send_message(admin, txt, reply_markup=kb.update_bot())
			except: pass
				
	except Exception as e:
		print(f"Ошибка при попытке найти обновление: {e}")
		

async def bot_update(call: types.CallbackQuery):
	if call.from_user.id not in cfg.admin:
		return
	
	check = await search_update(check=True)
	
	if not check:
		await bot.answer_callback_query(call.id, show_alert=True, text='🤩 У вас уже установлена последняя версия.')
		return
	
	with open('users.db', 'rb') as file:
		await bot.send_document(call.message.chat.id, file, caption=f'🛡 Резервная копия базы данных')
	
	await call.message.edit_text('<i>🎩 Установка обновления...</i>')
	
	with tempfile.TemporaryDirectory() as temp_dir:
		subprocess.run(['git', 'clone', 'https://github.com/Ijidishurka/bfg.git', temp_dir], check=True)
		
		for item in os.listdir(temp_dir):
			if item in ['config_ex.py', 'modules']:
				continue
				
			src_path = os.path.join(temp_dir, item)
			dest_path = os.path.join(os.getcwd(), item)
			
			if os.path.isdir(src_path):
				shutil.rmtree(dest_path, ignore_errors=True)
				shutil.copytree(src_path, dest_path)
			else:
				shutil.copy2(src_path, dest_path)
		
	with open('updates.json', 'w') as json_file:
		data = {"type": "update", "message": (call.message.chat.id, call.message.message_id), "time": time.time()}
		json.dump(data, json_file, indent=4)
					
	os.execv(sys.executable, [sys.executable] + sys.argv)


@admin_only(private=True)
async def control(message: types.Message):
	await message.answer('<b>🕹️ Меню управления:</b>', reply_markup=kb.control_menu())


@admin_only()
async def restart_bot(message: types.Message):
	msg = await message.answer("<i>🔄 Перезагрузка бота...</i>")
	
	with open('updates.json', 'w') as json_file:
		data = {"type": "restart", "message": (msg.chat.id, msg.message_id), "time": time.time()}
		json.dump(data, json_file, indent=4)
	
	await asyncio.sleep(2)
	await bot.close()
	await dp.storage.close()
	
	os.execl(sys.executable, sys.executable, *sys.argv)


def sizeof_fmt(num):
	for unit in ['Б', 'КБ', 'МБ']:
		if abs(num) < 1024.0:
			return "%3.1f %s" % (num, unit)
		num /= 1024.0
	return "%.1f %s" % (num, 'ТБ')


@admin_only(private=True)
async def RAM_control(message: types.Message):
	earning = sizeof_fmt(sys.getsizeof(earning_msg))
	help_menu = sizeof_fmt(sys.getsizeof(help_msg))
	bonus = sizeof_fmt(sys.getsizeof(bonus_time))
	kazna = sizeof_fmt(sys.getsizeof(kazna_time))
	
	await message.answer(f'''💽 Информация о использовании ОЗУ:
💸 Заработок: {earning}
🆘 Помощь: {help_menu}
🎁 Бонусы: {bonus}
💰 Казна: {kazna}''', reply_markup=kb.ram_clear())


async def RAM_clear(call: types.CallbackQuery):
	global earning_msg, help_msg, bonus_time, kazna_time
	earning_msg.clear()
	help_msg.clear()
	bonus_time.clear()
	kazna_time.clear()
	
	await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🗑 Очищено!')


def reg(dp: Dispatcher):
	dp.register_message_handler(control, lambda message: message.text == '🕹 Управление')
	dp.register_message_handler(restart_bot, lambda message: message.text in ['🔄 Перезагрузка', '/brestart'])
	dp.register_message_handler(RAM_control, lambda message: message.text == '💽 ОЗУ')
	dp.register_callback_query_handler(RAM_clear, text='ram-clear')
	dp.register_callback_query_handler(bot_update, text='update-bot')