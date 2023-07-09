from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_pagination_button(*buttons: str) -> InlineKeyboardMarkup:
    builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    builder.row(*[
      InlineKeyboardButton(text=LEXICON[button] if button in LEXICON else button,
                           callback_data=button)
    for button in buttons], width=3)
    return builder.as_markup()