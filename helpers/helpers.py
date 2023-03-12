import sys
from telebot import types

import bot_config
from bot_config import cache_client
from functools import partial
from time import sleep
from traceback import print_exception
from requests_futures import sessions


class Locale:
    ENGLISH = 'en'
    RUSSIAN = 'ru'


class Const:
    pass


class CachePhase:
    DEFAULT_DIALOG = 0
    WRITE_TEXT_FOR_GPT = 1


class BotMessage:
    """
    Тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Hi, {}!\nUse possibilities of ChatGPT in Telegram'
    MAIN_MENU_TEXT = 'Редактируйте свой профиль или начните диалог с ботом'
    HELP = 'Помощь'
    ABOUT = 'О боте'
    START_BOT = 'Начать диалог c Сhat GPT'
    PROFILE = 'Мой профиль'
    MAIN_MENU = 'Главное меню'
    EARN_WITH_CHATGPT = 'Заработай с ботом'

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознаавть как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]


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

    START_DESCRIPTION = 'Start main bot'
    START_BOT_DESCRIPTION = 'Start dialog with ChatGPT'
    ABOUT_DESCRIPTION = 'Learn about bot'
    HELP_DESCRIPTION = 'Get help info'

    @classmethod
    def get_menu_commands(cls):
        return {
            cls.START: BotMessage.START_BOT,
            cls.PROFILE: BotMessage.PROFILE,
            cls.EARN_WITH_CHATGPT: BotMessage.EARN_WITH_CHATGPT,
        }

    @classmethod
    def get_menu_after_dialog_commands(cls):
        return {
            cls.MAIN_MENU: BotMessage.MAIN_MENU,
            cls.EARN_WITH_CHATGPT: BotMessage.EARN_WITH_CHATGPT,
        }


def log_error_in_file():
    error_file = 'error_log.txt'
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        with open(error_file, 'a') as file:
            print('_______________________________________', file=file)
            print_exception(exc_type, exc_value, exc_traceback, file=file)
            print('_______________________________________', file=file)
    except Exception as e:
        print(e)
    finally:
        print('end log error')


def get_locale_for_user(user_id: int) -> str:
    """
    Получаем локаль для пользователя
    :param user_id: идентификатор пользователя
    :return: локаль для работы с ботом
    """
    return Locale.ENGLISH


def set_locale_for_user(user_id: int) -> None:
    """
    Установка локали пользователя для работы с ботом
    :param user_id: идентификатор пользователя
    """
    pass
    return


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


def get_main_menu_keyboard():
    """
    Генерация клавиатуры главного меню
    :return: Обьект клавиатуры для вставки в реплай сообщения
    """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_commands = BotCommands.get_menu_commands()
    for command_text in bot_commands.values():
        keyboard_button = partial(types.KeyboardButton, text=command_text)
        keyboard.add(keyboard_button())
    return keyboard


def get_menu_after_write_keyboard():
    """
    Генерация клавиатуры c меню после отправки ChatGPT
    :return: Обьект клавиатуры для вставки в реплай сообщения
    """
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    bot_commands = BotCommands.get_menu_after_dialog_commands()
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
    return text.html_text in BotMessage.get_unique_methods()


def start_bot_command_validator(text) -> bool:
    """
    Проверка сообщения на принадлежность к команде /start_bot
    :param text: обьект сообщения
    :return: bool - ожидаем команду start_bot?
    """
    return text.html_text in [BotMessage.START_BOT, f'/{BotCommands.START_BOT}']


def write_chat_gpt_command_validator(message) -> bool:
    """
    Проверка того, что мы находимся в режиме написания Chat GPT
    """
    chat_id = message.chat.id
    command_phase = cache_client.get(str(chat_id))
    return command_phase and command_phase == b'1'


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
    return not command_phase or command_phase == b'0' and command not in BotMessage.get_unique_methods()
