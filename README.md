# book-bot

Это Telegram-бот-книга, в котором можно читать книгу Роберта Кийосаки "Богатый папа, бедный папа".  
Бот позволяет удобно читать книгу по страницам, сохранять закладки и управлять ими.

## Особенности проекта

- Инлайн кнопки пагинации для чтения книги
- Удобное меню с кнопками для навигации
- Интеграция с базой данных для постоянного хранения информации о закладках и текущей страницы книги пользователя

## Основной стек технологий

- Python, aiogram, PostgreSQL, SQLAlchemy, Pydantic, Alembic, Docker, Docker-compose, logging

## Установка и запуск

1. Клонируйте репозиторий, находясь в директории, куда хотите скачать проект:
```bash
git clone https://github.com/s0wll/book-bot.git
```

2. В корне проекта создайте файл .env и установите в нем следующие значения:
```bash
BOT_TOKEN=<токен вашего бота>
ADMIN_IDS='[ваш телеграм id]'

DB_HOST=book_bot_db
DB_PORT=5432
DB_USER=book_bot_user
DB_PASS=book_bot_pass
DB_NAME=book-bot
```

3. Запустите проект с помощью Docker Compose:
```bash
docker-compose up --build
```

## Команды бота

- `/start` — запуск бота и регистрация пользователя
- `/beginning` — перейти в начало книги
- `/continue` — продолжить чтение
- `/bookmarks` — показать список закладок
- `/help` — справка по работе бота
