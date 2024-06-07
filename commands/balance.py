from datetime import datetime
from commands.db import getstatus, getbalance, getads, getpofildb, url_name, chek_user
from assets.antispam import antispam
from commands.assets.transform import transform
from decimal import Decimal


@antispam
async def balance_cmd(message):
    name, balance, btc, bank = await getbalance(message.from_user.id)
    ads = await getads()

    if len(str(balance)) < 35:
        balance = '{:,}'.format(balance).replace(',', '.')
    else:
        balance = Decimal(balance)
        balance = f"{balance:1.1e}"

    bank = '{:,}'.format(bank).replace(',', '.')
    btc = '{:,}'.format(btc).replace(',', '.')
    await message.answer(f'''👫Ник: {name}
💰Деньги: {balance}$
🏦Банк: {bank}$
💽Биткоины: {btc}🌐

{ads}''', parse_mode='html', disable_web_page_preview=True)


@antispam
async def btc_cmd(message):
    name, _, btc, _ = await getbalance(message)
    btc = '{:,}'.format(btc).replace(',', '.')
    await message.answer(f'{name}, на вашем балансе {btc} BTC 🌐', disable_web_page_preview=True)


@antispam
async def profil_cmd(message):
    user_id = message.from_user.id
    msg = message.text

    profil = '{0}, ваш профиль:'

    if len(msg.split()) >= 2:
        status = await getstatus(user_id)
        try:
            user_id = int(msg.split()[1])
            if status != 4:
                await message.answer(f'❌ Вы не администратор чтобы просматривать профили.')
                return

            if not (await chek_user(user_id)):
                await message.answer(f'❌ Данного игрока не существует. Перепроверьте указанный <b>Telegram ID</b>')
                return

            profil = 'Профиль игрока {0}:'
        except:
            pass

    status = await getstatus(user_id)
    url = await url_name(user_id)
    profil = profil.format(url)

    data, property = await getpofildb(user_id)

    fdata = []
    for item in data[:8]:
        transformed_item = await transform(int(item))
        fdata.append(transformed_item)

    print(fdata)

    status_dict = {
        0: "Обычный",
        1: "Standart VIP",
        2: "Gold VIP",
        3: "Platinum VIP",
        4: "Администратор"
    }

    st = status_dict.get(status, status_dict[0])
    dregister = datetime.fromtimestamp(data[8]).strftime('%Y-%m-%d в %H:%M:%S')

    txt = ''
    if property[0]: txt += '\n 🔋 Ферма'
    if property[1]: txt += '\n 🏭 Бизнес'
    if property[2]: txt += '\n 🌳 Сад'
    if property[3]: txt += '\n ⛏ Генератор'
    if txt == '': txt = '\n🥲 У вас нету имущества'

    await message.answer(f'''{profil}
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
