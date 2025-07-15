from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def farm(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"ferma-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"ferma-nalog|{user_id}"),
    )
    keyboard.row(InlineKeyboardButton(text="⬆️ Купить видеокарту", callback_data=f"ferma-bycards|{user_id}"))
    return keyboard.as_markup()


def generator(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"generator-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"generator-nalog|{user_id}"),
    )
    keyboard.row(InlineKeyboardButton(text="⬆️ Купить турбину", callback_data=f"generator-buy-turb|{user_id}"))
    return keyboard.as_markup()


def business(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"business-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"business-nalog|{user_id}")
    )
    keyboard.row(
        InlineKeyboardButton(text="⬆️ Увеличить территорию", callback_data=f"business-ter|{user_id}"),
        InlineKeyboardButton(text="⬆️ Увеличить бизнес", callback_data=f"business-bis|{user_id}")
    )
    return keyboard.as_markup()


def tree(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"tree-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"tree-nalog|{user_id}")
    )
    keyboard.row(
        InlineKeyboardButton(text="⬆️ Увеличить участок", callback_data=f"tree-ter|{user_id}"),
        InlineKeyboardButton(text="🆙 Увеличить дерево", callback_data=f"tree-tree|{user_id}")
    )
    return keyboard.as_markup()


def quarry(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"quarry-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"quarry-nalog|{user_id}")
    )
    keyboard.row(
        InlineKeyboardButton(text="⬆️ Купить установку", callback_data=f"quarry-bur|{user_id}"),
        InlineKeyboardButton(text="🆙 Увеличить территорию", callback_data=f"quarry-ter|{user_id}")
    )
    keyboard.row(
        InlineKeyboardButton(text="🔧 Увеличить уровень", callback_data=f"quarry-lvl|{user_id}"),
        InlineKeyboardButton(text="📦 Текущий доход", callback_data=f"quarry-dox|{user_id}")
    )
    return keyboard.as_markup()


def garden(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(text="💰 Собрать прибыль", callback_data=f"garden-sobrat|{user_id}"),
        InlineKeyboardButton(text="💸 Оплатить налоги", callback_data=f"garden-nalog|{user_id}"),
    )
    keyboard.row(
        InlineKeyboardButton(text="⬆️ Купить дерево", callback_data=f"garden-buy-tree|{user_id}"),
        InlineKeyboardButton(text="💦 Полить сад", callback_data=f"garden-polit|{user_id}"),
    )
    return keyboard.as_markup()
