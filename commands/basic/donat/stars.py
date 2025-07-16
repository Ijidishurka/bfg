import time

from aiogram import Dispatcher, types, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery

from assets.antispam import new_earning, antispam_earning, antispam
from filters.custom import StartsWith
from assets import keyboards as kb
from commands.basic.donat import db
from states.stars import InvoiceState
from user import BFGuser
from utils.settings import get_setting
from bot import bot


@antispam
async def help_cmd(message: types.Message):
    await message.answer(text="‼️ <b>Все пожертвования добровольны и не подлежат возврату!</b>")


@antispam_earning
async def donat_cmd(call: types.CallbackQuery, state: FSMContext):
    if not get_setting(key="stars_donat", default=False):
        return

    user_id = call.from_user.id

    text = (
        "⭐ Выберите сумму для доната через Telegram Stars или введите свою.\n\n"
        "Ответьте на это сообщение целым числом (например: 500)."
    )

    await call.message.edit_text(text=text, reply_markup=kb.donat_select_amount(user_id=user_id))
    await state.update_data(
        user_id=user_id,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    await state.set_state(InvoiceState.amount)


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


@antispam
async def check_amount_cmd(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    message_id = message.reply_to_message.message_id

    if not message.reply_to_message or not message.reply_to_message.text.startswith("⭐ Выберите сумму для"):
        return

    data = await state.get_data()

    if data["user_id"] != user_id or data["chat_id"] != chat_id or data["message_id"] != message_id:
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

    await state.clear()

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
    if not get_setting(key="stars_donat", default=False):
        return

    amount = int(call.data.split("_")[1].split("|")[0])

    await call.message.delete()

    await call.message.answer_invoice(
        title="📗 Покупка B-Coins",
        description=f"{amount} B-Coins через Telegram Stars",
        prices=[LabeledPrice(label="XTR", amount=amount)],
        provider_token="",
        payload=f"{amount}_stars",
        currency="XTR"
    )


async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    if get_setting(key="stars_donat", default=False):
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False)


async def on_successful_payment(message: types.Message):
    user_id = message.from_user.id
    amount = message.successful_payment.total_amount

    text = f"💰 <b>Успешное пополнение!</b>\n\nНа ваш баланс зачислено <b>{amount} B-coins</b>"
    message_effect_id = "5104841245755180586" if message.chat.type == "private" else None

    await message.answer(text=text, message_effect_id=message_effect_id)

    await db.new_pay(
        user_id=user_id,
        amount=amount,
        transaction_id=message.successful_payment.telegram_payment_charge_id
    )


@antispam_earning
async def refund_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id
    page = int(call.data.split("_")[1].split("|")[0])

    if not get_setting(key="refund", default=False) or page <= 0:
        await call.answer(text="")
        return

    transactions = await db.get_transactions_to_refund(user_id=user_id)

    if not transactions:
        await call.answer(text="❌ У вас нет недавних транзакций.", show_alert=True)
        return

    max_page = (len(transactions) + 4) // 5 if transactions else 1

    if max_page < page:
        await call.answer(text="")
        return

    text = (
        "⭐ Выберите транзакцию для возврата:\n"
        "<i>Возврат возможен в течение 24 часов после покупки, при наличии B-coins на балансе.</i>"
    )

    await call.message.edit_text(text=text, reply_markup=kb.donat_select_refund(user_id=user_id, transactions=transactions, page=page))


@antispam_earning
async def start_refund_cmd(call: types.CallbackQuery, user: BFGuser):
    user_id = call.from_user.id
    donat_id = int(call.data.split("_")[1].split("|")[0])

    if not get_setting(key="refund", default=False):
        return

    transaction = await db.get_transaction(donat_id=donat_id)

    if not transaction or transaction[1] != user_id or transaction[5] == 1:
        return

    if transaction[4] < int(time.time() - 84600):
        await call.answer(text="⌛️ Время, отведённое на возврат, уже истекло.", show_alert=True)
        return

    if user.bcoins.get() < transaction[2]:
        await call.answer(text="❌ На вашем балансе недостаточно B-coins!", show_alert=True)
        return

    try:
        await bot.refund_star_payment(
            user_id=call.from_user.id,
            telegram_payment_charge_id=transaction[3]
        )
        await call.message.edit_text(text=f"✅ Звёзды за покупку возвращены на ваш баланс. Списано <b>{transaction[2]} B-coins</b>.")
        await db.new_refund(user_id=user_id, amount=transaction[2], donat_id=transaction[0])
    except TelegramBadRequest as error:
        if "CHARGE_ALREADY_REFUNDED" in error.message:
            text = "❌ Эта транзакция уже отменена."
        else:
            text = "❌ Транзакция не найдена."

        await call.message.edit_text(text=text)


def reg(dp: Dispatcher):
    dp.message.register(help_cmd, Command("paysupport"))

    dp.callback_query.register(donat_cmd, StartsWith("donat-stars"))

    dp.callback_query.register(check_keyboard_amount_cmd, StartsWith("select-stars"))
    dp.message.register(check_amount_cmd, InvoiceState.amount)

    dp.callback_query.register(buy_stars_cmd, StartsWith("buy-stars"))
    dp.pre_checkout_query.register(on_pre_checkout_query)
    dp.message.register(on_successful_payment, F.successful_payment)

    dp.callback_query.register(refund_cmd, StartsWith("refund"))
    dp.callback_query.register(start_refund_cmd, StartsWith("start-refund"))
