from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery


class IsDigitCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and callback.data.isdigit()


class IsDelBookmarkCallbackData(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return isinstance(callback.data, str) and 'del' \
            in callback.data and callback.data[:-3].isdigit()


class IsBookmarkNumber(BaseFilter):
    async def __call__(self, callback: CallbackQuery):
        return isinstance(callback.data, str) and \
            '/' in callback.data and \
            callback.data.replace(' / ', '').isdigit()