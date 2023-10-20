import telebot
from pymemcache.client import base
from googletrans import Translator
from config import BOT_TOKEN

# CHAT_GPT_MODEL_NAME = "text-davinci-003"
CHAT_GPT_MODEL_NAME = 'gpt-3.5-turbo-instruct'

MODEL_TEMPERATURE_COMMENT = """
Remember that the model predicts which text is most likely to follow the text preceding it.\n 
Temperature is a value between 0 and 1 that essentially lets you control how confident the model should be when making\n 
these predictions. Lowering temperature means it will take fewer risks, and completions \n 
will be more accurate and deterministic. \n
Increasing temperature will result in more diverse completions.
"""


KEY_LIST = [
    "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",
    "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",
    "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"
]


cache_client = base.Client(('localhost', 11211))
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()


def get_translator():
    """
    Обьект переводчика
    :return:
    """
    return translator

# bot real answer
#
# {
#   "choices": [
#     {
#       "finish_reason": "stop",
#       "index": 0,
#       "logprobs": null,
#       "text": "\n\n1. Fresh Groceries\n2. Green Markets\n3. Supermarket Express\n4. Corner Pantry\n5. The Grocery Cart"
#     }
#   ],
#   "created": 1678543320,
#   "id": "cmpl-6su5IfjXsDhbYgAfyCv1mTnkSj50p",
#   "model": "text-davinci-003",
#   "object": "text_completion",
#   "usage": {
#     "completion_tokens": 32,
#     "prompt_tokens": 10,
#     "total_tokens": 42
#   }
# }