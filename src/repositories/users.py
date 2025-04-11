from sqlalchemy import insert, update

from src.models.users import UsersORM
from src.schemas.users import User, UserAdd, UserUpdate


class UsersRepository:
    model = UsersORM
    schema = User

    def __init__(self, session) -> None:
        self.session = session

    async def add_user(self, user_data: UserAdd) -> None:
        add_stmt = insert(self.model).values(**user_data.model_dump())
        await self.session.execute(add_stmt)

    async def update_page_and_bookmarks(
        self, update_data: UserUpdate, user_id: int, exclude_unset: bool = True
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(user_id=user_id)
            .values(
                **update_data.model_dump(exclude_unset=exclude_unset),
            )
        )
        await self.session.execute(update_stmt)
