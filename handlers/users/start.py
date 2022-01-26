from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils import user_language


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    name = message.from_user.first_name

    async def send_photo():
        path_to_download = Path().joinpath("utils", "qrgenerator", "preview.jpg")
        with open(path_to_download, 'rb') as photo:
            await dp.bot.send_photo(message.chat.id, photo)

    await message.answer(str(await user_language(message, state, "welcome")).format(name))
    await send_photo()
    await message.answer(str(await user_language(message, state, "start")).format(name))
