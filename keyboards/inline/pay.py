from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from . import cancel_button

check_pay_button = InlineKeyboardButton(text='', callback_data='check_pay')

pay_pkpass_button = InlineKeyboardButton(text='', callback_data='pay_pkpass')
pay_pkpass_keyboard = InlineKeyboardMarkup(row_width=2).add(cancel_button, pay_pkpass_button)

confirm_pay_pkpass_button = InlineKeyboardButton(text='', callback_data='confirm_pay_pkpass')
confirm_pay_pkpass_keyboard = InlineKeyboardMarkup(row_width=2).add(cancel_button, confirm_pay_pkpass_button,
                                                                    check_pay_button)
