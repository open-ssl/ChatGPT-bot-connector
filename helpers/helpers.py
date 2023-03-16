import sys
from datetime import date, datetime
from telebot import types

import bot_config
from bot_config import cache_client
from functools import partial
from time import sleep
from traceback import print_exception
from requests_futures import sessions
from locales.ru.locale import BotMessage as BotMessageRu
from locales.en.locale import BotMessage as BotMessageEn
from locales.main import get_unique_methods


class Locale:
    ENGLISH = 'en'
    RUSSIAN = 'ru'

    ENGLISH_LANGUAGE = '🇺🇸English🇺🇸'
    RUSSIAN_LANGUAGE = '🇷🇺Русский🇷🇺'

    @classmethod
    def get_opposite_locale_for_user(cls, current_locale):
        """
        Получение новой локали для смены языка
        :param current_locale: текущая локаль пользователя
        :return: локаль на которую будем менять язык
        """
        return cls.ENGLISH if current_locale == cls.RUSSIAN else cls.RUSSIAN

    @classmethod
    def get_language_name_by_preffix(cls, prefix):
        return {
            cls.RUSSIAN: cls.RUSSIAN_LANGUAGE,
            cls.ENGLISH: cls.ENGLISH_LANGUAGE,
        }.get(prefix)


class Const:
    DEFAULT_TEMPERATURE_FOR_USER = 0.6
    TEMPERATURE = 'temperature'
    LANGUAGE = 'language'
    ACTIVITY_STATUS = 'activity_status'
    TOKENS = 'tokens'


class CachePhase:
    DEFAULT_DIALOG = 0
    WRITE_TEXT_FOR_GPT = 1


class BotCommands:
    """
    Команды бота
    """
    START = 'start'
    START_BOT = 'start_bot'
    MAIN_MENU = 'main_menu'
    PROFILE = 'my_profile'
    EARN_WITH_CHATGPT = 'earn_with_chatgpt'
    HELP = 'help'
    ABOUT = 'about'
    LANGUAGE = 'language'
    TEMPERATURE = 'temperature'
    SAVE_PROFILE = 'save_profile'

    START_DESCRIPTION = 'Start main bot'
    START_BOT_DESCRIPTION = 'Start dialog with ChatGPT'
    ABOUT_DESCRIPTION = 'Learn about bot'
    HELP_DESCRIPTION = 'Get help info'

    @classmethod
    def get_menu_commands(cls, locale_obj):
        return {
            cls.START: locale_obj.START_BOT,
            cls.PROFILE: locale_obj.PROFILE,
            cls.EARN_WITH_CHATGPT: locale_obj.EARN_WITH_CHATGPT,
        }

    @classmethod
    def get_menu_after_dialog_commands(cls, locale_object):
        return {
            cls.MAIN_MENU: locale_object.MAIN_MENU,
            cls.EARN_WITH_CHATGPT: locale_object.EARN_WITH_CHATGPT,
        }


def log_error_in_file():
    data_for_file = date.today().strftime("%m-%d-%Y")
    time_for_file = datetime.now().strftime("%H:%M:%S")
    error_file = f'logs/error_log_{data_for_file}.txt'
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        with open(error_file, 'a') as file:
            print('_______________________________________', file=file)
            print(f'Current time {time_for_file}', file=file)
            print_exception(exc_type, exc_value, exc_traceback, file=file)
            print('_______________________________________', file=file)
    except Exception as e:
        print(e)
    finally:
        print('end log error')


def decode_str(text: bytes) -> str:
    """
    Декодировать текст из байтов
    :param text: байтовый текст
    :return: декодированный текст
    """
    return text.decode()


def encode_text(text: str) -> bytes:
    """
    Закодировать текст в байты
    :param text: текст
    :return: байтовый текст
    """
    return text.encode()


def get_session_for_request():
    return sessions.FuturesSession()


