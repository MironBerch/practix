from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException

from services.filmworks import FilmworksService, get_filmworks_service


async def check_filmwork_exist(
        filmwork_id: UUID,
        filmworks_service: FilmworksService = Depends(get_filmworks_service),
):
    """Функция для проверки наличия фильма."""
    if not (await filmworks_service.get(filmwork_id)):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
