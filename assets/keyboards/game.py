from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def miracles_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🎲 Случайное (всё)", callback_data=f"miracles-start_random|{user_id}"),
        InlineKeyboardButton(text="👤 Человек", callback_data=f"miracles-start_people|{user_id}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🏠 Быт", callback_data=f"miracles-start_life|{user_id}"),
        InlineKeyboardButton(text="🌏 Мир", callback_data=f"miracles-start_world|{user_id}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="🎮 Развлечения", callback_data=f"miracles-start_attractions|{user_id}"),
        InlineKeyboardButton(text="🧪 Наука", callback_data=f"miracles-start_science|{user_id}"),
    )
    return keyboard.as_markup()


def miracles_start() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="🔁 Сменить категорию", callback_data=f"miracles-change-category"),
        InlineKeyboardButton(text="🛑 Завершить игру", callback_data=f"miracles-stop"),
    )
    return keyboard.as_markup()

