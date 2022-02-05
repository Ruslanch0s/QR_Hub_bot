import asyncio

import asyncpg
from asyncpg import UniqueViolationError

from data.config import POSTGRES_URL
from utils.db_api.db_gino import db
from utils.db_api.schemas.users import User
from utils.db_api.schemas.payments import Payment
from sqlalchemy import and_

from utils.loggers.database import logger


async def add_user(id_user: int, name: str, amount_gen: int = 0, language: str = None):
    try:
        await User(
            name=name,
            id=id_user,
            amount_gen=amount_gen,
            language=language
        ).create()
    except asyncpg.UniqueViolationError as err:
        logger.info(f'error - add_user:\n{err}')


async def add_payment(id: int, user_id: int, status: str):
    try:
        await Payment(id=id, user_id=user_id, status=status).create()
    except Exception as err:
        logger.info(f'error - add_payment:\n{err}')


async def select_pending_payments(user_id: int):
    payments = await Payment.query.where(and_(Payment.user_id == user_id, Payment.status == "pending")).gino.all()
    return payments



"""
---------------------
"""


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.id).gino.scalar()  # scalar вывод одного значения
    return total


async def update_user_email(id: int, email: str):
    user = await User.get(id)  # only ID
    await user.update(email=email).apply()  # apply - применить

