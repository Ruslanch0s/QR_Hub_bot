from pathlib import Path

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"🚀 Здравствуйте, {message.from_user.first_name}\n\n"
                         "Я умею генерировать QR коды с вашей ссылкой/текстом и картинкой\n\n"
                         "<b>Что бы начать, отправте текст, ссылку или картинку с QR кодом</b>\n\n"
                         "Готовые примеры:")
    path_to_download = Path().joinpath("utils", "qrgenerator", "preview.jpg")
    with open(path_to_download, 'rb') as photo:
        await dp.bot.send_photo(message.chat.id, photo)
