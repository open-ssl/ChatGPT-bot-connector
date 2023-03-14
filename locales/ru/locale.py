class BotMessage:
    """
    Русские тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Привет, {}!\nИспользуй возможности Chat GPT в Телеграм!'
    MAIN_MENU_TEXT = 'Редактируйте свой профиль или начните диалог с ботом'
    HELP = 'Помощь'
    ABOUT = 'О боте'
    START_BOT = 'Начать диалог c Сhat GPT'
    PROFILE = 'Мой профиль'
    MAIN_MENU = 'Главное меню'
    LANGUAGE = 'Язык бота: '
    TEMPERATURE = 'Точность генерации: '
    SAVE_PROFILE = 'Сохранить профиль'
    EARN_WITH_CHATGPT = 'Заработай с ботом'
    MY_PROFILE_TEXT = "Ваш профиль:"

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]
