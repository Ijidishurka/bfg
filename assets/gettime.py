from datetime import datetime

bonus_time = dict()
kazna_time = dict()
luck_time = dict()


async def bonustime(id):
    utime = 86400
    dnow = datetime.now()
    last = bonus_time.get(id)

    if not last:
        bonus_time[id] = dnow
        last = datetime.fromtimestamp(0)
    if last:
        delta_seconds = (dnow - last).total_seconds()
        sl = int(utime - delta_seconds)

        if sl > 0:
            left = sl
            return 1, left
        else:
            bonus_time[id] = dnow
            return 0, 0


async def kaznatime(id):
    utime = 86400
    dnow = datetime.now()
    last = kazna_time.get(id)

    if not last:
        kazna_time[id] = dnow
        last = datetime.fromtimestamp(0)
    if last:
        delta_seconds = (dnow - last).total_seconds()
        sl = int(utime - delta_seconds)

        if sl > 0:
            left = sl
            return 1, left
        else:
            kazna_time[id] = dnow
            return 0, 0


async def lucktime(id):
    utime = 86400
    dnow = datetime.now()
    last = luck_time.get(id)

    if not last:
        luck_time[id] = dnow
        last = datetime.fromtimestamp(0)
    if last:
        delta_seconds = (dnow - last).total_seconds()
        sl = int(utime - delta_seconds)

        if sl > 0:
            left = sl
            return 1, left
        else:
            luck_time[id] = dnow
            return 0, 0