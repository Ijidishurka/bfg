from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg


def help_menu():
    helpKB = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💡 Основные", callback_data="help_osn"),
        InlineKeyboardButton("🎲 Игры", callback_data="help_game"),
        InlineKeyboardButton("💥 Развлекательное", callback_data="help_rz"),
        InlineKeyboardButton("🏰 Кланы", callback_data="help_clans"),
    ]
    helpKB.add(buttons[0], buttons[1])
    helpKB.add(buttons[2], buttons[3])
    return helpKB


def help_back():
    back_button = InlineKeyboardButton("Назад", callback_data="help_back")
    return InlineKeyboardMarkup().add(back_button)


startKB = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton("😄 Добавить в чат", url=f"https://t.me/{cfg.bot_username}?startgroup=true"),
    InlineKeyboardButton("👥 Общая беседа", url=f"{cfg.chat}"),
    InlineKeyboardButton("👥 Наш канал", url=f"{cfg.chanell}"),
]
startKB.add(buttons[0], buttons[1])
startKB.add(buttons[2])


help_fermaKB = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton("💰 Собрать прибыль", callback_data="ferma_sobrat"),
    InlineKeyboardButton("💸 Оплатить налоги", callback_data="ferma_nalog"),
    InlineKeyboardButton("⬆️ Купить видеокарту", callback_data="ferma_bycards"),
]
help_fermaKB.add(buttons[0], buttons[1])
help_fermaKB.add(buttons[2])


help_generatorKB = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton("💰 Собрать прибыль", callback_data="generator_sobrat"),
    InlineKeyboardButton("💸 Оплатить налоги", callback_data="generator_nalog"),
    InlineKeyboardButton("⬆️ Купить турбину", callback_data="generator_byturb"),
]
help_generatorKB.add(buttons[0], buttons[1])
help_generatorKB.add(buttons[2])


help_bsKB = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton("💰 Собрать прибыль", callback_data="business_sobrat"),
    InlineKeyboardButton("💸 Оплатить налоги", callback_data="business_nalog"),
    InlineKeyboardButton("⬆️ Увеличить территорию", callback_data="business_ter"),
    InlineKeyboardButton("⬆️ Увеличить бизнес", callback_data="business_bis"),
]
help_bsKB.add(buttons[0], buttons[1])
help_bsKB.add(buttons[2], buttons[3])


helpGarden_kb = InlineKeyboardMarkup()
buttons = [
    InlineKeyboardButton("💰 Собрать прибыль", callback_data="garden_sobrat"),
    InlineKeyboardButton("💸 Оплатить налоги", callback_data="garden_nalog"),
    InlineKeyboardButton("⬆️ Купить дерево", callback_data="garden_baytree"),
    InlineKeyboardButton("💦 Полить сад", callback_data="garden_polit"),
]
helpGarden_kb.add(buttons[0], buttons[1])
helpGarden_kb.add(buttons[2], buttons[3])