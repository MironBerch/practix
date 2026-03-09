package auth

import (
	"context"
	"errors"
	"fmt"
	"time"

	"auth/internal/token"

	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

var (
	ErrInvalidToken = errors.New("invalid token")
	ErrTokenExpired = errors.New("token expired")
	ErrBlacklisted  = errors.New("token is blacklisted")
)

type Auth struct {
	secret        string
	accessExpiry  time.Duration
	refreshExpiry time.Duration
	redis         *redis.Client
}

func New(secret string, redisClient *redis.Client) *Auth {
	return &Auth{
		secret:        secret,
		accessExpiry:  1 * time.Minute,
		refreshExpiry: 7 * 24 * time.Hour,
		redis:         redisClient,
	}
}

func (a *Auth) generateToken(subject string, tokenType string, expiry time.Duration) (string, error) {
	now := time.Now()
	claims := token.Claims{
		RegisteredClaims: jwt.RegisteredClaims{
			Subject:   subject,
			IssuedAt:  jwt.NewNumericDate(now),
			ExpiresAt: jwt.NewNumericDate(now.Add(expiry)),
		},
		Type: tokenType,
		Jti:  uuid.New().String(),
	}

	tokenObj := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return tokenObj.SignedString([]byte(a.secret))
}

func (a *Auth) GenerateAccessToken(userID string) (string, error) {
	return a.generateToken(userID, "access", a.accessExpiry)
}

func (a *Auth) GenerateRefreshToken(userID string) (string, error) {
	return a.generateToken(userID, "refresh", a.refreshExpiry)
}

func (a *Auth) parseToken(tokenString string, verifyExp bool) (*token.Claims, error) {
	parser := jwt.NewParser(
		jwt.WithValidMethods([]string{jwt.SigningMethodHS256.Name}),
	)
	if !verifyExp {
		parser = jwt.NewParser(
			jwt.WithValidMethods([]string{jwt.SigningMethodHS256.Name}),
			jwt.WithoutClaimsValidation(),
		)
	}

	var claims token.Claims
	_, err := parser.ParseWithClaims(tokenString, &claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(a.secret), nil
	})
	if err != nil {
		if errors.Is(err, jwt.ErrTokenExpired) {
			return nil, ErrTokenExpired
		}
		return nil, ErrInvalidToken
	}

	ctx := context.Background()
	val, err := a.redis.Get(ctx, "blacklist:"+claims.Jti).Result()
	if err == nil && val != "" {
		return nil, ErrBlacklisted
	}
	if err != nil && err != redis.Nil {
		return nil, fmt.Errorf("redis error: %w", err)
	}

	return &claims, nil
}

func (a *Auth) ValidateToken(tokenString string) (*token.Claims, error) {
	return a.parseToken(tokenString, true)
}

func (a *Auth) VerifyToken(tokenString string) (*token.Claims, error) {
	return a.ValidateToken(tokenString)
}

func (a *Auth) GetTokenPayload(tokenString string) (*token.Claims, error) {
	return a.parseToken(tokenString, false)
}

func (a *Auth) AddTokenToBlacklist(tokenString string) (*token.Claims, error) {
	claims, err := a.GetTokenPayload(tokenString)
	if err != nil {
		return nil, err
	}

	ttl := time.Until(claims.ExpiresAt.Time)
	if ttl <= 0 {
		return claims, nil
	}

	ctx := context.Background()
	if err := a.redis.Set(ctx, "blacklist:"+claims.Jti, "revoked", ttl).Err(); err != nil {
		return nil, fmt.Errorf("failed to blacklist token: %w", err)
	}

	return claims, nil
}
