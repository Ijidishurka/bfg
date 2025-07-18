# bot version: 3.0.0,2
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

import config as cfg


bot = Bot(token=cfg.API_TOKEN, default=DefaultBotProperties(parse_mode='html', link_preview_is_disabled=True))
dp = Dispatcher(storage=MemoryStorage())
