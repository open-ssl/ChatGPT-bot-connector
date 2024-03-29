from dotenv import load_dotenv

import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_SCHEME = os.environ.get("DB_SCHEME")
ADMIN_TG_ID = os.environ.get("TG_USER_ID")
TG_AUTHOR_LINK = os.environ.get("TG_AUTHOR_LINK")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ORGANISATION_ID = os.environ.get("ORGANISATION_ID")
API_KEY1 = os.environ.get("API_KEY1")
API_KEY2 = os.environ.get("API_KEY2")
API_KEY3 = os.environ.get("API_KEY3")

