from src.repositories.users import UsersRepository
from src.database.database import async_session_maker


class DBManager:
    def __init__(self):
        self.session = async_session_maker()
        self.users = UsersRepository(self.session)

    async def commit(self):
        await self.session.commit()

    async def close(self):
        await self.session.close()


# Глобальный экземпляр для использования в хэндлерах
db = DBManager()
