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
    <td align="center" width="90">
      <a href="https://docs.docker.com/" target="_blank">
        <img alt="Docker" width="60" height="45" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original.svg" />
      </a>
      <br><h4>Docker</h4>
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
docker compose up```

