from elasticsearch import AsyncElasticsearch, NotFoundError

from fastapi import APIRouter, Depends, HTTPException, Query

from api.paginator import Paginator
from db.elastic import get_elastic
from models.filmwork import BaseFilmwork, Filmwork, FilmworkList

router = APIRouter(tags=['filmworks'])


@router.get(
    '/filmworks',
    response_model=FilmworkList,
)
async def filmworks(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    sort: str | None = Query(default=None, alias='sort_by'),
    filter_by_genres: list[str] | None = Query(
        default=None,
        alias='filter[genres]',
        description='Filter by genres',
    ),
    paginator: Paginator = Depends(),
) -> list[BaseFilmwork]:
    query = {
        'query': {
            'bool': {},
        },
        'sort': {},
        'from': (paginator.page - 1) * paginator.size,
        'size': paginator.size,
    }
    if sort:
        field = sort.lstrip('-')
        query['sort'][field] = {'order': 'desc' if sort.startswith('-') else 'asc'}
    if filter_by_genres:
        query['query']['bool']['must'] = [
            {
                'terms': {
                    'genres': filter_by_genres,
                },
            },
        ]
    result = await elastic.search(
        index='movies',
        body=query,
    )
    return FilmworkList(root=[filmwork['_source'] for filmwork in result['hits']['hits']])


@router.get(
    '/filmworks/search',
    response_model=FilmworkList,
    summary='Search filmworks',
    description='Full-text search by filmworks titles and descriptions',
)
async def filmworks_search(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    query: str = Query(default=None, description='Search query'),
    paginator: Paginator = Depends(),
) -> list[BaseFilmwork]:
    query = {
        'query': {
            'multi_match': {
                'query': query,
                'fields': ['title', 'description'],
            },
        },
        'from': (paginator.page - 1) * paginator.size,
        'size': paginator.size,
    }
    result = await elastic.search(
        index='movies',
        body=query,
    )
    return FilmworkList(root=[filmwork['_source'] for filmwork in result['hits']['hits']])


@router.get(
    '/filmworks/{filmwork_id}',
    response_model=Filmwork,
    summary='Filmwork page',
    description='Full information about the filmwork',
)
async def filmwork_by_pk(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    filmwork_id: str = None,
) -> Filmwork:
    try:
        result = await elastic.get(index='movies', id=filmwork_id)
        return Filmwork(**result['_source'])
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Filmwork not found')
