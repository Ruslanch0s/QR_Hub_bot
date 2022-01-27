import datetime
from typing import List

import sqlalchemy as sa
from aiogram import Dispatcher
from gino import Gino

from data import config

db = Gino()


# выводит название и значение модели (сервисная информация например для логгирования)
class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns  # колонки и значения
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


# при каждом создании новой записи в таблицу будут добавляться дата создания и обновления значений
class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = db.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=db.func.now(),
    )


# на запуске нужно выполнять функцию привязки БД к ссылке
async def on_startup(dispatcher: Dispatcher):
    print("Установка связи с PostgreSQL")
    await db.set_bind(config.POSTGRES_URL)