import telebot
from telebot import types
from random import choice
from string import ascii_uppercase
from functools import partial

from bot_config import bot
from helpers.helpers import (
    Const,
    BotCommands,
    BotMessage,
    post_request,
    log_error_in_file,
)


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Показываем главное меню бота
    :return: Отображаем кнопки Получить пробный, Купить подписку или Написать в поддержку
    Если это админ, то ему даем еще и кнопку админки
    """
    user_first_name = message.chat.first_name
    return bot.send_message(message.chat.id, BotMessage.START.format(user_first_name))


if __name__ == '__main__':
    print("Bot started")
    bot.polling(none_stop=True)
    print("Bot finished")
