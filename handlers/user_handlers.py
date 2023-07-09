from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from lexicon.lexicon import LEXICON

router: Router = Router()


@router.message(Command(commands=['start']))
async def answer_start(message: Message):
    await message.answer(LEXICON['/start'])


@router.message(Command(commands=['help']))
async def answer_start(message: Message):
    await message.answer(LEXICON['/help'])