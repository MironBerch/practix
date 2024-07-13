from elasticsearch import AsyncElasticsearch, NotFoundError

from fastapi import APIRouter, Depends, HTTPException

from db.elastic import get_elastic
from models.genre import Genre, GenreList

router = APIRouter(tags=['genres'])


@router.get(
    '/genres',
    response_model=GenreList,
    summary='Genres',
    description='Genres list',
)
async def genres(elastic: AsyncElasticsearch = Depends(get_elastic)) -> list[Genre]:
    result = await elastic.search(
        index='genres',
        body={
            'query': {'match_all': {}},
            'size': 10000,
        },
    )
    return GenreList(root=[genre['_source'] for genre in result['hits']['hits']])


@router.get(
    '/genres/{genre_id}',
    response_model=Genre,
    summary='Genre page',
    description='Genre information by id',
)
async def genre_by_id(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    genre_id: str = None,
) -> Genre:
    try:
        result = await elastic.get(index='genres', id=genre_id)
        return Genre(**result['_source'])
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Genre not found')
