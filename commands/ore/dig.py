from commands.db import getname, getstatus, getads
from commands.main import geturl
from commands.main import win_luser
from commands.ore.db import *
import random


async def energy_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    i = await getenergy(message)
    await message.answer(f'''{url}, на данный момент у тебя {i} ⚡''', parse_mode='html', disable_web_page_preview=True)


async def mine_cmd(message):
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
        result_message = "\n".join([f'{info["name"]}: {int(info["quantity"]):,} шт.' for name, info in positive_resources.items()])
        await message.answer(f"{url},\n{result_message}", parse_mode='html')
    else:
        await message.answer(f"{url}, ваш инвентарь пуст.", parse_mode='html')


async def mine_level(expe):
    levels = [
        ('Эктоплазма ☄️', 'SOON...', '???', 10000000000),
        ('Кобаль 🧪', 'Эктоплазма ☄️', '10.000.000.000', 20000000),
        ('Титан ⚙️', 'Кобаль 🧪', '20.000.000', 5000000),
        ('Никель 🪙', 'Титан ⚙️', '5.000.000', 950000),
        ('Плазма 💥', 'Никель 🪙', '950.000', 500000),
        ('Материя 🌌', 'Плазма 💥', '500.000', 100000),
        ('Изумруд 🍀', 'Материя 🌌', '100.000', 60000),
        ('Аквамарин 💠', 'Изумруд 🍀', '60.000', 25000),
        ('Аметист 🎆', 'Аквамарин 💠', '25.000', 10000),
        ('Алмазы 💎', 'Аметист 🎆', '10.000', 2000),
        ('Золото 🌕', 'Алмазы 💎', '2.000', 500),
        ('Железо ⛓', 'Золото 🌕', '500', 0)
    ]

    for level, next_level, limit, threshold in levels:
        if expe >= threshold:
            return level, next_level, limit


async def mymine_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    expe, energy = await getexpe(message)
    mine_level_t, mine_level_s, tr = await mine_level(expe)

    expe = '{:,}'.format(expe).replace(',', '.')

    await message.answer(f'''{url}, это ваш профиль шахты:
🏆 Опыт: {expe}
⚡ Энергия: {energy}
⛏ Ваш уровень: {mine_level_t}
➡ Следующий уровень: {mine_level_s}
⭐️ Требуется {tr} опыта''', parse_mode='html')


async def digmine(message):
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

    status_limits = {0: 1, 1: 2, 2: 3, 3: 5, 4: 10}
    status = await getstatus(message.from_user.id)
    coff = status_limits.get(status, status_limits[0])

    txt = message.text.split()
    if len(txt) < 2:
        await message.answer(f'{url}, данной руды не существует {rloser}', parse_mode='html', disable_web_page_preview=True)
        return
    else:
        ruda = txt[1].lower()

    ruda_data = {
        'железо': ('iron', 40, 1, 0),
        'золото': ('gold', 4, 3, 500),
        'алмазы': ('diamond', 2, 5, 2000),
        'аметисты': ('amethyst', 1, 15, 10000),
        'аквамарин': ('aquamarine', 1, 30, 25000),
        'изумруды': ('emeralds', 1, 55, 60000),
        'материю': ('matter', 1, 65, 100000),
        'плазму': ('plasma', 1, 180, 500000),
        'никель': ('nickel', 1, 500, 950000),
        'титан': ('titanium', 1, 2300, 5000000),
        'кобальт': ('cobalt', 1, 3600, 20000000),
        'эктоплазму': ('ectoplasm', 1, 7200, 10000000000)
    }

    if ruda in ruda_data:
        eng_ruda, min_i, op, min_expe = ruda_data[ruda]
        if expe < min_expe:
            min_expe = '{:,}'.format(expe).replace(',', '.')
            await message.answer(f'{url}, чтобы копать {ruda} вам требуется {min_expe} опыта {rloser}', parse_mode='html')
            return

        i = random.randint(min_i, min_i + 5) * coff
        await digdb(i, user_id, eng_ruda, op)
        opit = expe + op
        opit = '{:,}'.format(opit).replace(',', '.')

        await message.answer(f'{url}, +{i} {ruda}.\n💡 Энергия: {energy - 1}, опыт: {opit}\n\n{ads}', disable_web_page_preview=True)
    else:
        await message.answer(f'{url}, данной руды не существует {rloser}')


async def sellruda_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    txt = message.text.split()
    result = await win_luser()
    rwin, rloser = result
    iron, gold, diamond, amestit, aquamarine, emeralds, matter, plasma, nickel, titanium, cobalt, ectoplasm = await getmine(message)

    if len(txt) < 2:
        return
    ruda = txt[1].lower()

    ruda_data = {
        'железо': ('iron', 230000),
        'золото': ('gold', 1000000),
        'алмазы': ('diamond', 116000000),
        'аметисты': ('amestit', 217000000),
        'аквамарин': ('aquamarine', 461000000),
        'изумруды': ('emeralds', 792000000),
        'материю': ('matter', 8000000000),
        'плазму': ('plasma', 12000000000),
        'никель': ('nickel', 30000000000),
        'титан': ('titanium', 70000000000000),
        'кобальт': ('cobalt', 120000000000000),
        'эктоплазму': ('ectoplasm', 270000000000000)
    }

    if ruda in ruda_data:
        if len(txt) >= 3:
            try: kolvo = int(txt[2].lower())
            except: return
        else:
            kolvo = int(eval(ruda_data[ruda][0]))

        if kolvo <= 0 or kolvo > eval(ruda_data[ruda][0]):
            await message.answer(f'{url}, у вас недостаточно {ruda} {rloser}', parse_mode='html')
            return

        i = kolvo * int(ruda_data[ruda][1])
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, ruda_data[ruda][0], kolvo)
        await message.answer(f'{url}, вы продали {kolvo} {ruda} за {i2}$ ✅', parse_mode='html')