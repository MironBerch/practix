from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import check_filmwork_exist, check_review_exists
from api.paginator import Paginator
from models.models import Review, Text
from services.auth import AuthService
from services.reviews import ReviewsService, get_reviews_service

router = APIRouter(tags=['reviews'])


@router.get(
    path='/filmworks/{filmwork_id}/reviews',
    summary='Просмотр списка рецензий',
    response_description='Список рецензий на фильм',
    response_model=list[Review],
    dependencies=[Depends(check_filmwork_exist)],
)
async def get_filmwork_reviews(
    service: ReviewsService = Depends(get_reviews_service),
    filmwork_id: UUID | str = Path(title='UUID фильма'),
    paginator: Paginator = Depends(),
) -> list[Review]:
    return service.filter(filmwork_id=filmwork_id, paginator=paginator)


@router.post(
    path='/filmworks/{filmwork_id}/reviews',
    summary='Добавление рецензии к фильму',
    response_description='Результат добавления рецензии на фильм',
    response_model=Review,
    response_model_exclude_none=True,
    dependencies=[Depends(check_filmwork_exist)],
)
async def create_filmwork_review(
    text: Text,
    auth: AuthService = Depends(),
    service: ReviewsService = Depends(get_reviews_service),
    filmwork_id: UUID | str = Path(title='UUID фильма'),
):
    return service.update(user_id=auth.user_id, filmwork_id=filmwork_id, text=text)


@router.delete(
    path='/filmworks/{filmwork_id}/reviews/{review_id}',
    summary='Удаление рецензии у фильма',
    response_description='Результат удаления рецензии на фильму',
    dependencies=[Depends(check_filmwork_exist), Depends(check_review_exists)],
)
async def delete_filmwork_review(
    auth: AuthService = Depends(),
    service: ReviewsService = Depends(get_reviews_service),
    filmwork_id: UUID | str = Path(title='UUID фильма'),
):
    return service.remove(user_id=auth.user_id, filmwork_id=filmwork_id)