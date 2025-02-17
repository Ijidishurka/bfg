from aiogram import Dispatcher, types
from commands.db import getpofildb, chek_user
from assets.antispam import antispam, new_earning_msg, antispam_earning
from commands.basic.property import lists
from assets import kb

from user import BFGuser, BFGconst


@antispam
async def balance_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'''👫 Ник: {user.name}
💰 Деньги: {user.balance.tr()}$
💴 Йены: {user.yen.tr()}¥
🏦 Банк: {user.bank.tr()}$
💽 Биткоины: {user.btc.tr()}🌐

{BFGconst.ads}''', disable_web_page_preview=True)


@antispam
async def btc_cmd(message: types.Message, user: BFGuser):
    await message.answer(f'{user.url}, на вашем балансе {user.btc.tr()} BTC 🌐', disable_web_page_preview=True)


async def creat_help_msg(profil, user: BFGuser):
    profil = profil.format(user.url)

    text = f'''{profil}
🪪 ID: {user.game_id}
🏆 Статус: {user.Fstatus}
💰 Денег: {user.balance.tr()}$
💴 Йены: {user.yen.tr()}¥
🏦 В банке: {user.bank.tr()}$
💳 B-Coins: {user.bcoins.tr()}
💽 Биткоины: {user.btc.tr()}฿
🏋 Энергия: {user.energy}
👑 Рейтинг: {user.rating.tr()}
🌟 Опыт: {user.expe.tr()}
🎲 Всего сыграно игр: {user.games.tr()}

<blockquote>📅 Дата регистрации:\n{user.Fregister}</blockquote>'''
    return text


@antispam
async def profil_cmd(message: types.Message, user: BFGuser):
    profil = '{0}, ваш профиль:'

    if len(message.text.split()) >= 2:
        try:
            user_id = int(message.text.split()[1])
            if user.status != 4:
                await message.answer(f'❌ Вы не администратор чтобы просматривать профили.')
                return

            if not (await chek_user(user_id)):
                await message.answer(f'❌ Данного игрока не существует. Перепроверьте указанный <b>Telegram ID</b>')
                return

            profil = 'Профиль игрока {0}:'
        except:
            pass

    text = await creat_help_msg(profil, user)
    msg = await message.answer(text, reply_markup=kb.profil(user.user_id))
    await new_earning_msg(msg.chat.id, msg.message_id)


@antispam_earning
async def profil_busines(call: types.CallbackQuery, user: BFGuser):
    _, business, _ = await getpofildb(call.from_user.id)

    txt = ''
    if business[0]: txt += '\n  🔋 Ферма: Майнинг ферма'
    if business[1]: txt += '\n  💼 Бизнес: Бизнес'
    if business[2]: txt += '\n  🌳 Сад: Сад'
    if business[3]: txt += '\n  ⛏ Генератор: Генератор'
    if txt == '': txt = '\n🥲 У вас нету бизнесов'

    await call.message.edit_text(text=f'🧳 Ваши бизнесы:{txt}', reply_markup=kb.profil_back(call.from_user.id))


@antispam_earning
async def profil_property(call: types.CallbackQuery, user: BFGuser):
    _, _, data = await getpofildb(call.from_user.id)

    txt = ''
    if data[4]:
        name = lists.phones.get(data[4])
        txt += f'\n  📱 Телефон: {name[0]}'

    if data[2]:
        name = lists.cars.get(data[2])
        txt += f'\n  🚘 Машина: {name[0]}'

    if data[1]:
        name = lists.helicopters.get(data[1])
        txt += f'\n  🚁 Вертолёт: {name[0]}'

    if data[6]:
        name = lists.planes.get(data[6])
        txt += f'\n  🛩 Самолёт: {name[0]}'

    if data[3]:
        name = lists.yahts.get(data[3])
        txt += f'\n  🛥 Яхта: {name[0]}'

    if data[5]:
        name = lists.house.get(data[5])
        txt += f'\n  🏠 Дом: {name[0]}'

    if txt == '': txt = '\n🥲 У вас нету имущества'

    await call.message.edit_text(text=f'📦 Ваше имущество:{txt}', reply_markup=kb.profil_back(call.from_user.id))


@antispam_earning
async def profil_back(call: types.CallbackQuery, user: BFGuser):
    text = await creat_help_msg('{0}, ваш профиль:', user)
    await call.message.edit_text(text=text, reply_markup=kb.profil(call.from_user.id))


def reg(dp: Dispatcher):
    dp.register_message_handler(balance_cmd, lambda message: message.text in ['б', 'Б', 'Баланс', 'баланс'])
    dp.register_message_handler(btc_cmd, lambda message: message.text in ['биткоины', 'Биткоины'])
    dp.register_message_handler(profil_cmd, lambda message: message.text.lower().startswith('профиль'))
    dp.register_callback_query_handler(profil_busines, text_startswith='profil-busines')
    dp.register_callback_query_handler(profil_back, text_startswith='profil-back')
    dp.register_callback_query_handler(profil_property, text_startswith='profil-property')
