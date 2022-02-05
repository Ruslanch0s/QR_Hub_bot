from aiogram import types

from loader import dp
from utils.language import user_language
from aiogram.dispatcher import FSMContext

# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer(await user_language(message.from_user, 'start'))


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message):
    await message.answer(await user_language(message.from_user, 'error_format'))
