from install import empty
import asyncio
import importlib

from utils.logger import check_log_size
from commands.admin.module_manager import load_modules
from assets.auto import automatisation
from commands.basic.ore.db import auto_rate_btc_new
from utils.settings import init_settings
from bot import bot, dp

MODULES = [
    'commands.basic.property.main',
    'commands.admin.admin',
    'commands.admin.module_manager',
    'commands.admin.promo',
    'commands.admin.updater',
    'commands.admin.text_command',
    'commands.admin.donat',
    'commands.entertaining.earnings.farm.main',
    'commands.entertaining.earnings.business.main',
    'commands.entertaining.earnings.garden.main',
    'commands.entertaining.earnings.generator.main',
    'commands.entertaining.earnings.tree.main',
    'commands.entertaining.earnings.quarry.main',
    'commands.basic.balance',
    'commands.basic.donat.main',
    'commands.basic.donat.stars',
    'commands.basic.ore.main',
    'commands.help',
    'commands.entertaining.rz',
    'commands.basic.top',
    'commands.entertaining.wedlock',
    'commands.clans.main',
    'commands.games.main',
    'commands.games.miracles',
    'commands.basic.bank.main',
    'commands.entertaining.case.main',
    'commands.entertaining.earnings.garden.potions',
    'commands.basic.transfer',
    'commands.basic.rpmod',
    'commands.main',
    'commands.moderation',
]


async def main():
    check_log_size()
    init_settings()
    load_modules(dp)
    reg_handlers()
    await auto_rate_btc_new()
    await asyncio.gather(dp.start_polling(bot), automatisation())


def reg_handlers():
    for module_path in MODULES:
        module = importlib.import_module(module_path)
        if hasattr(module, 'reg'):
            module.reg(dp)


if __name__ == '__main__':
    asyncio.run(main())
    empty()
