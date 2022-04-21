from pathlib import Path

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils import user_language
from utils.db_api.schemas.users import User
from utils.db_api.example import add_user, add_payment
from middlewares.throttling import ThrottlingMiddleware
from utils import analytics


@dp.message_handler(CommandStart(), state='*')
@dp.throttled(rate=4)
@analytics
async def bot_start(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    name = message.from_user.first_name

    async def send_photo():
        path_to_download = Path().joinpath("utils", "qrgenerator", "ert.jpg")  # preview
        with open(path_to_download, 'rb') as photo:
            await dp.bot.send_photo(message.chat.id, photo)

    await send_photo()
    await message.answer(str(await user_language(message.from_user, "welcome")).format(name))

    await message.answer(str(await user_language(message.from_user, "start")).format(name))
