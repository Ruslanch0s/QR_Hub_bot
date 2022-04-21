import random
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardRemove

from keyboards.inline import images_keyboard, template_button, add_to_wallet_button, image_callback, \
    template_callback, wallet_callback, cancel_button, cancel_callback, create_pkpass_keyboard, \
    create_pkpass_callback, pay_pkpass_keyboard, pay_pkpass_button
from loader import dp
from utils import user_language, logger
from utils.db_api.schemas.users import User
from utils.pkpass.main import get_pkpass, create_pkpass
from utils.qrgenerator import gen_qr_code, read_qr_code


@dp.callback_query_handler(cancel_callback.filter(), state="*")
async def cancel_state(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()

    user = callback_query.from_user
    await dp.bot.send_message(callback_query.from_user.id, await user_language(user, "canceled"))
    await state.reset_state(with_data=False)
    await dp.bot.send_message(callback_query.from_user.id, await user_language(user, "start"))


async def print_choice(message, state, text_from_qr=None):
    if text_from_qr:
        text_from_user = text_from_qr
    else:
        text_from_user = message.text

    user = message.from_user
    cancel_button.text = await user_language(user, 'cancel_button')
    await message.answer(str(await user_language(user, "your_values")).format(text_from_user))
    template_button.text = await user_language(user, 'templates_button')
    add_to_wallet_button.text = await user_language(user, 'add_to_wallet_button')
    await message.answer(await user_language(user, "choose_template"))
    file_path = Path().joinpath("utils", "qrgenerator", "morfeus.jpg")
    image = types.InputFile(file_path)
    await dp.bot.send_photo(message.from_user.id, image,
                            reply_markup=types.InlineKeyboardMarkup(row_width=2).add(template_button,
                                                                                     add_to_wallet_button,
                                                                                     cancel_button))
    await state.update_data(send_image=text_from_user)
    await state.set_state("choice_of_option")


@dp.message_handler(content_types=ContentType.TEXT)
@dp.throttled(rate=5)
async def get_text(message: types.Message, state: FSMContext):
    await print_choice(message, state)


@dp.message_handler(content_types=['photo', 'document'])
@dp.throttled(rate=5)
async def get_text_from_qr(message: types.Message, state: FSMContext):
    user = message.from_user
    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)

    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)
    text_from_qr = read_qr_code(path_to_download)
    path_to_download.unlink()

    if text_from_qr is not None:
        await print_choice(message, state, text_from_qr)
        logger.info(f'success - read-qr - {message.from_user.id} - {message.from_user.first_name}')
    else:
        await message.answer(str(await user_language(user, "error_read_qr")))
        await state.reset_state(with_data=False)
        logger.info(f'error - read-qr - {message.from_user.id} - {message.from_user.first_name}')


