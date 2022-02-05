from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

template_button = InlineKeyboardButton(text='', callback_data='templates')
add_to_wallet_button = InlineKeyboardButton(text='', callback_data='wallet')
cancel_button = InlineKeyboardButton(text='cancel_button', callback_data='cancel')

create_pkpass_buttons = [
    InlineKeyboardButton(text='1', callback_data='picture:5774673378541568'),
    InlineKeyboardButton(text='2', callback_data='picture:4648773471698944'),
    InlineKeyboardButton(text='3', callback_data='picture:5359138740371456'),
    InlineKeyboardButton(text='4', callback_data='picture:6044435400622080'),
    InlineKeyboardButton(text='5', callback_data='picture:5011195252441088'),
    InlineKeyboardButton(text='6', callback_data='picture:6612359999913984'),
    InlineKeyboardButton(text='7', callback_data='picture:5310589436690432'),
    InlineKeyboardButton(text='8', callback_data='picture:4514555231993856'),
    InlineKeyboardButton(text='9', callback_data='picture:5182239707758592'),
    InlineKeyboardButton(text='10', callback_data='picture:5953170432589824'),
    InlineKeyboardButton(text='11', callback_data='picture:5680491548901376'),
    InlineKeyboardButton(text='12', callback_data='picture:5043824991404032'),
    cancel_button,
]
create_pkpass_keyboard = InlineKeyboardMarkup(row_width=3).add(*create_pkpass_buttons)

buttons = [
    InlineKeyboardButton(text='1', callback_data='picture:dogy_1.jpg'),
    InlineKeyboardButton(text='2', callback_data='picture:dogy_2.jpg'),
    InlineKeyboardButton(text='3', callback_data='picture:dogy_3.jpeg'),
    InlineKeyboardButton(text='4', callback_data='picture:dogy_4.jpg'),
    InlineKeyboardButton(text='5', callback_data='picture:virus.jpeg'),
    InlineKeyboardButton(text='6', callback_data='picture:the_witcher_1.jpg'),
    InlineKeyboardButton(text='7', callback_data='picture:zebra.jpg'),
    InlineKeyboardButton(text='8', callback_data='picture:china.jpg'),
    cancel_button,
]
images_keyboard = InlineKeyboardMarkup(row_width=4).add(*buttons)
