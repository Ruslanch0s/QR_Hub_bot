import asyncio
import concurrent.futures
import uuid

from yookassa import Configuration, Payment
from data.config import SHOP_ID, SHOP_KEY

Configuration.account_id = SHOP_ID
Configuration.secret_key = SHOP_KEY

data = {
    "amount": {
        "value": "35.00",
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.merchant-website.com/return_url"
    },
    "capture": True,
}


async def create_payment():
    response = await run_blocking_io(Payment.create, data)
    return response


async def get_update(payment_id):
    payment = await run_blocking_io(Payment.find_one, payment_id)
    return payment


async def run_blocking_io(func, *args):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(
            pool, func, *args
        )
    return result
