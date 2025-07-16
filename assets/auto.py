from apscheduler.schedulers.asyncio import AsyncIOScheduler

from commands.entertaining.earnings.farm.db import autoferma
from commands.entertaining.earnings.business.db import autobusiness
from commands.entertaining.earnings.garden.db import autogarden
from commands.entertaining.earnings.generator.db import autogen
from commands.entertaining.earnings.tree.db import autotree
from commands.basic.ore.db import auto_energy, auto_rate_btc_new
from commands.basic.bank.db import autobank
from commands.admin.updater import search_update, check_updates
from commands.db import reset_limit, update_ads_const

from bot import bot
import config as cfg


scheduler = AsyncIOScheduler()


async def autocommands() -> None:
    """Каждый час"""
    try:
        await autoferma()
        await autobusiness()
        await autogarden()
        await autogen()
        await autotree()
    except Exception as e:
        print(f'error autocommands: {e}')


async def autocommands2() -> None:
    """Каждые 15 минут"""
    await search_update()
    await auto_energy()


async def autocommands3() -> None:
    """Каждые 5 минут"""
    # await autokursbtc() изменение курса на рандом число
    # Сейчас курс идет за настоящим BTC (autokursbtc_new())
    await auto_rate_btc_new()


async def autocommands4() -> None:
    """Каждый день в 00:00"""
    await search_update(force=True)
    await autobank()
    await reset_limit()


async def upd_bot_username() -> None:
    """Выполняется при запуске бота"""
    bot_info = await bot.get_me()
    cfg.bot_username = bot_info.username
    await check_updates()
    await search_update()
    await update_ads_const()


async def automatisation() -> None:
    """Запуск задач"""
    await upd_bot_username()
    scheduler.add_job(autocommands, 'interval', hours=1)
    scheduler.add_job(autocommands2, 'interval', minutes=15)
    scheduler.add_job(autocommands3, 'interval', minutes=5)
    scheduler.add_job(autocommands4, 'cron', hour=00, minute=00)
    scheduler.start()
    