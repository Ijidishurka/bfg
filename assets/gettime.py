from datetime import datetime


bonus_time = dict()
kazna_time = dict()


async def bonustime(id):
    nd = 86400
    ct = datetime.now()
    ld = bonus_time.get(id)

    if not ld:
        bonus_time[id] = ct
        ld = datetime.fromtimestamp(0)
    if ld:
        delta_seconds = (ct - ld).total_seconds()
        sl = int(nd - delta_seconds)

        if sl > 0:
            left = sl
            return 1, left
        else:
            bonus_time[id] = ct
            return 0, 0


async def kaznatime(id):
    nd = 86400
    ct = datetime.now()
    ld = kazna_time.get(id)

    if not ld:
        kazna_time[id] = ct
        ld = datetime.fromtimestamp(0)
    if ld:
        delta_seconds = (ct - ld).total_seconds()
        sl = int(nd - delta_seconds)

        if sl > 0:
            left = sl
            return 1, left
        else:
            kazna_time[id] = ct
            return 0, 0