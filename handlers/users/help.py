from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.language import user_language


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer(await user_language(message.from_user, 'help'))
