from aiogram import types, Dispatcher
from assets.antispam import antispam
from commands.db import get_name
from assets import kb
import config as cfg
from bot import bot
from datetime import datetime

adm_us = cfg.admin_username.replace('@', '')
adm = f'<a href="t.me/{adm_us}">{cfg.admin_username}</a>'

help_msg = {}


def antispam_help(func):
    async def wrapper(call: types.CallbackQuery):
        chat_id = call.message.chat.id
        msg_id = call.message.message_id

        data = help_msg.get(chat_id, 'no')
        dt = int(datetime.now().timestamp())

        if data != 'no':
            if int(data[0]) == int(msg_id):
                if int(dt - 120) < int(data[1]):
                    if (int(dt) - int(data[1])) > 2:
                        help_msg[chat_id] = (msg_id, dt)
                        await func(call)
                    else:
                        await bot.answer_callback_query(call.id, text='⏳ Не так быстро! (2 сек)')
                    return

        try: await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except: pass

    return wrapper


CONFIG = {
    "help_cmd": f'''Игрок, выберите категорию:
   1️⃣ Основное
   2️⃣ Игры
   3️⃣ Развлекательное
   4️⃣ Кланы

💬 Так же у нас есть общая беседа №1 и общая беседа №2
🆘 По всем вопросам - {adm}''',
    
    
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
   💸 Продать бизнес (временно недоступно)

🏭Генератор
   🏭 Мой генератор/генератор
   💷 Продать генератор (временно недоступно)

🧰 Майнинг ферма:
   🔋 Моя ферма/ферма
   💰 Продать ферму (временно недоступно)

⚠️ Карьер:
   🏗 Мой карьер/карьер
   💰 Продать карьер (временно недоступно)

🌳 Сады:
   🪧 Мой сад/сад
   💰 Продать сад (временно недоступно)
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

📜 Будьте осторожнее с командами повышения и понижения, повысив игрока до определенного статуса он сможет изменять название клана и управлять им.'''

}


@antispam
async def help_cmd(message):
    dt = int(datetime.now().timestamp())
    mid = message.message_id + 1
    help_msg[message.chat.id] = (mid, (dt - 2))

    await message.answer(CONFIG['help_cmd'], reply_markup=kb.help_menu(), disable_web_page_preview=True)


@antispam_help
async def help_back(call):
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=CONFIG['help_cmd'], reply_markup=kb.help_menu(), disable_web_page_preview=True)


@antispam_help
async def help_osn(call):
    name = await get_name(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=CONFIG['help_osn'].format(name), reply_markup=kb.help_back())


@antispam_help
async def help_game(call):
    name = await get_name(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=CONFIG['help_game'].format(name), reply_markup=kb.help_back())


@antispam_help
async def help_rz(call):
    name = await get_name(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=CONFIG['help_rz'].format(name), reply_markup=kb.help_back())


@antispam_help
async def help_clans(call: types.CallbackQuery):
    name = await get_name(call.from_user.id)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                text=CONFIG['help_clans'].format(name), reply_markup=kb.help_back())


def reg(dp: Dispatcher):
    dp.register_message_handler(help_cmd, lambda message: message.text.lower().startswith(('помощь', '/help')))
    dp.register_callback_query_handler(help_back, text_startswith='help_back')
    dp.register_callback_query_handler(help_osn, text_startswith='help_osn')
    dp.register_callback_query_handler(help_game, text_startswith='help_game')
    dp.register_callback_query_handler(help_rz, text_startswith='help_rz')
    dp.register_callback_query_handler(help_clans, text_startswith='help_clans')