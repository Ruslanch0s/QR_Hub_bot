import functools

from utils.db_api.example import add_user, update_touch_points


def analytics(func: callable):  # аргументы декоратора

    # Внутри себя декоратор определяет функцию-"обёртку". Она будет обёрнута вокруг декорируемой,
    # получая возможность исполнять произвольный код до и после неё.
    @functools.wraps(func)
    async def analytics_wrapper(message, *args, **kwargs):  # аргументы декорируемой функции
        id_user = message.from_user.id
        name = message.from_user.first_name
        language = message.from_user.language_code

        await add_user(id_user, name, language)

        return await func(message, *args, **kwargs)

    return analytics_wrapper