def post_request(url, json_data):
    session = get_session_for_request()

    while True:
        try:
            request_result = session.post(url, json=json_data, verify=False)
            break
        except Exception as e:
            print('Unknown error %s' % e)
            sleep(0.5)

    return request_result.result()


def get_main_menu_keyboard(locale_obj):
    """
    Генерация клавиатуры главного меню
    :return: Обьект клавиатуры для вставки в реплай сообщения
    """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_commands = BotCommands.get_menu_commands(locale_obj=locale_obj)
    for command_text in bot_commands.values():
        keyboard_button = partial(types.KeyboardButton, text=command_text)
        keyboard.add(keyboard_button())
    return keyboard


def get_profile_keyboard(profile_buttons: dict):
    """
    Генерация клавиатуры для профиля пользователя
    :param profile_buttons: обьект названий кнопок и колбекеков из БД
    :return: Обьект клавиатуры для вставки в реплай сообщения
    """
    keyboard = types.InlineKeyboardMarkup()

    for callback_handler, command_text in profile_buttons.items():
        keyboard_button = partial(types.InlineKeyboardButton, text=command_text, callback_data=callback_handler)
        keyboard.add(keyboard_button())
    return keyboard


def get_menu_after_write_keyboard(locale_object):
    """
    Генерация клавиатуры c меню после отправки ChatGPT
    :return: Обьект клавиатуры для вставки в реплай сообщения
    """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_commands = BotCommands.get_menu_after_dialog_commands(locale_object)
    for command_text in bot_commands.values():
        keyboard_button = partial(types.KeyboardButton, text=command_text)
        keyboard.add(keyboard_button())
    return keyboard


def initialize_main_menu():
    bot = bot_config.bot
    bot.set_my_commands(commands=[
        types.BotCommand(BotCommands.START, BotCommands.START_DESCRIPTION),
        types.BotCommand(BotCommands.START_BOT, BotCommands.START_BOT_DESCRIPTION),
        types.BotCommand(BotCommands.ABOUT, BotCommands.ABOUT_DESCRIPTION),
        types.BotCommand(BotCommands.HELP, BotCommands.HELP_DESCRIPTION),
    ])
    bot.set_chat_menu_button(menu_button=types.MenuButtonCommands(type='commands'))
    print("Initialized main menu")


def main_menu_bot_command_validator(text) -> bool:
    """
    Проверка сообщения на принадлежность к команде /start
    Директ в главное меню
    :param text: обьект сообщения
    :return: bool - ожидаем команду start?
    """
    return text.html_text in get_unique_methods()


def start_bot_command_validator(text) -> bool:
    """
    Проверка сообщения на принадлежность к команде /start_bot
    :param text: обьект сообщения
    :return: bool - ожидаем команду start_bot?
    """

    return text.html_text in [BotMessageRu.START_BOT, BotMessageEn.START_BOT, f'/{BotCommands.START_BOT}']


def write_chat_gpt_command_validator(message) -> bool:
    """
    Проверка того, что мы находимся в режиме написания Chat GPT
    """
    chat_id = message.chat.id
    command_phase = cache_client.get(str(chat_id))
    return command_phase and command_phase == b'1'


def my_profile_command_validator(text) -> bool:
    """
    Проверка сообщения на принадлежность к команде /my_profile
    :param text: обьект сообщения
    :return: bool - ожидаем команду my_profile?
    """
    return text.html_text in [BotMessageRu.PROFILE, BotMessageEn.PROFILE, f'/{BotCommands.PROFILE}']


def unknown_command_validator(message) -> bool:
    """
    Проверка сообщения, на несоответствие какой-либо команде,
    если находимся не в режиме написанию боту
    :param message: обьект сообщения
    :return: bool - сообщение является командой?
    """
    chat_id = message.chat.id
    command = message.html_text
    command_phase = cache_client.get(str(chat_id))
    return not command_phase or command_phase == b'0' and command not in get_unique_methods()
