# 🤖 Deepbot Backend

**FastAPI | PostgreSQL | JWT | Docker**

---

## 💬 About Project

- 🧩 **Backend** для платформы чат-бота (Deepbot)
- 🐍 Написан на **Python (FastAPI)**
- 🗄️ Хранение в **PostgreSQL** (asyncpg + SQLAlchemy)
- 🔐 Авторизация через **Google OAuth2 + JWT (cookies)**
- 💬 Управление **диалогами** и **сообщениями** (user ↔ AI)
- 🛠️ Контейнеризация через **Docker / Docker Compose**
- ☁️ Работает в связке с **Frontend** и **Nginx**
  - **Frontend**: https://github.com/mangyst/chatbot-front
  - **Nginx**: https://github.com/mangyst

---

<h1> Tech Stack <a href="#-tech-stack--"><img src="https://raw.githubusercontent.com/HighAmbition211/HighAmbition211/auxiliary/others/skill.gif" width="32"></a> </h1>

### Languages
<table>
  <tr>
    <td align="center" width="90">
      <a href="https://www.python.org/" target="_blank">
        <img alt="Python" width="45" height="45" src="https://raw.githubusercontent.com/HighAmbition211/HighAmbition211/auxiliary/languages/python.svg" />
      </a>
      <br><h4>Python</h4>
    </td>
    <td align="center" width="90">
      <a href="https://en.wikipedia.org/wiki/SQL" target="_blank">
        <img alt="SQL" width="45" height="45" src="https://www.svgrepo.com/show/331760/sql-database-generic.svg" />
      </a>
      <br><h4>SQL</h4>
    </td>
  </tr>
</table>

### Frameworks & Libraries
<table>
  <tr>
    <td align="center" width="90">
      <a href="https://fastapi.tiangolo.com/" target="_blank">
        <img alt="FastAPI" width="45" height="45" src="https://icon.icepanel.io/Technology/svg/FastAPI.svg" />
      </a>
      <br><h4>FastAPI</h4>
    </td>
    <td align="center" width="90">
      <a href="https://docs.pydantic.dev" target="_blank">
        <img alt="Pydantic" width="45" height="45" src="https://avatars.githubusercontent.com/u/116566593?s=200&v=4" />
      </a>
      <br><h4>Pydantic</h4>
    </td>
    <td align="center" width="90">
      <a href="https://www.sqlalchemy.org/" target="_blank">
        <img alt="SQLAlchemy" height="45" src="https://www.sqlalchemy.org/img/sqla_logo.png" />
      </a>
      <br><h4>SQLAlchemy</h4>
    </td>
  </tr>
</table>

### Databases
<table>
  <tr>
    <td align="center" width="90">
      <a href="https://www.postgresql.org/" target="_blank">
        <img alt="PostgreSQL" width="45" height="45" src="https://raw.githubusercontent.com/HighAmbition211/HighAmbition211/auxiliary/databases/postgres.svg" />
      </a>
      <br><h4>PostgreSQL</h4>
    </td>
  </tr>
</table>

### Tools & DevOps
<table>
 <td align="center" width="90">
        <a href="https://www.docker.com/" target="_blank"><img alt="Docker" width="45" height="45" style="padding:10px;" src="https://raw.githubusercontent.com/HighAmbition211/HighAmbition211/auxiliary/tools/docker.svg" /></a>
        <br><h4>Docker</h4>
  </td>
  <td align="center" width="90">
        <a href="https://www.nginx.com/" target="_blank"><img alt="Nginx" width="45" height="45" style="padding:10px;" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" /></a>
        <br><h4>Nginx</h4>
  </td>
</table>

---

## 📂 Структура проекта

```
├─ src/
│ ├─ api/ # эндпоинты (auth, dialogs, messages, health)
│ ├─ core/ # config.py (env), security.py (JWT)
│ ├─ schemas/ # Pydantic-схемы
│ ├─ repository/ # слой работы с БД
│ ├─ services/ # бизнес-логика (лимиты, флаги, ожидание AI)
│ ├─ utils/ # логирование
│ └─ main.py
├─ .env.example # переменные окружения
├─ requirements.txt
├─ Dockerfile
└─ docker-compose.yml
```

---

## 📦 Installation & Run

```bash
git clone https://github.com/mangyst/chatbot-backend.git
cd chatbot-backend

# локально
pip install -r requirements.txt
uvicorn src.main:app --reload

# через Docker
docker build -t chatbot-backend .
docker run -d -p 8000:8000 --env-file .env chatbot-backend

# через Docker Compose (с фронтом и nginx)
docker compose up -d
```

---

## 📑 Env Examples

### `.env.example`
```env
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
```

---

## 📑 Env Examples Production

### `.env.production.example`
```env
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
```

---

## 🗄️ Database Schema
``` SQL
CREATE TABLE users (
  user_id BIGSERIAL PRIMARY KEY,
  mail TEXT NOT NULL,
  google_id TEXT NOT NULL UNIQUE,
  given_name TEXT,
  family_name TEXT,
  picture TEXT
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE dialogs (
  dialog_id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  dialog_name VARCHAR(20) NOT NULL,
  status_flag BOOLEAN NOT NULL DEFAULT FALSE
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE messages (
  message_id BIGSERIAL PRIMARY KEY,
  dialog_id BIGINT NOT NULL REFERENCES dialogs(dialog_id) ON DELETE CASCADE,
  user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
⚠️ Бот в системе = user_id=1.

---

## 📡 API Endpoints

Auth (/create/users, /me, /logout)
- POST /create/users — вход по Google ID Token, создание пользователя, установка JWT в cookie
- GET /me — текущий пользователь
- POST /logout — выход, очистка cookie

Dialogs (/dialogs)
- POST /create — создать диалог (макс. 5)
- POST /delete — удалить
- POST /rename — переименовать
- POST / — список диалогов
- GET /{id} — диалог по id (контекст сообщений)
- GET /flag/{id} — флаг «ожидания ответа ИИ»

Messages
- POST /send/message/ai — пользователь → AI (ожидание ответа)
- GET /messages — служебный (X-Messages-Key)
- POST /send/message/user — служебный (ИИ отвечает пользователю)

Health
- GET /health (заголовок X-Health-Key)

---

## 🌐 CORS

В main.py настроен CORS:

```python
origins = [ADDRESS_FRONT]
```

Разрешён только домен из .env (ADDRESS_FRONT).
Cookie передаются кросс-доменно (allow_credentials=True).

---

## 📝 Логирование

Единый логгер (src/utils/utils.py):

```bash
2025-09-03 12:34:56 - INFO - repository.py - Пользователь id:1 создал диалог id:10
```

- Уровень INFO+
- Вывод в консоль
- Логи: операции с БД, ошибки, JWT-валидация

---

## 🐳 Docker Compose (общая система)

Файл docker-compose.yml поднимает три сервиса:
- backend — FastAPI API
- frontend — клиентское SPA
- nginx — реверс-прокси с SSL

После старта:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Через nginx (SSL): https://your-domain/
  
---

## 🛡️ Безопасность

- Авторизация: JWT в HttpOnly cookie
- SECURE_HTTP_HTTPS=True — включает флаг Secure (нужен HTTPS)
- Служебные эндпоинты /messages и /send/message/user — по ключу API_KEY_AI
- Healthcheck — по ключу HEALTH_SECRET_KEY
- Лимит диалогов — 5 на пользователя

---



