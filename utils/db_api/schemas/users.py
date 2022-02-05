from utils.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql, Integer


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    name = Column(String(100))
    amount_gen = Column(Integer, default=0)
    language = Column(String(100))

    query: sql.Select  # выбор данных из таблицы