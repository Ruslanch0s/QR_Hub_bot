from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


buttons = [
    InlineKeyboardButton(text='English', callback_data='change_language:EN'),
    InlineKeyboardButton(text='Russian', callback_data='change_language:RU')
]

languages_keyboard = InlineKeyboardMarkup(row_width=2).add(*buttons)
