from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg
import random


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


def top(uid, tab):
    sh = random.randint(1, 100)
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("👑 Топ рейтинга", callback_data=f"top-rating|{uid}|{tab}"),
        InlineKeyboardButton("💰 Топ денег", callback_data=f"top-balance|{uid}|{tab}"),
    ]

    if sh > 40:
        buttons.extend([
            InlineKeyboardButton("🧰 Топ ферм", callback_data=f"top-cards|{uid}|{tab}"),
            InlineKeyboardButton("🗄 Топ бизнесов", callback_data=f"top-bsterritory|{uid}|{tab}"),
            InlineKeyboardButton("🏆 Топ опыта", callback_data=f"top-exp|{uid}|{tab}"),
            InlineKeyboardButton("💴 Топ йен", callback_data=f"top-yen|{uid}|{tab}")
        ])
    else:
        buttons.extend([
            InlineKeyboardButton("📦 Топ обычных кейсов", callback_data=f"top-case1|{uid}|{tab}"),
            InlineKeyboardButton("🏵 Топ золотых кейсов", callback_data=f"top-case2|{uid}|{tab}"),
            InlineKeyboardButton("🏺 Топ рудных кейсов", callback_data=f"top-case3|{uid}|{tab}"),
            InlineKeyboardButton("🌌 Топ материальных кейсов", callback_data=f"top-case4|{uid}|{tab}")
        ])
        
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2], buttons[3])
    keyboards.add(buttons[4], buttons[5])
    return keyboards


def wedlock(uid, r_id):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("😍 Согласиться", callback_data=f"wedlock-true|{r_id}|{uid}")
    k2 = InlineKeyboardButton("😔 Отклонить", callback_data=f"wedlock-false|{r_id}|{uid}")
    keyboards.add(k1, k2)
    return keyboards


def divorce(uid):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("😞 Развестись", callback_data=f"divorce-true|{uid}")
    k2 = InlineKeyboardButton("😊 Отменить", callback_data=f"divorce-false|{uid}")
    keyboards.add(k1, k2)
    return keyboards


def clan(uid):
    keyboards = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("🛡 О клане", callback_data=f"clan-info|{uid}"),
        InlineKeyboardButton("👥 Участники", callback_data=f"clan-users:0|{uid}"),
        InlineKeyboardButton("🛠 Настройким", callback_data=f"clan-settings|{uid}"),
    ]
    keyboards.add(buttons[0], buttons[1])
    keyboards.add(buttons[2])
    return keyboards


def new_own_clan(uid, cid, user_id):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("✅ Да, передать", callback_data=f"clan-new-owner_true|{uid}|{cid}|{user_id}")
    k2 = InlineKeyboardButton("❌ Нет, отменить", callback_data=f"clan-new-owner_false|{uid}|{cid}|{user_id}")
    keyboards.add(k1, k2)
    return keyboards


def dell_clan(uid, cid):
    keyboards = InlineKeyboardMarkup(row_width=2)
    k1 = InlineKeyboardButton("✅ Да, удалить", callback_data=f"clan-dell_true|{uid}|{cid}")
    k2 = InlineKeyboardButton("❌ Нет, оставить", callback_data=f"clan-dell_false|{uid}|{cid}")
    keyboards.add(k1, k2)
    return keyboards