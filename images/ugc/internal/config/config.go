package config

import (
	"github.com/caarlos0/env/v11"
)

type Config struct {
	Server ServerConfig
	Mongo  MongoConfig
	Auth   AuthConfig
}

type ServerConfig struct {
	Port string `env:"RUN_ADDRESS"`
}

type MongoConfig struct {
	Host     string `env:"MONGO_HOST"`
	Port     string `env:"MONGO_PORT"`
	Username string `env:"MONGO_USERNAME"`
	Password string `env:"MONGO_PASSWORD"`
	DB       string `env:"MONGO_DB"`
}

type AuthConfig struct {
	JWTSecretKey string `env:"JWT_SECRET_KEY"`
	Algorithm    string `env:"JWT_ALGORITHM"`
}

func New() (*Config, error) {
	var cfg Config
	if err := env.Parse(&cfg.Server); err != nil {
		return nil, err
	}
	if err := env.Parse(&cfg.Mongo); err != nil {
		return nil, err
	}
	if err := env.Parse(&cfg.Auth); err != nil {
		return nil, err
	}
	return &cfg, nil
}
