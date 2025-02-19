from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from assets.transform import transform_int as tr
from assets.antispam import antispam, admin_only
from commands.admin.admin import admin_menu_cmd
from commands.admin.db import *
from commands.admin.loger import new_log
from commands.admin import keyboards as kb
import config as cfg
from bot import bot
from user import BFGuser, BFGconst
from commands.admin.state import NewPromoState, DellPromoState, PromoInfoState


@admin_only(private=True)
async def promo_menu(message: types.Message):
    await message.answer('👾 Выберите действие:', reply_markup=kb.promo_menu())


@admin_only(private=True)
async def new_promo(message, state: FSMContext, type='name'):
    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        await message.answer("😄 Введите название промо", reply_markup=kb.cancel())
        await NewPromoState.txt.set()
        return

    if type == 'txt':
        await state.update_data(name=message.text.split()[0])
        await message.answer("📟 Введите валюту которую будет выдавать промокод (таблица/столбик эмодзи)\n\n"
                             "Пример для промо на йены: <code>users/yen 💴</code>\n\n"
                             "<i>Для создания промокода на деньги используйте '-'</i>")
        await NewPromoState.name.set()
        return

    if type == 'summ':
        txt = 'users/balance $' if message.text == '-' else message.text
        await state.update_data(txt=txt)
        await message.answer("😃 Введите сумму $ за активацию")
        await NewPromoState.summ.set()
        return

    try:
        summ = message.text.split()[0].replace('е', 'e')
        summ = int(float(summ))
    except:
        await message.answer("😔 Значение должно быть числом...")
        return

    if type == 'activ':
        await state.update_data(summ=summ)
        await message.answer("😊 Введите количество активаций")
        await NewPromoState.activ.set()
        return

    await state.update_data(activ=summ)
    data = await state.get_data()
    await state.finish()

    data2 = (data['name'], data['summ'], data['activ'], data['txt'])
    
    if (await new_promo_db(data2)):
        await message.answer("⚠️ Промокод с таким названием уже существует.")
        await admin_menu_cmd(message)
        return

    summ = tr(data['summ'])
    summ2 = tr(int(data['summ'] * data['activ']))
    activ = tr(data['activ'])
    emj = ' '.join(data['txt'].split()[1:])

    await message.answer(f'''🎰 Вы успешно создали промокод:\n
Название: <code>{data['name']}</code>
Сумма: {summ}{emj}
Активаций: {activ}\n
Общая сумма: {summ2}{emj}''')
    await admin_menu_cmd(message)


@admin_only(private=True)
async def promo_info(message, state: FSMContext, type='name'):
    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        await message.answer("💻 Введите название промо", reply_markup=kb.cancel())
        await PromoInfoState.name.set()
        return

    name = message.text.split()[0]
    res = await promo_info_db(name)
    
    if not res:
        await message.answer(f"❌ Промокод <b>{name}</b> не найден.")
    else:
        summ = tr(int(res[1]))
        emj = ' '.join(res[3].split()[1:])
        await message.answer(f'''🎰 Информация о промокоде:

Название: <code>{res[0]}</code>
Сумма: {summ}{emj}
Осталось активаций: {res[2]}''')
    await state.finish()
    await promo_menu(message)


@admin_only(private=True)
async def dell_promo(message, state: FSMContext, type='name'):
    if message.text == 'Отмена':
        await state.finish()
        await promo_menu(message)
        return

    if type == 'name':
        await message.answer("🗑 Введите название промо который вы хотите удалить", reply_markup=kb.cancel())
        await DellPromoState.name.set()
        return

    name = message.text.split()[0]
    res = await dell_promo_db(name)
    if res:
        await message.answer(f"❌ Промокод <b>{name}</b> не найден.")
    else:
        await message.answer(f"✅ Промокод <b>{name}</b> успешно удалён!")
    await state.finish()
    await promo_menu(message)


@antispam
async def activ_promo(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    
    if len(message.text.split()) < 2:
        await message.answer(f"Вы не ввели промокод {lose}")
        return
    
    try:
        chanell = await bot.get_chat_member(chat_id="@"+cfg.chanell.replace('t.me/', ''), user_id=message.from_user.id)
    
        if chanell["status"] in ['left', 'kicked']:
            await message.answer(f'Для активации промокода вам надо подписаться на <a href="{cfg.chanell}">официальный канал бота</a> {lose}\n\n{BFGconst.ads}')
            return
    except Exception as e:
        print(f'Ошибка проверки подписки на канал {e}')

    name = message.text.split()[1]
    res = await activ_promo_db(name, user.id)

    if res == 'no promo':
        await message.answer(f'Данного промокода не существует {lose}\n\n{BFGconst.ads}')
        return

    if res == 'activated':
        await message.answer(f'Данный промокод уже активирован {lose}\n\n{BFGconst.ads}')
        return

    if res == 'used':
        await message.answer(f'Вы уже активировали этот промокод {lose}\n\n{BFGconst.ads}')
        return

    summ = tr(int(res[1]))
    emj = ' '.join(res[3].split()[1:])

    await new_log(f'#промоактив\nИгрок: {message.from_user.id}\nПромо: {name}\nСумма: {summ}{emj}', 'promo')
    await message.answer(f"{user.url}, вы активировали промокод <b>{res[0]}</b>!\nПолучено: <b>{summ}</b>{emj} {win}")


def reg(dp: Dispatcher):
    dp.register_message_handler(promo_menu, lambda message: message.text == '✨ Промокоды')
    dp.register_message_handler(promo_info, lambda message: message.text == 'ℹ️ Промо инфо')
    dp.register_message_handler(lambda message, state: promo_info(message, state, type='finish'), state=PromoInfoState.name)

    dp.register_message_handler(new_promo, lambda message: message.text == '📖 Создать промо')
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='txt'), state=NewPromoState.txt)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='summ'), state=NewPromoState.name)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='activ'), state=NewPromoState.summ)
    dp.register_message_handler(lambda message, state: new_promo(message, state, type='finish'), state=NewPromoState.activ)

    dp.register_message_handler(dell_promo, lambda message: message.text == '🗑 Удалить промо')
    dp.register_message_handler(lambda message, state: dell_promo(message, state, type='finish'), state=DellPromoState.name)
    dp.register_message_handler(activ_promo, lambda message: message.text.lower().startswith('промо'))
