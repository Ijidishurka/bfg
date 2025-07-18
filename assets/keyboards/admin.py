from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from utils.settings import get_setting


def admin_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="💰 Донат"))
	keyboard.row(KeyboardButton(text="📣 Реклама"), KeyboardButton(text="🔄 Перезагрузка"))
	keyboard.row(KeyboardButton(text="✨ Промокоды"), KeyboardButton(text="📥 Выгрузка"))
	keyboard.row(KeyboardButton(text="🌟 Модули"), KeyboardButton(text="🔙 Закрыть меню"))
	return keyboard.as_markup(resize_keyboard=True)


def my_modules_kb(module_keys: list, index: int, user_id: int, mod: str) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardBuilder()
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"mymodules-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"mymodules-list_{index}_up|{user_id}")
	)
	keyboard.row(InlineKeyboardButton(text="❌ Удалить", callback_data=f"dell-modul_{mod}|{user_id}"))
	return keyboard.as_markup()


def load_modules_type(user_id: int, amount: tuple) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardBuilder()
	keyboard.row(InlineKeyboardButton(text=f"🕹 Игры ({amount[0]})", callback_data=f"mod-catalog_games|{user_id}"))
	keyboard.row(InlineKeyboardButton(text=f"👾 Ивенты ({amount[1]})", callback_data=f"mod-catalog_events|{user_id}"))
	keyboard.row(InlineKeyboardButton(text=f"✨ Разные ({amount[2]})", callback_data=f"mod-catalog_other|{user_id}"))
	keyboard.row(InlineKeyboardButton(text=f"⚙️ Системные ({amount[3]})", callback_data=f"mod-catalog_system|{user_id}"))
	return keyboard.as_markup()


def load_modules_kb(module_keys: list, index: int, user_id: int, mod: str, modules: dict) -> InlineKeyboardMarkup:
	keyboard = InlineKeyboardBuilder()
	keyboard.row(
		InlineKeyboardButton(text="‹", callback_data=f"catalogmod-list_{index}_down|{user_id}"),
		InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
		InlineKeyboardButton(text="›", callback_data=f"catalogmod-list_{index}_up|{user_id}")
	)

	if mod in modules:
		keyboard.row(InlineKeyboardButton(text="✅ Загружен", callback_data="userbotik"))
	else:
		keyboard.row(InlineKeyboardButton(text="📥 Загрузить", callback_data=f"load-modul_{mod}|{user_id}"))

	return keyboard.as_markup()


def modules_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="🛎 Загруженые"), KeyboardButton(text="📂 Каталог"))
	keyboard.row(KeyboardButton(text="🔙 Назад"))
	return keyboard.as_markup(resize_keyboard=True)


def unloading_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="💾 Бд"), KeyboardButton(text="❗️ Ошибки"), KeyboardButton(text="📋 Логи"))
	keyboard.row(KeyboardButton(text="🔙 Назад"))
	return keyboard.as_markup(resize_keyboard=True)


def ads_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="📍 Рассылка"), KeyboardButton(text="🪪 Текст рекламы"))
	keyboard.row(KeyboardButton(text="🔙 Назад"))
	return keyboard.as_markup(resize_keyboard=True)


def cancel() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="Отмена"))
	return keyboard.as_markup(resize_keyboard=True)


def update_bot(force: bool = False) -> InlineKeyboardMarkup:
	force = 1 if force else 0
	keyboard = InlineKeyboardBuilder()
	keyboard.row(InlineKeyboardButton(text="🐙 Обновить", callback_data=f"update-bot_{force}"))
	return keyboard.as_markup()


def promo_menu() -> ReplyKeyboardMarkup:
	keyboard = ReplyKeyboardBuilder()
	keyboard.row(KeyboardButton(text="📖 Создать промо"), KeyboardButton(text="🗑 Удалить промо"))
	keyboard.row(KeyboardButton(text="ℹ️ Промо инфо"))
	keyboard.row(KeyboardButton(text="🔙 Назад"))
	return keyboard.as_markup(resize_keyboard=True)


def admin_donat_menu(user_id: int) -> InlineKeyboardMarkup:
	keyboards = InlineKeyboardBuilder()

	donat_emj= "✅" if get_setting(key="stars_donat", default=False) else "❌"
	donat_action = "false" if get_setting(key="stars_donat", default=False) else "true"

	refund_emj = "✅" if get_setting(key="refund", default=False) else "❌"
	refund_action = "false" if get_setting(key="refund", default=False) else "true"

	keyboards.row(InlineKeyboardButton(text=f"{donat_emj} Донат через звёзды", callback_data=f"adm-donat_1_{donat_action}|{user_id}"))
	keyboards.row(InlineKeyboardButton(text=f"{refund_emj} Возврат средств", callback_data=f"adm-donat_2_{refund_action}|{user_id}"))

	return keyboards.as_markup()