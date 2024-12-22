import install
import asyncio
import os
import requests
from bot import dp
from aiogram import types, Dispatcher
from assets.antispam import new_earning_msg, antispam_earning, admin_only
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from commands.admin import keyboards as kb
import config as cfg

MODULES = {}
CATALOG = {}
MOD_TYPE = 'games'


def load_modules(dp):
    """Загрузка модулей при включении бота"""
    txt, mlist = 0, []
    
    for filename in os.listdir('modules'):
        if filename.endswith(".py") and filename != "__init__.py" and not filename.startswith("add"):
            fmodule_name = filename[:-3]
            module = __import__(f"modules.{fmodule_name}", fromlist=["register_handlers"])
            module.register_handlers(dp)
            txt += 1
            
            if hasattr(module, 'MODULE_DESCRIPTION'):
                module_info = module.MODULE_DESCRIPTION
                module_name = module_info.get('name', 'Без названия')
                module_description = module_info.get('description', 'Нет описания')
                mlist.append(module_name)
                MODULES[fmodule_name] = {'name': module_name, 'description': module_description}
    
    if txt > 0:
        mlist = ', '.join(mlist)
        print(f'Загрузка модулей "{mlist}"')
        print(f'Импортировано {txt} модулей.')


def load_new_mod(filename, dp):
    """Регестрация хандлеров нового модуля (при загрузке командой)"""
    if filename.endswith(".py") and filename != "__init__.py" and not filename.startswith("add"):
        fmodule_name = filename[:-3]
        module = __import__(f"modules.{fmodule_name}", fromlist=["register_handlers"])
        module.register_handlers(dp)
        
        if hasattr(module, 'MODULE_DESCRIPTION'):
            module_info = module.MODULE_DESCRIPTION
            module_name = module_info.get('name', 'Без названия')
            module_description = module_info.get('description', 'Нет описания')
            MODULES[fmodule_name] = {'name': module_name, 'description': module_description}


@admin_only(private=True)
async def modules_menu(message: types.Message):
    await message.answer('<b>🛡 Меню модулей:</b>', reply_markup=kb.modules_menu())
    

@admin_only(private=True)
async def load_modules_cmd(message: types.Message):
    user_id = message.from_user.id
    if not MODULES:
        await message.answer("У вас нет загруженых модулей.")
        return

    module_keys = list(MODULES.keys())
    mod = module_keys[0]
    
    txt = f'✨ Модуль <code>{MODULES[mod]["name"]}</code>\n<i>{MODULES[mod]["description"]}</i>'
    
    msg = await message.answer(txt, reply_markup=kb.my_modules_kb(module_keys, 0, user_id, mod))
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
    
    await call.message.edit_text(txt, reply_markup=kb.my_modules_kb(module_keys, current_index, user_id, mod))


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


@admin_only(private=True)
async def catalog_modules(message: types.Message):
    user_id = message.from_user.id
    global CATALOG
    
    try:
        response = requests.get('https://raw.githubusercontent.com/Ijidishurka/bfg-modules/refs/heads/main/modules.json')
        CATALOG = response.json()
    except:
        pass
    
    if not CATALOG:
        await message.answer("Модули не найдены.")
        return
    
    txt = '🌟 Выберите тип модулей:'
    colvo = (len(CATALOG['games']), len(CATALOG['events']), len(CATALOG['other']), len(CATALOG['system']))
    
    msg = await message.answer(txt, reply_markup=kb.load_modules_type(user_id, colvo))
    await new_earning_msg(msg.chat.id, msg.message_id)


@antispam_earning
async def catalog_type(call: types.CallbackQuery):
    global MOD_TYPE
    MOD_TYPE = call.data.split('_')[1].split('|')[0]
    user_id = call.from_user.id
    
    if len(CATALOG[MOD_TYPE]) == 0:
        return
    
    module_keys = list(CATALOG[MOD_TYPE].keys())
    mod = CATALOG[MOD_TYPE][module_keys[0]]
    name = list(CATALOG[MOD_TYPE].keys())[0]

    txt = f'✨ Модуль <code>{mod["name"]}</code>\n<i>{mod["description"]}</i>'

    await call.message.edit_text(txt, reply_markup=kb.load_modules_kb(module_keys, 0, user_id, name, MODULES))
    

@antispam_earning
async def catalog_modules_next(call: types.CallbackQuery):
    user_id = call.from_user.id
    
    if not CATALOG[MOD_TYPE] or len(CATALOG[MOD_TYPE]) < 2:
        return
    
    current_index = int(call.data.split('_')[1])
    type = call.data.split('_')[2].split('|')[0]
    module_keys = list(CATALOG[MOD_TYPE].keys())
    
    if type == 'down':
        current_index = (current_index - 1) % len(module_keys)
    else:
        current_index = (current_index + 1) % len(module_keys)

    mod = CATALOG[MOD_TYPE][module_keys[current_index]]
    name = list(CATALOG[MOD_TYPE].keys())[current_index]
    txt = f'✨ Модуль <code>{mod["name"]}</code>\n<i>{mod["description"]}</i>'
    
    await call.message.edit_text(txt, reply_markup=kb.load_modules_kb(module_keys, current_index, user_id, name, MODULES))
    
    
@antispam_earning
async def load_mod(call: types.CallbackQuery):
    name = call.data.split('_')[1].split('|')[0]
    url = CATALOG[MOD_TYPE].get(name, {}).get('url', None)
    
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
        await call.message.edit_text(f'🌟 <b>Модуль {CATALOG[MOD_TYPE][name]["name"]} загружен!</b>\n<i>{CATALOG[MOD_TYPE][name]["description"]}</i>')
    else:
        await call.message.edit_text(f'🍎 Ошибка загрузки модуля.')
        
        
@admin_only(private=True)
async def load_mod_cmd(message: types.Message):
    try:
        url = message.text.split()[1:]
        url = ''.join(url)

        msg = await message.answer('<i>⚡️ Загрузка модуля...</i>')
        await asyncio.sleep(0.3)
    
        response = requests.get(url)
        if response.status_code == 200:
            filename = url.split('/')[-1]
            with open(f'modules/{filename}', "wb") as file:
                file.write(response.content)
            load_new_mod(filename, dp)
            await msg.edit_text(f'🌟 Модуль {url} загружен')
        else:
            await msg.edit_text('🍎 Ошибка загрузки модуля.')
    except:
        await message.answer('🍎 Ошибка загрузки модуля.')


def reg(dp: Dispatcher):
    dp.register_message_handler(modules_menu, lambda message: message.text == '🌟 Модули')
    dp.register_message_handler(load_modules_cmd, lambda message: message.text == '🛎 Загруженые')
    dp.register_callback_query_handler(load_modules_next, text_startswith='mymodules-list_')
    dp.register_callback_query_handler(dell_mod, text_startswith='dell-modul_')
    dp.register_message_handler(catalog_modules, lambda message: message.text == '📂 Каталог')
    dp.register_callback_query_handler(catalog_type, text_startswith='mod-catalog_')
    dp.register_callback_query_handler(catalog_modules_next, text_startswith='catalogmod-list_')
    dp.register_callback_query_handler(load_mod, text_startswith='load-modul_')
    dp.register_message_handler(load_mod_cmd, lambda message: message.text.startswith('/loadmodb '))