from uuid import UUID

from fastapi import APIRouter, Depends, Path

from api.dependencies import check_filmwork_exist, check_review_exists
from api.paginator import Paginator
from models.models import Review, ReviewRating, ReviewScore, Text
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
    filmwork_id: UUID = Path(title='UUID фильма'),
    paginator: Paginator = Depends(),
) -> list[Review]:
    result = await service.filter(filmwork_id=filmwork_id, paginator=paginator)
    return result


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
    filmwork_id: UUID = Path(title='UUID фильма'),
) -> dict:
    result = await service.update(user_id=auth.user_id, filmwork_id=filmwork_id, text=text)
    return result


@router.delete(
    path='/filmworks/{filmwork_id}/reviews/{review_id}',
    summary='Удаление рецензии у фильма',
    response_description='Результат удаления рецензии на фильму',
    dependencies=[Depends(check_filmwork_exist), Depends(check_review_exists)],
)
async def delete_filmwork_review(
    auth: AuthService = Depends(),
    service: ReviewsService = Depends(get_reviews_service),
    filmwork_id: UUID = Path(title='UUID фильма'),
) -> dict:
    result = await service.remove(user_id=auth.user_id, filmwork_id=filmwork_id)
    return result


@router.get(
    path='/filmworks/{filmwork_id}/reviews/{review_id}/ratings',
    summary='Просмотр рейтинга рецензии',
    response_description='Рейтинг рецензии (лайки, дизлайки и сумма)',
    response_model=ReviewRating,
    dependencies=[Depends(check_filmwork_exist)],
)
async def get_review_rating(
    service: ReviewsService = Depends(get_reviews_service),
    review_id: UUID = Path(title='UUID отзыва'),
) -> dict:
    result = await service.get_rating(review_id=review_id)
    return result


@router.post(
    path='/filmworks/{filmwork_id}/reviews/{review_id}/ratings',
    summary='Добавление оценки рецензии',
    response_description='Рейтинг рецензии (лайки, дизлайки и сумма)',
    response_model=ReviewRating,
    dependencies=[Depends(check_filmwork_exist)],
)
async def rate_review(
    score: ReviewScore,
    auth: AuthService = Depends(),
    service: ReviewsService = Depends(get_reviews_service),
    review_id: UUID = Path(title='UUID отзыва'),
) -> dict:
    result = await service.rate(review_id=review_id, user_id=auth.user_id, score=score.score)
    return result


@router.delete(
    path='/filmworks/{filmwork_id}/reviews/{review_id}/ratings',
    summary='Удаление оценки у рецензии',
    response_description='Результат удаления рейтинга рецензии',
    dependencies=[Depends(check_filmwork_exist)],
)
async def unrate_review(
    auth: AuthService = Depends(),
    service: ReviewsService = Depends(get_reviews_service),
    review_id: UUID = Path(title='UUID отзыва'),
) -> dict:
    result = await service.unrate(review_id=review_id, user_id=auth.user_id)
    return result
