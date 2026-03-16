package handlers

import (
	"net/http"

	"github.com/google/uuid"
	"github.com/labstack/echo/v5"
	"ugc/internal/services"
)

type BookmarksHandler struct {
	bookmarksService *services.BookmarksService
}

func NewBookmarksHandler(bookmarksService *services.BookmarksService) *BookmarksHandler {
	return &BookmarksHandler{bookmarksService: bookmarksService}
}

func (h *BookmarksHandler) GetBookmarks(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	paginator := getPaginator(c)

	bookmarks, err := h.bookmarksService.Filter(c.Request().Context(), userID, paginator.Page, paginator.Size)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, bookmarks)
}

func (h *BookmarksHandler) BookmarkFilmwork(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	bookmark, err := h.bookmarksService.Update(c.Request().Context(), userID, filmworkID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, bookmark)
}

func (h *BookmarksHandler) UnbookmarkFilmwork(c *echo.Context) error {
	userID := c.Get("user_id").(uuid.UUID)
	filmworkID, err := uuid.Parse(c.Param("filmwork_id"))
	if err != nil {
		return echo.NewHTTPError(http.StatusBadRequest, "invalid filmwork_id")
	}

	bookmark, err := h.bookmarksService.Remove(c.Request().Context(), userID, filmworkID)
	if err != nil {
		return echo.NewHTTPError(http.StatusInternalServerError, err.Error())
	}
	return c.JSON(http.StatusOK, bookmark)
}
