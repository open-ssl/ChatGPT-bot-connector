class BotMessage:
    """
    Английские тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Hello, {}!\nUse ChatGPT in Telegram!'
    MAIN_MENU_TEXT = 'Edit your profile and start to chat with ChatGPT'
    HELP = 'Help'
    ABOUT = 'About bot'
    START_BOT = 'Start dialog with СhatGPT'
    PROFILE = 'My profile'
    MAIN_MENU = 'Main menu'
    LANGUAGE = 'Bot language: '
    TEMPERATURE = 'Precision of generation: '
    SAVE_PROFILE = 'Save profile'
    EARN_WITH_CHATGPT = 'Earn with bot'
    MY_PROFILE_TEXT = "Your profile:"

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]
