import time
from datetime import datetime

bonus_time = dict()
kazna_time = dict()
luck_time = dict()
game_time = dict()


def get_ptime(dt: int) -> str:
    dt = datetime.fromtimestamp(dt)
    current_time = datetime.now()
    delta = current_time - dt
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    def pluralize(number: int, one: str, few: str, many: str) -> str:
        if number % 10 == 1 and number % 100 != 11:
            return one
        elif 2 <= number % 10 <= 4 and (number % 100 < 10 or number % 100 >= 20):
            return few
        else:
            return many

    if days > 0:
        return f"{days} {pluralize(days, 'день', 'дня', 'дней')}"
    elif hours > 0:
        return f"{hours} {pluralize(hours, 'час', 'часа', 'часов')}"
    else:
        return f"{minutes} {pluralize(minutes, 'минута', 'минуты', 'минут')}"


async def check_time(time_dict: dict, user_id: int, utime=86400) -> tuple:
    current_time = int(time.time())
    last_time = time_dict.get(user_id, 0)

    delta_seconds = current_time - last_time
    sl = int(utime - delta_seconds)

    if sl > 0:
        return 1, sl
    else:
        time_dict[user_id] = current_time
        return 0, 0


async def bonustime(user_id: int) -> tuple:
    return await check_time(bonus_time, user_id)


async def kaznatime(user_id: int) -> tuple:
    return await check_time(kazna_time, user_id)


async def lucktime(user_id: int) -> tuple:
    return await check_time(luck_time, user_id)


async def gametime(user_id: int) -> tuple:
    return await check_time(game_time, user_id)