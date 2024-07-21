from elasticsearch import AsyncElasticsearch, NotFoundError

from fastapi import APIRouter, Depends, HTTPException

from db.elastic import get_elastic
from models.genre import Genre

router = APIRouter(tags=['genres'])


@router.get(
    '/genres',
    response_model=list[Genre],
    summary='Genres',
    description='Genres list',
)
async def get_genres(elastic: AsyncElasticsearch = Depends(get_elastic)) -> list[Genre]:
    result = await elastic.search(
        index='genres',
        body={
            'query': {'match_all': {}},
            'size': 10000,
        },
    )
    return [Genre(**genre['_source']) for genre in result['hits']['hits']]


@router.get(
    '/genres/{genre_pk}',
    response_model=Genre,
    summary='Genre page',
    description='Genre information by pk',
)
async def get_genre_by_pk(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    genre_pk: str = None,
) -> Genre:
    try:
        result = await elastic.get(index='genres', id=genre_pk)
        return Genre(**result['_source'])
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Genre not found')
