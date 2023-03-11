import telebot
from pymemcache.client import base
BOT_API_TOKEN = ""


cache_client = base.Client(('localhost', 11211))
bot = telebot.TeleBot(BOT_API_TOKEN)