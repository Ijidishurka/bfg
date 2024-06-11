from commands.db import url_name
from commands.main import win_luser
from commands.ore.db import *


async def rrating_cmd(message):
    user_id = message.from_user.id
    url = await url_name(user_id)
    r = await getrrating(message)
    r = '{:,}'.format(r).replace(',', '.')
    await message.answer(f'''{url}, ваш рейтинг {r}👑''', parse_mode='html', disable_web_page_preview=True)


async def sellrating(message):
    user_id = message.from_user.id
    r = await getrrating(message)
    url = await url_name(user_id)
    rwin, rloser = await win_luser()

    try:
        summ_r = int(message.text.split()[2])
    except:
        summ_r = r
    summ_r = Decimal(summ_r)

    kurs = 100000000
    summ = summ_r * kurs
    summ2 = '{:,}'.format(summ).replace(',', '.')
    summ_r2 = '{:,}'.format(summ_r).replace(',', '.')

    if r >= summ_r:
        if r - summ_r >= 0 and summ_r > 0:
            await sellrrating_db(summ, summ_r, user_id)
            await message.answer(f'{url}, вы понизили количество вашего рейтинга на {summ2}👑 за {summ_r2}$ {rwin}', parse_mode='html')
        else:
            await message.answer(f'{url}, вы неправильно ввели число рейтинга которое хотите продать {rloser}',
                                 parse_mode='html')
    else:
        await message.answer(f'{url}, у вас недостаточно рейтинга для его продажи {rloser}', parse_mode='html')

