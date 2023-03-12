import sys
from telebot import types

import bot_config
from bot_config import cache_client
from functools import partial
from time import sleep
from traceback import print_exception
from requests_futures import sessions


class Const:
    pass


class CachePhase:
    DEFAULT_DIALOG = 0
    WRITE_TEXT_FOR_GPT = 1


class BotMessage:
    """
    Тексты сообщений при нажатии на команды
    """
    START = 'Hi, {}!\nUse possibilities of ChatGPT in Telegram'
    HELP = 'Помощь'
    ABOUT = 'О боте'
    MENU = 'Главное меню'
    START_BOT = 'Начать диалог c Сhat GPT'
    SHARE_BOT = 'Поделиться'
    MAIN_MENU = 'Главное меню'
    EARN_WITH_CHATGPT = 'Заработай с ботом'


class BotCommands:
    """
    Команды бота
    """
    START = 'start'
    START_BOT = 'start_bot'
    MAIN_MENU = 'main_menu'
    SHARE_BOT = 'share_bot'
    EARN_WITH_CHATGPT = 'earn_with_chatgpt'
    HELP = 'help'
    ABOUT = 'about'
    MENU = 'menu'

    START_DESCRIPTION = 'Start main bot'
    START_BOT_DESCRIPTION = 'Start dialog with ChatGPT'
    ABOUT_DESCRIPTION = 'Learn about bot'
    HELP_DESCRIPTION = 'Get help info'


    @classmethod
    def get_bot_commands(cls):
        return {
            cls.START: BotMessage.START,
            cls.HELP: BotMessage.HELP,
            cls.ABOUT: BotMessage.ABOUT,
            cls.MENU: BotMessage.MENU,
        }

    @classmethod
    def get_menu_commands(cls):
        return {
            cls.START: BotMessage.START_BOT,
            cls.SHARE_BOT: BotMessage.SHARE_BOT,
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


def start_bot_command_validator(text):
    """
    Проверка сообщения на принадлежность к команде /start_bot
    :param text: обьект сообщения
    :return: bool - ожидаем команду start_bot?
    """
    return text.html_text in [BotMessage.START_BOT, f'/{BotCommands.START_BOT}']


def unknown_command_validator(message):
    chat_id = message.chat.id
    command_phase = cache_client.get(str(chat_id))
    return not command_phase or command_phase == b'0'
