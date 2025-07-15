from aiogram import types, Dispatcher
from aiogram.filters import Command

from assets.antispam import antispam, admin_only, antispam_earning, new_earning_msg
from filters.custom import TextIn, StartsWith
from user import BFGuser
from assets import keyboards as kb
import config as cfg


adm_us = cfg.admin_username.replace('@', '')
adm = f'<a href="t.me/{adm_us}">{cfg.admin_username}</a>'

help_msg = {}


CONFIG = {
    "help_cmd": '''{}, выберите категорию:
   1️⃣ Основное
   2️⃣ Игры
   3️⃣ Развлекательное
   4️⃣ Кланы

💬 Так же у нас есть общая беседа №1 и общая беседа №2
🆘 По всем вопросам - ''' + adm,
    
    
    "help_osn": '''{}, основные команды:
   💡 Разное:
   📒 Профиль
   💫 Мой лимит
   👑 Рейтинг
   👑 Продать рейтинг
   ⚡ Энергия
   ⛏ Шахта
   🚗 Машины
   📱 Телефоны
   ✈ Самолёты
   🛥 Яхты
   🚁 Вертолёты
   🏠 Дома
   💸 Б/Баланс
   📦 Инвентарь
   📊 Курс руды
   🏢 Ограбить мэрию
   💰 Банк [положить/снять] [сумма/всё]
   💵 Депозит [положить/снять] [сумма/всё]
   🤝 Дать [сумма]
   🌐 Биткоин курс/купить/продать [кол-во]
   ⚱ Биткоины
   💈 Ежедневный бонус
   💷 Казна
   💢 Сменить ник [новый ник]
   👨 Мой ник - узнать ник
   ⚖ РП Команды - узнать РП команды
   🏆 Мой статус
   🔱 Статусы️
   💭 !Беседа - беседа бота''',
    
    
    "help_game": '''{}, игровые команды:
   🚀 Игры:
   🎮 Спин [ставка]
   🎲 Кубик [число] [ставка]
   🏀 Баскетбол [ставка]
   🎯 Дартс [ставка]
   ⚽️ Футбол [ставка]
   🎳️ Боулинг [ставка]
   📉 Трейд [вверх/вниз] [ставка]
   🎰 Казино [ставка]''',
    
    
    'help_rz': '''{}, развлекательные команды:
   🔮 Шар [фраза]
   💬 Выбери [фраза] или [фраза2]
   📊 Инфа [фраза]

💒 Браки:
   💖 Свадьба [ID пользователя]
   💖 Развод
   💌 Мой брак

📦 Кейсы:
   🛒 Купить кейс [номер] [количество]
   🔐 Открыть кейс [номер] [количество]

🗄 Бизнес:
   💰 Мой бизнес/бизнес
   💸 Продать бизнес

🏭Генератор
   🏭 Мой генератор/генератор
   💷 Продать генератор

🧰 Майнинг ферма:
   🔋 Моя ферма/ферма
   💰 Продать ферму

⚠️ Карьер:
   🏗 Мой карьер/карьер
   💰 Продать карьер
   
🏡 Денежное дерево:
   🌳 Моё дерево
   💰 Продать участок

🌳 Сады:
   🪧 Мой сад/сад
   💰 Продать сад
   💦 Сад полить
   🍸 Зелья
   🔮 Создать зелье [номер]''',
    
    
    'help_clans': '''{}, клановые команды:
🗂 Общие команды:
   💡 Мой клан - общая информация
   🏆 Клан топ - общий рейтинг кланов(Недоступно)
   ✅ Клан пригласить [ID] - пригласить игрока в клан
   🙋‍♂ Клан вступить [ID клана] - вступить в клан
   📛 Клан исключить [ID] - исключает игрока
   🚷 Клан выйти - выйти из клана
   💰 Клан казна - состояние казны
   💵 Клан казна [сумма] - снять деньги с казны

⚙ Создание и настройка кланов:
   ⚙ Клан создать [название] - стоимость 250.000.000.000$
   ⤴ Клан настройки - информация о настройках
   📥 Клан настройки приглашениие [1-4]
   💢 Клан настройки кик [1-4]
   🔰 Клан настройки ранги [1-4]
   💵 Клан настройки казна [1-4]
   💰 Клан настройки ограбление [1-4]
   ⚔ Клан настройки война [1-4]
   ✏ Клан настройки название [1-4]
   🔐 Клан настройки тип [закрытый/открытый]

🔎 Управление кланом:
   ✏ Клан название [название] - изменить название клана
   ⤴ Клан повысить [ID] - повысить игрока
   ⤵ Клан понизить [ID] - понизить игрока
   📛 Клан удалить - удалить клан

🛡 Клановые захваты:
   👮‍♀ Клан ограбление (недоступно) - ограбление казны штата

📜 Будьте осторожнее с командами повышения и понижения, повысив игрока до определенного статуса он сможет изменять название клана и управлять им.''',
    
    'help_adm': '''{}, админ команды:
   🔄 /restartb
   ⬆️ /updateb
   ⚠️ /loadmodb [raw ссылка]
   🚀 /sql [запрос]
   📛 /banb [id] [время] [причина]
   ✅ /unbanb [id]
   🎩 Выдать [сумма]
   🐙 Забрать [сумма]
   😶 Обнулить [сумма]''',

}


@antispam
async def help_cmd(message: types.Message, user: BFGuser):
    msg = await message.answer(CONFIG['help_cmd'].format(user.url), reply_markup=kb.help_menu(user.user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


@admin_only(private=False)
async def help_adm(message: types.Message):
    await message.answer(CONFIG['help_adm'].format('Admin'))
    

@antispam
async def help_game_msg(message: types.Message, user: BFGuser):
    await message.answer(CONFIG['help_game'].format(user.url))


@antispam_earning
async def help_back(call: types.CallbackQuery, user: BFGuser):
    await call.message.edit_text(text=CONFIG['help_cmd'].format(user.url), reply_markup=kb.help_menu(user.user_id))


@antispam_earning
async def help_callback(call: types.CallbackQuery, user: BFGuser):
    data = call.data.split('_')[1].split('|')[0]
    
    txt = {
        'osn': CONFIG['help_osn'],
        'game': CONFIG['help_game'],
        'rz': CONFIG['help_rz'],
        'clans': CONFIG['help_clans'],
    }.get(data)
    
    await call.message.edit_text(text=txt.format(user.url), reply_markup=kb.help_back(user.user_id))


def reg(dp: Dispatcher):
    dp.message.register(help_adm, Command("help_adm"))
    dp.message.register(help_cmd, TextIn("/help", "помощь"))
    dp.message.register(help_game_msg, TextIn("игры"))
    dp.callback_query.register(help_back, StartsWith("help_back"))
    dp.callback_query.register(help_callback, StartsWith("help_"))
