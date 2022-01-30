from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from . import cancel_button

create_pkpass_button = InlineKeyboardButton(text='', callback_data='create_pkpass')
create_pkpass_keyboard = InlineKeyboardMarkup(row_width=2).add(create_pkpass_button, cancel_button)

pay_pkpass_button = InlineKeyboardButton(text='', callback_data='pay_pkpass')
pay_pkpass_keyboard = InlineKeyboardMarkup(row_width=2).add(cancel_button)
