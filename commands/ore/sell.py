from commands.db import register_users, getname, getonlibalance, getidname, getads
from commands.main import geturl
from commands.main import win_luser
from commands.ore.db import *

async def sellruda_cmd(message):
    await register_users(message)
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
    if ruda == 'железо':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(iron)
        if kolvo == 0 or kolvo > int(iron):
            await message.answer(f'{url}, у вас нет железа {rloser}',parse_mode='html')
            return
        i = kolvo * 230000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'iron', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} железо за {i2}$ ✅', parse_mode='html')
    elif ruda == 'золото':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(gold)
        if kolvo == 0 or kolvo > int(gold):
            await message.answer(f'{url}, у вас нет золота {rloser}', parse_mode='html')
            return
        i = kolvo * 1000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'gold', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} золота за {i2}$ ✅', parse_mode='html')
    elif ruda == 'алмазы':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(diamond)
        if kolvo == 0 or kolvo > int(diamond):
            await message.answer(f'{url}, у вас нет алмазов {rloser}', parse_mode='html')
            return
        i = kolvo * 116000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'diamond', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} алмазов за {i2}$ ✅', parse_mode='html')
    elif ruda == 'аметисты':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(amestit)
        if kolvo == 0 or kolvo > int(amestit):
            await message.answer(f'{url}, у вас нет аметистов {rloser}', parse_mode='html')
            return
        i = kolvo * 217000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'amestit', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} аметистов за {i2}$ ✅', parse_mode='html')
    elif ruda == 'аквамарин':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(aquamarine)
        if kolvo == 0 or kolvo > int(aquamarine):
            await message.answer(f'{url}, у вас нет аквамарина {rloser}', parse_mode='html')
            return
        i = kolvo * 461000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'aquamarine', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} аквамаринов за {i2}$ ✅', parse_mode='html')
    elif ruda == 'изумруды':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(emeralds)
        if kolvo == 0 or kolvo > int(emeralds):
            await message.answer(f'{url}, у вас нет изумрудов {rloser}', parse_mode='html')
            return
        i = kolvo * 792000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'emeralds', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} изумрудов за {i2}$ ✅', parse_mode='html')
    elif ruda == 'материю':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(matter)
        if kolvo == 0 or kolvo > int(matter):
            await message.answer(f'{url}, у вас нет материи {rloser}', parse_mode='html')
            return
        i = kolvo * 8000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'matter', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} материи за {i2}$ ✅', parse_mode='html')
    elif ruda == 'плазму':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(plasma)
        if kolvo == 0 or kolvo > int(plasma):
            await message.answer(f'{url}, у вас нет плазмы {rloser}', parse_mode='html')
            return
        i = kolvo * 12000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'plasma', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} плазмы за {i2}$ ✅', parse_mode='html')
    elif ruda == 'никель':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(nickel)
        if kolvo == 0 or kolvo > int(nickel):
            await message.answer(f'{url}, у вас нет никеля {rloser}', parse_mode='html')
            return
        i = kolvo * 30000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'nickel', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} никеля за {i2}$ ✅', parse_mode='html')
    elif ruda == 'титан':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(titanium)
        if kolvo == 0 or kolvo > int(titanium):
            await message.answer(f'{url}, у вас нет титана {rloser}', parse_mode='html')
            return
        i = kolvo * 70000000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'titanium', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} титана за {i2}$ ✅', parse_mode='html')
    elif ruda == 'кобальт':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(cobalt)
        if kolvo == 0 or kolvo > int(cobalt):
            await message.answer(f'{url}, у вас нет кобальта {rloser}', parse_mode='html')
            return
        i = kolvo * 120000000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'cobalt', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} кобальта за {i2}$ ✅', parse_mode='html')
    elif ruda == 'эктоплазма':
        if len(txt) >= 3:
            kolvo = int(txt[2].lower())
        else:
            kolvo = int(ectoplasm)
        if kolvo == 0 or kolvo > int(ectoplasm):
            await message.answer(f'{url}, у вас нет эктоплазмы {rloser}', parse_mode='html')
            return
        i = kolvo * 270000000000000
        i2 = '{:,}'.format(i).replace(',', '.')
        await sell_ruda_db(i, user_id, 'ectoplasm', kolvo)
        await message.answer(f'{url}, вы продали {kolvo} эктоплазмы за {i2}$ ✅', parse_mode='html')