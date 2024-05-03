from commands.db import register_users, getbalance, getads


async def balance_cmd(message):
    await register_users(message)
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


async def btc_cmd(message):
    await register_users(message)
    name, balance, btc, bank = await getbalance(message)
    btc = '{:,}'.format(btc).replace(',', '.')
    await message.answer(f'''{name}, на вашем балансе {btc} BTC 🌐''', parse_mode='html', disable_web_page_preview=True)