import logging
from os import environ

from elasticsearch import Elasticsearch

logger = logging.getLogger('elastic')

elastic_host: str = environ.get('ELASTIC_HOST', 'elastic')
elastic_port: str = str(environ.get('ELASTIC_PORT', '9200'))
elastic_user: str = environ.get('ELASTIC_USER', 'elastic')
elastic_password: int = environ.get('ELASTIC_PASSWORD', '')

elastic = Elasticsearch(
    f'http://{elastic_host}:{elastic_port}',
    http_auth=(elastic_user, elastic_password),
)


def get_elastic() -> Elasticsearch:
    return elastic
