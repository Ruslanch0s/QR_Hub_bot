import logging

from aiogram import types
from aiogram.dispatcher import FSMContext

from . import english
from . import russian


async def user_language(message: types.Message, state: FSMContext, text: str):
    user_data = await state.get_data()

    try:
        language = user_data['language']
    except KeyError:
        default_language = message.from_user.language_code
        if default_language == 'ru':
            await state.update_data(language='RU')
            language = 'RU'
        else:
            await state.update_data(language='EN')
            language = 'EN'

    if language == "RU":
        try:
            return russian.data.get(text)
        except Exception:
            logging.error(f"Отсутствует ключ ({text}) в russian.data")
    else:
        try:
            return english.data.get(text)
        except Exception:
            logging.error(f"Отсутствует ключ ({text}) в english.data")
