from config.settings import TELEGRAM_URL, BOT_TOKEN
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    """ Функция отправки сообщения в телеграм. """
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    response = requests.get(f'{TELEGRAM_URL}{BOT_TOKEN}/sendMessage', params=params)
    logger.info(f"Telegram response: {response.json()}")
    response.raise_for_status()  # Поднимет исключение, если запрос не был успешным
