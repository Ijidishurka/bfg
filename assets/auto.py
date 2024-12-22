from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands.entertaining.earnings.farm.db import autoferma
from commands.entertaining.earnings.business.db import autobusiness
from commands.basic.ore.db import autoenergy, autokursbtc_new
from commands.basic.bank.db import autobank
from commands.entertaining.earnings.garden.db import autogarden
from commands.entertaining.earnings.generator.db import autogen
from commands.entertaining.earnings.tree.db import autotree
from commands.admin.updater import search_update, check_updates
from commands.db import reset_limit

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
    await search_update()
    await autoenergy()


async def autocommands3():
    # await autokursbtc() изменение курса на рандом число
    # Сейчас курс идет за настоящим BTC (autokursbtc_new())
    await autokursbtc_new()


async def autocommands4():
    await search_update(force=True)
    await autobank()
    await reset_limit()


async def upd_bot_username():
    bot_info = await bot.get_me()
    cfg.bot_username = bot_info.username
    await check_updates()
    await search_update()
    await reset_limit()


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
    scheduler.add_job(autocommands4, 'cron', hour=00, minute=00)
    scheduler.add_job(auto_clear, 'interval', minutes=cfg.cleaning)
    scheduler.start()