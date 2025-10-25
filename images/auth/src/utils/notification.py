import aiohttp

from core.config import settings
from src.schemas.schemas import Notification


async def send_notification(data: Notification) -> bool:
    """Отправка уведомления"""
    try:
        async with aiohttp.ClientSession() as session:
            path = 'notifications/api/notification'
            notifications = settings.notifications
            url = f'http://{notifications.receiver_host}:{notifications.receiver_port}/{path}'
            async with session.post(
                url,
                json=data,
            ) as response:
                return response.status == 200
    except Exception:
        return False
