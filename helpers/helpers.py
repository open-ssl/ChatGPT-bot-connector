import sys
from time import sleep
from traceback import print_exception
from requests_futures import sessions


class Const:
    pass


class BotMessage:
    """
    Тексты сообщений при нажатии на команды
    """
    START = 'Hi, {}!\nUse possibilities of ChatGPT in Telegram'
    HELP = 'Помощь'
    ABOUT = 'О боте'
    MENU = 'Главное меню'


class BotCommands:
    """
    Команды бота
    """
    START = 'start'
    HELP = 'help'
    ABOUT = 'about'
    MENU = 'menu'

    @classmethod
    def get_bot_commands(cls):
        return {
            cls.START: BotMessage.START,
            cls.HELP: BotMessage.HELP,
            cls.ABOUT: BotMessage.ABOUT,
            cls.MENU: BotMessage.MENU,
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