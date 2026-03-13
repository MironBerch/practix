package request

import (
	"strconv"
	"strings"
)

func ValidateGenres(genresParam string) []string {
	var genres []string
	if genresParam != "" {
		genres = strings.Split(genresParam, ",")
		for i := range genres {
			genres[i] = strings.TrimSpace(genres[i])
		}
	}
	return genres
}

func ValidatePaginator(pageNumberStr string, pageSizeStr string) (int, int) {
	pageNumber, pageSize := 1, 100
	if pageNumberStr != "" {
		if p, err := strconv.Atoi(pageNumberStr); err == nil && p > 0 {
			pageNumber = p
		}
	}
	if pageSizeStr != "" {
		if s, err := strconv.Atoi(pageSizeStr); err == nil && s > 0 {
			if s > 100 {
				pageSize = 100
			} else {
				pageSize = s
			}
		}
	}
	return pageNumber, pageSize
}
