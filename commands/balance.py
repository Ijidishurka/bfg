from datetime import datetime
from commands.db import getstatus, getbalance, getads, getname, getpofildb
from assets.antispam import antispam
from commands.assets.transform import transform
from commands.main import geturl


@antispam
async def balance_cmd(message):
    name, balance, btc, bank = await getbalance(message)
    ads = await getads(message)
    balance = '{:,}'.format(balance).replace(',', '.')
    bank = '{:,}'.format(bank).replace(',', '.')
    btc = '{:,}'.format(btc).replace(',', '.')
    await message.answer(f'''👫Ник: {name}
💰Деньги: {balance}$
🏦Банк: {bank}$
💽Биткоины: {btc}🌐

{ads}''', parse_mode='html', disable_web_page_preview=True)


@antispam
async def btc_cmd(message):
    name, balance, btc, bank = await getbalance(message)
    btc = '{:,}'.format(btc).replace(',', '.')
    await message.answer(f'''{name}, на вашем балансе {btc} BTC 🌐''', parse_mode='html', disable_web_page_preview=True)


@antispam
async def profil_cmd(message):
    user_name = await getname(message)
    user_id = message.from_user.id
    url = await geturl(user_id, user_name)
    data, property = await getpofildb(user_id)

    fdata = []
    for item in data[:8]:
        transformed_item = await transform(item)
        fdata.append(transformed_item)

    status_dict = {
        0: "Обычный",
        1: "Standart VIP",
        2: "Gold VIP",
        3: "Platinum VIP",
        4: "Администратор"
    }

    status = await getstatus(user_id)
    st = status_dict.get(status, status_dict[0])

    dregister = datetime.strptime(data[8], '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d в %H:%M:%S')

    txt = ''
    if property[0]: txt += '\n 🔋 Ферма'
    if property[1]: txt += '\n 🏭 Бизнес'
    if property[2]: txt += '\n 🌳 Сад'
    if property[3]: txt += '\n ⛏ Генератор'

    await message.answer(f'''{url}, ваш профиль:
🔎 ID: {user_id}
🏆 Статус: {st}
💰 Денег: {fdata[0]}$
🏦 В банке: {fdata[2]}$
💳 B-Coins: {fdata[3]}
💽 Биткоины: {fdata[1]}฿
🏋 Энергия: {fdata[4]}
👑 Рейтинг: {fdata[7]}
🌟 Опыт: {fdata[5]}
🎲 Всего сыграно игр: {fdata[6]}

📦 Имущество:{txt}

📅 Дата регистрации: <blockquote>{dregister}</blockquote>''')