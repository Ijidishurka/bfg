from decimal import Decimal


def transform(value: str | int) -> str:
    value = int(value)
    ranges = [
        (1_000, 'тыс'),
        (1_000_000, 'млн'),
        (1_000_000_000, 'млрд'),
        (1_000_000_000_000, 'трлн'),
        (1_000_000_000_000_000, 'квдр'),
        (1_000_000_000_000_000_000, 'квнт'),
        (1_000_000_000_000_000_000_000, 'скст'),
        (1_000_000_000_000_000_000_000_000, 'трикс'),
        (1_000_000_000_000_000_000_000_000_000, 'твинкс'),
        (1_000_000_000_000_000_000_000_000_000_000, 'септ'),
        (1_000_000_000_000_000_000_000_000_000_000_000, 'октл'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000, 'нонл'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000, 'декал'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'эндк'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'доктл'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'гугл'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'кинд'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'трипт'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'срист'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'манит'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'гвинт'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'секст'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'октлт'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'нонлт'),
        (1_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000, 'децлт')
    ]

    for threshold, label in reversed(ranges):
        if int(float(value)) >= threshold:
            i1 = int(float(value)) / threshold
            i2 = round(i1)
            return f'{i2} {label}'
    value = Decimal(value)
    return f"{value:1.1e}"


def transform_int(value: str | int) -> str:
    value = int(value)
    if len(str(value)) < 21:
        return '{:,}'.format(value).replace(',', '.')
    value = Decimal(value)
    return f"{value:1.1e}"

