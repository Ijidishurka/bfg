from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config as cfg


def help_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💡 Основные", callback_data=f"help_osn|{user_id}"),
        InlineKeyboardButton(text="🎲 Игры", callback_data=f"help_game|{user_id}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="💥 Развлекательное", callback_data=f"help_rz|{user_id}"),
        InlineKeyboardButton(text="🏰 Кланы", callback_data=f"help_clans|{user_id}"),
    )
    return keyboard.as_markup()


def help_back(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data=f"help_back|{user_id}"))
    return keyboard.as_markup()


def start() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="😄 Добавить в чат", url=f"t.me/{cfg.bot_username}?startgroup=true"),
        InlineKeyboardButton(text="👥 Общая беседа", url=cfg.chat),
    )
    keyboard.row(InlineKeyboardButton(text="👥 Наш канал", url=cfg.channel))
    return keyboard.as_markup()


def profile(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="🏠 Имущество", callback_data=f"profil-property|{user_id}"))
    keyboard.row(InlineKeyboardButton(text="🏭 Бизнесы", callback_data=f"profil-busines|{user_id}"))
    return keyboard.as_markup()


def profile_back(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"profil-back|{user_id}"))
    return keyboard.as_markup()


def top(user_id: int, tab: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="👑 Топ рейтинга", callback_data=f"top-rating|{user_id}|{tab}"),
        InlineKeyboardButton(text="💰 Топ денег", callback_data=f"top-balance|{user_id}|{tab}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🧰 Топ ферм", callback_data=f"top-cards|{user_id}|{tab}"),
        InlineKeyboardButton(text="🗄 Топ бизнесов", callback_data=f"top-bsterritory|{user_id}|{tab}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🏆 Топ опыта", callback_data=f"top-exp|{user_id}|{tab}"),
        InlineKeyboardButton(text="💴 Топ йен", callback_data=f"top-yen|{user_id}|{tab}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="📦 Топ обычных кейсов", callback_data=f"top-case1|{user_id}|{tab}"),
        InlineKeyboardButton(text="🏵 Топ золотых кейсов", callback_data=f"top-case2|{user_id}|{tab}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🏺 Топ рудных кейсов", callback_data=f"top-case3|{user_id}|{tab}"),
        InlineKeyboardButton(text="🌌 Топ материальных кейсов", callback_data=f"top-case4|{user_id}|{tab}")
    )
    return keyboard.as_markup()



def wedlock(user_id: int, r_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="😍 Согласиться", callback_data=f"wedlock-true|{r_id}|{user_id}"),
        InlineKeyboardButton(text="😔 Отклонить", callback_data=f"wedlock-false|{r_id}|{user_id}")
    )
    return keyboard.as_markup()


def divorce(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="😞 Развестись", callback_data=f"divorce-true|{user_id}"),
        InlineKeyboardButton(text="😊 Отменить", callback_data=f"divorce-false|{user_id}")
    )
    return keyboard.as_markup()
