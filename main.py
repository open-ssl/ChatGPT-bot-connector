import telebot
from telebot import types
from random import choice
from string import ascii_uppercase
from functools import partial

import openai
from bot_config import bot, cache_client, CHAT_GPT_MODEL_NAME, KEY_LIST
from random import randint
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


def test_chat_gpt_dialog():
    request_text = 'Please come up with five names for the grocery store'
    # real_response = openai.Completion.create(
    #     api_key=get_random_api_key(),
    #     organization='org-j49bIGhFvzZ8qLOBajUzv5i0',
    #     model=CHAT_GPT_MODEL_NAME,
    #     prompt=request_text,
    #     max_tokens=100,
    #     temperature=0.6
    # )
    # sample_text = '\n\n1. Fresh Groceries\n2. Green Markets\n3. Supermarket Express\n4. Corner Pantry\n5. The Grocery Cart'
    # text = response.choices[0].text
    pass


def get_random_api_key():
    'gpt-3.5-turbo'
    key_index = randint(0, len(KEY_LIST) - 1)
    return KEY_LIST[key_index]


if __name__ == '__main__':
    print("Bot started")
    # helpers.initialize_main_menu()
    # bot.polling(none_stop=True)
    test_chat_gpt_dialog()
    print("Bot finished")
