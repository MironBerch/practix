from typing import Any

from elasticsearch import AsyncElasticsearch, NotFoundError

from fastapi import APIRouter, Depends, HTTPException, Query

from api.paginator import Paginator
from db.elastic import get_elastic
from models.filmwork import BaseFilmwork, FilmworkList
from models.person import Person, PersonList
from services.person import PersonService, get_person_service

router = APIRouter(tags=['persons'])


@router.get(
    '/persons',
    response_model=PersonList,
    summary='Persons',
    description='Person list',
)
async def persons(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    paginator: Paginator = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    query = {
        'query': {
            'match_all': {},
        },
        'from': (paginator.page - 1) * paginator.size,
        'size': paginator.size,
    }
    result = await elastic.search(
        index='persons',
        body=query,
    )
    root: list[dict[str, Any]] = []
    for person in result['hits']['hits']:
        filmwork_ids_and_roles = await person_service.get_person_filmwork_ids_and_roles(
            person_id=person['_source']['id'],
        )
        person['_source']['filmwork_ids'] = filmwork_ids_and_roles['filmwork_ids']
        person['_source']['roles'] = filmwork_ids_and_roles['roles']
        root.append(person['_source'])
    return PersonList(root=root)


@router.get(
    '/persons/search',
    response_model=PersonList,
    summary='Search persons',
    description='Full-text search by persons names',
)
async def persons_search(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    query: str = Query(default=None, description='Search query'),
    paginator: Paginator = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    query = {
        'query': {
            'match': {
                'full_name': query,
            },
        },
        'from': (paginator.page - 1) * paginator.size,
        'size': paginator.size,
    }
    result = await elastic.search(
        index='persons',
        body=query,
    )
    root: list[dict[str, Any]] = []
    for person in result['hits']['hits']:
        filmwork_ids_and_roles = await person_service.get_person_filmwork_ids_and_roles(
            person_id=person['_source']['id'],
        )
        person['_source']['filmwork_ids'] = filmwork_ids_and_roles['filmwork_ids']
        person['_source']['roles'] = filmwork_ids_and_roles['roles']
        root.append(person['_source'])
    return PersonList(root=root)


@router.get(
    '/persons/{person_id}',
    response_model=Person,
    summary='Person page',
    description='Full information about the person',
)
async def person_by_pk(
    elastic: AsyncElasticsearch = Depends(get_elastic),
    person_id: str = None,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    try:
        result = await elastic.get(index='persons', id=person_id)
        filmwork_ids_and_roles = await person_service.get_person_filmwork_ids_and_roles(
            person_id=result['_source']['id'],
        )
        result['_source']['filmwork_ids'] = filmwork_ids_and_roles['filmwork_ids']
        result['_source']['roles'] = filmwork_ids_and_roles['roles']
        return Person(**result['_source'])
    except NotFoundError:
        raise HTTPException(status_code=404, detail='Person not found')


@router.get(
    '/persons/{person_id}/filmworks',
    response_model=FilmworkList,
    summary='Filmworks by person',
    description='Filmworks of the person',
)
async def person_filmworks_by_pk(
    person_id: str = None,
    person_service: PersonService = Depends(get_person_service),
) -> list[BaseFilmwork]:
    return FilmworkList(
        root=[
            filmwork['_source'] for filmwork in await person_service.get_person_filmworks(
                person_id=person_id,
            )
        ],
    )
