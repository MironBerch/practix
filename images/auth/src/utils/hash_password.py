import hashlib
import hmac

from core.config import settings


def hash_password(password: str) -> str:
    """Хеширует пароль с использованием HMAC и секретного ключа."""
    hmac_hash = hmac.new(
        settings.flask.secret_key.encode('utf-8'),
        password.encode('utf-8'),
        hashlib.sha256,
    )
    return hmac_hash.hexdigest()


def check_password(stored_hash: str, password: str) -> bool:
    """Проверяет, соответствует ли предоставленный пароль хранящемуся хешу."""
    return stored_hash == hash_password(password)
