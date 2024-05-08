from commands.db import reg_user, getname
from commands.assets.kb import startKB
import random
import config as cfg
from assets.antispam import antispam


async def on_start(message):
    await reg_user(message.from_user.id)
    sticker_id = 'CAACAgQAAxkBAAEKs6JlSQUtGTtSzXGVcJGBe0PwnWkI9QACRwkAAm0NeFIe5FE9nk15XTME'
    await message.answer_sticker(sticker=sticker_id)

    await message.answer(f'''🤖 Добро пожаловать на борт, Кто-то! Меня зовут BFG, твой верный игровой бот.

🎮 У меня есть множество интересных команд и игр, чтобы скрасить твоё время, будь ты один или в компании друзей! (Кстати, вместе всегда веселее) 💙
🔍 Познакомиться со всеми моими возможностями ты можешь, введя команду «помощь».

<a href="{cfg.chanell}">🔈 Наш канал</a>
<a href="{cfg.chat}">💬 Наш чат</a>''', parse_mode='html', disable_web_page_preview=True, reply_markup=startKB)

    await message.answer(f'''🚀 Не уверен, с чего начать своё приключение?
Присоединяйся к нашему официальному чату {cfg.bot_name}: {cfg.chat}''', parse_mode='html', disable_web_page_preview=True)


async def chat_list(message):
    await message.answer(f'''💭 Официальная беседа бота:
{cfg.chat}
💭 Официальный канал разработки:
{cfg.chanell}
🏆 Официальный чат с розыгрышами:
...''', parse_mode='html', disable_web_page_preview=True)


@antispam
async def myname_cmd(message):
    name = await getname(message)
    await message.answer(f'🗂 Ваш ник - «{name}»')


async def win_luser():
    win = ['🙂', '😋', '😄', '🤑', '😃', '😇']
    loser = ['😔', '😕', '😣', '😞', '😢']
    rwin = random.choice(win)
    rloser = random.choice(loser)
    return rwin, rloser


async def geturl(id, txt):
    url = f'<a href="tg://user?id={id}">{txt}</a>'
    return url
