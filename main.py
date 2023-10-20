import time

import openai
from decimal import Decimal
from random import randint
from threading import Thread

from bot_config import bot, cache_client, KEY_LIST
from config import ADMIN_TG_ID, ORGANISATION_ID
from helpers import helpers
from bot_config import CHAT_GPT_MODEL_NAME
from db_helpers.db_helpers import (
    initialise_user_if_need,
    generate_buttons_for_profile_menu_keyboard,
    get_localisation_for_user,
    set_new_locale_for_user,
    set_new_temperature_for_user,
    get_text_for_profile
)
from helpers.helpers import (
    BotCommands,
    get_main_menu_keyboard,
    get_profile_info_back_keyboard,
    get_menu_after_write_keyboard,
    get_menu_after_subscription_expired_keyboard,
    get_profile_keyboard,
    author_inline_keyboard,
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
            set_temperature_command(call.message)
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
    user_chat_id = message.chat.id
    message_id = message.message_id
    remove_message(user_chat_id, message_id)

    locale_object = get_localisation_for_user(user_chat_id)
    cache_client.set(str(user_chat_id), helpers.CachePhase.TEMPERATURE_INPUT)

    return bot.send_message(
        chat_id=user_chat_id,
        text=locale_object.TYPE_TEMPERATURE_TEXT,
    )


@bot.message_handler(func=helpers.input_temperature_validator)
def after_set_temperature_command(message):
    user_chat_id = message.chat.id
    text_from_user = message.html_text
    locale_object = get_localisation_for_user(user_chat_id)
    keyboard = get_profile_info_back_keyboard(locale_object)

    try:
        num_from_user = int(text_from_user)
    except:
        return bot.send_message(
            chat_id=user_chat_id,
            text=locale_object.WRONG_TEMPERATURE_TEXT,
            reply_markup=keyboard
        )

    if num_from_user < 0 or num_from_user > 10:
        return bot.send_message(
            chat_id=user_chat_id,
            text=locale_object.WRONG_TEMPERATURE_VALUE,
            reply_markup=keyboard
        )

    num_from_db = Decimal(num_from_user) / Decimal(10)
    num_from_db = float(num_from_db)
    cache_client.set(str(user_chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    set_new_temperature_for_user(user_chat_id, num_from_db)

    return bot.send_message(
        chat_id=user_chat_id,
        text=locale_object.REWRITE_TEMPERATURE_SUCCESS.format(num_from_user),
        reply_markup=keyboard
    )


def show_parameters_info(message):
    """
    Показать информацию по тому, как установить корректные параметры для бота
    :param message: обьект информации от телеграм
    :return: текст и клавиатура
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    keyboard = get_profile_info_back_keyboard(locale_object)

    remove_message(user_chat_id, message.message_id)

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


@bot.message_handler(func=helpers.start_conversation_command_validator)
def start_conversation_command_handler(message):
    """
    Нажали на запуск общения с ботом GPT
    :param message: обьект сообщения бота
    :return:
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    if not is_subscription_active_for_user(user_chat_id):
        return bot.send_message(
            user_chat_id,
            locale_object.EXPIRED_SUBSCRIPTION_TEXT,
            reply_markup=get_menu_after_subscription_expired_keyboard(locale_object),
            parse_mode='HTML'
        )

    cache_client.set(str(user_chat_id), helpers.CachePhase.WRITE_TEXT_FOR_GPT)
    return bot.send_message(user_chat_id, locale_object.TYPE_TEXT)


@bot.message_handler(func=helpers.about_bot_validator)
def about_bot_command_handler(message):
    """
    Нажали на команду о боте
    :param message: обьект сообщения бота
    :return:
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    keyboard = get_main_menu_keyboard(locale_object)
    return bot.send_message(user_chat_id, locale_object.ABOUT_BOT_TEXT, reply_markup=keyboard)


@bot.message_handler(func=helpers.write_chat_gpt_command_validator)
def answer_user_after_request(message):
    """
    Ответ пользователю от Chat-GPT после ввода информации
    :param message: обьект сообщения от пользователя
    :return:
    """
    user_chat_id = message.chat.id
    locale_object = get_localisation_for_user(user_chat_id)
    start_param = '=' * 5

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

    answer_from_chat_gpt = generate_answer_from_chat_gpt(user_chat_id, message.html_text)
    keyboard = get_menu_after_write_keyboard(locale_object)
    return bot.send_message(
        user_chat_id, answer_from_chat_gpt + locale_object.ANOTHER_QUESTION, reply_markup=keyboard
    )


@bot.message_handler(func=helpers.my_profile_command_validator)
def my_profile_request(message):
    """
    Нажали на команду мой профиль бота
    :param message: обьект сообщения телеграмма
    """
    user_chat_id = message.chat.id
    cache_client.set(str(user_chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    locale_object = get_localisation_for_user(user_chat_id)
    remove_message(user_chat_id, message.message_id)
    remove_message(user_chat_id, message.message_id-1)

    profile_buttons = generate_buttons_for_profile_menu_keyboard(locale_object, user_chat_id)
    keyboard = get_profile_keyboard(profile_buttons)

    profile_text = get_text_for_profile(user_chat_id, locale_object)
    return bot.send_message(user_chat_id, profile_text, reply_markup=keyboard, parse_mode='HTML')


@bot.message_handler(func=helpers.write_author_validator)
def write_author_request(message):
    """
    Нажали на команду мой профиль бота
    :param message: обьект сообщения телеграмма
    """
    user_chat_id = message.chat.id
    cache_client.set(str(user_chat_id), helpers.CachePhase.DEFAULT_DIALOG)
    locale_object = get_localisation_for_user(user_chat_id)
    inline_keyboard = author_inline_keyboard(locale_object)
    main_keyboard = get_main_menu_keyboard(locale_object)

    write_author_text = locale_object.WRITE_AUTHOR_TEXT
    main_menu_text= locale_object.MAIN_MENU
    bot.send_message(user_chat_id, write_author_text, reply_markup=inline_keyboard)
    return bot.send_message(user_chat_id, main_menu_text, reply_markup=main_keyboard)


@bot.message_handler(func=helpers.help_command_validator)
def help_request(message):
    """
    Нажали на команду "Помощь"
    :param message: обьект сообщения телеграмма
    """
    return write_author_request(message)


@bot.message_handler(func=helpers.unknown_command_validator)
def unknown_command_handler(message):
    """
    Нажали неизвестную команду не в режиме когда пишем боту
    :param message: обьект сообщения телеграмма
    """
    # do nothing
    pass
    # user_chat_id = message.chat.id
    # locale_object = get_localisation_for_user(user_chat_id)
    #
    # keyboard = get_main_menu_keyboard(locale_object)
    # locale_object = get_localisation_for_user(user_chat_id)
    # return bot.send_message(message.chat.id, locale_object.UNKNOWN_COMMAND, reply_markup=keyboard)


def remove_message(user_chat_id, message_id) -> None:
    """
    Удаление сообщения из диалога
    :param user_chat_id: идентификатор диалога
    :param message_id: идентификатор сообщения
    :return: None
    """
    try:
        thread = Thread(target=bot.delete_message, kwargs={"chat_id": user_chat_id, "message_id": message_id})
        thread.start()
    except Exception as e:
        log_error_in_file()


def generate_answer_from_chat_gpt(user_id, request_text):
    """
    Получить ответ от Chat GPT
    :param user_id: идентификатор пользователя
    :param request_text: текст запроса к Chat-GPT
    :return:
    """
    # 'gpt-3.5-turbo'
    res_rext = "Something went wrong"
    try:
        real_response = openai.Completion.create(
            api_key=get_random_api_key(),
            organization=ORGANISATION_ID,
            model=CHAT_GPT_MODEL_NAME,
            prompt=request_text,
            temperature=get_temperature_for_user(user_id)
        )
        # sample_text = '\n\n1. Fresh Groceries\n2. Green Markets\n3. Supermarket Express\n4. Corner Pantry\n5. The Grocery Cart'
        res_rext = real_response.choices[0].text
        # записать количество токенов для пользователя в базу
        # real_response.usage.total_tokens
    except Exception as e:
        log_error_in_file()

    return res_rext


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
    bot.send_message(chat_id=ADMIN_TG_ID, text="Start text")
    bot.polling(none_stop=True)
    # while True:
    #     bot.infinity_polling(timeout=10, long_polling_timeout=5)
    # generate_answer_from_chat_gpt()
    print("Bot finished")
