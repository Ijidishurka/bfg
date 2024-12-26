from aiogram import types
from functools import wraps
import time

from aiogram.types import ChatMemberOwner, ChatMemberAdministrator

import config as cfg
import commands.db as db
from bot import bot

from user import BFGuser


earning_msg = {}


def admin_only(private=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            if message.from_user.id not in cfg.admin:
                return
            
            if private and message.chat.type != "private":
                return
            
            return await func(message, *args, **kwargs)
        return wrapper
    return decorator


def antispam(func):
    async def wrapper(message: types.Message):
        if message.forward_from:
            return

        if message.chat.type == 'supergroup':
            await db.upd_chat_db(message.chat.id)

        uid = message.from_user.id

        ban = await ban_chek(uid)  # проверка бана
        if ban:
            return

        user = BFGuser(message=message)
        await user.update()

        await func(message, user)

    return wrapper


def antispam_earning(func):
    async def wrapper(call: types.CallbackQuery):
        uid = int(call.from_user.id)
        mid = call.data.split('|')
        mid = mid[1] if len(mid) > 1 else None

        if mid and uid != int(mid):
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

                if int(time.time() - 750) < int(data[1]):

                    if (time.time() - data[1]) < 1:  # антиспам (1сек)
                        await bot.answer_callback_query(call.id, text='⏳ Не так быстро! (1 сек)')
                        return

                    earning_msg[chat, msg] = (data[0] + 1, int(time.time()))

                    user = BFGuser(call=call)
                    await user.update()
                    
                    await func(call, user)
                    return

        try:
            await bot.delete_message(chat_id=chat, message_id=msg)
        except:
            pass
        earning_msg.pop((chat, msg), None)

    return wrapper


def moderation(func):
    async def wrapper(message: types.Message, user: BFGuser):
        if message.forward_from:
            return

        if message.chat.type != 'supergroup':
            await message.answer('👇 <b>Эту команду можно использовать только в чатах.</b>')
            return

        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)

        if member.status not in ['creator', 'administrator']:
            await message.reply(f'😨 <b>Эту команду могут использовать только администраторы чата.</b>')
            return

        bot = await message.chat.get_member(user_id=message.bot.id)
        text = ''

        if not isinstance(bot, (ChatMemberOwner, ChatMemberAdministrator)):
            await message.reply('⚠️ <b>Боту необходимы права администратора в чате.</b>')
            return

        if not bot.can_delete_messages:
            text += '- 🗑️ Удаление сообщений\n'
        if not bot.can_restrict_members:
            text += '- 📛 Блокировка пользователей\n'
            
        if text:
            await message.reply(f'⚠️ <b>Боту необходимы права администратора в чате:</b>\n\n{text}')
            return

        await func(message, user)

    return wrapper


async def ban_chek(uid: int) -> bool:
    await db.reg_user(uid)
    btime = await db.getban(uid)
    if btime:
        if time.time() < btime[1]:
            return True


async def new_earning_msg(chat_id: int, message_id: int) -> None:
    earning_msg[chat_id, message_id] = (0, time.time()-2)
    
    
async def new_earning(msg: types.Message) -> None:
    earning_msg[msg.chat.id, msg.message_id] = (0, time.time()-2)