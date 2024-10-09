from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def my_modules_kb(module_keys, index, user_id, mod):
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"mymodules-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index +1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"mymodules-list_{index}_up|{user_id}")
	)
	keyboard.add(InlineKeyboardButton(text="❌ Удалить", callback_data=f"dell-modul_{mod}|{user_id}"))
	return keyboard


def load_modules_type(user_id, colvo):
	keyboard = InlineKeyboardMarkup(row_width=1)
	keyboard.add(InlineKeyboardButton(text=f"🕹 Игры ({colvo[0]})", callback_data=f"mod-catalog_games|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"👾 Ивенты ({colvo[1]})", callback_data=f"mod-catalog_events|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"✨ Разные ({colvo[2]})", callback_data=f"mod-catalog_other|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"⚙️ Системные ({colvo[3]})", callback_data=f"mod-catalog_system|{user_id}"))
	return keyboard


def load_modules_kb(module_keys, index, user_id, mod, MODULES):
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"catalogmod-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index +1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"catalogmod-list_{index}_up|{user_id}")
	)
	
	if mod in MODULES:
		keyboard.add(InlineKeyboardButton(text="✅ Загружен", callback_data="userbotik"))
	else:
		keyboard.add(InlineKeyboardButton(text="📥 Загрузить", callback_data=f"load-modul_{mod}|{user_id}"))
	return keyboard


def modules_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("🛎 Загруженые"), types.KeyboardButton("📂 Каталог"))
	keyboard.add(types.KeyboardButton("🔙 Назад"))
	return keyboard


def control_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("🔄 Перезагрузка"), types.KeyboardButton("💽 ОЗУ"))
	keyboard.add(types.KeyboardButton("🔙 Назад"))
	return keyboard


def ram_clear():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton("🗑 Очистить все", callback_data="ram-clear"))
	return keyboard


def unloading_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("💾 Бд"), types.KeyboardButton("❗️ Ошибки"), types.KeyboardButton("📋 Логи"))
	keyboard.add(types.KeyboardButton("🔙 Назад"))
	return keyboard


def admin_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("📣 Реклама"), types.KeyboardButton("🕹 Управление"))
	keyboard.add(types.KeyboardButton("✨ Промокоды"), types.KeyboardButton("📥 Выгрузка"))
	keyboard.add(types.KeyboardButton("🌟 Модули"))
	return keyboard


def ads_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("📍 Рассылка"), types.KeyboardButton("🪪 Текст рекламы"))
	keyboard.add(types.KeyboardButton("🔙 Назад"))
	return keyboard


def cancel():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("Отмена"))
	return keyboard


def update_bot():
	keyboard = types.InlineKeyboardMarkup()
	keyboard.add(types.InlineKeyboardButton("🐙 Обновить", callback_data="update-bot"))
	return keyboard


def promo_menu():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(types.KeyboardButton("📖 Создать промо"), types.KeyboardButton("🗑 Удалить промо"))
	keyboard.add(types.KeyboardButton("ℹ️ Промо инфо"))
	keyboard.add(types.KeyboardButton("🔙 Назад"))
	return keyboard