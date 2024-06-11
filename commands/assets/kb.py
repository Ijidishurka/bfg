from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg


def help_menu():
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💡 Основные", callback_data="help_osn"),
        InlineKeyboardButton("🎲 Игры", callback_data="help_game"),
        InlineKeyboardButton("💥 Развлекательное", callback_data="help_rz"),
        InlineKeyboardButton("🏰 Кланы", callback_data="help_clans"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def help_back():
    back_button = InlineKeyboardButton("Назад", callback_data="help_back")
    return InlineKeyboardMarkup().add(back_button)


def start():
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("😄 Добавить в чат", url=f"https://t.me/{cfg.bot_username}?startgroup=true"),
        InlineKeyboardButton("👥 Общая беседа", url=f"https://{cfg.chat}"),
        InlineKeyboardButton("👥 Наш канал", url=f"https://{cfg.chanell}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def ferma(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"ferma-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"ferma-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Купить видеокарту", callback_data=f"ferma-bycards|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def generator(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"generator-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"generator-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Купить турбину", callback_data=f"generator-buy-turb|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def business(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"business-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"business-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Увеличить территорию", callback_data=f"business-ter|{uid}"),
        InlineKeyboardButton("⬆️ Увеличить бизнес", callback_data=f"business-bis|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def tree(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"tree-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"tree-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Увеличить участок", callback_data=f"tree-ter|{uid}"),
        InlineKeyboardButton("🆙 Увеличить дерево", callback_data=f"tree-tree|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def quarry(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"quarry-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"quarry-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Купить установку", callback_data=f"quarry-bur|{uid}"),
        InlineKeyboardButton("🆙 Увеличить территорию", callback_data=f"quarry-ter|{uid}"),
        InlineKeyboardButton("🔧 Увеличить уровень", callback_data=f"quarry-lvl|{uid}"),
        InlineKeyboardButton("📦 Текущий доход", callback_data=f"quarry-dox|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def garden(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"garden-sobrat|{uid}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"garden-nalog|{uid}"),
        InlineKeyboardButton("⬆️ Купить дерево", callback_data=f"garden-buy-tree|{uid}"),
        InlineKeyboardButton("💦 Полить сад", callback_data=f"garden-polit|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def profil(uid):
    keyboards = InlineKeyboardMarkup(row_width=1)
    keyboards.add(InlineKeyboardButton("🏠 Имущество", callback_data=f"profil-property|{uid}"))
    keyboards.add(InlineKeyboardButton("🏭 Бизнесы", callback_data=f"profil-busines|{uid}"))

    return keyboards


def profil_back(uid):
    keyboards = InlineKeyboardMarkup()
    keyboards.add(InlineKeyboardButton("⬅️ Назад", callback_data=f"profil-back|{uid}"))
    return keyboards
