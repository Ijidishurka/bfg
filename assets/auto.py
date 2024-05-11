from apscheduler.schedulers.asyncio import AsyncIOScheduler
from commands.earnings.farm.db import autoferma
from commands.earnings.business.db import autobusiness
from commands.ore.db import autoenergy, autokursbtc
from commands.bank.db import autobank
from commands.earnings.garden.db import autogarden
from commands.earnings.generator.db import autogen
from bot import bot
import config as cfg


scheduler = AsyncIOScheduler()


async def autocommands():
    await autoferma()
    await autobusiness()
    await autogarden()
    await autogen()


async def autocommands2():
    await autoenergy()


async def autocommands3():
    await autokursbtc()


async def autocommands4():
    await autobank()


async def upd_bot_username():
    bot_info = await bot.get_me()
    cfg.bot_username = bot_info.username


async def automatisation():
    await upd_bot_username()
    scheduler.add_job(autocommands, 'interval', hours=1)
    scheduler.add_job(autocommands2, 'interval', minutes=15)
    scheduler.add_job(autocommands3, 'interval', seconds=5)
    scheduler.add_job(autocommands4, 'interval', hours=24)
    scheduler.start()