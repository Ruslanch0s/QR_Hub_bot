import os
import random
from pathlib import Path

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from keyboards.default import cancel
from loader import dp, logging
from utils.qrgenerator import gen_qr_code, read_qr_code


@dp.message_handler(text="Отменить", state="send_image")
async def cancel_state(message: types.Message, state: FSMContext):
    await message.answer("Отменено\n\n"
                         "<b>Что бы начать, отправте текст или ссылку</b>",
                         reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(content_types=ContentType.TEXT)
async def get_text(message: types.Message, state: FSMContext):
    text = message.text

    await message.answer(f"Вы ввели: {text}\n"
                         "<b>Теперь отправте картинку для фона</b>", reply_markup=cancel)
    await state.update_data(send_image=text)
    await state.set_state("send_image")


@dp.message_handler(content_types=['photo', 'document'])
async def get_text_from_qr(message: types.Message, state: FSMContext):
    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)

    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)
    text = read_qr_code(path_to_download)
    path_to_download.unlink()
    if text is not None:
        await message.answer(f"Вы ввели: {text}\n"
                             "<b>Теперь отправте картинку для фона</b>", reply_markup=cancel)
        await state.update_data(send_image=text)
        await state.set_state("send_image")
    else:
        await message.answer(
            "Упсс, QR код на вашей картинке не считался попробуйте еще раз или напишите текст/ссылку вручную")
        await state.finish()
        logging.info(f'--- conversion error {message.chat.id, message.from_user.first_name}')


@dp.message_handler(content_types=['photo', 'document'], state="send_image")
async def get_picture(message: types.Message, state: FSMContext):
    file_name = str(random.randint(1, 9999)) + '.png'
    path_to_download = Path().joinpath("utils", "qrgenerator", "images", file_name)
    data = await state.get_data()
    text = data.get("send_image")
    await message.answer("⚙ генерирую !", reply_markup=ReplyKeyboardRemove())
    if message.content_type == "photo":
        await message.photo[-1].download(destination_file=path_to_download, make_dirs=False)
    else:
        await message.document.download(destination_file=path_to_download, make_dirs=False)

    successed = gen_qr_code(message=text, path_to_download=path_to_download)
    if successed is False:
        await message.answer('Что то пошло не так, проверте отправляемый файл\n\n'
                             '<b>Отправте картинку для фона</b>')
    else:
        # with open(path_to_download, 'rb') as photo:
        photo = types.InputFile(path_or_bytesio=path_to_download)
        await dp.bot.send_photo(message.chat.id, photo)
        await message.answer("<b>Готово!</b>\n"
                             "Отправте текст, ссылку или картинку с QR кодом")
        await state.finish()
        logging.info(f'--- successful conversion {message.chat.id, message.from_user.first_name}')

    path_to_download.unlink()


@dp.message_handler(content_types=ContentType.TEXT, state="send_image")
async def wrong_type(message: types.Message):
    await message.answer(f"Ожидаю картинку для фона...\n\n"
                         "Для отмены наберите: <b>отменить</b>")
