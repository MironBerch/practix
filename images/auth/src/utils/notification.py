import requests

from src.core.config import settings
from src.core.logger import logger


def send_notification(data: dict):
    path = 'notifications/api/notification'
    notifications = settings.notifications
    url = f'http://{notifications.receiver_host}:{notifications.receiver_port}/{path}'
    if not notifications.receiver_host:
        return None
    try:
        requests.post(url, json=data)
    except Exception as e:
        logger.error(
            msg=(
                f'Can not send message with use notifications receiver '
                f'Json data: {data} '
                f'Exception: {e} '
            )
        )
