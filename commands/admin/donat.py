from aiogram import types, Dispatcher

from utils.settings import get_setting, update_setting
from assets.antispam import admin_only, antispam_earning, new_earning
from commands.admin import keyboards as kb


@admin_only(private=True)
async def donat_menu_cmd(message: types.Message):
    user_id = message.from_user.id
    text = "<b>💰 Донат меню:</b>"

    if get_setting(key="stars_donat", default=False):
        text += "\n<a href='t.me/copybfg/123'>· Как вывести звёзды с бота?</a>"

    msg = await message.answer(text=text, reply_markup=kb.donat_menu(user_id=user_id))
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
        await call.message.edit_text(text=text, reply_markup=kb.donat_menu(user_id=user_id))
    except:
        pass


def reg(dp: Dispatcher):
    dp.register_message_handler(donat_menu_cmd, lambda message: message.text == "💰 Донат")
    dp.register_callback_query_handler(donat_set_cmd, lambda call: call.data.startswith("adm-donat"))
