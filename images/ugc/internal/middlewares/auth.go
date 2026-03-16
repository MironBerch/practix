package middlewares

import (
	"net/http"
	"strings"

	"github.com/labstack/echo/v5"
	"ugc/internal/services"
)

type AuthMiddleware struct {
	authService *services.AuthService
}

func NewAuthMiddleware(authService *services.AuthService) *AuthMiddleware {
	return &AuthMiddleware{authService: authService}
}

func (m *AuthMiddleware) Auth(next echo.HandlerFunc) echo.HandlerFunc {
	return func(c *echo.Context) error {
		authHeader := c.Request().Header.Get("Authorization")
		if authHeader == "" {
			return echo.NewHTTPError(http.StatusUnauthorized, "missing authorization header")
		}

		// Extract token
		parts := strings.SplitN(authHeader, " ", 2)
		if len(parts) != 2 || parts[0] != "Bearer" {
			return echo.NewHTTPError(http.StatusUnauthorized, "invalid authorization header format")
		}
		token := parts[1]

		userID, err := m.authService.ExtractUserID(token)
		if err != nil {
			return echo.NewHTTPError(http.StatusUnauthorized, "invalid token: "+err.Error())
		}

		c.Set("user_id", userID)
		return next(c)
	}
}
