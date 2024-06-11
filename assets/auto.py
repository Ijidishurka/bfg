import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands.earnings.farm.db import autoferma
from commands.earnings.business.db import autobusiness
from commands.ore.db import autoenergy, autokursbtc_new
from commands.bank.db import autobank
from commands.earnings.garden.db import autogarden
from commands.earnings.generator.db import autogen
from commands.earnings.tree.db import autotree

from bot import bot
import config as cfg
from assets.antispam import earning_msg


scheduler = AsyncIOScheduler()


async def autocommands():
    try:
        await autoferma()
        await autobusiness()
        await autogarden()
        await autogen()
        await autotree()
    except:
        print('error autocommands')


async def autocommands2():
    await autoenergy()


async def autocommands3():
    # await autokursbtc() изменение курса на рандом число
    # Сейчас курс идет за настоящим BTC
    await autokursbtc_new()


async def autocommands4():
    await autobank()


async def upd_bot_username():
    bot_info = await bot.get_me()
    cfg.bot_username = bot_info.username


async def auto_clear():
    dt = int(datetime.now().timestamp())
    keys_to_delete = []

    for key, value in earning_msg.items():
        if int(dt - 500) > int(value[1]):
            keys_to_delete.append(key)

    for key in keys_to_delete:
        earning_msg.pop(key, None)


async def automatisation():
    await upd_bot_username()
    scheduler.add_job(autocommands, 'interval', hours=1)
    scheduler.add_job(autocommands2, 'interval', minutes=15)
    scheduler.add_job(autocommands3, 'interval', minutes=5)
    scheduler.add_job(autocommands4, 'interval', hours=24)
    scheduler.add_job(auto_clear, 'interval', minutes=cfg.cleaning)
    scheduler.start()