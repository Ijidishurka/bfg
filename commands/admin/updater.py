import subprocess
import tempfile
import requests
import shutil
import time
import sys
import os

from aiogram.types import FSInputFile

from assets.antispam import admin_only
from assets import keyboards as kb
from utils.settings import get_setting, update_setting
from filters.custom import TextIn, StartsWith
from aiogram import types, Dispatcher
import config as cfg
from bot import bot, dp
import asyncio

if_notification = False


async def check_updates() -> None:
	update = get_setting(key="update_flag", default={})
	restart = get_setting(key="restart_flag", default={})

	if update and "time" in update and "chat_id" in update and "message_id" in update:
		ctime = time.time() - update["time"]
		txt = f"<b>🏖 Обновление загружено!</b>\n<i>Обновление заняло {ctime:.1f}сек</i>\n\n<tg-spoiler>Официальный канал разработки бота - @copybfg</tg-spoiler>"
		await bot.edit_message_text(chat_id=update["chat_id"], message_id=update["message_id"], text=txt)

	if restart and "time" in restart and "chat_id" in restart and "message_id" in restart:
		ctime = time.time() - restart["time"]
		txt = f"<b>💫 Бот перезагружен!</b>\n\n<i>Перезагрузка заняла {ctime:.1f}сек</i>"
		await bot.edit_message_text(chat_id=restart["chat_id"], message_id=restart["message_id"], text=txt)

	update_setting(key="update_flag", value={})
	update_setting(key="restart_flag", value={})


async def search_update(force: bool = False, check: bool = False) -> bool:
	global if_notification
	try:
		if not check and if_notification and not force:
			return False
		
		response = requests.get("https://raw.githubusercontent.com/Ijidishurka/bfg/refs/heads/V3/bot.py")
		response.raise_for_status()
		
		content = response.text
		last_version = content.splitlines()[0].strip().split(": ")[1]
		
		with open("bot.py", "r", encoding="utf-8") as file:
			version = file.readline().strip().split(": ")[1]
		
		last_version_int = float(last_version.replace(".", "").replace(",", "."))
		version_int = float(version.replace(".", "").replace(",", "."))

		if last_version_int <= version_int:
			if_notification = False
			return False
		
		if check:
			return True
		
		if_notification = True
		
		response = requests.get("https://raw.githubusercontent.com/Ijidishurka/bfg/refs/heads/V3/update_list.txt")
		
		txt = f"<b>🔍 Доступно обновление 🛎</b>\nЧто нового?\n\n<i>{response.text}</i>"
		
		for admin in cfg.admin:
			try:
				await bot.send_message(admin, txt, reply_markup=kb.update_bot())
			except:
				pass

		return False
				
	except Exception as e:
		print(f"Ошибка при попытке найти обновление: {e}")
		return False
		

@admin_only(private=True)
async def update_bot(message: types.Message):
	force = False
	check = await search_update(check=True)

	if not check and "-f" not in message.text:
		await message.answer(f"<b>😄 У вас установлена последняя версия бота!</b>\n Вы также можете попробовать <a href='https://github.com/Ijidishurka/bfg'>обновиться вручную</a>")
		return
	
	if not check:
		txt = "⚠️ У вас уже установлена последняя версия бота.\n<i>Нажмите на кнопку ниже, если вы хотите</i> <a href='https://github.com/Ijidishurka/bfg'>обновить файлы бота</a>"
		force = True
	else:
		response = requests.get("https://raw.githubusercontent.com/Ijidishurka/bfg/refs/heads/V3/update_list.txt")
		txt = f"<b>🔍 Доступно обновление 🛎</b>\nЧто нового?\n\n<i>{response.text}</i>"

	await message.answer(txt, reply_markup=kb.update_bot(force=force))
	
	
async def bot_update(call: types.CallbackQuery) -> None:
	global if_notification
	if call.from_user.id not in cfg.admin:
		return
	
	check = await search_update(check=True)
	force = int(call.data.split("_")[1])
	if_notification = False
	
	if not check and force == 0:
		await bot.answer_callback_query(call.id, show_alert=True, text="🤩 У вас уже установлена последняя версия.")
		return

	file = FSInputFile("users.db")
	await bot.send_document(call.message.chat.id, file, caption=f"🛡 Резервная копия базы данных")
	
	await call.message.edit_text("<i>🎩 Установка обновления...</i>")
	
	with tempfile.TemporaryDirectory() as temp_dir:
		subprocess.run(["git", "clone", "--branch", "V3", "--single-branch", "https://github.com/Ijidishurka/bfg.git", temp_dir], check=True)
		for item in os.listdir(temp_dir):
			if item in ["config_ex.py", "modules"]:
				continue

			src_path = os.path.join(temp_dir, item)
			dest_path = os.path.join(os.getcwd(), item)

			if os.path.isdir(src_path):
				shutil.rmtree(dest_path, ignore_errors=True)
				shutil.copytree(src_path, dest_path)
			else:
				shutil.copy2(src_path, dest_path)

	update_setting(key="update_flag", value={"time": time.time(), "chat_id": call.message.chat.id, "message_id": call.message.message_id})

	os.execv(sys.executable, [sys.executable] + sys.argv)


@admin_only()
async def restart_bot(message: types.Message):
	msg = await message.answer("<i>🔄 Перезагрузка бота...</i>")

	update_setting(key="restart_flag", value={"time": time.time(), "chat_id": msg.chat.id, "message_id": msg.message_id})

	await asyncio.sleep(2)
	await bot.close()
	await dp.storage.close()
	
	os.execl(sys.executable, sys.executable, *sys.argv)


def reg(dp: Dispatcher):
	dp.message.register(restart_bot, TextIn("🔄 Перезагрузка", "/restartb"))
	dp.message.register(update_bot, TextIn("/updateb", "/updateb -f"))
	dp.callback_query.register(bot_update, StartsWith("update-bot"))
