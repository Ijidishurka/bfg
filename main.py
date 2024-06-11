# YT: userbotik
import install
from config import *
from commands.main import *
from commands.help import *
from commands.rz import *
from commands.transfer import *
from commands.games.games import *
from assets.auto import automatisation
from commands.ore.btcs import *
from commands.ore.dig import *
from commands.ore.rating import *
from commands.case.main import *
from commands.case.buy import *
from commands.bank.main import *
from commands.earnings.garden.potions import *
from assets.modules import *
from commands.admin.promo import activ_promo
from bot import dp

import commands.property.main
import commands.admin.admin
import commands.property.buy
import commands.earnings.farm.main
import commands.earnings.business.main
import commands.earnings.garden.main
import commands.earnings.generator.main
import commands.earnings.tree.main
import commands.earnings.quarry.main
import commands.balance
import commands.status.main
import commands.status.buy_status


@dp.message_handler(commands=['start'])
async def on_start_s(message: types.Message):
    await on_start(message)


@dp.message_handler(lambda message: message.text in ['помощь', 'Помощь', '/help'])
async def help_cmd_s(message: types.Message):
    await help_cmd(message)


@dp.message_handler(lambda message: message.text in ['топ', 'Топ'])
async def top_command_s(message: types.Message):
    await top_command(message)


@dp.message_handler(lambda message: message.text in ['казна', 'Казна'])
async def kazna_cmd_s(message: types.Message):
    await kazna_cmd(message)


@dp.message_handler(lambda message: message.text in ['статистика бота', 'Статистика бота'])
async def stats_cmd_s(message: types.Message):
    await stats_cmd(message)


@dp.message_handler(lambda message: message.text in ['энергия', 'Энергия'])
async def energy_cmd_s(message: types.Message):
    await energy_cmd(message)


@dp.message_handler(lambda message: message.text in ['рейтинг', 'Рейтинг'])
async def rrating_cmd_s(message: types.Message):
    await rrating_cmd(message)


@dp.message_handler(lambda message: message.text in ['!Беседа', '!беседа'])
async def chat_list_s(message: types.Message):
    await chat_list(message)


@dp.message_handler(lambda message: message.text in ['банк', 'Банк'])
async def bank_cmd_s(message: types.Message):
    await bank_cmd(message)


@dp.message_handler(lambda message: message.text in ['мой лимит', 'Мой лимит'])
async def limit_cmd_s(message: types.Message):
    await limit_cmd(message)


@dp.message_handler(lambda message: message.text in ['мой ник', 'Мой ник'])
async def myname_cmd_s(message: types.Message):
    await myname_cmd(message)


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


@dp.message_handler(lambda message: message.text.lower().startswith('ограбить мэрию') or message.text.lower().startswith('ограбить казну'))
async def ogr_kazna_s(message: types.Message):
    await ogr_kazna(message)


@dp.message_handler(lambda message: message.text.lower().startswith('продать рейтинг'))
async def sellrating_s(message: types.Message):
    await sellrating(message)


@dp.message_handler(lambda message: message.text.lower().startswith('продать биткоин') or message.text.lower().startswith('биткоин продать'))
async def sellbtc_s(message: types.Message):
    await sellbtc(message)


@dp.message_handler(lambda message: message.text.lower().startswith('купить биткоин') or message.text.lower().startswith('биткоин купить'))
async def buybtc_s(message: types.Message):
    await buybtc(message)


@dp.message_handler(lambda message: message.text.lower().startswith('курс биткоин') or message.text.lower().startswith('биткоин курс'))
async def btc_kurs_s(message: types.Message):
    await btc_kurs(message)


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


@dp.message_handler(lambda message: message.text in ['Ежедневный бонус', 'ежедневный бонус'])
async def bonus_cmd_s(message: types.Message):
    await bonus_cmd(message)


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


@dp.message_handler(lambda message: message.text.startswith("шар ") or message.text.startswith("Шар "))
async def shar_cmd_s(message: types.Message):
    await shar_cmd(message)


@dp.message_handler(lambda message: message.text.startswith("сменить ник") or message.text.startswith("Сменить ник"))
async def setname_cmd_s(message: types.Message):
    await setname_cmd(message)


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


@dp.message_handler(lambda message: message.text.lower().startswith("испытать удачу"))
async def try_luck_s(message: types.Message):
    await try_luck(message)


async def main(dp):
    load_modules(dp)
    await autokursbtc_new()
    await automatisation()


if __name__ == '__main__':
    from aiogram import executor

    commands.property.main.reg(dp)
    commands.property.buy.reg(dp)
    commands.admin.admin.reg(dp)
    commands.earnings.farm.main.reg(dp)
    commands.earnings.business.main.reg(dp)
    commands.earnings.garden.main.reg(dp)
    commands.earnings.generator.main.reg(dp)
    commands.earnings.quarry.main.reg(dp)
    commands.balance.reg(dp)
    commands.status.buy_status.reg(dp)
    commands.status.main.reg(dp)
    commands.earnings.tree.main.reg(dp)

    executor.start_polling(dp, on_startup=main, skip_updates=True)

