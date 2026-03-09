package user

import (
	"context"
	"errors"

	"auth/internal/token"
	"auth/internal/utils"
)

type Service interface {
	RegisterUser(ctx context.Context, req *SignupRequest, userAgent, deviceType string) (*FullTokensResponse, error)
	LoginUser(ctx context.Context, req *SigninRequest, userAgent, deviceType string) (*FullTokensResponse, error)
	LogoutUser(ctx context.Context, token string) error
	RefreshToken(ctx context.Context, refreshToken string) (*RefreshTokenResponse, error)
	GetUserInfo(ctx context.Context, userID string) (*GetUserInfoResponse, error)
	ChangeUserPassword(ctx context.Context, userID string, req *PasswordChangeRequest) error
	ChangeUserEmail(ctx context.Context, userID string, req *ChangeEmailRequest) error
	GetUserSessions(ctx context.Context, userID string) ([]UserSessionResponse, error)
}

type service struct {
	repo         Repository
	tokenManager token.Manager
}

func NewService(repo Repository, tokenManager token.Manager) Service {
	return &service{
		repo:         repo,
		tokenManager: tokenManager,
	}
}

func (s *service) RegisterUser(ctx context.Context, req *SignupRequest, userAgent, deviceType string) (*FullTokensResponse, error) {
	existing, _ := s.repo.GetUserByEmail(ctx, req.Email)
	if existing != nil {
		return nil, ErrUserExists
	}

	hash, err := utils.HashPassword(req.Password)
	if err != nil {
		return nil, err
	}

	user, err := s.repo.CreateUser(ctx, req.Email, hash)
	if err != nil {
		return nil, err
	}

	_, _ = s.repo.CreateUserSession(ctx, user.ID, userAgent, deviceType)

	accessToken, _ := s.tokenManager.GenerateAccessToken(user.ID)
	refreshToken, _ := s.tokenManager.GenerateRefreshToken(user.ID)

	return &FullTokensResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	}, nil
}

func (s *service) LoginUser(ctx context.Context, req *SigninRequest, userAgent, deviceType string) (*FullTokensResponse, error) {
	user, err := s.repo.GetUserByEmail(ctx, req.Email)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			return nil, ErrInvalidCredentials
		}
		return nil, err
	}

	if !utils.CheckPasswordHash(req.Password, user.PasswordHash) {
		return nil, ErrInvalidCredentials
	}

	_, _ = s.repo.CreateUserSession(ctx, user.ID, userAgent, deviceType)

	accessToken, _ := s.tokenManager.GenerateAccessToken(user.ID)
	refreshToken, _ := s.tokenManager.GenerateRefreshToken(user.ID)

	return &FullTokensResponse{
		AccessToken:  accessToken,
		RefreshToken: refreshToken,
	}, nil
}

func (s *service) LogoutUser(ctx context.Context, token string) error {
	_, err := s.tokenManager.AddTokenToBlacklist(token)
	return err
}

func (s *service) RefreshToken(ctx context.Context, refreshToken string) (*RefreshTokenResponse, error) {
	claims, err := s.tokenManager.ValidateToken(refreshToken)
	if err != nil {
		return nil, err
	}
	if claims.Type != "refresh" {
		return nil, ErrInvalidToken
	}

	_, _ = s.tokenManager.AddTokenToBlacklist(refreshToken)

	accessToken, _ := s.tokenManager.GenerateAccessToken(claims.Subject)
	return &RefreshTokenResponse{AccessToken: accessToken}, nil
}

func (s *service) GetUserInfo(ctx context.Context, userID string) (*GetUserInfoResponse, error) {
	user, err := s.repo.GetUserByID(ctx, userID)
	if err != nil {
		return nil, err
	}
	return &GetUserInfoResponse{
		UserID:        user.ID,
		UserCreatedAt: user.CreatedAt.Format("2006-01-02T15:04:05Z"),
		UserEmail:     user.Email,
	}, nil
}

func (s *service) ChangeUserPassword(ctx context.Context, userID string, req *PasswordChangeRequest) error {
	user, err := s.repo.GetUserByID(ctx, userID)
	if err != nil {
		return err
	}
	if !utils.CheckPasswordHash(req.OldPassword, user.PasswordHash) {
		return ErrInvalidPassword
	}
	newHash, err := utils.HashPassword(req.NewPassword)
	if err != nil {
		return err
	}
	_, err = s.repo.ChangeUserPassword(ctx, userID, newHash)
	return err
}

func (s *service) ChangeUserEmail(ctx context.Context, userID string, req *ChangeEmailRequest) error {
	existing, _ := s.repo.GetUserByEmail(ctx, req.Email)
	if existing != nil && existing.ID != userID {
		return ErrEmailAlreadyExists
	}
	_, err := s.repo.ChangeUserEmail(ctx, userID, req.Email)
	return err
}

func (s *service) GetUserSessions(ctx context.Context, userID string) ([]UserSessionResponse, error) {
	return s.repo.GetUserSessions(ctx, userID)
}
