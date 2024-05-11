from datetime import datetime, timedelta
import commands.db as db


earning_msg = {(-1295495, 76): (9, 243267656)}


def antispam(func):
    async def wrapper(message):
        if message.forward_from:
            return

        if message.chat.type == 'supergroup':
            await db.upd_chat_db(message.chat.id)

        uid = message.from_user.id
        await db.reg_user(uid)

        btime = await db.getban(uid)
        if btime:
            if datetime.now().timestamp() < btime:
                return

        await func(message)

    return wrapper


def antispam_earning(func):
    async def wrapper(call):
        uid = call.from_user.id
        await db.reg_user(uid)

        btime = await db.getban(uid)
        if btime:
            if datetime.now().timestamp() < btime:
                return

        chat = call.message.chat.id
        msg = call.message.message_id

        data = earning_msg.get((chat, msg))
        if not data:
            return

        if data[0] >= 15:
            return

        dt = int(datetime.now().timestamp())
        if int(dt - 500) > int(data[1]):
            return

        earning_msg[chat, msg] = (data[0] + 1, data[1])
        await func(call)

    return wrapper


async def new_earning_msg(chat, id):
    dt = int(datetime.now().timestamp())
    earning_msg[chat, id] = (0, dt)