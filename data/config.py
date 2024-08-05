from os import environ as ev
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv(dotenv_path=".env")

API_TOKEN = ev.get('BOT_TOKEN')
ADMIN_ID = ev.get('ADMIN_TELEGRAM_ID')

DB_HOST = "postgres"
DB_PORT = "5432"

DB_USERNAME = ev.get("DB_USERNAME")
DB_PWD = ev.get("DB_PWD")
DB_NAME = "main"

DB_REDIS_HOST = "redis"
DB_REDIS_PORT: int = 6379
REDIS_PASSWORD = "1234"
REDIS_USER = "redis"
REDIS_USER_PASSWORD = "1234"