from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


template_button = InlineKeyboardButton(text='', callback_data='templates')
buttons = [
    InlineKeyboardButton(text='1', callback_data='picture:dogy_1.jpg'),
    InlineKeyboardButton(text='2', callback_data='picture:dogy_2.jpg'),
    InlineKeyboardButton(text='3', callback_data='picture:dogy_3.jpeg'),
    InlineKeyboardButton(text='4', callback_data='picture:dogy_4.jpg'),
    InlineKeyboardButton(text='5', callback_data='picture:virus.jpeg'),
    InlineKeyboardButton(text='6', callback_data='picture:the_witcher_1.jpg'),
    InlineKeyboardButton(text='7', callback_data='picture:zebra.jpg'),
    InlineKeyboardButton(text='8', callback_data='picture:china.jpg')
]
images_keyboard = InlineKeyboardMarkup(row_width=4).add(*buttons)
