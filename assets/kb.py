from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg
import random


def help_menu(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💡 Основные", callback_data=f"help_osn|{user_id}"),
        InlineKeyboardButton("🎲 Игры", callback_data=f"help_game|{user_id}"),
        InlineKeyboardButton("💥 Развлекательное", callback_data=f"help_rz|{user_id}"),
        InlineKeyboardButton("🏰 Кланы", callback_data=f"help_clans|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def help_back(user_id):
    back_button = InlineKeyboardButton("Назад", callback_data=f"help_back|{user_id}")
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


def ferma(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"ferma-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"ferma-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Купить видеокарту", callback_data=f"ferma-bycards|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def generator(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"generator-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"generator-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Купить турбину", callback_data=f"generator-buy-turb|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def business(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"business-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"business-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Увеличить территорию", callback_data=f"business-ter|{user_id}"),
        InlineKeyboardButton("⬆️ Увеличить бизнес", callback_data=f"business-bis|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def tree(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"tree-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"tree-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Увеличить участок", callback_data=f"tree-ter|{user_id}"),
        InlineKeyboardButton("🆙 Увеличить дерево", callback_data=f"tree-tree|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def quarry(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"quarry-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"quarry-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Купить установку", callback_data=f"quarry-bur|{user_id}"),
        InlineKeyboardButton("🆙 Увеличить территорию", callback_data=f"quarry-ter|{user_id}"),
        InlineKeyboardButton("🔧 Увеличить уровень", callback_data=f"quarry-lvl|{user_id}"),
        InlineKeyboardButton("📦 Текущий доход", callback_data=f"quarry-dox|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def garden(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("💰 Собрать прибыль", callback_data=f"garden-sobrat|{user_id}"),
        InlineKeyboardButton("💸 Оплатить налоги", callback_data=f"garden-nalog|{user_id}"),
        InlineKeyboardButton("⬆️ Купить дерево", callback_data=f"garden-buy-tree|{user_id}"),
        InlineKeyboardButton("💦 Полить сад", callback_data=f"garden-polit|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    return keyboards


def profil(user_id):
    keyboards = InlineKeyboardMarkup(row_width=1)
    keyboards.add(InlineKeyboardButton("🏠 Имущество", callback_data=f"profil-property|{user_id}"))
    keyboards.add(InlineKeyboardButton("🏭 Бизнесы", callback_data=f"profil-busines|{user_id}"))
    return keyboards


def profil_back(user_id):
    keyboards = InlineKeyboardMarkup()
    keyboards.add(InlineKeyboardButton("⬅️ Назад", callback_data=f"profil-back|{user_id}"))
    return keyboards


def top(user_id, tab):
    sh = random.randint(1, 100)
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("👑 Топ рейтинга", callback_data=f"top-rating|{user_id}|{tab}"),
        InlineKeyboardButton("💰 Топ денег", callback_data=f"top-balance|{user_id}|{tab}"),
        InlineKeyboardButton("🧰 Топ ферм", callback_data=f"top-cards|{user_id}|{tab}"),
        InlineKeyboardButton("🗄 Топ бизнесов", callback_data=f"top-bsterritory|{user_id}|{tab}"),
        InlineKeyboardButton("🏆 Топ опыта", callback_data=f"top-exp|{user_id}|{tab}"),
        InlineKeyboardButton("💴 Топ йен", callback_data=f"top-yen|{user_id}|{tab}"),
        InlineKeyboardButton("📦 Топ обычных кейсов", callback_data=f"top-case1|{user_id}|{tab}"),
        InlineKeyboardButton("🏵 Топ золотых кейсов", callback_data=f"top-case2|{user_id}|{tab}"),
        InlineKeyboardButton("🏺 Топ рудных кейсов", callback_data=f"top-case3|{user_id}|{tab}"),
        InlineKeyboardButton("🌌 Топ материальных кейсов", callback_data=f"top-case4|{user_id}|{tab}")
    ]
        
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    keyboards.add(buttons[4], buttons[5])
    if sh >= 50:
        keyboards.add(buttons[6], buttons[7])
    else:
        keyboards.add(buttons[8], buttons[9])
    return keyboards


def wedlock(user_id, r_id):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("😍 Согласиться", callback_data=f"wedlock-true|{r_id}|{user_id}")
    k2 = InlineKeyboardButton("😔 Отклонить", callback_data=f"wedlock-false|{r_id}|{user_id}")
    keyboards.add(k1, k2)
    return keyboards


def divorce(user_id):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("😞 Развестись", callback_data=f"divorce-true|{user_id}")
    k2 = InlineKeyboardButton("😊 Отменить", callback_data=f"divorce-false|{user_id}")
    keyboards.add(k1, k2)
    return keyboards


def clan(user_id):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("🛡 О клане", callback_data=f"clan-info|{user_id}"),
        InlineKeyboardButton("👥 Участники", callback_data=f"clan-users:0|{user_id}"),
        InlineKeyboardButton("🛠 Настройким", callback_data=f"clan-settings|{user_id}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def new_own_clan(user_id, cid, user_id_2):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("✅ Да, передать", callback_data=f"clan-new-owner_true|{user_id}|{cid}|{user_id_2}")
    k2 = InlineKeyboardButton("❌ Нет, отменить", callback_data=f"clan-new-owner_false|{user_id}|{cid}|{user_id_2}")
    keyboards.add(k1, k2)
    return keyboards


def dell_clan(user_id, cid):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("✅ Да, удалить", callback_data=f"clan-dell_true|{user_id}|{cid}")
    k2 = InlineKeyboardButton("❌ Нет, оставить", callback_data=f"clan-dell_false|{user_id}|{cid}")
    keyboards.add(k1, k2)
    return keyboards