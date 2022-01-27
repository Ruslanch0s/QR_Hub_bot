import os
import random
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.default import cancel_button
from keyboards.inline import images_keyboard, template_button, image_callback, template_callback
from loader import dp
from utils.qrgenerator import gen_qr_code, read_qr_code
from utils import user_language, logger


@dp.message_handler(text=["Отменить", "Cancel"], state="send_image")
async def cancel_state(message: types.Message, state: FSMContext):
    await message.answer(str(await user_language(message, state, "canceled")), reply_markup=ReplyKeyboardRemove())
    await state.reset_state(with_data=False)
    await message.answer(str(await user_language(message, state, "start")))


@dp.message_handler(content_types=ContentType.TEXT)
async def get_text(message: types.Message, state: FSMContext):
    text_from_user = message.text
    cancel_button.text = await user_language(message, state, 'cancel_button')
    await message.answer(str(await user_language(message, state, "your_values")).format(text_from_user),
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_button))

    template_button.text = await user_language(message, state, 'templates_button')

    await message.answer(str(await user_language(message, state, "choose_template")),
                         reply_markup=types.InlineKeyboardMarkup().add(template_button))
    await state.update_data(send_image=text_from_user)
    await state.set_state("send_image")


@dp.message_handler(content_types=['photo', 'document'])
async def get_text_from_qr(message: types.Message, state: FSMContext):
    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)

    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)
    text_from_qr = read_qr_code(path_to_download)
    path_to_download.unlink()

    if text_from_qr is not None:
        cancel_button.text = await user_language(message, state, 'cancel_button')
        await message.answer(str(await user_language(message, state, "your_values")).format(text_from_qr),
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(cancel_button))
        template_button.text = await user_language(message, state, 'templates_button')
        await message.answer(str(await user_language(message, state, "choose_template")),
                             reply_markup=types.InlineKeyboardMarkup().add(template_button))
        await state.update_data(send_image=text_from_qr)
        await state.set_state("send_image")
        logger.info(f'success - read-qr - {message.from_user.id} - {message.from_user.first_name}')

    else:
        await message.answer(str(await user_language(message, state, "error_read_qr")))
        await state.reset_state(with_data=False)
        logger.info(f'error - read-qr - {message.from_user.id} - {message.from_user.first_name}')


@dp.callback_query_handler(image_callback.filter(), state="send_image")
async def get_template(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback_query.message.answer(await user_language(callback_query.message, state, "generating"),
                                        reply_markup=ReplyKeyboardRemove())

    file_name = str(random.randint(1, 9999)) + '.png'
    template_name = callback_data.get("file_name")
    path_to_download = Path().joinpath("utils", "qrgenerator", "templates", template_name)
    path_to_save = Path().joinpath("utils", "qrgenerator", "images", file_name)

    data = await state.get_data()
    text_for_generate = data.get("send_image")
    gen_qr_code(message=text_for_generate, path_to_download=path_to_download, path_to_save=path_to_save)

    image = types.InputFile(path_or_bytesio=path_to_save)
    await dp.bot.send_photo(callback_query.message.chat.id, image)
    await callback_query.message.answer(await user_language(callback_query.message, state, 'success'))
    await callback_query.message.answer(await user_language(callback_query.message, state, 'start'))
    await state.reset_state(with_data=False)
    logger.info(f'success - template-image - {callback_query.from_user.id} - {callback_query.from_user.first_name}')
    path_to_save.unlink()


@dp.callback_query_handler(template_callback.filter(), state="send_image")
async def view_templates(callback_query: types.CallbackQuery, state: FSMContext):
    path_to_download = Path().joinpath("utils", "qrgenerator", "templates", "view_template.jpg")
    with open(path_to_download, 'rb') as photo:
        await dp.bot.send_photo(callback_query.message.chat.id, photo)

    await callback_query.message.answer(str(await user_language(callback_query.message, state, 'background')),
                                        reply_markup=images_keyboard)


@dp.message_handler(content_types=['photo', 'document'], state="send_image")
async def get_picture(message: types.Message, state: FSMContext):
    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)
    data = await state.get_data()
    text_for_generate = data.get("send_image")

    await message.answer(await user_language(message, state, "generating"), reply_markup=ReplyKeyboardRemove())
    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)

    successful_generation = gen_qr_code(message=text_for_generate, path_to_download=path_to_download)
    if successful_generation is False:
        await message.answer(await user_language(message, state, "error_format"))
        logger.info(f'error - user-image - {message.from_user.id} - {message.from_user.first_name}')

    else:
        photo = types.InputFile(path_or_bytesio=path_to_download)
        await dp.bot.send_photo(message.chat.id, photo)
        await message.answer(await user_language(message, state, "success"))
        await message.answer(await user_language(message, state, "start"))
        await state.reset_state(with_data=False)
        logger.info(f'success - user-image - {message.from_user.id} - {message.from_user.first_name}')

    path_to_download.unlink()


@dp.message_handler(content_types=ContentType.TEXT, state="send_image")
async def wrong_type(message: types.Message, state: FSMContext):
    await message.answer(await user_language(message, state, 'error_get_image'))
    logger.info(f'error - wrong_type(text) - {message.from_user.id} - {message.from_user.first_name}')
