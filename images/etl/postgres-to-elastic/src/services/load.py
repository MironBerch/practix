from dataclasses import dataclass

from elasticsearch import Elasticsearch, helpers

from models import filmwork, genre, person


@dataclass
class ElasticLoader(object):
    """Класс для валидации и загрузки данных в `ElasticSearch`."""

    elastic: Elasticsearch

    SETTINGS = {
        'refresh_interval': '1s',
        'analysis': {
            'filter': {
                'english_stop': {
                    'type': 'stop',
                    'stopwords': '_english_',
                },
                'english_stemmer': {
                    'type': 'stemmer',
                    'language': 'english',
                },
                'english_possessive_stemmer': {
                    'type': 'stemmer',
                    'language': 'possessive_english',
                },
                'russian_stop': {
                    'type': 'stop',
                    'stopwords': '_russian_',
                },
                'russian_stemmer': {
                    'type': 'stemmer',
                    'language': 'russian',
                },
            },
            'analyzer': {
                'ru_en': {
                    'tokenizer': 'standard',
                    'filter': [
                        'lowercase',
                        'english_stop',
                        'english_stemmer',
                        'english_possessive_stemmer',
                        'russian_stop',
                        'russian_stemmer',
                    ],
                },
            },
        },
    }

    INDICES = {
        'movies': {
            'id': {'type': 'keyword'},
            'rating': {'type': 'float'},
            'genres': {'type': 'keyword'},
            'title': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {'raw': {'type': 'keyword'}},
            },
            'description': {'type': 'text', 'analyzer': 'ru_en'},
            'directors_names': {'type': 'text', 'analyzer': 'ru_en'},
            'actors_names': {'type': 'text', 'analyzer': 'ru_en'},
            'writers_names': {'type': 'text', 'analyzer': 'ru_en'},
            'actors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {'type': 'text', 'analyzer': 'ru_en'},
                },
            },
            'writers': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {'type': 'text', 'analyzer': 'ru_en'},
                },
            },
            'directors': {
                'type': 'nested',
                'dynamic': 'strict',
                'properties': {
                    'id': {'type': 'keyword'},
                    'name': {'type': 'text', 'analyzer': 'ru_en'},
                },
            },
        },
        'persons': {
            'id': {'type': 'keyword'},
            'full_name': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {'raw': {'type': 'keyword'}},
            },
        },
        'genres': {
            'id': {'type': 'keyword'},
            'name': {
                'type': 'text',
                'analyzer': 'ru_en',
                'fields': {'raw': {'type': 'keyword'}},
            },
            'description': {'type': 'text', 'analyzer': 'ru_en'},
        },
    }

    def _create_indexes(self) -> None:
        """Создаёт индексы с соответствующими настройками и схемой данных."""
        for index, properties in self.INDICES.items():
            if not self.elastic.indices.exists(index=index):
                body = {
                    'settings': self.SETTINGS,
                    'mappings': {
                        'dynamic': 'strict',
                        'properties': properties,
                    },
                }
                self.elastic.indices.create(index=index, body=body)

    def __post_init__(self) -> None:
        self._create_indexes()

    def bulk_insert(
        self,
        data: list[filmwork.Filmwork | person.Person | genre.Genre],
    ) -> None:
        """Загружает данные."""
        actions = (
            {
                '_index': document._index,
                '_id': document.id,
                '_source': document.model_dump(by_alias=True),
            }
            for document in data
        )
        helpers.bulk(self.elastic, actions)
