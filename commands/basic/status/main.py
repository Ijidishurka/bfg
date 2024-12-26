from aiogram import Dispatcher, types
from assets.antispam import antispam
from assets.transform import transform_int as tr
from commands.basic.status.db import *
import config as cfg
from user import BFGuser, BFGconst

CONFIG = {
    'money_for_bcoins': 2_000_000_000_000_000,  # "обменять" (цена)
    
    'status_price': {  # "купить привилегию" (название, цена)
        1: ("Standart VIP", 250),
        2: ("Gold VIP", 500),
        3: ("Platinum VIP", 750),
        4: ("Admin Status", 1500)
    },
    
    'limit_list': {  # "купить лимит" (лимит, цена)
        1: (350_000_000_000_000, 100),
        2: (3_000_000_000_000_000_000, 1000),
        3: (100_000_000_000_000_000_000, 3000),
        4: (2_000_000_000_000_000_000_000, 6500),
    },
    
    'energy_price': {  # "купить флягу" (кол-во энергии, цена)
        1: (20, 15),
        2: (60, 35),
    },
}


@antispam
async def status_list(message: types.Message, user: BFGuser):
    await message.answer(f'''{user.url}, доступные статусы в игре:

1️⃣ Standart VIP:
- Повышенный процент в банке
- Увеличенный шанс победы в играх
- Увеличен процент в депозите до 8%
- Уменьшен налог при снятии депозита до 4.5%
- Увеличен лимит передачи другим игрокам до 300.000.000.000.000$ в сутки
- Красивая отметка в профиле
- Возможность установить более длинный ник
- Время до получения ежедневного бонуса уменьшено в два раза
- Увеличена максимальная энергия до 25
- Увеличено количество открываемых кейсов до 20

2️⃣ Gold VIP:
- Увеличен шанс в играх
- Увеличен процент в депозите до 10%
- Уменьшен налог при снятии депозита до 3.5%
- Возможность установить ещё длинее ник
- Уникальный золотой ежедневный бонус
- Увеличен лимит передачи другим игрокам до 750.000.000.000.000$ в сутки
- Увеличена максимальная энергия до 50
- Увеличено количество открываемых кейсов до 40

3️⃣ Platinum VIP:
- Увеличен лимит передачи другим игрокам до 1.000.000.000.000.000$ в сутки
- Повышенный процент выигрыша в играх
- Увеличен процент в депозите до 12%
- Уменьшен налог при снятии депозита до 3%
- Увеличена максимальная энергия до 75
- Красивая отметка в профиле
- Опыт и добыча увеличена в два раза
- Увеличено количество открываемых кейсов до 60

4️⃣ Администратор:
- Выдача денег в сутки - 150.000.000.000.000
- Увеличен процент в депозите до 15%
- Уменьшен налог при снятии депозита до 2.5%
- Возможность просматривать профили других игроков
- Максимальная энергия увеличенная до 100
- Красивая отметка в профиле
- Увеличен лимит передачи другим игрокам до 30.000.000.000.000.000$ в сутки
- Увеличено количество открываемых кейсов до 250''')


@antispam
async def donat_list(message: types.Message, user: BFGuser):
    adm_us = cfg.admin_username.replace('@', '')
    st_price = CONFIG['status_price']
    await message.answer(f'''{user.url}, наш магазин:

💵 Текущий курс: 1 RUB = 1 B-Coin
💸 Валюта: 1 B-Coin можно обменять на {tr(CONFIG['money_for_bcoins'])}$

🪙 Обмен коинов на валюту: Обменять [количество]

🏆 Привилегии:
1️⃣ Standart VIP | {st_price[1][1]} B-Coin
2️⃣ Gold VIP | {st_price[2][1]} B-Coin
3️⃣ Platinum VIP | {st_price[3][1]} B-Coin
4️⃣ Admin Status | {tr(st_price[4][1])} B-Coin

🔝Покупка: Купить привилегию [номер]

⚡️ Энергия:
    - 20 энергии | 15 B-Coin 
     🔝 Покупка: Купить флягу 1
    - 60 энергии | 35 B-Coin
     🔝 Покупка: Купить флягу 2

🚧 Лимит:
 - 350.000.000.000.000 | 100 B-Coin
🔝 Покупка: Купить лимит 1

- 3e18 | 1000 B-Coin
🔝 Покупка: Купить лимит 2

- 1e20 | 3000 B-Coin
🔝 Покупка: Купить лимит 3

- 2e21 | 6500 B-Coin
🔝 Покупка: Купить лимит 4

💰Ваш баланс: {user.bcoins.tr()} B-Coin
📲 Пополнить баланс: <a href="t.me/{adm_us}">{cfg.admin_username}</a>''', disable_web_page_preview=True)


