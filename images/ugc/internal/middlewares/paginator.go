package middlewares

import (
	"github.com/labstack/echo/v5"
	"strconv"
)

type Paginator struct {
	Page int64
	Size int64
}

func PaginatorMiddleware(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c *echo.Context) error {
		pageStr := c.QueryParam("page[number]")
		sizeStr := c.QueryParam("page[size]")

		page := int64(1)
		size := int64(50)

		if pageStr != "" {
			if p, err := strconv.ParseInt(pageStr, 10, 64); err == nil && p >= 1 {
				page = p
			}
		}
		if sizeStr != "" {
			if s, err := strconv.ParseInt(sizeStr, 10, 64); err == nil && s >= 1 && s <= 100 {
				size = s
			}
		}

		c.Set("paginator", Paginator{Page: page, Size: size})
		return next(c)
	}
}
