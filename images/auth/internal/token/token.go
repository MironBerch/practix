package token

import (
	"github.com/golang-jwt/jwt/v5"
)

type Manager interface {
	GenerateRefreshToken(userID string) (string, error)
	GenerateAccessToken(userID string) (string, error)
	ValidateToken(tokenString string) (*Claims, error)
	VerifyToken(tokenString string) (*Claims, error)
	GetTokenPayload(tokenString string) (*Claims, error)
	AddTokenToBlacklist(tokenString string) (*Claims, error)
}

type Claims struct {
	jwt.RegisteredClaims
	Type string `json:"type"`
	Jti  string `json:"jti"`
}

const (
	UserIDKey = "user_id"
)
