import telebot
from telebot import types
from random import choice
from string import ascii_uppercase
from functools import partial

from bot_config import bot, cache_client
from helpers import helpers
from helpers.helpers import (
    Const,
    BotCommands,
    BotMessage,
    post_request,
    get_main_menu_keyboard,
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
    start_message = helpers.BotMessage.START.format(user_first_name)
    keyboard = get_main_menu_keyboard()

    return bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


@bot.message_handler(func=helpers.start_command_validator)
def start_bot_command_handler(message):
    """
    Нажали на запуск бота
    :param message:
    :return:
    """
    chat_id = message.chat.id
    cache_client.set(str(chat_id), helpers.CachePhase.WRITE_TEXT_FOR_GPT)
    return bot.send_message(chat_id, "Введите текст запрос к Chat GPT по-английски")


@bot.message_handler(func=helpers.unknown_command_validator)
def unknown_command_handler(message):
    """
    Нажали неизвестную команды
    :param message:
    :return:
    """
    keyboard = get_main_menu_keyboard()
    return bot.send_message(message.chat.id, "Не знаю такой команды\nПопробуйте ввести заново)", reply_markup=keyboard)


@bot.message_handler()
def answer_user_after_request(message):
    chat_id = message.chat.id
    cache_client.set(str(chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    return bot.send_message(chat_id, "Ждем ответа от Chat GPT")


if __name__ == '__main__':
    print("Bot started")
    helpers.initialize_main_menu()
    bot.polling(none_stop=True)
    print("Bot finished")
