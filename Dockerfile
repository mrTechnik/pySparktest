# Используем базовый образ Python
FROM python:3.10

# Устанавливаем переменную окружения для предотвращения вывода сообщений ошибок от Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# активировать bash окружение
CMD ["bash"]

# Обновление и установка jre для запуска spark
RUN apt-get update && apt-get install -y default-jre

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы приложения в рабочую директорию
COPY . /app

# Устанавливаем зависимости
RUN pip install  --default-timeout=300 -r requirements.txt

# Команда для автоматического запуска скрипта main.py
CMD ["python", "/app/main.py"]