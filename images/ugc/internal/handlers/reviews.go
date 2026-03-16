package handlers

import (
	"net/http"

	"github.com/google/uuid"
	"github.com/labstack/echo/v5"
	"ugc/internal/models"
	"ugc/internal/services"
)

type ReviewsHandler struct {
	reviewsService *services.ReviewsService
}

func NewReviewsHandler(reviewsService *services.ReviewsService) *ReviewsHandler {
	return &ReviewsHandler{reviewsService: reviewsService}
}

func (h *ReviewsHandler) GetFilmworkReviews(c *echo.Context) error {
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}
	paginator := getPaginator(c)

	reviews, err := h.reviewsService.Filter(c.Request().Context(), filmworkID, paginator.Page, paginator.Size)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, reviews)
}

func (h *ReviewsHandler) CreateFilmworkReview(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	var text models.Text
	if err := c.Bind(&text); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	review, err := h.reviewsService.Update(c.Request().Context(), userID, filmworkID, text.Text)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, review)
}

func (h *ReviewsHandler) DeleteFilmworkReview(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}
	reviewID, err := uuid.Parse(c.Param("review_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid review_id")
	}

	err = h.reviewsService.Remove(c.Request().Context(), reviewID, userID, filmworkID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.NoContent(http.StatusNoContent)
}

func (h *ReviewsHandler) GetReviewRating(c *echo.Context) error {
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}
	reviewID, err := uuid.Parse(c.Param("review_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid review_id")
	}

	rating, err := h.reviewsService.GetRating(c.Request().Context(), reviewID, filmworkID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, rating)
}

func (h *ReviewsHandler) RateReview(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}
	reviewID, err := uuid.Parse(c.Param("review_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid review_id")
	}

	var score models.ReviewScore
	if err := c.Bind(&score); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	if err := c.Validate(score); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	rating, err := h.reviewsService.Rate(c.Request().Context(), reviewID, userID, filmworkID, score.Score)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, rating)
}

func (h *ReviewsHandler) UnrateReview(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}
	reviewID, err := uuid.Parse(c.Param("review_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid review_id")
	}

	rating, err := h.reviewsService.Unrate(c.Request().Context(), reviewID, filmworkID, userID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, rating)
}
