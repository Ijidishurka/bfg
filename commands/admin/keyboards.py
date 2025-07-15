from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from utils.settings import get_setting


def admin_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("💰 Донат"))
	keyboard.add(KeyboardButton("📣 Реклама"), KeyboardButton("🔄 Перезагрузка"))
	keyboard.add(KeyboardButton("✨ Промокоды"), KeyboardButton("📥 Выгрузка"))
	keyboard.add(KeyboardButton("🌟 Модули"), KeyboardButton("🔙 Закрыть меню"))
	return keyboard


def my_modules_kb(module_keys: list, index: int, user_id: int, mod: str) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"mymodules-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"mymodules-list_{index}_up|{user_id}")
	)
	keyboard.add(InlineKeyboardButton(text="❌ Удалить", callback_data=f"dell-modul_{mod}|{user_id}"))
	return keyboard


def load_modules_type(user_id: int, amount: tuple) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup(row_width=1)
	keyboard.add(InlineKeyboardButton(text=f"🕹 Игры ({amount[0]})", callback_data=f"mod-catalog_games|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"👾 Ивенты ({amount[1]})", callback_data=f"mod-catalog_events|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"✨ Разные ({amount[2]})", callback_data=f"mod-catalog_other|{user_id}"))
	keyboard.add(InlineKeyboardButton(text=f"⚙️ Системные ({amount[3]})", callback_data=f"mod-catalog_system|{user_id}"))
	return keyboard


def load_modules_kb(module_keys: list, index: int, user_id: int, mod: str, MODULES: dict) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardMarkup(row_width=3)
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"catalogmod-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"catalogmod-list_{index}_up|{user_id}")
	)

	if mod in MODULES:
		keyboard.add(InlineKeyboardButton(text="✅ Загружен", callback_data="userbotik"))
	else:
		keyboard.add(InlineKeyboardButton(text="📥 Загрузить", callback_data=f"load-modul_{mod}|{user_id}"))
	return keyboard


def modules_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("🛎 Загруженые"), KeyboardButton("📂 Каталог"))
	keyboard.add(KeyboardButton("🔙 Назад"))
	return keyboard


def unloading_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("💾 Бд"), KeyboardButton("❗️ Ошибки"), KeyboardButton("📋 Логи"))
	keyboard.add(KeyboardButton("🔙 Назад"))
	return keyboard


def ads_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("📍 Рассылка"), KeyboardButton("🪪 Текст рекламы"))
	keyboard.add(KeyboardButton("🔙 Назад"))
	return keyboard


def cancel() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("Отмена"))
	return keyboard


def update_bot(force: bool = False) -> InlineKeyboardMarkup:
	force = 1 if force else 0
	keyboard = InlineKeyboardMarkup()
	keyboard.add(InlineKeyboardButton("🐙 Обновить", callback_data=f"update-bot_{force}"))
	return keyboard


def promo_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(KeyboardButton("📖 Создать промо"), KeyboardButton("🗑 Удалить промо"))
	keyboard.add(KeyboardButton("ℹ️ Промо инфо"))
	keyboard.add(KeyboardButton("🔙 Назад"))
	return keyboard


def donat_menu(user_id: int) -> InlineKeyboardMarkup:
	keyboards = InlineKeyboardMarkup()

	donat_emj= "✅" if get_setting(key="stars_donat", default=False) else "❌"
	donat_action = "false" if get_setting(key="stars_donat", default=False) else "true"

	refund_emj = "✅" if get_setting(key="refund", default=False) else "❌"
	refund_action = "false" if get_setting(key="refund", default=False) else "true"

	keyboards.add(InlineKeyboardButton(text=f"{donat_emj} Донат через звёзды", callback_data=f"adm-donat_1_{donat_action}|{user_id}"))
	keyboards.add(InlineKeyboardButton(text=f"{refund_emj} Возврат средств", callback_data=f"adm-donat_2_{refund_action}|{user_id}"))

	return keyboards