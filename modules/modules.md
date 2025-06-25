# Инструкция по созданию модуля

## Введение
В этом руководстве вы узнаете, как создать свой модуль для бота на платформе Aiogram. Мы рассмотрим основные шаги, необходимые для импорта необходимых библиотек, регистрации хендлеров и настройки вашего модуля.

## Шаг 1: Импорт необходимых библиотек

### Помимо стандартных импортов, необходимых для работы с *aiogram*, в вашем модуле могут пригодиться дополнительные импорты файлов самого бота. Вот несколько полезных примеров:

#### 1. Форматирование чисел с разделителями
Если вам нужно преобразовать большие числа в более удобочитаемый формат (например, 1.000.000), вы можете воспользоваться функцией из модуля:

```python
from assets.transform import transform_int as tr
```
```python
summ = 10000000
print(f'{tr(summ)}$')
---------------------
10.000.000$
```  

<br>

#### 2. Получение случайных эмоджи
Для работы с эмоджи (например, для отображения случайного грустного или весёлого лица) используйте функцию:

```python
from user import BFGconst
```
```python
win, lose = BFGconst.emj()
print(win, lose)
---------------------
🤑😢
```

<br>

#### 3. Использование дополнительных декораторов для безопасности и ограничений
В дополнение к основным функциям, описанным ранее, в вашем модуле могут быть полезны следующие декораторы и функции для управления доступом и безопасностью. Эти элементы помогут вам защитить функционал бота от спама, зарегестрировать новых игроков, ограничить доступ только для администраторов и ограничить нажатия на кнопки.
```python
from assets.antispam import antispam, antispam_earning, new_earning, admin_only
from user import BFGuser
```
#### Декоратор *@antispam*
Декоратор @antispam предназначен для обработки сообщений (*Message*). Он автоматически регистрирует новых пользователей, проверяет, не заблокирован ли пользователь в боте и возвращает всю информациюю о нем (user: BFGuser). Этот декоратор рекомендуется добавлять во все ваши хэндлеры для регистрации новых пользователей.

```python
@antispam
async def test(message: types.Message, user: BFGuser):
    user_id = message.from_user.id
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🐙 Кальмар", callback_data=f"kalimar|{user_id}"))
    msg = await message.answer("Нажми на инлайн кнопку", reply_markup=keyboard)
    await new_earning(msg)  #  смотрите след пункт
```

#### Функция *new_earning*
Эта функция используется для регистрации нового сообщения, которое будет защищено декоратором *@antispam_earning*. После отправки сообщения вызовите эту функцию, чтобы связать его с системой антиспама.

```python
msg = await message.answer("Нажми на инлайн кнопку", reply_markup=keyboard)
await new_earning(msg)
```

#### Декоратор *@antispam_earning*
Этот декоратор предназначен для обработки коллбеков (*CallbackQuery*). Он предотвращает нажатие кнопки другими пользователями и работает совместно с функцией *new_earning*.

```python
@antispam_earning
async def test2(call: types.CallbackQuery, user: BFGuser):
    # Ваш код обработки коллбека
```

#### Декоратор *@admin_only*
Декоратор *@admin_only* предназначен для ограничения выполнения команды только администраторами бота. Он работает только для сообщений (*Message*). Также можно ограничить доступ к выполнению команды в чатах.

```python
@admin_only()
async def test(message: types.Message):
    # Команда доступна только администраторам
```
```python
@admin_only(private=True)  # Добавляем private=True
async def test2(message: types.Message):
    # Команда доступна только в личных сообщениях с ботом
```

<br>

#### 4. Работа с основной базой данных
Для взаимодействия с базой данных бота (для измнения баланса игрока и тд.) необходимо импортировать соединение и курсор, которые используются для выполнения запросов. Эти объекты нужны для чтения и записи данных, а также для обработки запросов к основной базе данных.

```python
from commands.db import conn as conngdb, cursor as cursorgdb
```

Пример добавления 20 B-coins к балансу игрока с *user_id = 6201573146*

