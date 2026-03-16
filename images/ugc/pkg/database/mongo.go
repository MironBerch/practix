package database

import (
	"context"
	"fmt"
	"time"

	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
	"go.mongodb.org/mongo-driver/v2/mongo/readpref"

	"ugc/internal/config"
)

func NewMongoDB(uri string) (*mongo.Client, error) {
	opts := options.Client().
		ApplyURI(uri).
		SetMaxPoolSize(50).
		SetMinPoolSize(5).
		SetMaxConnIdleTime(10 * time.Minute)

	client, err := mongo.Connect(opts)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to MongoDB: %w", err)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := client.Ping(ctx, readpref.Primary()); err != nil {
		return nil, fmt.Errorf("failed to ping MongoDB: %w", err)
	}

	return client, nil
}

func GetMongoURI(c *config.MongoConfig) string {
	if c.Host == "" || c.Port == "" {
		return ""
	}
	userInfo := ""
	if c.Username != "" && c.Password != "" {
		userInfo = fmt.Sprintf("%s:%s@", c.Username, c.Password)
	} else if c.Username != "" {
		userInfo = fmt.Sprintf("%s@", c.Username)
	}
	return fmt.Sprintf("mongodb://%s%s:%s", userInfo, c.Host, c.Port)
}
