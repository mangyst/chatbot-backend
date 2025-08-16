FROM python:3.12-slim

WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip --disable-pip-version-check && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходники
COPY src/ ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
