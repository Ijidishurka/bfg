# YT: userbotik
import install
from config import *
from commands.main import *
from commands.basic.transfer import *
from commands.games.games import *
from assets.auto import automatisation
from commands.basic.ore.dig import *
from commands.entertaining.case.main import *
from commands.entertaining.case.buy import *
from commands.basic.bank.main import *
from commands.entertaining.earnings.garden.potions import *
from assets.filters import FilterAdmin
from assets.modules import *
from bot import dp

import commands.basic.property.main
import commands.admin.admin
import commands.entertaining.earnings.farm.main
import commands.entertaining.earnings.business.main
import commands.entertaining.earnings.garden.main
import commands.entertaining.earnings.generator.main
import commands.entertaining.earnings.tree.main
import commands.entertaining.earnings.quarry.main
import commands.entertaining.wedlock
import commands.basic.balance
import commands.basic.status.main
import commands.basic.ore.main
import commands.help
import commands.entertaining.rz
import commands.basic.top
import commands.clans.main
import commands.admin.promo


@dp.message_handler(commands=['start'])
async def on_start_s(message: types.Message):
    await on_start(message)


@dp.message_handler(lambda message: message.text in ['энергия', 'Энергия'])
async def energy_cmd_s(message: types.Message):
    await energy_cmd(message)


@dp.message_handler(lambda message: message.text in ['банк', 'Банк'])
async def bank_cmd_s(message: types.Message):
    await bank_cmd(message)


@dp.message_handler(lambda message: message.text in ['мой лимит', 'Мой лимит'])
async def limit_cmd_s(message: types.Message):
    await limit_cmd(message)


@dp.message_handler(lambda message: message.text in ['зелья', 'Зелья'])
async def potions_list_s(message: types.Message):
    await potions_list(message)


@dp.message_handler(lambda message: message.text.lower().startswith('создать зелье'))
async def bay_potions_s(message: types.Message):
    await bay_potions(message)


@dp.message_handler(lambda message: message.text.lower().startswith('банк положить'))
async def putbank_s(message: types.Message):
    await putbank(message)


@dp.message_handler(lambda message: message.text.lower().startswith('банк снять'))
async def takeoffbank_s(message: types.Message):
    await takeoffbank(message)


@dp.message_handler(lambda message: message.text.lower().startswith('депозит положить'))
async def pudepozit_s(message: types.Message):
    await pudepozit(message)


@dp.message_handler(lambda message: message.text.lower().startswith('депозит снять'))
async def takeoffdepozit_s(message: types.Message):
    await takeoffdepozit(message)


@dp.message_handler(lambda message: message.text in ['курс руды', 'Курс руды'])
async def kursrud_cmd_s(message: types.Message):
    await kursrud_cmd(message)


@dp.message_handler(lambda message: message.text in ['кейсы', 'Кейсы'])
async def getcase_cmd_s(message: types.Message):
    await getcase_cmd(message)


@dp.message_handler(lambda message: message.text.lower().startswith('открыть кейс'))
async def open_case_s(message: types.Message):
    await open_case(message)


@dp.message_handler(lambda message: message.text.lower().startswith('купить кейс'))
async def buy_case_s(message: types.Message):
    await buy_case(message)


@dp.message_handler(lambda message: message.text in ['Моя шахта', 'моя шахта'])
async def mymine_cmd_s(message: types.Message):
    await mymine_cmd(message)


@dp.message_handler(lambda message: message.text in ['шахта', 'Шахта'])
async def mine_cmd_s(message: types.Message):
    await mine_cmd(message)


@dp.message_handler(lambda message: message.text.lower().startswith('копать'))
async def digmine_s(message: types.Message):
    await digmine(message)


sell_ruda_txt = ['железо', 'золото', 'алмазы', 'аметисты', 'аквамарины', 'изумруды',
                 'материю', 'плазму', 'никель', 'титан', 'кобальт', 'эктоплазму', 'палладий']


@dp.message_handler(lambda message: message.text.lower().startswith('продать') and any(ruda in message.text.lower() for ruda in sell_ruda_txt))
async def sellruda_cmd_s(message: types.Message):
    await sellruda_cmd(message)


@dp.message_handler(lambda message: message.text in ['инвентарь', 'Инвентарь'])
async def inventary_cmd_s(message: types.Message):
    await inventary_cmd(message)


@dp.message_handler(lambda message: message.text in ['курс руды', 'Курс руды'])
async def kursrud_cmd_s(message: types.Message):
    await kursrud_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("дать") or message.text.startswith("Дать"))
async def dat_cmd_s(message: types.Message):
    await dat_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("дартс") or message.text.startswith("Дартс"))
async def darts_cmd_s(message: types.Message):
    await darts_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("кубик") or message.text.startswith("Кубик"))
async def kybik_game_cmd_s(message: types.Message):
    await kybik_game_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("баскетбол") or message.text.startswith("Баскетбол"))
async def basketbol_cmd_s(message: types.Message):
    await basketbol_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("боулинг") or message.text.startswith("Боулинг"))
async def bowling_cmd_s(message: types.Message):
    await bowling_cmd(message)


@dp.message_handler(lambda message: message.text.lower().startswith("казино"))
async def game_casino_s(message: types.Message):
    await game_casino(message)


@dp.message_handler(lambda message: message.text.lower().startswith("спин"))
async def game_spin_s(message: types.Message):
    await game_spin(message)


@dp.message_handler(lambda message: message.text.lower().startswith(("трейд вверх", "трейд вниз")))
async def game_trade_s(message: types.Message):
    await game_trade(message)


async def main(dp):
    load_modules(dp)
    await autokursbtc_new()
    await automatisation()


if __name__ == '__main__':
    from aiogram import executor

    dp.filters_factory.bind(FilterAdmin)

    commands.basic.property.main.reg(dp)
    commands.admin.admin.reg(dp)
    commands.entertaining.earnings.farm.main.reg(dp)
    commands.entertaining.earnings.business.main.reg(dp)
    commands.entertaining.earnings.garden.main.reg(dp)
    commands.entertaining.earnings.generator.main.reg(dp)
    commands.entertaining.earnings.quarry.main.reg(dp)
    commands.basic.balance.reg(dp)
    commands.basic.status.main.reg(dp)
    commands.entertaining.earnings.tree.main.reg(dp)
    commands.basic.ore.main.reg(dp)
    commands.help.reg(dp)
    commands.entertaining.rz.reg(dp)
    commands.basic.top.reg(dp)
    commands.entertaining.wedlock.reg(dp)
    commands.clans.main.reg(dp)
    commands.admin.promo.reg(dp)

    executor.start_polling(dp, on_startup=main, skip_updates=True)

