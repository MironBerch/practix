import requests

from core.config import settings
from core.logger import logger


def send_notification(data: dict):
    try:
        path = 'notifications/api/notification'
        notifications = settings.notifications
        url = f'http://{notifications.receiver_host}:{notifications.receiver_port}/{path}'
        response = requests.post(url, json=data)
        if response.status_code != 200:
            pass
    except Exception as e:
        logger.error(
            msg=(
                f'Can not send message with use notifications receiver '
                f'Json data: {data} '
                f'Exception: {e} '
            )
        )
