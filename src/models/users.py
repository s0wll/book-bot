from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ARRAY, Integer

from src.database.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(unique=True)
    page: Mapped[int] = mapped_column(Integer, default=1, nullable=True)
    bookmarks: Mapped[list[int]] = mapped_column(ARRAY(Integer), default=[], nullable=True)
    

