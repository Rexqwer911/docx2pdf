# Используем Python базовый образ
FROM python:3.9-slim

# Устанавливаем LibreOffice
RUN apt-get update && \
    apt-get install -y libreoffice && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копируем приложение в контейнер
COPY docxtopdf.py .

# Открываем порт для доступа к API
EXPOSE 8080

# Запуск приложения с gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "docxtopdf:app"]