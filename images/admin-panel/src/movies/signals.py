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
        ...
    except Exception as e:
        print(f"Ошибка асинхронного обновления фильма: {e}")


# Сигналы для Filmwork
@receiver(post_save, sender=Filmwork)
def filmwork_saved(sender, instance, created, **kwargs):
    """При сохранении фильма"""
    # Запускаем в фоновом потоке чтобы не блокировать ответ админки
    if created:
        mongo_service = MongoDBService()
        mongo_service.create_filmwork_by_id(str(instance.id))
        mongo_service.stop()
    threading.Thread(target=async_update_filmwork, args=(instance.id,)).start()


@receiver(post_delete, sender=Filmwork)
def filmwork_deleted(sender, instance, **kwargs):
    """При удалении фильма"""
    mongo_service = MongoDBService()
    mongo_service.delete_filmwork_cascade_by_id(str(instance.id))
    mongo_service.stop()
    threading.Thread(target=elastic_service.delete_filmwork, args=(instance.id,)).start()


# Сигналы для Person
@receiver(post_save, sender=Person)
def person_saved(sender, instance, created, **kwargs):
    """При сохранении персоны"""
    # Индексируем персону
    threading.Thread(target=elastic_service.index_person, args=(instance,)).start()

    # Обновляем все фильмы с этой персоной
    filmwork_ids = Filmwork.objects.filter(persons=instance).values_list('id', flat=True)

    for filmwork_id in filmwork_ids:
        threading.Thread(target=async_update_filmwork, args=(filmwork_id,)).start()


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
    threading.Thread(target=elastic_service.index_genre, args=(instance,)).start()

    # Обновляем все фильмы с этим жанром
    filmwork_ids = Filmwork.objects.filter(genres=instance).values_list('id', flat=True)

    for filmwork_id in filmwork_ids:
        threading.Thread(target=async_update_filmwork, args=(filmwork_id,)).start()


# Сигналы для промежуточных таблиц
@receiver(post_save, sender=GenreFilmwork)
@receiver(post_delete, sender=GenreFilmwork)
def genrefilmwork_changed(sender, instance, **kwargs):
    """При изменении связи фильм-жанр"""
    threading.Thread(target=async_update_filmwork, args=(instance.film_work_id,)).start()


@receiver(post_save, sender=PersonFilmwork)
@receiver(post_delete, sender=PersonFilmwork)
def personfilmwork_changed(sender, instance, **kwargs):
    """При изменении связи фильм-персона"""
    threading.Thread(target=async_update_filmwork, args=(instance.film_work_id,)).start()
