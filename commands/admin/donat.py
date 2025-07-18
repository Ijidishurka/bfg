from aiogram import types, Dispatcher

from filters.custom import TextIn, StartsWith
from utils.settings import get_setting, update_setting
from assets.antispam import admin_only, antispam_earning, new_earning
from assets import keyboards as kb


@admin_only(private=True)
async def donat_menu_cmd(message: types.Message):
    user_id = message.from_user.id
    text = "<b>💰 Донат меню:</b>"

    if get_setting(key="stars_donat", default=False):
        text += "\n<a href='t.me/copybfg/123'>· Как вывести звёзды с бота?</a>"

    msg = await message.answer(text=text, reply_markup=kb.admin_donat_menu(user_id=user_id))
    await new_earning(msg)


@antispam_earning
async def donat_set_cmd(call: types.CallbackQuery):
    user_id = call.from_user.id

    key = int(call.data.split("_")[1])
    key = "stars_donat" if key == 1 else "refund"

    value = call.data.split("_")[2].split("|")[0]
    value = True if value == "true" else False

    update_setting(key=key, value=value)

    text = "<b>💰 Донат меню:</b>"

    if get_setting(key="stars_donat", default=False):
        text += "\n<a href='t.me/copybfg/124'>· Как вывести звёзды с бота?</a>"

    try:
        await call.message.edit_text(text=text, reply_markup=kb.admin_donat_menu(user_id=user_id))
    except:
        pass


def reg(dp: Dispatcher):
    dp.message.register(donat_menu_cmd, TextIn("💰 Донат"))
    dp.callback_query.register(donat_set_cmd, StartsWith("adm-donat"))
