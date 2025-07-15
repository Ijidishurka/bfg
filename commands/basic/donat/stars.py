from aiogram import Dispatcher, types
from aiogram.filters import Command

from assets.antispam import new_earning, antispam_earning, antispam
from filters.custom import StartsWith
from assets import keyboards as kb
from utils.settings import get_setting
from user import BFGuser
from bot import bot

buy_stars_messages = set()  # {(user_id, chat_id, message_id)}


@antispam
async def help_cmd(message: types.Message):
    await message.answer(text="‼️ <b>Все пожертвования добровольны и не подлежат возврату!</b>")


@antispam_earning
async def donat_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id

    text = (
        "⭐ Выберите сумму для доната через Telegram Stars или введите свою.\n\n"
        "Ответьте на это сообщение целым числом (например: 500)."
    )

    msg = await call.message.edit_text(text=text, reply_markup=kb.donat_select_amount(user_id=user_id))
    buy_stars_messages.add((user_id, msg.chat.id, msg.message_id))


@antispam_earning
async def check_keyboard_amount_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id
    stars = int(call.data.split("_")[1].split("|")[0])

    text = (
        f"💰 Вы хотите задонатить <b>{stars}⭐</b> через Telegram Stars?\n"
        f"📍 Вы получите <b>{stars} B-Coins</b>.\n\n"
        "✅ Подтвердите действие кнопкой ниже."
    )

    await call.message.edit_text(text=text, reply_markup=kb.confirm_donat(user_id=user_id, stars=stars))


async def check_amount_cmd(message: types.Message, user: BFGuser, event_type: str):
    if event_type != "message":
        return

    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id

    if not message.reply_to_message or not message.reply_to_message.text.startswith("⭐ Выберите сумму для"):
        return

    if not get_setting(key="stars_donat", default=False) or not (user_id, chat_id, message_id) in buy_stars_messages:
        return

    try:
        stars = int(message.text)
    except:
        await message.answer("❌ Введите корректное целое число.")
        return

    if stars <= 0:
        await message.answer("❌ Введите корректное целое число.")
        return

    if stars > 25_000:
        await message.answer("❌ За раз можно купить не более 25000 B-Coins.")
        return

    buy_stars_messages.discard((user_id, chat_id, message_id))

    text = (
        f"💰 Вы хотите задонатить <b>{stars}⭐</b> через Telegram Stars?\n"
        f"📍 Вы получите <b>{stars} B-Coins</b>.\n\n"
        "✅ Подтвердите действие кнопкой ниже."
    )

    await bot.delete_message(chat_id=chat_id, message_id=message_id)
    await message.delete()

    msg = await message.answer(text=text, reply_markup=kb.confirm_donat(user_id=user_id, stars=stars))
    await new_earning(msg=msg)


@antispam_earning
async def buy_stars_cmd(call: types.CallbackQuery):
    await call.answer(text="Покупка за звёзды не поддерживается в этой версии бота!", show_alert=True)


def reg(dp: Dispatcher):
    dp.message.register(help_cmd, Command("paysupport"))
    dp.callback_query.register(donat_cmd, StartsWith("donat-stars"))
    dp.callback_query.register(check_keyboard_amount_cmd, StartsWith("select-stars"))
    dp.callback_query.register(buy_stars_cmd, StartsWith("buy-stars"))
