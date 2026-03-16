package services

import (
	"errors"
	"strings"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"ugc/internal/config"
)

type AuthService struct {
	cfg *config.AuthConfig
}

func NewAuthService(cfg *config.AuthConfig) *AuthService {
	return &AuthService{cfg: cfg}
}

func (s *AuthService) ExtractUserID(tokenString string) (uuid.UUID, error) {
	tokenString = strings.TrimPrefix(tokenString, "Bearer ")

	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errors.New("unexpected signing method")
		}
		return []byte(s.cfg.JWTSecretKey), nil
	})
	if err != nil {
		return uuid.Nil, err
	}

	if !token.Valid {
		return uuid.Nil, errors.New("invalid token")
	}

	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return uuid.Nil, errors.New("invalid claims")
	}

	sub, ok := claims["sub"].(string)
	if !ok {
		return uuid.Nil, errors.New("sub claim missing")
	}

	userID, err := uuid.Parse(sub)
	if err != nil {
		return uuid.Nil, err
	}

	return userID, nil
}
