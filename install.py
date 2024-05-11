import time
import os


def cprint(text, color_hex):
    print("\033[38;2;{};{};{}m{}\033[0m".format(*tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4)), text))


def cinput(text, color_hex):
    print("\033[38;2;{};{};{}m{}\033[0m".format(*tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4)), text))
    a = input("\033[38;2;{};{};{}m{}\033[0m".format(*tuple(int('59c3e3'[i:i + 2], 16) for i in (0, 2, 4)), '> '))
    return a


def main():
    cprint("Настройка BFG", "FF00000")
    time.sleep(0.5)
    cprint("Наш канал - @copybfg", "21db53")

    a = cinput("Вы уверены что хотите удалить файл <config> и создать новый? Y/n", "FF90044")
    load_cfg(a)


def load_cfg(a):
    if a.lower() not in ['y', 'yes', 'да', 'д']:
        cprint("Поиск конфига...", "FF00000")
        time.sleep(1)
        res = chek_config()
        if res:
            return cprint("Конифг найден! Можете запускать бота.", "FF00000")
        else:
            cprint("Конфиг не найден! Создаю новый.", "FF00000")
            return load_cfg('y')

    name = cinput("Введите имя вашего бота", "FF90044")
    start_money = cinput("Введите начальный баланс", "FF90044")
    admin = cinput("Введите айди админа", "FF90044")
    token = cinput("Введите токен бота", "FF90044")
    adm_username = cinput("Введите юзерйнем админа", "FF90044")
    chat = cinput("Введите ссылку на официальный чат бота", "FF90044")
    chanell = cinput("Введите ссылку на официальный канал бота", "FF90044")

    confirm = cinput(
        f"Все данные введены правильно?\n * Имя бота: {name}\n * Начальный баланс: {start_money}\n * Айди админа: {admin}\n * Токен бота: {token}"
        f"\n * Юз админа: {adm_username}\n * Чат: {chat}\n * Канал: {chanell}\nВведите Y чтобы продолжить, n чтобы ввести данные заново.",
        "FF90044")

    data = (token, admin, start_money, name, chat, chanell, adm_username)

    cheker(confirm, data)


def cheker(a, data):
    if a not in ['y', 'yes', 'да', 'д']:
        return load_cfg('да')

    cprint("\nСохраняю...", "FF00000")
    create_config_file(data)
    cprint("Конфиг успешно сохранён.", "FF00000")


def create_config_file(data):
    config_template = """API_TOKEN = '<edit>'

admin = [<edit>]
start_money = <edit>

bot_name = '<edit>'
chat = '<edit>'
chanell = '<edit>'
admin_username = '<edit>'
bot_username = 'bfgcopybot'

chat_log = 0"""

    replacements = [str(value) for value in data]

    for replacement in replacements:
        config_template = config_template.replace('<edit>', replacement, 1)

    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_template)


def chek_config():
    if not os.path.isfile('config.py'):
        a = cinput("Файл config.py не найден.\nХотите создать его сейчас? Y/n", "FF00000")
        if a in ['y', 'yes', 'да', 'д']:
            cprint("Для создания конфига вам нужно ответить на пару вопросов...", "f59b42")
            time.sleep(0.5)
            main()
    else:
        return True


if __name__ == '__main__':
    main()
else:
    chek_config()