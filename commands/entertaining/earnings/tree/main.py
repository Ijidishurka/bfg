from aiogram import types, Dispatcher

from commands.entertaining.earnings.tree import db
from assets.transform import transform_int as tr
from assets import kb
from assets.antispam import new_earning, antispam, antispam_earning
from user import BFGuser, BFGconst


@antispam
async def tree_cmd(message: types.Message, user: BFGuser):
    await message.answer('''🌳 Добро пожаловать в новую возможность заработка - денежное дерево! Теперь, помимо управления своим бизнесом, у вас есть шанс выращивать деньги прямо на своем участке.

🏡 Для начала вам нужно создать участок под ваше денежное дерево. Используйте команду "Построить участок", чтобы купить небольшой участок земли для вашего нового источника дохода.

💰 Далее вы сможете улучшать ваше денежное дерево, используя биоресурсы. Чем больше улучшений, тем больше денег оно будет приносить.

🌟 Не забывайте, что управление вашим денежным деревом поможет вам увеличить доход и достичь финансового успеха. Чтобы узнать все доступные команды, введите "Помощь" и выберите соответствующий раздел.''')


@antispam
async def my_tree(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if not tree:
        await message.answer(f'{user.url}, у вас нет своего участка денежного дерева {lose}')
        return

    await edit_tree_msg(message, user, action='send')


async def edit_tree_msg(call: types.CallbackQuery | types.Message, user: BFGuser, action='edit') -> None:
    tree = user.tree
    
    if action == 'edit':
        await user.update()

    profit = int(3000 * (tree.tree.get() ** 3.8))
    tre_price = int(5000 * (tree.tree.get() ** 3.8))
    ter_price = int(5000 * (tree.territory.get() ** 3.8))

    txt = f'''{user.url}, информация о вашем участке "Денежное дерево":
🏡 Участок: {tree.territory} м²
🆙 для следующего уровня: {tr(ter_price)} ☣️
🌳 Размер дерева: {tree.tree} м
🆙 для следующего уровня: {tr(tre_price)} ☣️

💷 Доход: {tr(profit)}$
💸 Налоги: {tree.nalogs.tr()}$/5.000.000$
💰 Прибыль: {tree.balance.tr()}$
💴 Йены: {tree.yen.tr()}¥'''
    
    try:
        if action == 'edit':
            await call.message.edit_text(text=txt, reply_markup=kb.tree(user.id))
        else:
            msg = await call.answer(text=txt, reply_markup=kb.tree(user.id))
            await new_earning(msg)
    except:
        return


@antispam
async def buy_tree(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if tree:
        await message.answer(f'{user.url}, у вас уже есть свой участок. Для подробностей введите "Моё дерево" {win}')
        return

    if int(user.biores) < 500_000_000:
        await message.answer(f'{user.url}, у вас недостаточно биоресурсов для постройки участка денежного дерева. '
                             f'Его стоимость 500.000.000 кг биоресурса {lose}')
        return

    await db.buy_tree(user.id)
    await message.answer(f'{user.url}, вы успешно построили свой участок для подробностей введите "Моё дерево" {win}')


@antispam_earning
async def withdraw_profit(call: types.CallbackQuery, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if not tree:
        return

    if int(tree.balance) <= 0 and int(tree.yen) <= 0:
        await call.answer(f'{user.name}, на данный момент на балансе вашего участка нет прибыли {lose}')
        return

    await db.withdraw_profit(user.id, tree.balance.get(), tree.yen.get())
    await call.answer(f'{user.name}, вы успешно сняли {tree.balance.tr()}$ и {tree.yen.tr()}¥ с баланса вашего участка {win}')
    await edit_tree_msg(call, user)


@antispam_earning
async def pay_taxes(call: types.CallbackQuery, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if not tree:
        return

    if int(user.balance) < int(tree.nalogs):
        await call.answer(f'{user.name}, у вас недостаточно денег чтоб оплатить налоги {lose}')
        return

    if int(tree.nalogs) <= 0:
        await call.answer(f'{user.name}, у вас нет налогов чтобы их оплатить {win}')
        return

    await db.pay_taxes(user.id, tree.nalogs.get())
    await call.answer(f'{user.name}, вы успешно оплатили налоги на сумму {tree.nalogs.tr()}$ с вашего игрового баланса {win}')
    await edit_tree_msg(call, user)


@antispam_earning
async def buy_ter(call: types.CallbackQuery, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if not tree:
        return

    summ = int(5000 * (tree.territory.get() ** 3.8))

    if int(user.biores) < summ:
        await call.answer(f'{user.name}, у вас недостаточно биоресурсов {lose}')
        return

    await db.buy_ter(user.id, summ)
    await call.answer(f'{user.name}, вы успешно увеличили участок за {tr(summ)}☣️ {win}')
    await edit_tree_msg(call, user)


@antispam_earning
async def buy_tree_call(call: types.CallbackQuery, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree

    if not tree:
        return

    summ = int(5000 * (tree.tree.get() ** 3.8))

    if int(user.balance) < summ:
        await call.answer(f'{user.name}, у вас недостаточно биоресурсов {lose}')
        return

    if int(tree.territory) <= int(tree.tree):
        await call.answer(f'{user.name}, у вас недостаточно места {lose}')
        return

    await db.buy_tree_ter(user.id, summ)
    await call.answer(f'{user.name}, вы успешно увеличили дерево за {tr(summ)}☣️ {win}')
    await edit_tree_msg(call, user)


@antispam
async def sell_tree(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()
    tree = user.tree
    
    if not tree:
        await message.answer(f'{user.url}, у вас нет своего участка денежного дерева {lose}')
        return

    summ = 250_000_000  # Половина стоимости дерева
    
    for i in range(1, tree.tree.get() + 1):  # Компенсация за деревья (50%)
        summ += int(5000 * (tree.tree.get() ** 3.8)) // 2

    for i in range(1, tree.territory.get() + 1):  # Компенсация за территорию (50%)
        summ += int(5000 * (tree.territory.get() ** 3.8)) // 2
    
    await db.sell_tree(user.id, summ)
    await message.answer(f'{user.url}, Вы успешно продали своё денежное дерево за {tr(summ)}☣️ {win}')


def reg(dp: Dispatcher):
    dp.register_message_handler(tree_cmd, lambda message: message.text.lower() == 'денежное дерево')
    dp.register_message_handler(my_tree, lambda message: message.text.lower() in ['моё дерево', 'мое дерево'])
    dp.register_message_handler(buy_tree, lambda message: message.text.lower() == 'построить участок')
    dp.register_callback_query_handler(withdraw_profit, text_startswith='tree-sobrat')
    dp.register_callback_query_handler(pay_taxes, text_startswith='tree-nalog')
    dp.register_callback_query_handler(buy_tree_call, text_startswith='tree-tree')
    dp.register_callback_query_handler(buy_ter, text_startswith='tree-ter')
    dp.register_message_handler(sell_tree, lambda message: message.text.lower() == 'Продать участок')
