import logging

from elasticsearch import Elasticsearch

logger = logging.getLogger('elastic')

elastic = Elasticsearch('http://elastic:9200')


def get_elastic() -> Elasticsearch:
    return elastic
