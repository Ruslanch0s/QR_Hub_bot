from aiogram.utils.callback_data import CallbackData


language_callback = CallbackData("change_language", "language")
image_callback = CallbackData("picture", "file_name")
template_callback = CallbackData("templates")
wallet_callback = CallbackData("wallet")
cancel_callback = CallbackData("cancel")
create_pkpass_callback = CallbackData("create_pkpass")
pay_pkpass_callback = CallbackData("pay_pkpass")
