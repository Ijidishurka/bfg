from aiogram.fsm.state import StatesGroup, State


class NewPromoState(StatesGroup):
    name = State()
    summ = State()
    activ = State()
    txt = State()


class DellPromoState(StatesGroup):
    name = State()


class PromoInfoState(StatesGroup):
    name = State()


class NewAdvState(StatesGroup):
    txt = State()


class MailingState(StatesGroup):
    mailing_text = State()
    mailing_conf = State()
