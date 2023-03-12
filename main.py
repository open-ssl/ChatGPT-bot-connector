import time

import telebot
from telebot import types
from random import choice
from string import ascii_uppercase
from functools import partial

import openai
from bot_config import bot, cache_client, CHAT_GPT_MODEL_NAME, KEY_LIST
from random import randint
from helpers import helpers
from helpers.translator import convert_text
from helpers.helpers import (
    Const,
    BotCommands,
    BotMessage,
    post_request,
    get_main_menu_keyboard,
    get_menu_after_write_keyboard,
    log_error_in_file,
)


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Показываем стартовое меню бота
    :return: Отображаем кнопки Получить пробный, Купить подписку или Написать в поддержку
    Если это админ, то ему даем еще и кнопку админки
    """
    user_first_name = message.chat.first_name
    start_message = helpers.BotMessage.START_TEXT.format(user_first_name)
    keyboard = get_main_menu_keyboard()

    return bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


@bot.message_handler(func=helpers.main_menu_bot_command_validator)
def show_main_menu_command(message):
    """
    Показываем главное меню бота после выхода из режима написания бота
    :return:
    """
    chat_id = message.chat.id

    cache_client.set(str(chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    result_message = helpers.BotMessage.MAIN_MENU_TEXT
    keyboard = get_main_menu_keyboard()
    return bot.send_message(message.chat.id, result_message, reply_markup=keyboard)


@bot.message_handler(func=helpers.start_bot_command_validator)
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
    Нажали неизвестную команду не в режиме когда пишем боту
    :param message:
    :return:
    """
    keyboard = get_main_menu_keyboard()
    # message.chat.id
    return bot.send_message(message.chat.id, "Не знаю такой команды\nПопробуйте ввести заново)", reply_markup=keyboard)


@bot.message_handler(func=helpers.write_chat_gpt_command_validator)
def answer_user_after_request(message):
    chat_id = message.chat.id
    start_param = '=' * 5

    base_text = "\nЖдем ответа от Chat GPT\n"
    result_text = "Ответ от Chat GPT:\n\n"
    msg = bot.send_message(chat_id, start_param + base_text + start_param)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=chat_id, message_id=msg.message_id)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=chat_id, message_id=msg.message_id)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=chat_id, message_id=msg.message_id)
    time.sleep(0.5)
    bot.edit_message_text(text=result_text, chat_id=chat_id, message_id=msg.message_id)

    answer_from_chat_gpt = generate_answer_from_chat_gpt('Please come up with five names for the grocery store')
    keyboard = get_menu_after_write_keyboard()
    bot.send_message(chat_id, answer_from_chat_gpt)
    return bot.send_message(chat_id, "Вы можете задать еще один вопрос прямо в этом диалоге\nЕсли хотите поменять настройки вы можете нажать кнопку \"Главное меню\"", reply_markup=keyboard)


def generate_answer_from_chat_gpt(request_text):
    return '\n\n1. Fresh Groceries\n2. Green Markets\n3. Supermarket Express\n4. Corner Pantry\n5. The Grocery Cart'


def get_random_api_key():
    'gpt-3.5-turbo'
    key_index = randint(0, len(KEY_LIST) - 1)
    return KEY_LIST[key_index]


if __name__ == '__main__':
    print("Bot started")
    # helpers.initialize_main_menu()
    bot.polling(none_stop=True)
    # generate_answer_from_chat_gpt()
    print("Bot finished")
