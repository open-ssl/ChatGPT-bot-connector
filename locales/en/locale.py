class BotMessage:
    """
    Английские тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Hello, {}!\nUse Chat GPT in Telegram!'
    START_COMMON_TEXT = 'Hello!\nUse Chat GPT in Telegram!'
    MAIN_MENU_TEXT = 'Edit your profile and start to chat with Chat GPT'
    HELP = 'Help'
    ABOUT = 'About bot'
    START_BOT = 'Start dialog with Сhat GPT'
    PROFILE = 'My profile'
    MAIN_MENU = 'Main menu'
    LANGUAGE = 'Bot language: '
    TEMPERATURE = 'Precision of generation: '
    SAVE_PROFILE = 'Save profile'
    PROFILE_INFO = 'How to set parameters?'
    BACK_TO_PROFILE = 'Back to profile'
    EARN_WITH_CHATGPT = 'Earn with bot'
    MY_PROFILE_TEXT = "Your profile:\n Press any button to change the value\n\n"
    MY_PROFILE_INFO_NOT_SUB_TEXT = "Count of tokens: <b>{}</b>\nBuy a subscription to use the bot without " \
                                   "restrictions\n\nUse command /buy_subscription"
    MY_PROFILE_INFO_WITH_SUB_TEXT = "Count of tokens: ∞\nYour subscription expired at: {}"
    TYPE_TEXT = "Type question for Chat GPT in English"
    WAITING_ANSWER_FROM_GPT = "\nWaiting answer from Chat GPT\n"
    ANSWER_FROM_GPT = "Answer from Chat GPT:\n\n"
    ANOTHER_QUESTION = "You can ask another one querstion right in this dialog\n" \
                       "If you would change preferences You could press \"Main menu\" button"
    UNKNOWN_COMMAND = "Unknown command\nTry again"
    TEMPERATURE_TEXT = "<b>What is the precision of generation?</b>\n\nIt is a value between 0 and 10 that essentially "\
                       "lets you control how confident the model should be when making these predictions. Lowering " \
                       "temperature means it will take fewer risks, and completions \nwill be more accurate and " \
                       "deterministic. \nIncreasing precision of generation will result in more diverse completions.\n\nThe " \
                       "value 6 is a good default value for generating unique results by model "

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]
