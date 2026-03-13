package genre

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type GenreHandler struct {
	service GenreService
}

func NewGenreHandler(service GenreService) *GenreHandler {
	return &GenreHandler{service: service}
}

func (h *GenreHandler) RegisterRoutes(router *gin.Engine) {
	router.GET("/movies/api/v1/genres", h.GetAll)
	router.GET("/movies/api/v1/genres/:id", h.GetByID)
}

func (h *GenreHandler) GetByID(c *gin.Context) {
	id := c.Param("id")
	g, err := h.service.GetByID(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, g)
}

func (h *GenreHandler) GetAll(c *gin.Context) {
	genres, err := h.service.GetAll(c.Request.Context())
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, genres)
}
