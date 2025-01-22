import uuid

from django.db import models

from notifications.validators import validate_jinja_template


class User(models.Model):
    """Модель пользователя."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name='почта', max_length=255)

    class Meta:
        db_table = 'users'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.id}'


class Template(models.Model):
    """Модель шаблона уведомлений."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(verbose_name='название', max_length=255)
    code = models.TextField(
        verbose_name='шаблон',
        validators=[validate_jinja_template],
    )
    updated_at = models.DateTimeField(
        verbose_name='дата последнего обновления',
        auto_now=True,
    )

    class Meta:
        db_table = 'templates'
        verbose_name = 'шаблон'
        verbose_name_plural = 'шаблоны'

    def __str__(self):
        return f'{self.id}'