```python
summ = 20
user_id = 6201573146
cursorgdb.execute('UPDATE users SET ecoins = ecoins + ? WHERE user_id = ?', (summ, user_id))
conngdb.commit()
```
`Обратите внимание: в запросах мы используем user_id, который соответствует Telegram ID пользователя.`

Для добавления денег нам потребуеться использовать библиотеку **decimial** (такой подоход требуеться ко всем столбикам у которых тип данных *TEXT*)
```python
from decimial import Decimial
```

В данном примере сначала извлекается текущий баланс игрока, после чего вычисляется новый баланс и записывается обратно в базу данных:

```python
user_id = 6201573146
summ = 1000

balance = cursorgdb.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,)).fetchone()[0]

new_balance = Decimal(str(balance)) + Decimal(str(summ))
new_balance = "{:.0f}".format(new_balance)

cursorgdb.execute('UPDATE users SET balance = ? WHERE user_id = ?', (new_balance, user_id))
conngdb.commit()
```

не забывайте применять *conngdb.commit()* после выполнения операций с записью данных в базу.

<br>

## Шаг 2: Создание функций
### Функции — это основа вашего модуля. Они позволяют реализовать логику бота и взаимодействие с пользователями. Обычно функции являются хендлерами, которые отвечают на сообщения, нажатия на кнопки и другие действия пользователей. Также они могут включать различные декораторы, чтобы добавлять функционал, такой как антиспам или доступ только для администраторов.

Пример создания легкой функции которая отпраляет сообщение  сообщение "привет"
```python
async def example(message: types.Message):
    await message.answer("привет")
```

<br>

### Добавление декораторов к функциям
#### Декоратор @antispam
Декоратор, который регистрирует новых игроков и проверяет их на наличие бана. Рекомендуется использовать этот декоратор в каждом хендлере.  

