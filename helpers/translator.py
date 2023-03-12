from helpers.helpers import Locale
from bot_config import translator
import re


def convert_text(message, src_lang=Locale.ENGLISH, dst_lang=Locale.RUSSIAN):
    """
    Переводим текст из одного языка в другой
    :param message: исходный текст
    :param src_lang: исходный язык
    :param dst_lang: язык перевода
    :return: переведенная текстовая строка
    """
    result_text = translator.translate(message, src=src_lang, dest=dst_lang).text
    return re.sub(r"([A-z,А-я][\.\,\!\?\*\"\№\%)])([A-Z,А-Я])", "\\1 \\2", result_text)
