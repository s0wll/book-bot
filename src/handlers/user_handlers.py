from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError

from src.database.db_manager import db
from src.schemas.users import UserAdd, UserUpdate
from src.filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from src.keyboards.bookmarks_kb import create_bookmarks_keyboard, create_edit_keyboard
from src.keyboards.pagination_kb import create_pagination_keyboard
from src.locales.lexicon import LEXICON
from src.services.file_handling import book


router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    try:
        await db.users.add_user(UserAdd(user_id=message.from_user.id))
    except IntegrityError as exc:
        if isinstance(exc.orig.__cause__, UniqueViolationError):
            await message.answer("Вы уже зарегистрированы и являетесь читателем")
    await db.commit()
    await message.answer(LEXICON[message.text])


@router.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands="beginning"))
async def process_beginning_command(message: Message):
    text = book[1]
    await message.answer(
        text=text, reply_markup=create_pagination_keyboard("backward", f"1/{len(book)}", "forward")
    )


@router.message(Command(commands="continue"))
async def process_continue_command(message: Message):
    user = await db.users.get_user_data(message.from_user.id)
    text = book[user.page]
    await message.answer(
        text=text,
        reply_markup=create_pagination_keyboard("backward", f"{user.page}/{len(book)}", "forward"),
    )


@router.message(Command(commands="bookmarks"))
async def process_bookmarks_command(message: Message):
    user = await db.users.get_user_data(message.from_user.id)
    if user.bookmarks:
        await message.answer(
            text=LEXICON[message.text], reply_markup=create_bookmarks_keyboard(*user.bookmarks)
        )
    else:
        await message.answer(text=LEXICON["no_bookmarks"])


@router.callback_query(F.data == "forward")
async def process_forward_press(callback: CallbackQuery):
    user = await db.users.get_user_data(callback.from_user.id)
    if user.page < len(book):
        new_page = user.page + 1
        await db.users.update_page_and_bookmarks(
            user_id=callback.from_user.id, update_data=UserUpdate(page=new_page)
        )
        text = book[new_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                "backward", f"{new_page}/{len(book)}", "forward"
            ),
        )
    await callback.answer()


@router.callback_query(F.data == "backward")
async def process_backward_press(callback: CallbackQuery):
    user = await db.users.get_user_data(callback.from_user.id)
    if user.page > 1:
        new_page = user.page - 1
        await db.users.update_page_and_bookmarks(
            user_id=callback.from_user.id, update_data=UserUpdate(page=new_page)
        )
        text = book[new_page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                "backward", f"{new_page}/{len(book)}", "forward"
            ),
        )
    await callback.answer()


@router.callback_query(lambda x: "/" in x.data and x.data.replace("/", "").isdigit())
async def process_page_press(callback: CallbackQuery):
    user = await db.users.get_user_data(callback.from_user.id)
    if user.bookmarks:
        new_bookmarks = user.bookmarks
    else:
        new_bookmarks = []
    new_bookmarks.append(user.page)
    await db.users.update_page_and_bookmarks(
        user_id=callback.from_user.id, update_data=UserUpdate(bookmarks=new_bookmarks)
    )
    await callback.answer("Страница добавлена в закладки!")


@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    text = book[int(callback.data)]
    user = await db.users.get_user_data(callback.from_user.id)
    user.page = int(callback.data)
    await callback.message.edit_text(
        text=text,
        reply_markup=create_pagination_keyboard("backward", f"{user.page}/{len(book)}", "forward"),
    )


@router.callback_query(F.data == "edit_bookmarks")
async def process_edit_press(callback: CallbackQuery):
    user = await db.users.get_user_data(callback.from_user.id)
    await callback.message.edit_text(
        text=LEXICON[callback.data], reply_markup=create_edit_keyboard(*user.bookmarks)
    )


@router.callback_query(F.data == "cancel")
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON["cancel_text"])


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    user = await db.users.get_user_data(callback.from_user.id)
    new_bookmarks = user.bookmarks
    new_bookmarks.remove(int(callback.data[:-3]))

    await db.users.update_page_and_bookmarks(
        user_id=callback.from_user.id, update_data=UserUpdate(bookmarks=new_bookmarks)
    )

    if new_bookmarks:
        await callback.message.edit_text(
            text=LEXICON["/bookmarks"], reply_markup=create_edit_keyboard(*new_bookmarks)
        )
    else:
        await callback.message.edit_text(text=LEXICON["no_bookmarks"])
