import asyncio
import re
from datetime import datetime
from aiogram import types, Dispatcher
import time
from assets.antispam import admin_only
from commands.admin import keyboards as kb
from commands.admin import db
from bot import bot


@admin_only()
async def sql(message: types.Message):
    res = await db.zap_sql(message.text[message.text.find(' '):])
    bot_msg = await message.answer(f'🕘 Выполнение запроса...')
    if not res:
        await bot_msg.edit_text(f"🚀 SQL Запрос выполнен.")
    else:
        await bot_msg.edit_text(f"❌ Возникла ошибка при изменении\n⚠️ Ошибка: {res}")
        
        
@admin_only()
async def ban(message: types.Message):
    try:
        user_id, time_str, *reason = message.get_args().split()
        time_s = sum(int(value) * {'д': 86400, 'ч': 3600, 'м': 60}[unit] for value, unit in re.findall(r'(\d+)([дчм])', time_str))
        time_s = int(time.time()) + time_s
        reason = ' '.join(reason) if reason else 'Не указана'
    except:
        await message.reply("Используйте: /banb [игровой id] [время] [причина]")
        return
    
    await db.new_ban(user_id, time_s, reason)
    await message.answer(f'📛 Пользователь {user_id} заблокирован на {time_str}\nПричина: <i>{reason}</i>')


@admin_only()
async def unban(message: types.Message):
    try:
        user_id = int(message.text.split()[1])
    except:
        await message.reply("Используйте: /unbanb [игровой id]")
        return
    
    await db.unban_user(user_id)
    await message.answer(f'🛡 Пользователь {user_id} разблокирован.')


def reg(dp: Dispatcher):
    dp.register_message_handler(sql, lambda message: message.text.lower().startswith('/sql'))
    dp.register_message_handler(ban, lambda message: message.text.lower().startswith('/banb'))
    dp.register_message_handler(unban, lambda message: message.text.lower().startswith('/unbanb'))