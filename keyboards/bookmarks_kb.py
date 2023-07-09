from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.file_handling import book
from lexicon.lexicon import LEXICON


def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in sorted(args):
        builder.row(
            InlineKeyboardButton(text=f'{button} - {book[button][:100]}',
                                 callback_data=str(button))
        )

    builder.row(InlineKeyboardButton(
        text=LEXICON['edit_bookmarks_button'],
        callback_data='edit_bookmarks'),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'),
        width=2)
    return builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for button in sorted(args):
        builder.row(
            InlineKeyboardButton(text=f'{LEXICON["del"]}{button} - {book[button][:100]}',
                                 callback_data=str(button))
        )

    builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'))
    return builder.as_markup()
