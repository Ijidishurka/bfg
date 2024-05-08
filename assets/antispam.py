from datetime import datetime, timedelta
import commands.db as db


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