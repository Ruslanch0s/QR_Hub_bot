from utils.db_api.db_gino import TimedBaseModel
from sqlalchemy import Column, BigInteger, String, sql, Integer, ForeignKey


class Payment(TimedBaseModel):
    __tablename__ = 'payments'
    id = Column(String(100), primary_key=True, unique=True)
    user_id = Column(None, ForeignKey("users.id"))
    status = Column(String(100))

    query: sql.Select  # выбор данных из таблицы