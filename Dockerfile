FROM python:3.12.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "sleep 5 && alembic upgrade head && python src/main.py"]
