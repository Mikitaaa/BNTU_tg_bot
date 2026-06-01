# Берём официальный образ Python 3.11 (можно заменить на 3.9/3.10, если нужно)
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Указываем команду для запуска бота
CMD ["/usr/local/bin/python", "Tg_bot.py"]
