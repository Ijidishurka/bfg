from aiogram import types, Dispatcher

from assets.antispam import new_earning, antispam, antispam_earning
from assets.transform import transform_int as tr
from commands.entertaining.earnings.quarry import db
from assets import keyboards as kb
from filters.custom import StartsWith, TextIn
from user import BFGuser, BFGconst


@antispam
async def quarry_list(message: types.Message):
    await message.answer(f'''Привет! 🚀 Готов покорить мир карьеров?

🛠 Построй свой первый карьер всего за 25 палладия! Для этого напиши "<code>Построить карьер</code>". Палладий можно получить, открыв рудные кейсы.

🌄 Как только карьер будет построен:
1. Начни добычу ресурсов.
2. Улучшай буровые установки, чтобы увеличивать добычу.
3. Расширяй территорию карьера для установки нового оборудования.

📈 Введи "Мой карьер", чтобы посмотреть статистику и доступные улучшения.

❓ Нужна помощь или хочешь узнать все команды? Введи "<code>Помощь</code>" и выбери раздел "<code>Развлекательные</code>".''')


@antispam
async def my_quarry(message: types.Message, user: BFGuser):
    quarry = user.quarry
    win, lose = BFGconst.emj()
    
    if not quarry:
        await message.answer(f'{user.url}, у вас нет своего карьера. Введите команду "Построить карьер" {lose}')
        return
    
    await edit_quarry_msg(message, user, action='send')


async def edit_quarry_msg(call: types.CallbackQuery | types.Message, user: BFGuser, action='edit') -> None:
    quarry = user.quarry
    
    if action == 'edit':
        await user.update()

    ter_upd = quarry.territory.get() * 130
    bur_upd = quarry.bur.get() * 166

    txt = f'''
{user.url}, информация о вашем карьере "Карьер":
🔧 Уровень: {quarry.lvl}
🧱 Размер территории: {quarry.territory.tr()}м²
🆙 для следующего уровня: {tr(ter_upd)} 🧪
🕳 Количество буровых установок: {quarry.bur.tr()}
🆙 для следующего уровня: {tr(bur_upd)} ⚙

💸 Налоги: {quarry.nalogs.tr()}/5.000.000$'''
    
    try:
        if action == 'edit':
            await call.message.edit_text(text=txt, reply_markup=kb.quarry(user.id))
        else:
            msg = await call.answer(text=txt, reply_markup=kb.quarry(user.id))
            await new_earning(msg)
    except:
        return


@antispam
async def buy_quarry(message: types.Message, user: BFGuser):
    quarry = user.quarry
    win, lose = BFGconst.emj()
    
    if quarry:
        await message.answer(f'{user.url}, у вас уже есть построенный карьер. Чтобы узнать подробнее, введите "Мой карьер" {lose}')
        return

    if int(user.mine.palladium) < 25:
        await message.answer(f'{user.url}, у вас недостаточно палладия для постройки карьера. Его стоимость 25 палладия {lose}')
        return
    
    await db.buy_quarry(user.id)
    await message.answer(f'{user.url}, вы успешно построили карьер для подробностей введите "Мой карьер" {win}')


@antispam_earning
async def withdraw_profit(call: types.CallbackQuery, user: BFGuser):
    quarry = user.quarry
    win, lose = BFGconst.emj()

    if not quarry:
        return

    if int(quarry.balance) == 0:
        await call.answer(f'{user.name}, на данный момент на балансе вашего карьера нету прибыли {lose}')
        return

    await db.withdraw_profit(user.id, quarry.balance.get())
    await call.answer(f'{user.name}, вы успешно сняли {quarry.balance.tr()}⚗️ с баланса вашего карьера {win}')
    await edit_quarry_msg(call, user)


@antispam_earning
async def payment_taxes(call: types.CallbackQuery, user: BFGuser):
    quarry = user.quarry
    win, lose = BFGconst.emj()

    if not quarry:
        return

    if int(user.balance) < int(quarry.nalogs):
        await call.answer(f'{user.name}, у вас недостаточно денег чтоб оплатить налоги {lose}')
        return

    if int(quarry.nalogs) == 0:
        await call.answer(f'{user.name}, у вас нет налогов чтобы их оплатить {win}')
        return

    await db.payment_taxes(user.id, quarry.nalogs.get())
    await call.answer(f'{user.name}, вы успешно оплатили налоги на сумму {quarry.nalogs.tr()}$ с вашего игрового баланса {win}')
    await edit_quarry_msg(call, user)


@antispam_earning
async def up_level(call: types.CallbackQuery, user: BFGuser):
    await call.answer(f'{user.name}, на данный момент у Вас максимальный уровень карьера.')


# @antispam
# async def sell_quarry(message: types.Message, user: BFGuser):
#     win, lose = BFGconst.emj()
#     quarry = user.quarry
#
#     if not quarry:
#         await message.answer(f'{user.url}, у вас нет своего генератора {lose}')
#         return
#
#     palladium = 25
#     cobalt = titanium = 0
#
#     cobalt = (1000 * quarry.territory.get())
#
#     await db.sell_quarry(user.id, summ)
#     await message.answer(f'{user.url}, Вы успешно продали свой карьер, получено {palladium}⚗️, {cobalt}🧪 и {titanium}⚙️ {win}')
    

def reg(dp: Dispatcher):
    dp.message.register(my_quarry, TextIn("мой карьер"))
    dp.message.register(quarry_list, TextIn("карьер"))
    dp.message.register(buy_quarry, TextIn("построить карьер"))
    dp.callback_query.register(withdraw_profit, StartsWith("quarry-sobrat"))
    dp.callback_query.register(payment_taxes, StartsWith("quarry-nalog"))
    dp.callback_query.register(up_level, StartsWith("quarry-lvl"))
