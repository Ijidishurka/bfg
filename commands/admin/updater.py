import subprocess

from assets.antispam import admin_only
from commands.admin import keyboards as kb
from aiogram import types, Dispatcher
import config as cfg
from bot import bot, dp
import requests
import sys
import os

from assets.antispam import earning_msg
from assets.gettime import bonus_time, kazna_time
from commands.help import help_msg

if_notification = False


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
	
	await call.message.edit_text('<i>🎩 Установка обновления...</i>')
	
	subprocess.run(["git", "pull", "origin", "main"], check=True)
	os.execv(sys.executable, [sys.executable] + sys.argv)


@admin_only(private=True)
async def control(message: types.Message):
	await message.answer('<b>🕹️ Меню управления:</b>', reply_markup=kb.control_menu())


@admin_only()
async def restart_bot(message: types.Message):
	await message.answer("🔄 Бот перезагружен!")
	
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