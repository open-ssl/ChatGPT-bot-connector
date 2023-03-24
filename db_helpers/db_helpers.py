from helpers.database import fetch_data_from_db, insert_data_in_db
from helpers.helpers import (
    Const,
    BotCommands,
    Locale,
    log_error_in_file
)
from db_helpers import sql_templates
from locales.main import get_language_object_by_locale


def initialise_user_if_need(message_obj):
    """
    Проверка наличия пользователя в базе при вызове команды /start
    Создаем нового пользователя и логику для написания боту если это необходимо
    :param message_obj: объект сообщения из телеграмма
    :return: True - пользователь проверен
    """
    if not check_user_in_db(message_obj.chat.id):
        create_new_user_in_db(message_obj)

    return bool('all checked')


def check_user_in_db(user_id: int) -> bool:
    """
    Проверка добавления пользователя в базу данных ранее
    :param user_id: айдишник пользователя для проверки
    :return: логика наличия нового пользователя
    """
    return fetch_data_from_db(sql_templates.CHECK_USER_IN_DB_TEMPLATE, user_id)


def create_new_user_in_db(message) -> bool:
    """
    Добавление нового пользователя в таблицу пользователей
    + Добавление стартовой информации о пользователе в таблицу информации по запросам в бота
    :param message: обьект сообщения телеграма с данными о пользователе
    :return: логический результат добавления пользователя
    """
    operation_result = True

    user_id = message.chat.id

    first_name = "\'{}\'".format(message.chat.first_name or '')
    last_name = "\'{}\'".format(message.chat.last_name or '')
    username = "\'{}\'".format(message.chat.username or '')
    language = "\'{}\'".format(Locale.ENGLISH)
    temperature = Const.DEFAULT_TEMPERATURE_FOR_USER

    try:
        insert_data_in_db(
            sql_templates.INSERT_NEW_USER_IN_DB_TEMPLATE,
            user_id, first_name, last_name, username, language, temperature
        )
        insert_data_in_db(sql_templates.INSERT_NEW_SUB_INFO_IN_DB_TEMPLATE, user_id)
    except Exception as e:
        log_error_in_file()
        operation_result = False

    return operation_result


def set_new_locale_for_user(user_id):
    """
    Замена локализации для пользователя
    :param user_id: идентификактор пользователя
    :return: новая установленная локаль
    """
    current_locale = fetch_data_from_db(sql_templates.GET_CURRENT_LOCALE_FOR_USER_TEMPLATE, user_id)
    new_locale = Locale.get_opposite_locale_for_user(current_locale)

    insert_data_in_db(sql_templates.UPDATE_LOCALE_FOR_USER_TEMPLATE, new_locale, user_id)

    return new_locale


def set_new_temperature_for_user(user_id, temperature_value: float):
    """
    Замена точности генерации для пользователя
    :param user_id: идентификактор пользователя
    :param temperature_value - новое значение точности
    :return: None
    """
    return insert_data_in_db(sql_templates.UPDATE_TEMPERATURE_FOR_USER_TEMPLATE, temperature_value, user_id)


def generate_buttons_for_profile_menu_keyboard(locale_object, user_id: int):
    """
    Генерирует элементы клавиатуры для пользователя исходя из данных в БД
    :param: locale_object - обьект локали для генерации текстов и надписей
    :param: user_id - айдишник пользователя
    :return: словарь обьектов клавиатуры
    """
    profile_data = fetch_data_from_db(sql_templates.GET_DATA_FOR_PROFILE_KEYBOARD_TEMPLATE, user_id)

    language = profile_data.get(Const.LANGUAGE)
    temperature = profile_data.get(Const.TEMPERATURE)
    temperature = float(temperature) * 10

    text_language = Locale.get_language_name_by_preffix(language)

    return {
        BotCommands.LANGUAGE: locale_object.LANGUAGE + f' {text_language}',
        BotCommands.TEMPERATURE: locale_object.TEMPERATURE + f' {int(temperature)}',
        BotCommands.PROFILE_INFO: locale_object.PROFILE_INFO,
        BotCommands.SAVE_PROFILE: locale_object.SAVE_PROFILE
    }


def get_localisation_for_user(user_id):
    """
    Получаем язык локализации для пользователя из БД
    и далее получаем по нему реальный обьект
    :param user_id: идентификтор пользователя
    :return: обьект локализации
    """
    current_locale = fetch_data_from_db(sql_templates.GET_CURRENT_LOCALE_FOR_USER_TEMPLATE, user_id)
    return get_language_object_by_locale(current_locale)


def get_text_for_profile(user_id, locale_object):
    """
    Получаем корректный текст для профиля пользоватеял
    :param user_id:
    :param locale_object:
    :return:
    """
    base_profile_text = locale_object.MY_PROFILE_TEXT
    activity_and_tokens_info = fetch_data_from_db(sql_templates.GET_ACTIVITY_AND_TOKENS_FOR_USER, user_id)

    has_subscription = activity_and_tokens_info.get(Const.ACTIVITY_STATUS)
    tokens = activity_and_tokens_info.get(Const.TOKENS)

    if has_subscription:
        # получить дату истечения подписки
        base_profile_text += locale_object.MY_PROFILE_INFO_WITH_SUB_TEXT
    else:
        # получить количество оставшихся токенов
        base_profile_text += locale_object.MY_PROFILE_INFO_NOT_SUB_TEXT.format(tokens)

    return base_profile_text
