class BotMessage:
    """
    Английские тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Hello, {}!\nUse Chat GPT in Telegram!'
    MAIN_MENU_TEXT = 'Edit your profile and start to chat with Chat GPT'
    HELP = 'Help'
    ABOUT = 'About bot'
    START_BOT = 'Start dialog with Сhat GPT'
    PROFILE = 'My profile'
    MAIN_MENU = 'Main menu'
    LANGUAGE = 'Bot language: '
    TEMPERATURE = 'Precision of generation: '
    SAVE_PROFILE = 'Save profile'
    EARN_WITH_CHATGPT = 'Earn with bot'
    MY_PROFILE_TEXT = "Your profile:"
    TYPE_TEXT = "Type question for Chat GPT in English"
    WAITING_ANSWER_FROM_GPT = "\nWaiting answer from Chat GPT\n"
    ANSWER_FROM_GPT = "Answer from Chat GPT:\n\n"
    ANOTHER_QUESTION = "You can ask another one querstion right in this dialog\n" \
                       "If you would change preferences You could press \"Main menu\" button"
    UNKNOWN_COMMAND = "Unknown command\nTry again"

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]
