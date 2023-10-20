import psycopg2

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, DB_SCHEME


def get_db_session() -> psycopg2.connect:
    """
    Возвращает объект сессии для работы с базой данных
    :return: connection для работы с БД
    """
    return psycopg2.connect(
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        options="-c search_path=dbo,{}".format(DB_SCHEME)
    )


def fetch_data_from_db(query_template, *args, fetchone=True):
    """
    Безопасный запрос в базу данных на извлечение записей из выборки
    :param query_template: шаблон для запроса в БД
    :param fetchone: bool - выгружать только первую из выборки или все
    :param args: аргументы для вставки в шаблон запроса
    :return: Результаты запроса
    """
    connection = get_db_session()
    with connection as conn:
        pass
        cursor = conn.cursor()

        query_template = query_template.format(*args)
        cursor.execute(query_template)
        if fetchone:
            return cursor.fetchone()[0]
        return cursor.fetchall()[0]


def insert_data_in_db(query_template, *args):
    """
    Безопасный запрос в базу данных на вставку или изменение записей
    :param query_template: шаблон для запроса в БД
    :param args: аргументы для вставки в шаблон запроса
    :return: None
    """
    connection = get_db_session()
    with connection as conn:
        pass
        cursor = conn.cursor()

        query_template = query_template.format(*args)
        cursor.execute(query_template)
