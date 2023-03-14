from locales.ru.locale import BotMessage as BotMessageRu
from locales.en.locale import BotMessage as BotMessageEn


def get_unique_methods():
    """
    Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
    """
    return [BotMessageRu.MAIN_MENU, BotMessageEn.MAIN_MENU]


def get_language_object_by_locale(locale: str):
    """
    Получить языковой обьект для работы с ботом по входной локали
    :param locale: en or ru
    :return: обьект для работы с локалью
    """
    return {'en': BotMessageEn, 'ru': BotMessageRu}.get(locale)
