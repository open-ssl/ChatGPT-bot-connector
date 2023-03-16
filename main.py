import time

from random import randint
from threading import Thread

from bot_config import bot, cache_client, KEY_LIST
from helpers import helpers
from db_helpers.db_helpers import (
    initialise_user_if_need,
    generate_buttons_for_profile_menu_keyboard,
    get_localisation_for_user,
    set_new_locale_for_user,
    get_text_for_profile
)
from helpers.helpers import (
    BotCommands,
    get_main_menu_keyboard,
    get_profile_info_back_keyboard,
    get_menu_after_write_keyboard,
    get_profile_keyboard,
    log_error_in_file,
)


def main_callback():
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """
    Проверяем все колбеки и в зависимости от выбранной секции, основная или админская, даем ему ответ на сообщение
    """
    if call.message:
        if call.data == BotCommands.LANGUAGE:
            set_language_command(call.message)
        elif call.data == BotCommands.TEMPERATURE:
            set_language_command(call.message)
        elif call.data == BotCommands.PROFILE_INFO:
            show_parameters_info(call.message)
        elif call.data == BotCommands.SAVE_PROFILE:
            user_chat_id = call.message.chat.id
            message_id = call.message.message_id

            remove_message(user_chat_id, message_id)
            show_main_menu_command(call.message)


