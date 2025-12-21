import threading

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from movies.elastic import elastic_service
from movies.models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from movies.mongo import MongoDBService


def async_update_filmwork(filmwork_id):
    """Асинхронное обновление фильма в Elasticsearch"""
    try:
        filmwork = Filmwork.objects.prefetch_related('genres', 'personfilmwork_set__person').get(
            id=filmwork_id
        )
        elastic_service.index_filmwork(filmwork)
    except Filmwork.DoesNotExist:
        print(f"Ошибка асинхронного обновления фильма")
    except Exception as e:
        print(f"Ошибка асинхронного обновления фильма: {e}")


# Сигналы для Filmwork
@receiver(post_save, sender=Filmwork)
def filmwork_saved(sender, instance, created, **kwargs):
    """При сохранении фильма"""
    # Запускаем в фоновом потоке чтобы не блокировать ответ админки
    if created:
        mongo_service = MongoDBService()
        mongo_service.create_filmwork_by_id(instance.id)
        elastic_service.index_filmwork(instance)
    async_update_filmwork(instance.id)


@receiver(post_delete, sender=Filmwork)
def filmwork_deleted(sender, instance, **kwargs):
    """При удалении фильма"""
    mongo_service = MongoDBService()
    mongo_service.delete_filmwork_cascade_by_id(instance.id)
    elastic_service.delete_filmwork(instance.id)


# Сигналы для Person
@receiver(post_save, sender=Person)
def person_saved(sender, instance, created, **kwargs):
    """При сохранении персоны"""
    # Индексируем персону
    elastic_service.index_person(instance)
    # Обновляем все фильмы с этой персоной
    filmwork_ids = Filmwork.objects.filter(persons=instance).values_list('id', flat=True)

    for filmwork_id in filmwork_ids:
        async_update_filmwork(filmwork_id)


@receiver(post_delete, sender=Person)
def person_deleted(sender, instance, **kwargs):
    """При удалении персоны (просто удаляем из Elasticsearch)"""
    # В реальной системе нужно также обновить фильмы без этой персоны
    pass


# Сигналы для Genre
@receiver(post_save, sender=Genre)
def genre_saved(sender, instance, created, **kwargs):
    """При сохранении жанра"""
    # Индексируем жанр
    elastic_service.index_genre(instance)
    # Обновляем все фильмы с этим жанром
    filmwork_ids = Filmwork.objects.filter(genres=instance).values_list('id', flat=True)

    for filmwork_id in filmwork_ids:
        async_update_filmwork(filmwork_id)


# Сигналы для промежуточных таблиц
@receiver(post_save, sender=GenreFilmwork)
@receiver(post_delete, sender=GenreFilmwork)
def genrefilmwork_changed(sender, instance, **kwargs):
    """При изменении связи фильм-жанр"""
    async_update_filmwork(instance.film_work.id)


@receiver(post_save, sender=PersonFilmwork)
@receiver(post_delete, sender=PersonFilmwork)
def personfilmwork_changed(sender, instance, **kwargs):
    """При изменении связи фильм-персона"""
    async_update_filmwork(instance.film_work.id)
