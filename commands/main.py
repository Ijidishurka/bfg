from datetime import datetime
from aiogram import Dispatcher, types
from commands.db import reg_user, getban
from assets.classes import CastomEvent
from assets import kb
import random
import config as cfg


CONFIG = {
    "hello_text": f'''🤖 Добро пожаловать на борт, Кто-то! Меня зовут BFG, твой верный игровой бот.

🎮 У меня есть множество интересных команд и игр, чтобы скрасить твоё время, будь ты один или в компании друзей! (Кстати, вместе всегда веселее) 💙
🔍 Познакомиться со всеми моими возможностями ты можешь, введя команду «помощь».

<a href="{cfg.chanell}">🔈 Наш канал</a>
<a href="{cfg.chat}">💬 Наш чат</a>''',
    
    "hello_text2": f"🚀 Не уверен, с чего начать своё приключение?\nПрисоединяйся к нашему официальному чату {cfg.bot_name}: {cfg.chat}",
    
    "sticker_id": ["CAACAgQAAxkBAAEKs6JlSQUtGTtSzXGVcJGBe0PwnWkI9QACRwkAAm0NeFIe5FE9nk15XTME"]
}


async def on_start(message: types.Message):
    if len(message.text) >= 2:
        await CastomEvent.emit('start_event', {'message': message})
        
    # await reg_user(message.from_user.id)
    ban = await getban(message.from_user.id)
    
    if ban:
        dtime = datetime.fromtimestamp(ban[1]).strftime('%Y-%m-%d в %H:%M:%S')
        await message.answer(f'⛔️ Вы заблокированы в боте до <b>{dtime}</b>\nПричина: <i>{ban[2]}</i>')
        return
    
    sticker = random.choice(CONFIG['sticker_id'])
    await message.answer_sticker(sticker=sticker)
    await message.answer(CONFIG['hello_text'], disable_web_page_preview=True, reply_markup=kb.start())
    await message.answer(CONFIG['hello_text2'], disable_web_page_preview=True)


async def geturl(id, txt):
    url = f'<a href="tg://user?id={id}">{txt}</a>'
    return url


def reg(dp: Dispatcher):
    dp.register_message_handler(on_start, commands=['start'])