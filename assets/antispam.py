import config as cfg
from datetime import datetime
from functools import wraps
import commands.db as db
from bot import bot


earning_msg = {(-1295495, 76): (9, 243267656)}


def admin_only(private=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(message, *args, **kwargs):
            if message.from_user.id not in cfg.admin:
                return
            
            if private and message.chat.type != "private":
                return
            
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator


def antispam(func):
    async def wrapper(message):
        if message.forward_from:
            return

        if message.chat.type == 'supergroup':
            await db.upd_chat_db(message.chat.id)

        uid = message.from_user.id

        ban = await ban_chek(uid)  # проверка бана
        if ban:
            return

        await func(message)

    return wrapper


def antispam_earning(func):
    async def wrapper(call):
        uid = int(call.from_user.id)
        mid = int(call.data.split('|')[1])

        if uid != mid:
            await bot.answer_callback_query(call.id, text='❌ Это не Ваша кнопка!')
            return

        ban = await ban_chek(uid)  # проверка бана
        if ban:
            return

        chat = call.message.chat.id
        msg = call.message.message_id

        data = earning_msg.get((chat, msg))
        if data:
            if data[0] < 50:  # макс кол-во нажатий на кнопку

                dt = int(datetime.now().timestamp())
                if int(dt - 750) < int(data[1]):

                    if (int(dt) - int(data[1])) < 1:  # антиспам (1сек)
                        await bot.answer_callback_query(call.id, text='⏳ Не так быстро! (1 сек)')
                        return

                    earning_msg[chat, msg] = (data[0] + 1, dt)
                    await func(call)
                    return

        try: await bot.delete_message(chat_id=chat, message_id=msg)
        except: pass
        earning_msg.pop((chat, msg), None)

    return wrapper


async def ban_chek(uid):
    await db.reg_user(uid)
    btime = await db.getban(uid)
    if btime:
        if datetime.now().timestamp() < btime[1]:
            return True


async def new_earning_msg(chat, id):
    dt = int(datetime.now().timestamp())
    earning_msg[chat, id] = (0, dt-2)