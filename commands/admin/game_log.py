from bot import bot
import config as cfg

# 0 - отключить логирование
# 1 - отправлять логи только в логчат
# 2 - записывать логи только в файл logs.txt
# 3 - записывать логи в файл и отправлять в логчат

promo = 3  # активация промо
money_transfers = 3  # перевод денег
issuance_money = 3  # выдача денег
issuance_bcoins = 3  # выдача бкоинов


async def new_log(txt: str, log_type: str) -> None:
    log_levels = {
        'promo': promo,
        'money_transfers': money_transfers,
        'issuance_money': issuance_money,
        'issuance_bcoins': issuance_bcoins
    }

    logging_level = log_levels.get(log_type, 0)

    if logging_level == 0:
        return

    log_message = f'новый лог: {txt}'

    if logging_level == 1 or logging_level == 3:
        try:
            await bot.send_message(chat_id=cfg.chat_log, text=log_message)
        except:
            print('указан не верный айди чата для логов')

    if logging_level == 2 or logging_level == 3:
        with open('logs.txt', 'a', encoding='utf-8') as file:
            file.write(log_message + '\n\n')
