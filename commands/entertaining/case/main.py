import random
import commands.entertaining.case.db as db
from commands.db import getads, getstatus, url_name
from commands.main import win_luser


async def getcase_cmd(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    case1, case2, case3, case4 = await db.getcase(message)
    ads = await getads(message)
    ycase = {
        "case1": {"name": "📦 Обычный кейс", "quantity": case1},
        "case2": {"name": "🏵 Золотой кейс", "quantity": case2},
        "case3": {"name": "🏺 Рудный кейс", "quantity": case3},
        "case4": {"name": "🌌 Материальный кейс", "quantity": case4},
    }

    positive_resources = {name: info for name, info in ycase.items() if info["quantity"] > 0}

    if positive_resources:
        result_message = "\n".join(
            [f'{info["name"]} - {info["quantity"]} шт.' for name, info in positive_resources.items()])
        txt = f"{result_message}\n\n🔐 Для открытия кейсов используйте - «Кейс открыть [1/2/3/4] [кол-во]»"
    else:
        txt = f"😕 У вас нету кейсов."

    await message.answer(f'''{url}, доступные кейсы:
🎁 1. Обычный кейс — 750 квдр $
🎁 2. Золотой кейс - 5 квнт $
🎁 3. Рудный кейс - 50 ⚙️
🎁 4. Материальный кейс - 200 🌌

{txt}
🛒 Для покупки введите «Купить кейс [1/2/3] [кол-во]»

{ads}''', parse_mode='html', disable_web_page_preview=True)


async def open_case(message):
    rwin, rloser = await win_luser()
    name = await url_name(message.from_user.id)
    ads = await getads(message)

    try: case = int(message.text.split()[2])
    except: return await message.answer(f'{name}, к сожалению вы ввели неверный номер кейса {rloser}')

    if case not in range(1, 5):
        await message.answer(f'{name}, к сожалению вы ввели неверный номер кейса {rloser}')
        return

    try: u = int(message.text.split()[3])
    except: u = 1

    case1, case2, case3, case4 = await db.getcase(message)
    cases = {1: case1, 2: case2, 3: case3, 4: case4}
    ncase = cases.get(case, 0)

    status_limits = {0: 10, 1: 20, 2: 40, 3: 60, 4: 100}
    status = await getstatus(message.from_user.id)
    climit = status_limits.get(status, status_limits[0])

    if u <= 0:
        return await message.answer(f'🎁 | {name}, нельзя открывать отрицательное количество кейсов! {rloser}\n\n{ads}', disable_web_page_preview=True)

    if ncase < u:
        return await message.answer(f'🎁 | {name}, у вас недостаточно кейсов! {rloser}\n\n{ads}', parse_mode='html', disable_web_page_preview=True)

    if climit < u:
        return await message.answer(f'🎁 | {name}, вы не можете открывать более {climit} кейсов за раз! {rloser}\n\n{ads}', disable_web_page_preview=True)

    if case in [1, 2]:
        return await open_case_12(message, u, case)

    if case == 3:
        return await open_case_3(message, u)

    if case == 4:
        return await open_case_4(message, u)


async def open_case_12(message, u, case):
    coff = 1 if case == 1 else 8
    user_id = message.from_user.id
    name = await url_name(message.from_user.id)
    ads = await getads(message)

    smoney = 0
    srating = 0
    sexpe = 0
    txt = ''

    for _ in range(u):
        prize = random.randint(1, 100)

        if prize in range(1, 45):
            r = random.randint(100_000_000_000_000_000, 1_000_000_000_000_000_000) * coff
            smoney = smoney + r

        elif prize in range(45, 70):
            r = random.randint(5_000_000, 150_000_000) * coff
            srating = srating + r

        else:
            r = random.randint(100, 250) * coff
            sexpe = sexpe + r

    if smoney > 0:
        smoney2 = f'{smoney:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, smoney, 'balance')
        txt += f'🔥 Итого денег - {smoney2}₴\n'
    if srating > 0:
        srating2 = f'{srating:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, srating, 'rating')
        txt += f'👑 Итого рейтинга - {srating2}\n'
    if sexpe > 0:
        sexpe2 = f'{sexpe:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, sexpe, 'exp')
        txt += f'🏆 Итого опыта - {sexpe2}шт\n'

    await db.open_case2_db(user_id, u, f'case{case}')
    await message.answer(f'🎁 | {name}, вам выпало:\n\n{txt}\n\n{ads}', disable_web_page_preview=True)


async def open_case_3(message, u):
    user_id = message.from_user.id
    name = await url_name(message.from_user.id)
    ads = await getads(message)

    smoney = 0
    srating = 0
    sexpe = 0
    stitan = 0
    spalladium = 0
    txt = ''

    for _ in range(u):
        prize = random.randint(1, 100)

        if prize in range(1, 5):
            r = random.randint(1, 3)
            spalladium += r

        if prize in range(5, 30):
            r = random.randint(100_000_000_000_000_000, 1_000_000_000_000_000_000)
            smoney += r

        elif prize in range(30, 60):
            r = random.randint(5_000_000, 150_000_000)
            srating += r

        elif prize in range(60, 80):
            r = random.randint(30, 80)
            stitan += r

        else:
            r = random.randint(100, 250)
            sexpe += r

    if smoney > 0:
        smoney2 = f'{smoney:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, smoney, 'balance')
        txt += f'🔥 Итого денег - {smoney2}₴\n'

    if srating > 0:
        srating2 = f'{srating:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, srating, 'rating')
        txt += f'👑 Итого рейтинга - {srating2}\n'

    if sexpe > 0:
        sexpe2 = f'{sexpe:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, sexpe, 'exp')
        txt += f'🏆 Итого опыта - {sexpe2}шт\n'

    if stitan > 0:
        stitan2 = f'{stitan:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, stitan, 'titanium', table='mine')
        txt += f'⚙️ Итого титана - {stitan2}шт\n'

    if spalladium > 0:
        spalladium2 = f'{spalladium:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, spalladium, 'palladium', table='mine')
        txt += f'⚗️ Итого палладия - {spalladium2}шт\n'

    await db.open_case2_db(user_id, u, 'case3')
    await message.answer(f'🎁 | {name}, вам выпало:\n\n{txt}\n\n{ads}', disable_web_page_preview=True)


async def open_case_4(message, u):
    user_id = message.from_user.id
    name = await url_name(message.from_user.id)
    ads = await getads(message)

    smoney = 0
    srating = 0
    sexpe = 0
    smatter = 0
    txt = ''

    for _ in range(u):
        prize = random.randint(1, 100)

        if prize in range(1, 30):
            r = random.randint(100_000_000_000_000_000, 1_000_000_000_000_000_000)
            smoney += r

        elif prize in range(30, 60):
            r = random.randint(5_000_000, 150_000_000)
            srating += r

        elif prize in range(60, 80):
            r = random.randint(30, 80)
            smatter += r

        else:
            r = random.randint(100, 250)
            sexpe += r

    if smoney > 0:
        smoney2 = f'{smoney:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, smoney, 'balance')
        txt += f'🔥 Итого денег - {smoney2}₴\n'
    if srating > 0:
        srating2 = f'{srating:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, srating, 'rating')
        txt += f'👑 Итого рейтинга - {srating2}\n'
    if sexpe > 0:
        sexpe2 = f'{sexpe:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, sexpe, 'exp')
        txt += f'🏆 Итого опыта - {sexpe2}шт\n'
    if smatter > 0:
        smatter2 = f'{smatter:,.0f}'.replace(",", ".")
        await db.open_case_db(user_id, smatter, 'matter', table='mine')
        txt += f'🌌 Итого материи - {smatter2}шт\n'

    await db.open_case2_db(user_id, u, 'case4')
    await message.answer(f'🎁 | {name}, вам выпало:\n\n{txt}\n\n{ads}', disable_web_page_preview=True)