from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def clan(user_id: int) -> InlineKeyboardMarkup:
    user_id = int(user_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🛡 О клане", callback_data=f"clan-info|{user_id}"),
        InlineKeyboardButton(text="👥 Участники", callback_data=f"clan-users|{user_id}")
    )
    keyboard.row(InlineKeyboardButton(text="🛠 Настройким", callback_data=f"clan-settings|{user_id}"))
    return keyboard.as_markup()


def new_own_clan(user_id: int, cid: int, user_id_2: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="✅ Да, передать", callback_data=f"clan-new-owner_true|{user_id_2}|{cid}|{user_id}"),
        InlineKeyboardButton(text="❌ Нет, отменить", callback_data=f"clan-new-owner_false|{user_id_2}|{cid}|{user_id}")
    )
    return keyboard.as_markup()


def dell_clan(user_id: int, cid: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"clan-dell_true|{cid}|{user_id}"),
        InlineKeyboardButton(text="❌ Нет, оставить", callback_data=f"clan-dell_false|{cid}|{user_id}")
    )
    return keyboard.as_markup()

