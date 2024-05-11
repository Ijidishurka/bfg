from commands.earnings.garden.db import *
from commands.db import getname
from commands.main import geturl
from commands.main import win_luser


async def potions_list(message):
    id = message.from_user.id
    name = await getname(message)
    url = await geturl(id, name)
    await message.answer(f'''{url}, доступные зелья:
🍸 1. Чай: 40 зёрен
Прибыль: 1 энергия

🍸 2. Чефир: 240 зёрен
Прибыль: 5 энергии

🍸 3. Кофе: 520 зёрен
Прибыль: 10 энергии

🍸 4. Энергетик: 1.120 зёрен
Прибыль: 20 энергии

🍸 5. Крепкий кофе: 2.400 зёрен
Прибыль: 40 энергии

🍸 6. Настойка из вишни: 3.000 зёрен
Прибыль: 50 энергии

🍸 7. Сыворотка из плазмы: 30.000 зёрен
Прибыль: 400 энергии

🛒 Для покупки зелья введите "Создать зелье [номер]"
⛔ При покупке зелья энергия начисляется сразу.''')


async def bay_potions(message):
    user_id = message.from_user.id
    name = await getname(message)
    url = await geturl(user_id, name)
    result = await win_luser()
    rwin, rloser = result
    corn = await getcorn(user_id)

    potions = {
        1: {"name": "Чай", "summ": 1, "st": 40},
        2: {"name": "Чефир", "summ": 5, "st": 240},
        3: {"name": "Кофе", "summ": 10, "st": 520},
        4: {"name": "Энергетик", "summ": 20, "st": 1120},
        5: {"name": "Крепкий кофе", "summ": 40, "st": 2400},
        6: {"name": "Настойка из вишни", "summ": 50, "st": 3000},
        7: {"name": "Сыворотка из плазмы", "summ": 400, "st": 30000}
    }

    try:
        n = int(message.text.split()[2])
        potion = potions[n]
    except:
        await message.answer(f'{url}, вы ввели неверный номер зелья или не ввели его вовсе. {rloser}')
        return

    if corn < potion["st"]:
        await message.answer(f'{url}, у вас недостаточно зёрен для создания данного зелья. {rloser}')
        return

    await message.answer(f'{url}, вы успешно создали "{potion["name"]}", вам начислено {potion["summ"]} энергии. {rloser}')
    await buy_postion_db(potion["st"], potion["summ"], user_id)