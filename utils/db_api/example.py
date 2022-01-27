import asyncio

from asyncpg import UniqueViolationError

from data.config import POSTGRES_URL
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User


async def add_user(id: int, name: str, email: str = None):
    user = User(id=id, name=name, email=email)
    await user.create()


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


async def test():
    await db.set_bind(POSTGRES_URL)
    await db.gino.drop_all()
    await db.gino.create_all()

    print("Добавляем пользователей")
    await add_user(1, "One", "gsaddsaf@gmail.com")
    await add_user(2, "tue", "gsa222ddsaf@gmail.com")
    await add_user(5, "tree", "gsaa333dsfddsaf@gmail.com")
    await add_user(4, "fore4")

    users = await select_all_users()
    print("All users: ", users)

    count = await count_users()
    print("Count all users: ", count)

    user = await select_user(2)
    print("user with id=2 is: ", user)


loop = asyncio.get_event_loop()
loop.run_until_complete(test())
