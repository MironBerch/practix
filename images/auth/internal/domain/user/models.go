package user

import "time"

type User struct {
	ID           string
	Email        string
	PasswordHash string
	CreatedAt    time.Time
}

type SignupRequest struct {
	Email    string `json:"email" validate:"required,min=3,max=255"`
	Password string `json:"password" validate:"required,min=6"`
}

type SigninRequest struct {
	Email    string `json:"email" validate:"required"`
	Password string `json:"password" validate:"required"`
}

type PasswordChangeRequest struct {
	OldPassword string `json:"old_password" validate:"required,min=6"`
	NewPassword string `json:"new_password" validate:"required,min=6"`
}

type ChangeEmailRequest struct {
	Email string `json:"email" validate:"required,min=3,max=255"`
}

type FullTokensResponse struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
}

type RefreshTokenResponse struct {
	AccessToken string `json:"access_token"`
}

type GetUserInfoResponse struct {
	UserID        string `json:"user_id"`
	UserCreatedAt string `json:"user_created_at"`
	UserEmail     string `json:"user_email"`
}

type UserSessionResponse struct {
	UserID         string `json:"user_id"`
	UserAgent      string `json:"user_agent"`
	EventDate      time.Time `json:"event_date"`
	UserDeviceType string `json:"user_device_type"`
}
