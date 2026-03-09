package user

import (
	"context"
	"errors"
	"fmt"
	"log"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/jackc/pgx/v5/pgxpool"
	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
)

type Repository interface {
	CreateUser(ctx context.Context, email, passwordHash string) (*User, error)
	GetUserByEmail(ctx context.Context, email string) (*User, error)
	GetUserByID(ctx context.Context, id string) (*User, error)
	CreateUserSession(ctx context.Context, userId, userAgent, UserDeviceType string) (*UserSessionResponse, error)
	CheckUserPassword(ctx context.Context, id, passwordHash string) (bool, error)
	GetUserInfo(ctx context.Context, id string) (*GetUserInfoResponse, error)
	ChangeUserPassword(ctx context.Context, id string, passwordHash string) (*User, error)
	ChangeUserEmail(ctx context.Context, id, email string) (*User, error)
	GetUserSessions(ctx context.Context, id string) ([]UserSessionResponse, error)
}

type repository struct {
	db    *pgxpool.Pool
	mongo *mongo.Client
}

func NewRepository(db *pgxpool.Pool, mongo *mongo.Client) Repository {
	return &repository{db: db, mongo: mongo}
}

func (r *repository) CreateUser(ctx context.Context, email, passwordHash string) (*User, error) {
	query := `
        INSERT INTO users (email, password_hash)
        VALUES ($1, $2)
        RETURNING id, email, password_hash, created_at
    `

	var user User
	err := r.db.QueryRow(ctx, query, email, passwordHash).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)

	if err != nil {
		if err.Error() == "ERROR: duplicate key value violates unique constraint \"users_email_key\" (SQLSTATE 23505)" {
			return nil, ErrUserExists
		}
		return nil, err
	}

	db := r.mongo.Database("ugc_database")
	coll := db.Collection("users")

	uid, err := uuid.Parse(user.ID)
	if err != nil {
		return &user, fmt.Errorf("invalid UUID string: %w", err)
	}

	userID := uid[:]
	doc := bson.D{
		{Key: "_id", Value: userID},
		{Key: "bookmarks", Value: []bson.M{}},
	}

	_, err = coll.InsertOne(ctx, doc)
	if err != nil {
		return &user, fmt.Errorf("failed to insert user: %w", err)
	}

	return &user, nil
}

func (r *repository) GetUserByEmail(ctx context.Context, email string) (*User, error) {
	query := `
        SELECT id, email, password_hash, created_at
        FROM users
        WHERE email = $1
    `

	var user User
	err := r.db.QueryRow(ctx, query, email).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)

	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, ErrUserNotFound
		}
		return nil, err
	}

	return &user, nil
}

func (r *repository) GetUserByID(ctx context.Context, id string) (*User, error) {
	query := `
        SELECT id, email, password_hash, created_at
        FROM users
        WHERE id = $1
    `

	var user User
	err := r.db.QueryRow(ctx, query, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)

	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, ErrUserNotFound
		}
		return nil, err
	}

	return &user, nil
}

func (r *repository) CreateUserSession(ctx context.Context, userId string, userAgent string, UserDeviceType string) (*UserSessionResponse, error) {
	query := `
        INSERT INTO sessions (user_id, user_agent, user_device_type)
        VALUES ($1, $2, $3)
        RETURNING user_id, event_date, user_agent, user_device_type
    `

	var session UserSessionResponse
	err := r.db.QueryRow(ctx, query, userId, userAgent, UserDeviceType).Scan(
		&session.UserID,
		&session.EventDate,
		&session.UserAgent,
		&session.UserDeviceType,
	)

	if err != nil {
		if err.Error() == "ERROR: duplicate key value violates unique constraint \"users_email_key\" (SQLSTATE 23505)" {
			return nil, ErrUserExists
		}
		return nil, err
	}

	return &session, nil
}

func (r *repository) CheckUserPassword(ctx context.Context, id string, PasswordHash string) (bool, error) {
	query := `
        SELECT id, email, password_hash, created_at
        FROM users
        WHERE id = $1
    `

	var user User
	err := r.db.QueryRow(ctx, query, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)

	if err != nil {
		if err == pgx.ErrNoRows {
			return false, ErrUserNotFound
		}
		return false, err
	}

	return user.PasswordHash == PasswordHash, nil
}

func (r *repository) GetUserInfo(ctx context.Context, id string) (*GetUserInfoResponse, error) {
	query := `
        SELECT id, created_at, email
        FROM users
        WHERE id = $1
    `

	var userInfo GetUserInfoResponse
	err := r.db.QueryRow(ctx, query, id).Scan(
		&userInfo.UserID,
		&userInfo.UserCreatedAt,
		&userInfo.UserEmail,
	)

	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, ErrUserNotFound
		}
		return nil, err
	}

	return &userInfo, nil
}

func (r *repository) ChangeUserPassword(ctx context.Context, id string, passwordHash string) (*User, error) {
	query := `
        UPDATE users
        SET password_hash = $1
        WHERE id = $2
        RETURNING id, email, password_hash, created_at
    `

	var user User
	err := r.db.QueryRow(ctx, query, passwordHash, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)
	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, ErrUserNotFound
		}
		return nil, err
	}

	return &user, nil
}

func (r *repository) ChangeUserEmail(ctx context.Context, id string, email string) (*User, error) {
	query := `
        UPDATE users
        SET email = $1
        WHERE id = $2
        RETURNING id, email, password_hash, created_at
    `

	var user User
	err := r.db.QueryRow(ctx, query, email, id).Scan(
		&user.ID,
		&user.Email,
		&user.PasswordHash,
		&user.CreatedAt,
	)
	if err != nil {
		if errors.Is(err, pgx.ErrNoRows) {
			return nil, ErrUserNotFound
		}

		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == "23505" {
			return nil, ErrEmailAlreadyExists
		}
		return nil, err
	}

	return &user, nil
}

func (r *repository) GetUserSessions(ctx context.Context, id string) ([]UserSessionResponse, error) {
	query := `
        SELECT event_date, user_id, user_agent, user_device_type
        FROM sessions
        WHERE user_id = $1
        ORDER BY event_date DESC
    `

	rows, err := r.db.Query(ctx, query, id)
	if err != nil {
		log.Println(err)
		return nil, err
	}
	defer rows.Close()

	var sessions []UserSessionResponse
	for rows.Next() {
		var session UserSessionResponse

		err := rows.Scan(
			&session.EventDate,
			&session.UserID,
			&session.UserAgent,
			&session.UserDeviceType,
		)
		if err != nil {
			log.Println(err)
			return nil, err
		}

		sessions = append(sessions, session)
	}
	return sessions, nil
}
