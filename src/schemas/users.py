from pydantic import BaseModel


class UserAdd(BaseModel):
    user_id: int


class UserUpdate(BaseModel):
    page: int | None =  None
    bookmarks: list[int] | None = None


class User(UserAdd, UserUpdate):
    id: int
