from commands.db import register_users, getname, getonlibalance, getidname, getads
from commands.main import geturl
from commands.main import win_luser
from commands.ore.db import *
import random



async def energy_cmd(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    i = await getenergy(message)
    await message.answer(f'''{url}, на данный момент у тебя {i} ⚡''', parse_mode='html', disable_web_page_preview=True)


async def mine_cmd(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    await message.answer(f'''{url}, добро пожаловать на вашу шахту! 🏞️

Здесь вы можете добывать различные ресурсы для продажи, используя свою энергию ⚡.

✨ Для добычи ресурсов используйте:- копать железо
- копать золото
- копать алмазы
- копать аметисты
- копать аквамарин
- копать изумруды
- копать материю
- копать плазму
- копать никель
- копать титан
- копать кобальт
- копать эктоплазму
<b>«Статусы» увеличивают количество выпадаемой руды и получаемого опыта.</b>

🛒 Для продажи ресурсов:
- продать железо
- продать золото
- продать алмазы
- продать аметисты
- продать аквамарин
- продать изумруды
- продать материю
- продать плазму
- продать никель
- продать титан
- продать кобальт
- продать эктоплазму
- продать палладий

📊 Для статистики:
- Моя шахта''', parse_mode='html')


async def kursrud_cmd(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    await message.answer(f'''{url}, курс руды:
⛓ 1 железо - 230.000$
🌕 1 золото - 1.000.000$
💎 1 алмаз - 116.000.000$
🎆 1 аметист - 217.000.000$
💠 1 аквамарин - 461.000.000$
🍀 1 изумруд - 792.000.000$
🌌 1 материя - 8.000.000.000$
💥 1 плазма - 12.000.000.000$
🪙 1 никель - 30.000.000.000$
⚙ 1 титан - 70.000.000.000.000$
🧪 1 кобальт - 120.000.000.000.000$
☄️ 1 эктоплазма - 270.000.000.000.000$
⚗ 1 палладий - 2.000.000.000.000.000$''', parse_mode='html')


async def inventary_cmd(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    corn = await getcorn_garden(user_id)
    iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, nickel, titanium, cobalt, ectoplasm = await getmine(
        message)
    resources = {
        "iron": {"name": "⛓ Железо", "quantity": iron},
        "gold": {"name": "🌕 Золото", "quantity": gold},
        "diamond": {"name": "💎 Алмаз", "quantity": diamond},
        "amethyst": {"name": "🎆 Аметист", "quantity": amestit},
        "aquamarine": {"name": "💠 Аквамарин", "quantity": aquamarine},
        "emeralds": {"name": "🍀 Изумруд", "quantity": emeralds},
        "matter": {"name": "🌌 Материя", "quantity": matter},
        "plasma": {"name": "💥 Плазма", "quantity": plasma},
        "nickel": {"name": "🪙 Никель", "quantity": nickel},
        "titanium": {"name": "⚙️ Титан", "quantity": titanium},
        "cobalt": {"name": "🧪 Кобальт", "quantity": cobalt},
        "ectoplasm": {"name": "☄️ Эктоплазма", "quantity": ectoplasm},
        "corn": {"name": "🥜 Зёрна", "quantity": corn},
    }

    positive_resources = {name: info for name, info in resources.items() if info["quantity"] > 0}

    if positive_resources:
        result_message = "\n".join(
            [f'{info["name"]}: {info["quantity"]} шт.' for name, info in positive_resources.items()])
        await message.answer(f"{url},\n{result_message}", parse_mode='html')
    else:
        await message.answer(f"{url}, ваш инвентарь пуст.", parse_mode='html')


async def mine_level(expe):
    if expe >= 10000000000:
        i = 'Эктоплазма ☄️'
        i2 = 'SOON...'
        i3 = '???'
    elif expe >= 20000000:
        i = 'Кобаль 🧪'
        i2 = 'Эктоплазма ☄️'
        i3 = '10.000.000.000'
    elif expe >= 5000000:
        i = 'Титан ⚙️'
        i2 = 'Кобаль 🧪'
        i3 = '20.000.000'
    elif expe >= 950000:
        i = 'Никель 🪙'
        i2 = 'Титан ⚙️'
        i3 = '5.000.000'
    elif expe >= 500000:
        i = 'Плазма 💥'
        i2 = 'Никель 🪙'
        i3 = '950.000'
    elif expe >= 100000:
        i = 'Материя 🌌'
        i2 = 'Плазма 💥'
        i3 = '500.000'
    elif expe >= 60000:
        i = 'Изумруд 🍀'
        i2 = 'Материя 🌌'
        i3 = '100.000'
    elif expe >= 25000:
        i = 'Аквамарин 💠'
        i2 = 'Изумруд 🍀'
        i3 = '60.000'
    elif expe >= 10000:
        i = 'Аметист 🎆'
        i2 = 'Аквамарин 💠'
        i3 = '25.000'
    elif expe >= 2000:
        i = 'Алмазы 💎'
        i2 = 'Аметист 🎆 '
        i3 = '10.000'
    elif expe >= 500:
        i = 'Золото 🌕'
        i2 = 'Алмазы 💎'
        i3 = '2.000'
    else:
        i = 'Железо ⛓'
        i2 = 'Золото 🌕'
        i3 = '500'
    return i, i2, i3


async def mymine_cmd(message):
    await register_users(message)
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    expe, energy = await getexpe(message)
    mine_level_t, mine_level_s, tr = await mine_level(expe)
    await message.answer(f'''{url}, это ваш профиль шахты:
🏆 Опыт: {expe}
⚡ Энергия: {energy}
⛏ Ваш уровень: {mine_level_t}
➡ Следующий уровень: {mine_level_s}
⭐️ Требуется {tr} опыта''', parse_mode='html')


async def digmine(message):
    await register_users(message)
    user_name = await getname(message)
    ads = await getads(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    expe, energy = await getexpe(message)
    result = await win_luser()
    rwin, rloser = result
    if energy == 0:
        await message.answer(f'{url}, у вас недостаточно энергии для копки {rloser}', parse_mode='html')
        return
    txt = message.text.split()
    if len(txt) < 2:
        await message.answer(f'{url}, данной руды не существует {rloser}', parse_mode='html',
                             disable_web_page_preview=True)
        return
    else:
        ruda = txt[1].lower()
    if ruda == 'железо':
        i = random.randint(40, 69)
        op = 1
        await digdb(i, user_id, 'iron', op)
        await message.answer(f'{url}, +{i} железо.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'золото':
        if expe < 500:
            await message.answer(f'{url}, чтобы копать золото вам требуется 500 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(4, 30)
        op = 3
        await digdb(i, user_id, 'gold', op)
        await message.answer(f'{url}, +{i} золото.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'алмазы':
        if expe < 2000:
            await message.answer(f'{url}, чтобы копать алмазы вам требуется 2.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(2, 10)
        op = 5
        await digdb(i, user_id, 'diamond', op)
        await message.answer(f'{url}, +{i} алмазы.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'аметисты':
        if expe < 10000:
            await message.answer(f'{url}, чтобы копать аметисты вам требуется 10.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 6)
        op = 15
        await digdb(i, user_id, 'amestit', op)
        await message.answer(f'{url}, +{i} аметисты.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'аквамарин':
        if expe < 25000:
            await message.answer(f'{url}, чтобы копать аквамарин вам требуется 25.000 опыта {rloser}',
                                 parse_mode='html')
            return
        i = random.randint(1, 5)
        op = 30
        await digdb(i, user_id, 'aquamarine', op)
        await message.answer(f'{url}, +{i} аквамарин.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'изумруды':
        if expe < 60000:
            await message.answer(f'{url}, чтобы копать изумруды вам требуется 60.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 3)
        op = 55
        await digdb(i, user_id, 'emeralds', op)
        await message.answer(f'{url}, +{i} изумруды.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'материю':
        if expe < 100000:
            await message.answer(f'{url}, чтобы копать материю вам требуется 100.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 65
        await digdb(i, user_id, 'matter', op)
        await message.answer(f'{url}, +{i} материю.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'плазму':
        if expe < 500000:
            await message.answer(f'{url}, чтобы копать плазму вам требуется 500.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 180
        await digdb(i, user_id, 'plasma', op)
        await message.answer(f'{url}, +{i} плазму.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'никель':
        if expe < 950000:
            await message.answer(f'{url}, чтобы копать никель вам требуется 950.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 500
        await digdb(i, user_id, 'nickel', op)
        await message.answer(f'{url}, +{i} никель.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'титан':
        if expe < 5000000:
            await message.answer(f'{url}, чтобы копать титан вам требуется 5.000.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 2300
        await digdb(i, user_id, 'titanium', op)
        await message.answer(f'{url}, +{i} титан.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'кобальт':
        if expe < 20000000:
            await message.answer(f'{url}, чтобы копать кобальт вам требуется 20.000.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 3600
        await digdb(i, user_id, 'cobalt', op)
        await message.answer(f'{url}, +{i} кобальт.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    elif ruda == 'эктоплазму':
        if expe < 10000000000:
            await message.answer(f'{url}, чтобы копать эктоплазму вам требуется 10.000.000.000 опыта {rloser}', parse_mode='html')
            return
        i = random.randint(1, 2)
        op = 7200
        await digdb(i, user_id, 'ectoplasm', op)
        await message.answer(f'{url}, +{i} кобальт.\n💡 Энергия: {energy - 1}, опыт: {expe + op}\n\n{ads}',
                             parse_mode='html', disable_web_page_preview=True)
    else:
        await message.answer(f'{url}, данной руды не существует {rloser}', parse_mode='html')
