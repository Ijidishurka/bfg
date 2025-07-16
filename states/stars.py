from aiogram.fsm.state import StatesGroup, State


class InvoiceState(StatesGroup):
    user_id = State()
    chat_id = State()
    message_id = State()
    amount = State()
