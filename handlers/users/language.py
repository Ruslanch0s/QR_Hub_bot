from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards.inline import languages_keyboard, language_callback
from loader import dp
from utils import user_language


@dp.callback_query_handler(language_callback.filter(), state='*')
async def change_language(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    if callback_data.get("language") == "RU":
        await state.update_data(language='RU')
        text = "Язык изменен"
    else:
        await state.update_data(language='EN')
        text = "Language has been changed"

    await callback_query.message.answer(text)
    await callback_query.message.answer(await user_language(callback_query.from_user, 'start'))


@dp.message_handler(commands=['language'], commands_prefix='/', state='*')
async def choose_language(message: types.Message):
    await message.answer("Choose language", reply_markup=languages_keyboard)
