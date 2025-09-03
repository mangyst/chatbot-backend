🤖 Deepbot — Chatbot Platform (Backend)

Deepbot — это платформа для чат-бота с веб-интерфейсом и API.
Архитектура проекта:

🧩 Backend — FastAPI (аутентификация, диалоги, сообщения, интеграция с AI)

🎨 Frontend — клиентское SPA-приложение (отдельный контейнер)

🌐 Nginx — реверс-прокси + HTTPS (Let's Encrypt)

👉 В этом README подробно описан backend.

🚀 Возможности backend

FastAPI + Uvicorn, OpenAPI (Swagger / ReDoc)

Авторизация через Google ID Token

JWT-аутентификация (cookie access_token, HttpOnly, Secure)

Управление диалогами (CRUD, ограничение до 5 диалогов на пользователя)

Обмен сообщениями (пользователь ↔ AI, ожидание ответа)

Служебные эндпоинты для интеграции с AI

Защищённый healthcheck

PostgreSQL (asyncpg + SQLAlchemy raw queries)

Docker/Docker Compose для деплоя

📂 Структура проекта
chatbot-backend/
├─ src/
│  ├─ api/          # эндпоинты (auth, dialogs, messages, health)
│  ├─ core/         # config.py (env), security.py (JWT)
│  ├─ models/       # Pydantic-схемы
│  ├─ repository/   # слой работы с БД
│  ├─ services/     # бизнес-логика (лимиты, флаги, ожидание AI)
│  └─ utils/        # логирование
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ main.py

⚙️ Установка и запуск
Локально
git clone https://github.com/mangyst/chatbot-backend.git
cd chatbot-backend

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

uvicorn src.main:app --reload

Docker

Сборка:

docker build -t chatbot-backend .


Запуск:

docker run -d \
  --name chatbot-backend \
  -p 8000:8000 \
  --env-file .env \
  chatbot-backend

Docker Compose (общая система)

Вместе с фронтом и nginx:

docker compose up -d


Backend: http://localhost:8000

Frontend: http://localhost:3000

Через nginx (SSL): https://your-domain/

📑 Примеры .env
.env.example (локально)
# === Database (local) ===
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=appdb
DATABASE_USER=app
DATABASE_PASSWORD=change-me

# === Backend access for AI ===
API_KEY_AI=dev-change-me

# === JWT / Security ===
SECRET_KEY_JWT=dev-change-me
ALGORITHM=HS256

# === Frontend origin (local) ===
ADDRESS_FRONT=http://localhost:5173

# === Google OAuth (local) ===
GOOGLE_CLIENT_ID=your-dev-google-client-id.apps.googleusercontent.com

# === Cookies over HTTPS (local) ===
SECURE_HTTP_HTTPS=false

# === Health key (local) ===
HEALTH_SECRET_KEY=dev-health-key

.env.production.example (продакшен)
# === Database (prod) ===
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=appdb
DATABASE_USER=app
DATABASE_PASSWORD=change-me-strong

# === Backend access for AI ===
API_KEY_AI=prod-change-me

# === JWT / Security ===
SECRET_KEY_JWT=really-strong-secret
ALGORITHM=HS256

# === Frontend origin (prod) ===
ADDRESS_FRONT=https://your-frontend.example.com

# === Google OAuth (prod) ===
GOOGLE_CLIENT_ID=your-prod-google-client-id.apps.googleusercontent.com

# === Cookies over HTTPS (prod) ===
SECURE_HTTP_HTTPS=true

# === Health key (prod) ===
HEALTH_SECRET_KEY=prod-health-key

🗄️ База данных

PostgreSQL (asyncpg).

Минимальная схема
CREATE TABLE users (
  user_id BIGSERIAL PRIMARY KEY,
  mail TEXT NOT NULL,
  google_id TEXT NOT NULL UNIQUE,
  given_name TEXT,
  family_name TEXT,
  picture TEXT
);

CREATE TABLE dialogs (
  dialog_id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  dialog_name VARCHAR(20) NOT NULL,
  status_flag BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE messages (
  message_id BIGSERIAL PRIMARY KEY,
  dialog_id BIGINT NOT NULL REFERENCES dialogs(dialog_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


⚠️ В системе бот = user_id=1. Создай такого пользователя вручную.

📡 API
Auth (/create/users, /me, /logout)

POST /create/users — вход по Google ID Token, создание пользователя, установка JWT в cookie

GET /me — текущий пользователь

POST /logout — выход, очистка cookie

Dialogs (/dialogs)

POST /create — создать диалог (макс. 5)

POST /delete — удалить

POST /rename — переименовать

POST / — список диалогов

GET /{id} — диалог по id (контекст сообщений)

GET /flag/{id} — флаг «ожидания ответа ИИ»

Messages

POST /send/message/ai — пользователь → AI (ожидание ответа)

GET /messages — служебный (X-Messages-Key)

POST /send/message/user — служебный (ИИ отвечает пользователю)

Health

GET /health (заголовок X-Health-Key)

🌐 CORS

В main.py настроен CORS:

origins = [ADDRESS_FRONT]


Разрешён только домен из .env (ADDRESS_FRONT).

Cookie передаются кросс-доменно (allow_credentials=True).

📝 Логирование

Единый логгер (src/utils/utils.py):

2025-09-03 12:34:56 - INFO - repository.py - Пользователь id:1 создал диалог id:10


Уровень INFO+

Вывод в консоль

Логи: операции с БД, ошибки, JWT-валидация

🐳 Docker Compose (общая система)

Файл docker-compose.yml поднимает три сервиса:

backend — FastAPI API

frontend — клиентское SPA

nginx — реверс-прокси с SSL

Пример запуска:

docker compose up -d


После старта:

API: http://localhost:8000

Swagger: http://localhost:8000/docs

Frontend: http://localhost:3000

Через nginx (SSL): https://your-domain/

🛡️ Безопасность

Авторизация: JWT в HttpOnly cookie

SECURE_HTTP_HTTPS=True — включает флаг Secure (нужен HTTPS)

Служебные эндпоинты /messages и /send/message/user — по ключу API_KEY_AI

Healthcheck — по ключу HEALTH_SECRET_KEY

Лимит диалогов — 5 на пользователя
