from pathlib import Path

import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils import user_language
from utils.db_api.schemas.user import User

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.first_name
    id_user = message.from_user.id
    try:
        user = await User(
            name=message.from_user.username,
            id=id_user
        ).create()
    except asyncpg.UniqueViolationError:
        user = await User.get(id_user)

    async def send_photo():
        path_to_download = Path().joinpath("utils", "qrgenerator", "preview.jpg")
        with open(path_to_download, 'rb') as photo:
            await dp.bot.send_photo(message.chat.id, photo)

    await message.answer(str(await user_language(message, state, "welcome")).format(name))
    await send_photo()
    await message.answer(str(await user_language(message, state, "start")).format(name))
