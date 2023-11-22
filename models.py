import datetime

from sqlalchemy import Integer, String, func, Date
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tg_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String(200), nullable=True)
    created_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.date(func.now()))