from aiogram.utils.callback_data import CallbackData


language_callback = CallbackData("change_language", "language")
image_callback = CallbackData("picture", "file_name")
template_callback = CallbackData("templates")
wallet_callback = CallbackData("wallet")
cancel_callback = CallbackData("cancel")
create_pkpass_callback = CallbackData("picture", "template_id")
pay_pkpass_callback = CallbackData("pay_pkpass")
confirm_pay_pkpass_callback = CallbackData("confirm_pay_pkpass")
check_pay_callback = CallbackData("check_pay")