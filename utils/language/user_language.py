from aiogram import types

from utils.loggers.language import logger
from . import english
from . import russian


async def user_language(user: types.User, text: str) -> str:
    from loader import dp

    user_id = user.id
    state = dp.current_state(chat=user_id, user=user_id)
    user_data = await state.get_data()

    try:
        language = user_data['language']
    except KeyError:
        default_language = user.language_code
        if default_language == 'ru':
            await state.update_data(language='RU')
            language = 'RU'
        else:
            await state.update_data(language='EN')
            language = 'EN'

    if language == "RU":
        try:
            return russian.data.get(text)
        except Exception as err:
            logger.error(f"Отсутствует ключ: ({text}) в russian.data\n{err}\n\n")
    else:
        try:
            return english.data.get(text)
        except Exception as err:
            logger.error(f"Отсутствует ключ: ({text}) в english.data\n{err}\n\n")
