# Generated by Django 5.1.3 on 2025-01-13 20:07

import uuid

from django.db import migrations, models

import notifications.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('name', models.CharField(max_length=255, verbose_name='название')),
                (
                    'code',
                    models.TextField(
                        validators=[notifications.validators.validate_jinja_template],
                        verbose_name='шаблон',
                    ),
                ),
                (
                    'updated_at',
                    models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления'),
                ),
            ],
            options={
                'verbose_name': 'шаблон',
                'verbose_name_plural': 'шаблоны',
                'db_table': 'templates',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                    ),
                ),
                ('email', models.EmailField(max_length=255, verbose_name='почта')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'db_table': 'users',
            },
        ),
    ]