@antispam
async def my_status(message: types.Message, user: BFGuser):
    privileges = {
        0: "к сожалению вы не владеете какими либо привилегиями",
        1: "🏆 Статус: Standart VIP\n🏦 Процент вклада: 8%\n💸 Лимит передачи: 300.000.000.000.000$/сутки",
        2: "🏆 Статус: Gold VIP\n🏦 Процент вклада: 10%\n💸 Лимит передачи: 750.000.000.000.000$/сутки",
        3: "🏆 Статус: Platinum VIP\n🏦 Процент вклада: 12%\n💸 Лимит передачи: 1.000.000.000.000.000$/сутки",
        4: "🏆 Статус: Администратор\n🏦 Процент вклада: 15%\n💸 Лимит передачи: 30.000.000.000.000.000$/сутки"
    }

    await message.answer(f'{user.url}, информация о привилегии:\n{privileges[user.status]}\nПодробнее об плюшках можно узнать введя команду "Статусы"')


@antispam
async def buy_status(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{user.url}, вы не ввели число имущества или привелегии которое хотите купить {lose}')
        return

    data = CONFIG['status_price'].get(u)
    
    if not data:
        await message.answer(f'{user.url}, данного доната не существует. Проверьте введеную вами цифру.')
        return

    if user.bcoins < data[1]:
        await message.answer(f'{user.url},к сожалению у вас недостаточно B-Coins для покупки данной привелегии, '
                             f'чтобы пополнить напишите команду "Донат" {lose}')
        return

    if user.bcoins > u:
        await message.answer(f'{user.url}, у вас уже есть этот или более высокий статус {win}.')
        return

    await buy_status_db(user.user_id, data[1], u)
    await message.answer(f'{user.url}, вы успешно купили статус "{data[0]}" за {data[1]} B-Coins {win}.')


@antispam
async def exchange_value(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        u = int(message.text.split()[1])
    except:
        u = 1

    if u > 100000000 or u <= 0:
        return

    if user.bcoins < u:
        await message.answer(f'На твоём счету {user.bcoins.tr()} B-Coins, чтобы пополнить введите - Донат {lose}')
        return

    summ = u * CONFIG['money_for_bcoins']

    await exchange_value_db(user.user_id, summ, u)
    await message.answer(f'{user.url}, вы обменяли {u} B-Coins на {tr(summ)}$ {win}')


@antispam
async def buy_limit(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{user.url}, вы не ввели число имущества или привелегии которое хотите купить {lose}')
        return

    data = CONFIG['limit_list'].get(u)

    if not data:
        return

    if user.bcoins < data[1]:
        await message.answer(f'{user.url}, к сожалению у вас недостаточно B-Coins для покупки лимита,'
                             f' чтобы пополнить напишите команду "Донат" {lose}')
        return

    await buy_limit_db(user.user_id, data[0], data[1])
    await message.answer(f'{user.url}, вы увеличили свой лимит передачи на {tr(data[0])}$ за {data[1]} B-Coins {win}')
    
    
@antispam
async def buy_energy(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()

    try:
        u = int(message.text.split()[2])
    except:
        await message.answer(f'{user.url}, вы не ввели число имущества или привелегии которое хотите купить {lose}')
        return

    data = CONFIG['energy_price'].get(u)

    if not data:
        return

    if user.bcoins < data[1]:
        await message.answer(f'{user.url}, к сожалению у вас недостаточно B-Coins для покупки фляги,'
                             f' чтобы пополнить напишите команду "Донат" {lose}')
        return

    await buy_energy_db(user.user_id, data[1], data[0])
    await message.answer(f'{user.url}, вы купили {data[0]}⚡️ за {data[1]} B-Coins {win}')


def reg(dp: Dispatcher):
    dp.register_message_handler(donat_list, lambda message: message.text.lower().startswith('донат'))
    dp.register_message_handler(status_list, lambda message: message.text.lower().startswith('статусы'))
    dp.register_message_handler(my_status, lambda message: message.text.lower().startswith('мой статус'))
    dp.register_message_handler(buy_status, lambda message: message.text.lower().startswith('купить привилегию'))
    dp.register_message_handler(exchange_value, lambda message: message.text.lower().startswith('обменять'))
    dp.register_message_handler(buy_limit, lambda message: message.text.lower().startswith('купить лимит'))
    dp.register_message_handler(buy_energy, lambda message: message.text.lower().startswith('купить флягу'))