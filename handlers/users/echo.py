from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp
from utils.language import user_language

# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer(await user_language(message, state, 'start'))


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    await message.answer(await user_language(message, state, 'error_format'))
