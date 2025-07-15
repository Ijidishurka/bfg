from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


class TextIn(BaseFilter):
    def __init__(self, *values: str) -> None:
        self.values = [v.lower() for v in values]

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        text = None

        if isinstance(obj, Message):
            text = obj.text
        elif isinstance(obj, CallbackQuery):
            text = obj.data

        return text and text.lower() in self.values


class StartsWith(BaseFilter):
    def __init__(self, *prefixes: str) -> None:
        self.prefixes = [p.lower() for p in prefixes]

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        text = None

        if isinstance(obj, Message):
            text = obj.text
        elif isinstance(obj, CallbackQuery):
            text = obj.data

        if not text:
            return False

        return any(text.lower().startswith(prefix) for prefix in self.prefixes)