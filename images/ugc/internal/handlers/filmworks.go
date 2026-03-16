package handlers

import (
	"net/http"

	"github.com/google/uuid"
	"github.com/labstack/echo/v5"
	"ugc/internal/models"
	"ugc/internal/services"
)

type FilmworksHandler struct {
	filmworksService *services.FilmworksService
}

func NewFilmworksHandler(filmworksService *services.FilmworksService) *FilmworksHandler {
	return &FilmworksHandler{filmworksService: filmworksService}
}

func (h *FilmworksHandler) GetFilmworkRating(c *echo.Context) error {
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	rating, err := h.filmworksService.GetRating(c.Request().Context(), filmworkID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	if rating == nil {
		return echo.NewHTTPError(http.StatusNotFound, "filmwork not found")
	}
	return c.JSON(http.StatusOK, rating)
}

func (h *FilmworksHandler) RateFilmwork(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	var score models.Score
	if err := c.Bind(&score); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}
	if err := c.Validate(score); err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, err.Error())
	}

	rating, err := h.filmworksService.Rate(c.Request().Context(), filmworkID, userID, score.Score)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, rating)
}

func (h *FilmworksHandler) UnrateFilmwork(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	rating, err := h.filmworksService.Unrate(c.Request().Context(), filmworkID, userID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, rating)
}
