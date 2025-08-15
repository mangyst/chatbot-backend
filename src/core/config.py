from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Подключение к базе данных
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = int(os.getenv('DATABASE_PORT'))
DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
# Подключение к AI
URL_AI = os.getenv('URL_AI')
API_KEY_AI = os.getenv('API_KEY_AI')
# Доступ к бекенду
SECRET_KEY_JWT = os.getenv('SECRET_KEY_JWT')
ALGORITHM = os.getenv('ALGORITHM')
# Адрес фронта
ADDRESS_FRONT = os.getenv('ADDRESS_FRONT')
# GOOGLE_CLIENT_ID
GOOGLE_CLIENT_ID= os.getenv('GOOGLE_CLIENT_ID')

