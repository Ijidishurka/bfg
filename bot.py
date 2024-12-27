# bot version: 2.0.0,1

import config as cfg
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(cfg.API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())