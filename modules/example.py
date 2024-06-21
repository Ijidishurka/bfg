from aiogram import types
from aiogram.dispatcher import Dispatcher
import random


async def start(message: types.Message):
	await message.answer('привет')


async def botyara(message: types.Message):
	random_message = random.choice(["Я тут 😊", "На месте 👍", "Работает 💻"])
	await message.reply(random_message)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, lambda message: message.text.lower().startswith('привет'))
    dp.register_message_handler(botyara, lambda message: message.text.lower().startswith('ботяра'))