@dp.callback_query_handler(template_callback.filter(), state="choice_of_option")
async def view_templates(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()

    await state.set_state("send_image")
    path_to_download = Path().joinpath("utils", "qrgenerator", "templates", "view_template.jpg")
    with open(path_to_download, 'rb') as photo:
        await dp.bot.send_photo(callback_query.message.chat.id, photo)

    cancel_button.text = await user_language(callback_query.from_user, "cancel_button")
    await callback_query.message.answer(str(await user_language(callback_query.from_user, 'background')),
                                        reply_markup=images_keyboard)


@dp.callback_query_handler(image_callback.filter(), state="send_image")
async def print_create_qr(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.message.edit_reply_markup()

    user = callback_query.from_user
    await callback_query.message.answer(await user_language(user, "generating"),
                                        reply_markup=ReplyKeyboardRemove())

    file_name = str(random.randint(1, 9999)) + '.png'
    template_name = callback_data.get("file_name")
    path_to_download = Path().joinpath("utils", "qrgenerator", "templates", template_name)
    path_to_save = Path().joinpath("utils", "qrgenerator", "images", file_name)

    data = await state.get_data()
    text_for_generate = data.get("send_image")
    try:
        gen_qr_code(message=text_for_generate, path_to_download=path_to_download, path_to_save=path_to_save)
        image = types.InputFile(path_or_bytesio=path_to_save)
        await dp.bot.send_photo(callback_query.message.chat.id, image)
        await callback_query.message.answer(await user_language(user, 'success'))
        await callback_query.message.answer(await user_language(user, 'start'))
        await state.reset_state(with_data=False)
        logger.info(f'success - template-image - {user.id} - {user.first_name}')
    except Exception:
        await callback_query.message.answer(await user_language(user, "unknown_error"))
        await callback_query.message.answer(await user_language(user, "start"))
        await state.reset_state(with_data=False)
        logger.info(
            f'error - unknown_error(get_template) - {user.id} - {user.first_name}')

    path_to_save.unlink()


@dp.callback_query_handler(wallet_callback.filter(), state="choice_of_option")
async def check_fot_wallet(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_reply_markup()

    from_user = callback_query.from_user

    path_to_download = Path().joinpath("utils", "pkpass", "123.jpg")
    with open(path_to_download, 'rb') as photo:
        await dp.bot.send_photo(from_user.id, photo)
    await callback_query.message.answer(await user_language(from_user, 'select_pkpass_template'),
                                        reply_markup=create_pkpass_keyboard)
    await state.set_state('create_pkpass')


@dp.callback_query_handler(create_pkpass_callback.filter(), state="create_pkpass")
async def create_the_pkpass(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(await user_language(callback_query.from_user, 'generating'))
    data = await state.get_data()
    text_for_generate = data.get('send_image')
    print(text_for_generate)
    template_id = callback_data.get('template_id')
    print(template_id)
    path_to_download = Path().joinpath("utils", "pkpass", "files", f"{callback_query.from_user.id}.pkpass")
    try:
        url_to_download = await create_pkpass(text_for_generate=text_for_generate, template_id=template_id)
        await get_pkpass(path_to_download=path_to_download, url=url_to_download)

        file = types.InputFile(path_or_bytesio=path_to_download)
        await dp.bot.send_document(callback_query.from_user.id, document=file)
        path_to_download.unlink()
        await callback_query.message.answer(await user_language(callback_query.from_user, 'success'))
        logger.info(
            f'success - generate_pkpass - {callback_query.from_user.id} - {callback_query.from_user.first_name}')

    except Exception as err:
        print(err)
        logger.info(f'error - generate_pkpass - {callback_query.from_user.id} - {callback_query.from_user.first_name}')
        await callback_query.message.answer(await user_language(callback_query.from_user, "error_generate_pkpass"))

    await callback_query.message.answer(await user_language(callback_query.from_user, "start"))
    await state.reset_state(with_data=False)


@dp.message_handler(content_types=['photo', 'document'], state="send_image")
@dp.throttled(rate=5)
async def get_picture(message: types.Message, state: FSMContext):
    user = message.from_user
    await message.answer(await user_language(user, "generating"), reply_markup=ReplyKeyboardRemove())

    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)
    data = await state.get_data()
    text_for_generate = data.get("send_image")

    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)

    try:
        successful_generation = gen_qr_code(message=text_for_generate, path_to_download=path_to_download)
        if successful_generation is False:
            await message.answer(await user_language(user, "error_format"))
            logger.info(f'error - user-image - {message.from_user.id} - {message.from_user.first_name}')

        else:
            photo = types.InputFile(path_or_bytesio=path_to_download)
            await dp.bot.send_photo(message.chat.id, photo)
            await message.answer(await user_language(user, "success"))
            await message.answer(await user_language(user, "start"))
            await state.reset_state(with_data=False)
            logger.info(f'success - user-image - {user.id} - {user.first_name}')
    except Exception:
        await message.answer(await user_language(user, "unknown_error"))
        await message.answer(await user_language(user, "start"))
        await state.reset_state(with_data=False)
        logger.info(
            f'error - unknown_error(get_template) - {user.id} - {user.first_name}')

    path_to_download.unlink()


@dp.message_handler(content_types=ContentType.TEXT, state="send_image")
@dp.throttled(rate=5)
async def wrong_type(message: types.Message):
    await message.answer(await user_language(message.from_user, 'error_get_image'))
    logger.info(f'error - wrong_type(text) - {message.from_user.id} - {message.from_user.first_name}')


@dp.message_handler(content_types=ContentType.ANY, state=["choice_of_option", "create_pkpass"])
@dp.throttled(rate=5)
async def wrong_choice(message: types.Message):
    await message.answer(await user_language(message.from_user, 'error_choice'))
    logger.info(f'error - error_choice(text) - {message.from_user.id} - {message.from_user.first_name}')
