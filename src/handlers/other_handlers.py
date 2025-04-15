from aiogram import Router
from aiogram.types import Message


router = Router()


@router.message()
async def send_unknown_message(message: Message):
    await message.answer(
        "Упс... Незнакомое для меня сообщение.\n"
        "Пожалуйста, используйте соответствующие команды.\n\n"
        "Для просмотра списка команд напишите /help"
    )
