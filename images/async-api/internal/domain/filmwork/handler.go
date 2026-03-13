package filmwork

import (
	"async-api/internal/http/request"
	"net/http"
	"strings"

	"github.com/gin-gonic/gin"
)

type FilmworkHandler struct {
	service FilmworkService
}

func NewFilmworkHandler(service FilmworkService) *FilmworkHandler {
	return &FilmworkHandler{service: service}
}

func (h *FilmworkHandler) RegisterRoutes(router *gin.Engine) {
	router.GET("/movies/api/v1/filmworks/search", h.Search)
	router.GET("/movies/api/v1/filmworks", h.GetAll)
	router.GET("/movies/api/v1/filmworks/:id", h.GetByID)
}

func (h *FilmworkHandler) GetByID(c *gin.Context) {
	id := c.Param("id")
	g, err := h.service.GetByID(c.Request.Context(), id)
	if err != nil {
		statusCode := http.StatusInternalServerError
		if strings.Contains(err.Error(), "not found") {
			statusCode = http.StatusNotFound
		}
		c.JSON(statusCode, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, g)
}

func (h *FilmworkHandler) Search(c *gin.Context) {
	query := c.Query("query")
	filmworks, err := h.service.Search(c.Request.Context(), query, 1000)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, filmworks)
}

func (h *FilmworkHandler) GetAll(c *gin.Context) {
	pageNumberStr := c.Query("page_number")
	pageSizeStr := c.Query("page_size")
	genresParam := c.Query("genres")
	sort := c.Query("sort")

	genres := request.ValidateGenres(genresParam)
	pageNumber, pageSize := request.ValidatePaginator(pageNumberStr, pageSizeStr)

	filmworks, err := h.service.GetAll(c.Request.Context(), genres, sort, pageNumber, pageSize)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, filmworks)
}
