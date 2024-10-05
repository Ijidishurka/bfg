import asyncio
import os

import requests
from bot import dp
from aiogram import types, Dispatcher
from assets.antispam import new_earning_msg, antispam_earning
from assets.modules import MODULES, load_new_mod
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config as cfg

CATALOG = {}


def my_modules_kb(module_keys, index, user_id, mod):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(
        InlineKeyboardButton(text="‹", callback_data=f"mymodules-list_{index}_down|{user_id}"),
        InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
        InlineKeyboardButton(text="›", callback_data=f"mymodules-list_{index}_up|{user_id}")
    )
    keyboard.add(InlineKeyboardButton(text="❌ Удалить", callback_data=f"dell-modul_{mod}|{user_id}"))
    return keyboard


def load_modules_kb(module_keys, index, user_id, mod):
    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(
        InlineKeyboardButton(text="‹", callback_data=f"catalogmod-list_{index}_down|{user_id}"),
        InlineKeyboardButton(text=f"{index+1}/{len(module_keys)}", callback_data="userbotik"),
        InlineKeyboardButton(text="›", callback_data=f"catalogmod-list_{index}_up|{user_id}")
    )
    
    if mod in MODULES:
        keyboard.add(InlineKeyboardButton(text="✅ Загружен", callback_data="userbotik"))
    else:
        keyboard.add(InlineKeyboardButton(text="📥 Загрузить", callback_data=f"load-modul_{mod}|{user_id}"))
    return keyboard


async def modules_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text='🛎 Загруженые'), types.KeyboardButton(text='📂 Каталог')],
            [types.KeyboardButton(text='🔙 Назад')]
        ],
        resize_keyboard=True
    )

    await message.answer('<b>🛡 Меню модулей:</b>', reply_markup=keyboard)
    

async def load_modules(message: types.Message):
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return

    if not MODULES:
        await message.answer("У вас нет загруженых модулей.")
        return

    module_keys = list(MODULES.keys())
    mod = module_keys[0]
    
    txt = f'✨ Модуль <code>{MODULES[mod]["name"]}</code>\n<i>{MODULES[mod]["description"]}</i>'
    
    msg = await message.answer(txt, reply_markup=my_modules_kb(module_keys, 0, user_id, mod))
    await new_earning_msg(msg.chat.id, msg.message_id)
    

@antispam_earning
async def load_modules_next(call: types.CallbackQuery):
    user_id = call.from_user.id

    if not MODULES or len(MODULES) < 2:
        return

    current_index = int(call.data.split('_')[1])
    type = call.data.split('_')[2].split('|')[0]
    module_keys = list(MODULES.keys())

    if type == 'down':
        current_index = (current_index - 1) % len(module_keys)
    else:
        current_index = (current_index + 1) % len(module_keys)

    mod = module_keys[current_index]

    keyboard = InlineKeyboardMarkup(row_width=3)
    keyboard.row(
        InlineKeyboardButton(text="‹", callback_data=f"mymodules-list_{current_index}_down|{user_id}"),
        InlineKeyboardButton(text=f"{current_index+1}/{len(module_keys)}", callback_data="userbotik"),
        InlineKeyboardButton(text="›", callback_data=f"mymodules-list_{current_index}_up|{user_id}")
    )
    keyboard.add(InlineKeyboardButton(text="❌ Удалить", callback_data=f"dell-modul_{mod}|{user_id}"))

    txt = f'✨ Модуль <code>{MODULES[mod]["name"]}</code>\n<i>{MODULES[mod]["description"]}</i>'
    
    await call.message.edit_text(txt, reply_markup=my_modules_kb(module_keys, current_index, user_id, mod))


@antispam_earning
async def dell_mod(call: types.CallbackQuery):
    name = call.data.split('_')[1].split('|')[0]
    path = f'modules/{name}.py'
    
    await call.message.edit_text('<i>🚮 Удаление модуля...</i>')
    await asyncio.sleep(0.3)

    if os.path.exists(path):
        os.remove(path)
        await call.message.edit_text(f'🗑 Модуль <b>{name}</b> успешно удален!\n<i>Перезагрузите бота чтобы изменения вступили в силу</i>')
    else:
        await call.message.edit_text(f'❌ Модуль <b>{name}</b> не найден.')


async def catalog_modules(message: types.Message):
    global CATALOG
    user_id = message.from_user.id
    if user_id not in cfg.admin:
        return
    
    try:
        response = requests.get('https://raw.githubusercontent.com/Ijidishurka/bfg-modules/refs/heads/main/modules.json')
        CATALOG = response.json()
    except:
        pass
    
    if not CATALOG:
        await message.answer("Модули не найдены.")
        return
    
    module_keys = list(CATALOG.keys())
    mod = module_keys[0]
    
    txt = f'✨ Модуль <code>{CATALOG[mod]["name"]}</code>\n<i>{CATALOG[mod]["description"]}</i>'
    
    msg = await message.answer(txt, reply_markup=load_modules_kb(module_keys, 0, user_id, mod))
    await new_earning_msg(msg.chat.id, msg.message_id)


@antispam_earning
async def catalog_modules_next(call: types.CallbackQuery):
    user_id = call.from_user.id
    
    if not CATALOG or len(CATALOG) < 2:
        return
    
    current_index = int(call.data.split('_')[1])
    type = call.data.split('_')[2].split('|')[0]
    module_keys = list(CATALOG.keys())
    
    if type == 'down':
        current_index = (current_index - 1) % len(module_keys)
    else:
        current_index = (current_index + 1) % len(module_keys)
    
    mod = module_keys[current_index]
    txt = f'✨ Модуль <code>{CATALOG[mod]["name"]}</code>\n<i>{CATALOG[mod]["description"]}</i>'
    
    await call.message.edit_text(txt, reply_markup=load_modules_kb(module_keys, current_index, user_id, mod))
    
    
@antispam_earning
async def load_mod(call: types.CallbackQuery):
    name = call.data.split('_')[1].split('|')[0]
    url = CATALOG.get(name, {}).get('url', None)
    
    if not url:
        return
    
    await call.message.edit_text('<i>⚡️ Загрузка модуля...</i>')
    await asyncio.sleep(0.3)
    
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        with open(f'modules/{filename}', "wb") as file:
            file.write(response.content)
        load_new_mod(filename, dp)
        await call.message.edit_text(f'🌟 <b>Модуль {CATALOG[name]["name"]} загружен!</b>\n<i>{CATALOG[name]["description"]}</i>')
    else:
        await call.message.edit_text(f'🍎 Ошибка загрузки модуля.')
        

def reg(dp: Dispatcher):
    dp.register_message_handler(modules_menu, lambda message: message.text == '🌟 Модули')
    dp.register_message_handler(load_modules, lambda message: message.text == '🛎 Загруженые')
    dp.register_callback_query_handler(load_modules_next, text_startswith='mymodules-list_')
    dp.register_callback_query_handler(dell_mod, text_startswith='dell-modul_')
    dp.register_message_handler(catalog_modules, lambda message: message.text == '📂 Каталог')
    dp.register_callback_query_handler(catalog_modules_next, text_startswith='catalogmod-list_')
    dp.register_callback_query_handler(load_mod, text_startswith='load-modul_')