from sqlalchemy import insert, select, update

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

    async def get_user_data(self, user_id: int) -> User:
        query = select(self.model).filter_by(user_id=user_id)
        result = await self.session.execute(query)
        model = self.schema.model_validate(result.scalars().one(), from_attributes=True)
        return model


    async def update_page_and_bookmarks(
        self, user_id: int, update_data: UserUpdate, exclude_unset: bool = True
    ) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(user_id=user_id)
            .values(
                **update_data.model_dump(exclude_unset=exclude_unset),
            )
        )
        await self.session.execute(update_stmt)
        await self.session.commit()