**Важно:** Функции в вашем модуле ничем не отличаются от функций в библиотеке aiogram. Для подробного изучения их возможностей, вы можете обратиться к документации [aiogram](https://docs.aiogram.dev/en/v2.25.1/).

```python
from assets.antispam import antispam

@antispam
async def example(message: types.Message, user: BFGuser):
    await message.answer(f"Привет, {user.url}!")  # user.url - ссылка на пользователя
```

#### Работа с CallbackQuery (кнопками)
Если ваша функция должна обрабатывать нажатия на инлайн-кнопки, вы можете использовать декоратор *@antispam_earning* для того чтоб кнопка была доступна только определённому игроку.

```python
from assets.antispam import antispam_earning, new_earning

@antispam
async def start_game(message: types.Message, user: BFGuser):
    user_id = message.from_user.id

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🐙 Кальмар", callback_data=f"kalimar|{user_id}"))
    #  Обязательно добавьте айди человека который может нажимать на кнопку |{user_id}

    msg = await message.answer("Нажмите кнопку!", reply_markup=keyboard)
    await new_earning(msg)  # Добавляем кнопку в antispam_earning


@antispam_earning
async def process_game(call: types.CallbackQuery, user: BFGuser):
    await call.message.answer("Вы нажали кнопку.")
```

<br>

## Шаг 3: Регистрация хэндлеров
Регистрация хэндлеров — это ключевой этап, позволяющий вашему боту реагировать на сообщения и команды пользователей. Хэндлеры в Aiogram обрабатывают входящие события и выполняют соответствующие действия.

Основы регистрации хэндлеров
Для регистрации хэндлеров вам нужно использовать метод *register_message_handler* или *register_callback_query_handler*, в зависимости от типа входящего события. Также рекомендуется указывать имя и описание хэндлера, чтобы было легче ориентироваться в коде

#### Регистрация команд

```python
dp.register_message_handler(start_game, commands='start')
```
В этом примере хэндлер start_game будет вызываться, когда пользователь отправляет команду "/start"

**Объяснение:**

`dp` — это объект Dispatcher, который управляет хэндлерами.  
`register_message_handler` — метод для регистрации хэндлера, который будет вызываться на определённые сообщения.  
`start_game` — это ваша функция, которая будет обрабатывать команду.  
`commands='start'` — указывает, что хэндлер будет срабатывать только на команду /start.  

#### Регистрация текствовых сообщений

```python
dp.register_message_handler(game, lambda message: message.text.lower().startswith('охота'))
```
В этом примере хэндлер game будет вызываться, когда пользователь отправляет сообщение, начинающееся с "охота".

```python
dp.register_message_handler(game, lambda message: message.text.lower() == 'выстрел')
```
Хэндлер сработает только на сообщения, содержащие точное слово "привет" (включая слова, написанные с большой буквы).

```python
dp.register_message_handler(hello, lambda message: message.text.lower() in ['привет', 'ку'])
```
Хэндлер сработает только на сообщения "привет" и "ку"

#### Регистрация нажатий на кнопку

```python
dp.register_callback_query_handler(game, text_startswith='game')
```
Хэндлер сработает на инлайн-кнопки, данные которых равны game.

```python
dp.register_callback_query_handler(game, text_startswith='game_')
```
Хэндлер сработает на инлайн-кнопки, данные которых начинаются с game_.

#### Пример регистрации хандлеров [TicTacToe](https://github.com/Ijidishurka/bfg-modules/blob/main/TicTacToe.py)

Хэндлеры необходимо регистрировать в функции `register_handlers`. Вот как это можно сделать:

```python
def register_handlers(dp: Dispatcher):
    # Регистрация хэндлера на сообщения, которые начинаются с 'кн'
    dp.register_message_handler(start, lambda message: message.text.lower().startswith('кн'))
    
    # Регистрация хэндлера инлайн-кнопок, данные которых начинаються с 'tictactoe-start'
    dp.register_callback_query_handler(start_game_kb, text_startswith='tictactoe-start')
    
    # Аналогчиный хэндлер
    dp.register_callback_query_handler(game_kb, text_startswith='TicTacToe')
```

<br>

## Шаг 4: Описание модуля
После определения функции регистрации хэндлеров создайте словарь с информацией о модуле. Это поможет вам и другим разработчикам понять назначение вашего кода.

```python
MODULE_DESCRIPTION = {
	'name': '❌⭕️ Крестики-нолики',
	'description': 'Новая игра "крестики-нолики" против других игроков (на деньги)'
}
```

<br>
<br>

## Примеры модулей
Этот модуль добавляет функциональность для приветствия пользователей и отправки случайных эмоджи в ответ на команду `/emj`. Модуль использует функции Aiogram для обработки сообщений и команд.

```python
from aiogram import Dispatcher, types
from user import BFGconst             # Импортируем случайные эмоджи
from assets.antispam import antispam  # Импортируем антиспам

# Функция, которая отвечает на слово "привет"
@antispam
async def hello(message: types.Message, user: BFGuser):
    await message.answer(f"Привет, {user.url}! Как дела?")

# Функция для отправки случайного эмоджи
@antispam
async def send_random_emoji(message: types.Message, user: BFGuser):
    win, lose = BFGconst.emj()       # Получаем случайные эмоджи
    await message.answer(win, lose)  # Отправляем случайные эмоджи

# Функция для регистрации хэндлеров
def register_handlers(dp: Dispatcher):
    dp.register_message_handler(hello, lambda message: message.text.lower() == 'привет')
    dp.register_message_handler(send_random_emoji, commands=['emj'])

# Описание модуля
MODULE_DESCRIPTION = {
    'name': '😊 Приветствие и Эмоджи',
    'description': 'Модуль отвечает на слово "привет" и отправляет случайное эмоджи по команде /emj'
}
```

#### Пример работы модуля:
*привет*  
`Привет, skay! Как дела?`  
*/emj*  
`😃😣`

<br>

Вы можете посмотреть более сложные пример модулей на моем [GitHub](https://github.com/Ijidishurka)

- [Крестики-Нолики](https://github.com/Ijidishurka/bfg-modules/blob/main/TicTacToe.py)
 - [Охота](https://github.com/Ijidishurka/bfg-modules/blob/main/hunting.py)
 - [Хэллоуин-ивент](https://github.com/Ijidishurka/bfg-modules/blob/main/halloween.py)
