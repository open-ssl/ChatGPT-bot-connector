from time import sleep
from helpers.helpers import Config, log_error_in_file
from db_helpers.db_helpers import (
    get_users_for_refresh_default_subscription,
    refresh_default_subscription_for_users
)

REFRESH_TOKENS_TIMEOUT = 60


def refresh_tokens_for_users():
    """
    Поиск пользователей, у которых базовая подписка истекла неделю назад
    Обновление количества токенов и даты следующего обновления токенов
    :return:
    """
    try:
        users_ids = get_users_for_refresh_default_subscription()
        if not users_ids:
            return
        data = list()

        for user_id in users_ids:
            data.append((Config.DEFAULT_TOKENS_COUNT, user_id))

        refresh_default_subscription_for_users([(Config.DEFAULT_TOKENS_COUNT, user_id) for user_id in users_ids])
    except:
        log_error_in_file()


if __name__ == '__main__':
    while True:
        refresh_tokens_for_users()
        sleep(REFRESH_TOKENS_TIMEOUT)
