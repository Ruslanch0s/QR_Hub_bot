import yookassa
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentType

from keyboards.inline import confirm_pay_pkpass_keyboard, confirm_pay_pkpass_button, check_pay_button
from keyboards.inline import pay_pkpass_callback
from keyboards.inline.callback_dates import check_pay_callback
from loader import dp
from utils import user_language, create_payment, get_update
from utils.db_api.example import add_payment, select_pending_payments
from utils.db_api.schemas.users import User
from utils.loggers import database, payments


from .qrgen import check_fot_wallet


@dp.callback_query_handler(pay_pkpass_callback.filter(), state='limit')
async def create_payment_pkpass(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await state.set_state('confirm_pay')
    check_pay_button.text = await user_language(call.from_user, 'check_pay_button')
    confirm_pay_pkpass_button.text = await user_language(call.from_user, 'confirm_pay_pkpass_button')
    payment = await create_payment()
    await add_payment(id=payment.id, user_id=call.from_user.id, status='pending')
    confirm_pay_pkpass_button.url = payment.confirmation.confirmation_url
    await call.message.answer(await user_language(call.from_user, 'confirm_pay'),
                              reply_markup=confirm_pay_pkpass_keyboard)


@dp.callback_query_handler(check_pay_callback.filter(), state='confirm_pay')
@dp.throttled(rate=7)
async def check_payment(call: CallbackQuery, state: FSMContext):
    await call.message.answer(await user_language(call.from_user, 'please_wait'))
    user = await User.get(call.from_user.id)

    try:
        pending_payments = await select_pending_payments(user_id=call.from_user.id)
    except Exception as err:
        database.logger.info(f'error: {err}')
        pending_payments = []

    for payment in pending_payments:
        try:
            update = await get_update(payment.id)
        except Exception as err:
            database.logger.info(f'error: {err}')
            break

        print(payment.status)
        if update.status == "succeeded":
            count = user.amount_gen + 3
            await user.update(amount_gen=count).apply()
            await payment.update(status="succeeded").apply()
            payments.logger.info(f'success - payment_status(succeeded) - {call.from_user.id} - {call.from_user.first_name}')

        elif update.status != "pending":
            await payment.update(status=update.status).apply()

    if user.amount_gen > 0:
        await check_fot_wallet(callback_query=call, state=state)
        payments.logger.info(f'success - amount_gen( > 0) - {call.from_user.id} - {call.from_user.first_name}')
    else:
        await call.message.answer(await user_language(call.from_user, 'error_pay'))
        payments.logger.info(f'error - amount_gen( > 0) - {call.from_user.id} - {call.from_user.first_name}')


@dp.message_handler(content_types=ContentType.ANY, state=["confirm_pay"])
async def wrong_choice(message: types.Message):
    await message.answer(await user_language(message.from_user, 'error_choice'))
    payments.logger.info(f'error - choice(pay) - {message.from_user.id} - {message.from_user.first_name}')
