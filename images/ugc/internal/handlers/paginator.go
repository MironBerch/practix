package handlers

import (
	"github.com/labstack/echo/v5"
	"ugc/internal/middlewares"
)

func getPaginator(c *echo.Context) middlewares.Paginator {
	if p, ok := c.Get("paginator").(middlewares.Paginator); ok {
		return p
	}
	return middlewares.Paginator{Page: 1, Size: 50}
}
