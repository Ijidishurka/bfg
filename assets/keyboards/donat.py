from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config as cfg
from utils.settings import get_setting


def donat_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(InlineKeyboardButton(text="🛒 Наш магазин", callback_data=f"our-store|{user_id}"))

    if get_setting(key="stars_donat", default=False):
        keyboard.row(InlineKeyboardButton(text="⭐️ Донат через звёзды", callback_data=f"donat-stars|{user_id}"))

    if get_setting(key="refund", default=False):
        keyboard.row(InlineKeyboardButton(text="⚡️ Возврат средств", callback_data=f"refund|{user_id}"))

    keyboard.row(InlineKeyboardButton(text="🍀 Донат через админа", url=f"t.me/{cfg.admin_username.replace('@', '')}"))

    return keyboard.as_markup()


def donat_back(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"donat-menu|{user_id}"))
    return keyboard.as_markup()


def donat_select_amount(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(text="100⭐️", callback_data=f"select-stars_100|{user_id}"),
        InlineKeyboardButton(text="250⭐️", callback_data=f"select-stars_250|{user_id}")
    )

    keyboard.row(
        InlineKeyboardButton(text="500⭐️", callback_data=f"select-stars_500|{user_id}"),
        InlineKeyboardButton(text="750⭐️", callback_data=f"select-stars_750|{user_id}")
    )

    keyboard.row(
        InlineKeyboardButton(text="1000⭐️", callback_data=f"select-stars_1000|{user_id}"),
        InlineKeyboardButton(text="1500⭐️", callback_data=f"select-stars_1500|{user_id}")
    )

    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"donat-menu|{user_id}"))

    return keyboard.as_markup()


def confirm_donat(user_id: int, stars: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="✅ Подтвердить", callback_data=f"buy-stars_{stars}|{user_id}"))
    keyboard.row(InlineKeyboardButton(text="🔙 Назад", callback_data=f"donat-menu|{user_id}"))
    return keyboard.as_markup()
