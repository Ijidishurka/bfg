import time
import os


def cprint(text, color_hex):
    print("\033[38;2;{};{};{}m{}\033[0m".format(*tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4)), text))


def cinput(text, color_hex):
    print("\033[38;2;{};{};{}m{}\033[0m".format(*tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4)), text))
    return input()


def main(a='n'):
    cprint("Настройка BFG", "FF0000")
    time.sleep(0.5)
    cprint("Наш канал - @copybfg", "21db53")

    if chek_config():
        a = cinput("Вы уверены что хотите удалить файл config.py и создать новый? Y/n", "FF9004")

    load_cfg(a)


def load_cfg(a):
    if a.lower() not in ['y', 'yes', 'да', 'д']:
        if chek_config():
            return cprint("Конфиг найден! Можете запускать бота.", "FF0000")
        else:
            cprint("Конфиг не найден! Создаю новый.", "FF0000")
            return load_cfg('y')

    name = cinput("Введите имя вашего бота", "FF9004")
    start_money = cinput("Введите начальный баланс", "FF9004")
    admin = cinput("Введите айди админа", "FF9004")
    token = cinput("Введите токен бота", "FF9004")
    adm_username = cinput("Введите юзернейм админа", "FF9004")
    chat = cinput("Введите ссылку на официальный чат бота", "FF9004")
    chanell = cinput("Введите ссылку на официальный канал бота", "FF9004")

    data = (token, admin, start_money, name, chat, chanell, adm_username)
    cheker(data)


def cheker(data):
    cprint("\nСохраняю...", "FF0000")

    try:
        create_config_file(data)
        cprint("Конфиг успешно сохранён.", "FF0000")
    except Exception as e:
        cprint(f"Произошла ошибка при сохранении конфига: {e}", "FF0000")


def create_config_file(data):
    config_template = """API_TOKEN = '<edit>'

admin = [<edit>]
start_money = <edit>

bot_name = '<edit>'
chat = '<edit>'
chanell = '<edit>'
admin_username = '<edit>'
bot_username = 'bfgcopybot'

chat_log = 0
cleaning = 60"""

    replacements = [str(value) for value in data]

    for replacement in replacements:
        config_template = config_template.replace('<edit>', replacement, 1)

    with open('config.py', 'w', encoding='utf-8') as f:
        f.write(config_template)


def chek_config():
    if not os.path.isfile('config.py'):
        return False
    return True


def main_chek():
    if not os.path.isfile('config.py'):
        a = cinput("Файл config.py не найден.\nХотите создать его сейчас? Y/n", "FF0000")
        if a.lower() in ['y', 'yes', 'да', 'д']:
            cprint("Для создания конфига вам нужно ответить на пару вопросов!", "f59b42")
            time.sleep(0.5)
            main()
    else:
        return True
    

def update_db():
    ...


if __name__ == '__main__':
    main()
else:
    main_chek()