def set_language_command(message):
    """
    Команда Установить новый язык пользователю
    :param message: обьект сообщения пользователя из телеграмма
    :return: отредактированное сообщение
    """
    user_chat_id = message.chat.id
    message_id = message.message_id
    set_new_locale_for_user(user_chat_id)

    locale_object = get_localisation_for_user(user_chat_id)

    profile_buttons = generate_buttons_for_profile_menu_keyboard(locale_object, user_chat_id)
    keyboard = get_profile_keyboard(profile_buttons)

    profile_text = get_text_for_profile(user_chat_id, locale_object)

    return bot.edit_message_text(
        text=profile_text,
        chat_id=user_chat_id,
        message_id=message_id,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


def set_temperature_command(message):
    """
    Устанавливаем точность генерации сообщения для бота
    :param message: обьект сообщения пользователя из телеграмма
    :return: обновленный профиль
    """
    pass


def show_parameters_info(message):
    """
    Показать информацию по тому, как установить корректные параметры для бота
    :param message: обьект информации от телеграм
    :return: текст и клавиатура
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    keyboard = get_profile_info_back_keyboard(locale_object)

    thread = Thread(target=remove_message, args=(user_chat_id, message.message_id))
    thread.start()

    return bot.send_message(
        chat_id=user_chat_id,
        text=locale_object.TEMPERATURE_TEXT,
        reply_markup=keyboard,
        parse_mode='HTML'
    )


@bot.message_handler(commands=['start'])
def start_command(message):
    """
    Показываем стартовое меню бота
    :return: Отображаем кнопки Получить пробный, Купить подписку или Написать в поддержку
    Если это админ, то ему даем еще и кнопку админки
    """
    initialise_user_if_need(message)
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    user_first_name = message.chat.first_name

    if user_first_name:
        start_message = locale_object.START_TEXT.format(user_first_name)
    else:
        start_message = locale_object.START_COMMON_TEXT

    keyboard = get_main_menu_keyboard(locale_object)

    return bot.send_message(message.chat.id, start_message, reply_markup=keyboard)


@bot.message_handler(func=helpers.main_menu_bot_command_validator)
def show_main_menu_command(message):
    """
    Показываем главное меню бота после выхода из режима написания бота или редактирования профиля
    :return:
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)

    cache_client.set(str(user_chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    result_message = locale_object.MAIN_MENU_TEXT
    keyboard = get_main_menu_keyboard(locale_object)
    return bot.send_message(message.chat.id, result_message, reply_markup=keyboard)


@bot.message_handler(func=helpers.start_bot_command_validator)
def start_bot_command_handler(message):
    """
    Нажали на запуск бота
    :param message: обьект сообщения бота
    :return:
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    cache_client.set(str(user_chat_id), helpers.CachePhase.WRITE_TEXT_FOR_GPT)

    return bot.send_message(user_chat_id, locale_object.TYPE_TEXT)


@bot.message_handler(func=helpers.write_chat_gpt_command_validator)
def answer_user_after_request(message):
    user_chat_id = message.chat.id
    start_param = '=' * 5
    locale_object = get_localisation_for_user(user_chat_id)
    base_text = locale_object.WAITING_ANSWER_FROM_GPT
    result_text = locale_object.ANSWER_FROM_GPT
    msg = bot.send_message(user_chat_id, start_param + base_text + start_param)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=user_chat_id, message_id=msg.message_id)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=user_chat_id, message_id=msg.message_id)
    start_param += start_param
    time.sleep(1)
    bot.edit_message_text(text=start_param + base_text + start_param, chat_id=user_chat_id, message_id=msg.message_id)
    time.sleep(0.5)
    bot.edit_message_text(text=result_text, chat_id=user_chat_id, message_id=msg.message_id)

    answer_from_chat_gpt = generate_answer_from_chat_gpt('Please come up with five names for the grocery store')
    keyboard = get_menu_after_write_keyboard(locale_object)
    bot.send_message(user_chat_id, answer_from_chat_gpt)
    return bot.send_message(user_chat_id, locale_object.ANOTHER_QUESTION, reply_markup=keyboard)


@bot.message_handler(func=helpers.my_profile_command_validator)
def my_profile_request(message):
    """
    Нажали на команду мой профиль бота
    :param message: обьект сообщения телеграмма
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    thread = Thread(target=remove_message, args=(user_chat_id, message.message_id))
    thread2 = Thread(target=remove_message, args=(user_chat_id, message.message_id - 1))
    thread.start()
    thread2.start()

    profile_buttons = generate_buttons_for_profile_menu_keyboard(locale_object, user_chat_id)
    keyboard = get_profile_keyboard(profile_buttons)

    profile_text = get_text_for_profile(user_chat_id, locale_object)
    return bot.send_message(user_chat_id, profile_text, reply_markup=keyboard, parse_mode='HTML')


@bot.message_handler(func=helpers.unknown_command_validator)
def unknown_command_handler(message):
    """
    Нажали неизвестную команду не в режиме когда пишем боту
    :param message: обьект сообщения телеграмма
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)

    keyboard = get_main_menu_keyboard(locale_object)
    locale_object = get_localisation_for_user(user_chat_id)
    return bot.send_message(message.chat.id, locale_object.UNKNOWN_COMMAND, reply_markup=keyboard)


def remove_message(user_chat_id, message_id) -> None:
    """
    Удаление сообщения из диалога
    :param user_chat_id: идентификатор диалога
    :param message_id: идентификатор сообщения
    :return: None
    """
    try:
        return bot.delete_message(chat_id=user_chat_id, message_id=message_id)
    except Exception as e:
        log_error_in_file()
        return


def generate_answer_from_chat_gpt(request_text):
    """
    Получить ответ от Chat GPT
    :param request_text: текст запроса к Chat GPT по английски
    :return:
    """
    # 'gpt-3.5-turbo'

    return '\n\n1. Fresh Groceries\n2. Green Markets\n3. Supermarket Express\n4. Corner Pantry\n5. The Grocery Cart'


def get_random_api_key() -> str:
    """
    Получение случайного API ключа для запроса к Chat-GPT
    Снижаем нагрузку на сервер
    :return: str - API ключ для запроса в API Chat-GPT
    """
    key_index = randint(0, len(KEY_LIST) - 1)
    return KEY_LIST[key_index]


if __name__ == '__main__':
    print("Bot started")
    # helpers.initialize_main_menu()
    bot.polling(none_stop=True)
    # generate_answer_from_chat_gpt()
    print("Bot finished")
