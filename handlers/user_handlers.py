from copy import deepcopy

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination import create_pagination_button
from lexicon.lexicon import LEXICON
from database.database import users_db, user_dict_template
from services.file_handling import book
from filters.filters import *

router: Router = Router()


@router.message(Command(commands=['start']))
async def answer_start(message: Message):
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(LEXICON['/start'])


@router.message(Command(commands=['help']))
async def answer_start(message: Message):
    await message.answer(LEXICON['/help'])


@router.message(Command(commands=['beginning']))
async def begin_read_book(message: Message) -> None:
    user_id = message.from_user.id
    users_db[user_id]['page'] = 1
    text = book[users_db[user_id]['page']]

    await message.answer(
        text=text,
        reply_markup=create_pagination_button(
            'backward',
            f'{users_db[user_id]["page"]} / {len(book)}',
            'forward'
        )
    )


@router.message(Command(commands=['continue']))
async def continue_read__book(message: Message):
    user_id = message.from_user.id
    text = book[users_db[user_id]['page']]

    await message.answer(
        text=text,
        reply_markup=create_pagination_button(
            'backward',
            f'{users_db[user_id]["page"]} / {len(book)}',
            'forward'
        )
    )


@router.callback_query(Text(text=['forward']))
async def forward_page(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    if users_db[user_id]['page'] < len(book):
        users_db[user_id]['page'] += 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_button(
                'backward',
                f'{users_db[user_id]["page"]} / {len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(Text(text=['backward']))
async def backward_page(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    if users_db[user_id]['page'] > 1:
        users_db[user_id]['page'] -= 1
        text = book[users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_button(
                'backward',
                f'{users_db[user_id]["page"]} / {len(book)}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(IsBookmarkNumber())
async def add_to_bookmark(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page']
    )
    await callback.answer('Страница добавлена в закладки!')


@router.message(Command(commands=['bookmarks']))
async def show_bookmarks(message: Message):
    user_id = message.from_user.id
    if users_db[user_id]['bookmarks']:
        text = LEXICON['/bookmarks']
        await message.answer(
            text=text,
            reply_markup=create_bookmarks_keyboard(
                *users_db[user_id]['bookmarks']
            )
        )
    else:
        await message.answer('У вас закладок нету')


@router.callback_query(IsDigitCallbackData())
async def from_bookmarks_to_book(callback: CallbackQuery):
    text = book[int(callback.data)]
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_button(
            'backward',
            f'{users_db[callback.from_user.id]["page"]} / {len(book)}',
            'forward'
        )
    )
    await callback.answer()


@router.callback_query(Text(text=['edit_bookmarks']))
async def edit_bookmarks(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )
    await callback.answer()


@router.callback_query(IsDelBookmarkCallbackData())
async def delete_bookmark(callback: CallbackQuery):
    num_page = int(callback.data[:-3])
    users_db[callback.from_user.id]['bookmarks'].remove(num_page)
    await callback.message.edit_text(
        text=LEXICON['edit_bookmarks'],
        reply_markup=create_edit_keyboard(
            *users_db[callback.from_user.id]['bookmarks']
        )
    )

    await callback.answer()


@router.callback_query(Text(text=['cancel']))
async def cancel(callback: CallbackQuery):
    await callback.message.edit_text('Действие отменено')
    await callback.answer()