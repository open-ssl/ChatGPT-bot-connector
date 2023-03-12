import psycopg2

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


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
        database=DB_NAME
    )


def fetch_data_from_db(query_template, fetchall=True, *args):
    """
    Безопасный запрос в базу данных на извлечение записей из выборки
    :param query_template: шаблон для запроса в БД
    :param fetchall: bool - выгружать все записи или только первую из выборки
    :param args: аргументы для вставки в шаблон запроса
    :return: Результаты запроса
    """
    connection = get_db_session()
    with connection as conn:
        pass
        cursor = conn.cursor()

        query_template = query_template.format(*args)
        cursor.execute(query_template)
        if not fetchall:
            return cursor.fetchone()
        return cursor.fetchall()
