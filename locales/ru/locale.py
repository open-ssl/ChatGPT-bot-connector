class BotMessage:
    """
    Русские тексты сообщений при нажатии на команды
    """
    START_TEXT = 'Привет, {}!\nИспользуй возможности Chat GPT в Телеграм!'
    START_COMMON_TEXT = 'Привет!\nИспользуй возможности Chat GPT в Телеграм!'
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
    MY_PROFILE_TEXT = "Ваш профиль:\n\n"
    MY_PROFILE_INFO_NOT_SUB_TEXT = "Количество оставшихся токенов: <b>{}</b>\nКупите подписку для использования бота " \
                                   "без ограничений\n\nИспользуйте команду: /buy_subscription"
    MY_PROFILE_INFO_WITH_SUB_TEXT = "Количество оставшихся токенов: ∞\nВаша подписка истекает: {}"
    TYPE_TEXT = "Введите текст запрос к Chat GPT по-английски"
    WAITING_ANSWER_FROM_GPT = "\nЖдем ответа от Chat GPT\n"
    ANSWER_FROM_GPT = "Ответ от Chat GPT:\n\n"
    ANOTHER_QUESTION = "Вы можете задать еще один вопрос прямо в этом диалоге\n" \
                       "Если хотите поменять настройки вы можете нажать кнопку \"Главное меню\""
    UNKNOWN_COMMAND = "Не знаю такой команды\nПопробуйте ввести заново"

    @classmethod
    def get_unique_methods(cls):
        """
        Возвращает уникальные методы, которые не нужно распознавать как неизвестные команды
        :return:
        """
        return [BotMessage.MAIN_MENU]
