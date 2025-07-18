import json
import random
import time

from aiogram import types, Dispatcher
from aiogram.enums import ChatMemberStatus

from filters.custom import TextIn, StartsWith
from bot import bot
from assets.antispam import antispam, antispam_earning, new_earning
from assets import keyboards as kb
from user import BFGuser

game_category = {
    "random": "случайное",
    "people": "человек",
    "life": "быт",
    "world": "мир",
    "attractions": "развлечения",
    "science": "наука"
}

games_list = {}  # chat_id: {"category": category, "word": word, "correct_letters": set(), "incorrect_letters": set(), "last_update": int(time.time())}


def load_words(filepath: str) -> dict:
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except:
        return {}


def get_random_word(category: str) -> str:
    if category == "random":
        all_words = []
        for words in words_dict.values():
            all_words.extend(words)
        return random.choice(all_words)
    else:
        words = words_dict.get(category)
        if not words:
            return "юзерботик"
        return random.choice(words)


words_dict = load_words("commands/games/words.json")


@antispam
async def start_game_cmd(message: types.Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.chat.type not in ["supergroup", "group"]:
        await message.answer(text="❌ Игра доступна только в группах.")
        return

    if chat_id in games_list:
        await message.answer(text="⏳ В этом чате уже идёт игра!")
        return

    text = (
        "🎲 <b>Поле чудес</b>\n\n"
        "Выберите категорию, из которой будут загадываться слова.\n\n"
        "Угадывайте буквы или всё слово сразу и становитесь лидером!"
    )

    msg = await message.answer(text=text, reply_markup=kb.miracles_menu(user_id=user_id))
    await new_earning(msg)


@antispam_earning
async def new_game_cmd(call: types.CallbackQuery):
    chat_id = call.message.chat.id
    category = call.data.split("_")[1].split("|")[0]

    if chat_id in games_list:
        await call.answer(text="⏳ В этом чате уже идёт игра!", show_alert=True)
        return

    word = get_random_word(category=category)
    cipher = ''.join('*' if ch != ' ' else ' ' for ch in word)

    text = (
        "🎯 <b>Игра в слова запущена!</b>\n"
        f"📚 Категория: <b>{game_category[category]}</b>\n\n"
        f"Слово: <code>{cipher}</code>\n\n"
        "🔤 Отправьте букву так: <code>буква б</code>\n"
        "📖 Или попробуйте угадать всё слово так: <code>слово мост</code>"
    )

    games_list[chat_id] = {
        "category": category,
        "word": word,
        "correct_letters": set(),
        "incorrect_letters": set(),
        "last_update": int(time.time())
    }

    await call.message.delete()
    msg = await call.message.answer(text=text, reply_markup=kb.miracles_start())
    await new_earning(msg)


@antispam_earning
async def stop_game_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    member = await bot.get_chat_member(chat_id, user_id)

    if not member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        await call.answer(text="❌ Вы не администратор чата!", show_alert=True)
        return

    if chat_id not in games_list:
        await call.answer(text="❌ В этом чате нет активной игры.", show_alert=True)
        return

    game = games_list[chat_id]
    games_list.pop(chat_id)

    text = (
        "🛑 Игра досрочно завершена.\n\n"
        f"📦 Загаданное слово было: <b>{game['word']}</b>"
    )

    await call.message.delete()
    await call.message.answer(text=text)


@antispam_earning
async def change_game_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id
    chat_id = call.message.chat.id

    member = await bot.get_chat_member(chat_id, user_id)

    if not member.status in [ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR]:
        await call.answer(text="❌ Вы не администратор чата!", show_alert=True)
        return

    if chat_id not in games_list:
        await call.answer(text="❌ В этом чате нет активной игры.", show_alert=True)
        return

    game = games_list[chat_id]
    games_list.pop(chat_id)

    text = (
        "🔁 Игра завершена для выбора новой категории.\n"
        "Выберите категорию, из которой будут загадываться слова.\n\n"
        f"📦 Загаданное слово было: <b>{game['word']}</b>\n\n"
        "Выберите новую категорию:"
    )

    await call.message.edit_text(text=text, reply_markup=kb.miracles_menu(user_id=user_id))


@antispam
async def enter_letter_cmd(message: types.Message, user: BFGuser):
    message_id = message.message_id
    chat_id = message.chat.id

    if chat_id not in games_list:
        return

    try:
        letter = message.text.split()[1].upper()
    except:
        return

    if len(letter) != 1 or letter not in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯІЇ":
        return

    game = games_list[chat_id]

    if letter in game["incorrect_letters"] or letter in game["correct_letters"]:
        reaction = [{"type": "emoji", "emoji": "👎️"}]
        await bot.set_message_reaction(chat_id=chat_id, message_id=message_id, reaction=reaction)
        return

    if letter in game["word"].upper():
        game["correct_letters"].add(letter)
        cipher = ''.join(ch if ch.upper() in game["correct_letters"] or ch == ' ' else '*' for ch in game["word"])
        text = f"✅ <b>{user.name}</b> угадал букву \"{letter}\"!\n\nСлово: <code>{cipher}</code>"
    else:
        game["incorrect_letters"].add(letter)
        cipher = ''.join(ch if ch.upper() in game["correct_letters"] or ch == ' ' else '*' for ch in game["word"])
        text = f"❌ <b>{user.name}</b> буквы \"{letter}\" нет в слове!\n\nСлово: <code>{cipher}</code>"

    if not {ch.upper() for ch in game["word"] if ch != ' '}.issubset(game["correct_letters"]):
        game["last_update"] = int(time.time())
        await message.answer(text=text)
        return

    word = get_random_word(category=game['category'])
    cipher = ''.join('*' if ch != ' ' else ' ' for ch in word)

    games_list[chat_id] = {
        "category": game['category'],
        "word": word,
        "correct_letters": set(),
        "incorrect_letters": set(),
        "last_update": int(time.time())
    }

    win_text = (
        f"<b>{user.name}</b> открыл последнюю букву!\n"
        f"🗣 Слово было: <b>{game['word']}</b>\n"
        f"➡️ Новое слово: <code>{cipher}</code>\n\n"
        "🔤 Отправьте букву так: <code>буква б</code>\n"
        "📖 Или попробуйте угадать всё слово так: <code>слово мост</code>"
    )

    await message.answer(text=win_text, reply_markup=kb.miracles_start())


@antispam
async def enter_word_cmd(message: types.Message, user: BFGuser):
    chat_id = message.chat.id

    if chat_id not in games_list:
        return

    try:
        word = "".join(message.text.split()[1:]).lower()
    except:
        return

    game = games_list[chat_id]

    if word != game["word"]:
        game["last_update"] = int(time.time())
        cipher = ''.join(ch if ch.upper() in game["correct_letters"] or ch == ' ' else '*' for ch in game["word"])
        await message.answer(text=f"❌ <b>{user.name}</b> не угадал слово.\n\nСлово: <code>{cipher}</code>")
        return

    word = get_random_word(category=game['category'])
    cipher = ''.join('*' if ch != ' ' else ' ' for ch in word)

    games_list[chat_id] = {
        "category": game['category'],
        "word": word,
        "correct_letters": set(),
        "incorrect_letters": set(),
        "last_update": int(time.time())
    }

    win_text = (
        f"<b>{user.name}</b> отгадал слово!\n"
        f"🗣 Слово было: <b>{game['word']}</b>\n"
        f"➡️ Новое слово: <code>{cipher}</code>\n\n"
        "🔤 Отправьте букву так: <code>буква б</code>\n"
        "📖 Или попробуйте угадать всё слово так: <code>слово мост</code>"
    )

    await message.answer(text=win_text, reply_markup=kb.miracles_start())


async def auto_stop() -> None:
    now = int(time.time())
    expired_chats = [chat_id for chat_id, game in games_list.items() if now - game["last_update"] > 600]

    for chat_id in expired_chats:
        del games_list[chat_id]


def reg(dp: Dispatcher):
    dp.message.register(start_game_cmd, TextIn("поле чудес"))
    dp.callback_query.register(new_game_cmd, StartsWith("miracles-start"))
    dp.callback_query.register(stop_game_cmd, StartsWith("miracles-stop"))
    dp.callback_query.register(change_game_cmd, StartsWith("miracles-change-category"))
    dp.message.register(enter_letter_cmd, StartsWith("буква "))
    dp.message.register(enter_word_cmd, StartsWith("слово "))
