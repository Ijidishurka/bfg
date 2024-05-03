from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from commands.earnings.farm.db import autoferma
from commands.earnings.business.db import autobusiness
from commands.ore.db import autoenergy, autokursbtc
from commands.bank.db import autobank
from commands.earnings.garden.db import autogarden

scheduler = AsyncIOScheduler()

async def autocommands4(message):
    await autobank()

async def autocommands3(message):
    await autokursbtc()

async def autocommands2(message):
    await autoenergy()

async def autocommands(message):
    await autoferma()
    await autobusiness()
    await autogarden()

def add_scheduled_job(scheduler, func, interval, message):
    scheduler.add_job(func, 'interval', args=(message,), minutes=interval.total_seconds() // 60)

async def automatisation():
    scheduler = AsyncIOScheduler()
    add_scheduled_job(scheduler, autocommands, timedelta(hours=1), "Ферма/бизнес/сад")
    add_scheduled_job(scheduler, autocommands2, timedelta(minutes=15), "Энергия")
    add_scheduled_job(scheduler, autocommands3, timedelta(seconds=10), "курс BTC")
    add_scheduled_job(scheduler, autocommands4, timedelta(minutes=15), "Банк")
    scheduler.start()