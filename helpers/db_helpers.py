from helpers.database import fetch_data_from_db, insert_data_in_db
from helpers.helpers import Locale, log_error_in_file
from helpers import sql_templates


def initialise_user_if_need(message_obj):
    """
    Проверка наличия пользователя в базе при вызове команды /start
    Создаем нового пользователя и логику для написания боту если это необходимо
    :param message_obj: объект сообщения из телеграмма
    :return: True - пользователь проверен
    """
    if not check_user_in_db(message_obj.chat.id):
        # добавить инициализацию поля с токенами для пользователя
        create_new_user_in_db(message_obj)

    return bool('all checked')


def check_user_in_db(user_id: int) -> bool:
    """
    Проверка добавления пользователя в базу данных ранее
    :param user_id: айдишник пользователя для проверки
    :return: логика наличия нового пользователя
    """
    query_result = fetch_data_from_db(sql_templates.CHECK_USER_IN_DB_TEMPLATE, user_id, fetchall=False)
    return query_result[0]


def create_new_user_in_db(message) -> bool:
    operation_result = True

    user_id = message.chat.id

    first_name = "\'{}\'".format(message.chat.first_name or '')
    last_name = "\'{}\'".format(message.chat.last_name or '')
    username = "\'{}\'".format(message.chat.username or '')
    language = "\'{}\'".format(Locale.ENGLISH)

    try:
        insert_data_in_db(
            sql_templates.INSERT_NEW_USER_IN_DB_TEMPLATE,
            user_id, first_name, last_name, username, language,
        )
    except Exception as e:
        log_error_in_file()
        operation_result = False

    return operation_result
