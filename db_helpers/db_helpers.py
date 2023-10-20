from time import time as now_time
from helpers.database import fetch_data_from_db, insert_data_in_db
from helpers.helpers import (
    SubscriptionStatus,
    Const,
    Config,
    BotCommands,
    Locale,
    log_error_in_file,
    get_timestamp_from_datetime
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
    temperature = Config.DEFAULT_TEMPERATURE_FOR_USER

    try:
        insert_data_in_db(
            sql_templates.INSERT_NEW_USER_IN_DB_TEMPLATE,
            user_id, first_name, last_name, username, language, temperature
        )
        insert_data_in_db(sql_templates.INSERT_NEW_SUB_INFO_IN_DB_TEMPLATE, user_id, Config.DEFAULT_TOKENS_COUNT)
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
    tokens = int(activity_and_tokens_info.get(Const.TOKENS))

    if has_subscription:
        # получить дату истечения подписки
        base_profile_text += locale_object.MY_PROFILE_INFO_WITH_SUB_TEXT
    else:
        # получить количество оставшихся токенов
        tokens = tokens if tokens > 0 else 0
        base_profile_text += locale_object.MY_PROFILE_INFO_NOT_SUB_TEXT.format(tokens)

    return base_profile_text


def get_temperature_for_user(user_id):
    """
    Получение значения температуры у пользователя
    :param user_id:
    :return:
    """
    temperature_data = fetch_data_from_db(sql_templates.GET_TEMPERATURE_FOR_USER_TEMPLATE, user_id)
    return temperature_data.get(Const.TEMPERATURE)


def set_new_tokens_count_for_user(user_id, response_tokens):
    """
    Изменяем количество использованных пользователем токенов в базе данных
    :param user_id: идентификатор пользователя
    :param response_tokens: количество токенов пользователя которое он использовал в текущем респонсе
    :return:
    """
    user_info = fetch_data_from_db(sql_templates.GET_TOKENS_FOR_USER_TEMPLATE, user_id)
    activity_status = user_info.get(Const.ACTIVITY_STATUS)
    tokens_count = int(user_info.get(Const.TOKENS))

    if activity_status == SubscriptionStatus.UNACTIVE:
        new_tokens_count = int(tokens_count) - response_tokens
        insert_data_in_db(sql_templates.UPDATE_TOKENS_COUNT_FOR_USER_TEMPLATE, new_tokens_count, user_id)


def is_subscription_active_for_user(user_id):
    """
    Проверка наличия подписки у пользователя
    :param user_id: идентификатор пользователя
    :return: bool - активна ли подписка?
    """

    user_info = fetch_data_from_db(sql_templates.GET_INFO_FOR_USER_TEMPLATE, user_id)
    activity_status = user_info.get(Const.ACTIVITY_STATUS)
    expired_at = get_timestamp_from_datetime(user_info.get(Const.EXPIRED_AT))
    tokens_count = int(user_info.get(Const.TOKENS))

    if activity_status == SubscriptionStatus.UNACTIVE and tokens_count <= 0:
        return False

    if activity_status == SubscriptionStatus.ACTIVE:
        if now_time() > expired_at:
            set_unactive_subscription_for_user(user_id)
            return False

    return True


def set_unactive_subscription_for_user(user_id):
    """
    Устанавливаем подписку пользользователя в неактивное состояние
    :return:
    """
    insert_data_in_db(
        sql_templates.UPDATE_SUBSCRIPTION_STATUS_FOR_USER_TEMPLATE, SubscriptionStatus.UNACTIVE, 0, user_id
    )


def set_active_subscription_for_user(user_id):
    """
    Устанавливаем активное состояние подписки для пользователя
    :param user_id:
    :return:
    """
    insert_data_in_db(
        sql_templates.UPDATE_SUBSCRIPTION_STATUS_FOR_USER_TEMPLATE, SubscriptionStatus.ACTIVE, Config.DEFAULT_TOKENS_COUNT, user_id
    )

