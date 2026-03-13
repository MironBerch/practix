package person

import (
	"net/http"
	"strings"

	"async-api/internal/http/request"

	"github.com/gin-gonic/gin"
)

type PersonHandler struct {
	service PersonService
}

func NewPersonHandler(service PersonService) *PersonHandler {
	return &PersonHandler{service: service}
}

func (h *PersonHandler) RegisterRoutes(router *gin.Engine) {
	router.GET("/movies/api/v1/persons/search", h.Search)
	router.GET("/movies/api/v1/persons", h.GetAll)
	router.GET("/movies/api/v1/persons/:id", h.GetByID)
	router.GET("/movies/api/v1/persons/:id/filmworks", h.PersonFilmworks)
}

func (h *PersonHandler) GetByID(c *gin.Context) {
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

func (h *PersonHandler) Search(c *gin.Context) {
	query := c.Query("query")
	persons, err := h.service.Search(c.Request.Context(), query, 1000)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, persons)
}

func (h *PersonHandler) GetAll(c *gin.Context) {
	pageNumberStr := c.Query("page_number")
	pageSizeStr := c.Query("page_size")
	pageNumber, pageSize := request.ValidatePaginator(pageNumberStr, pageSizeStr)
	persons, err := h.service.GetAll(c.Request.Context(), pageNumber, pageSize)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, persons)
}

func (h *PersonHandler) PersonFilmworks(c *gin.Context) {
	id := c.Param("id")
	filmworks, err := h.service.GetPersonFilmworks(c.Request.Context(), id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, filmworks)
}
