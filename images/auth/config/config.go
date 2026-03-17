package config

import (
	"fmt"
	"os"
	"strconv"
)

type Config struct {
	RunAddress  string
	DatabaseURI string
	DBName      string
	DBUser      string
	DBPass      string
	DBHost      string
	DBPort      string
	RedisHost   string
	RedisPort   string
	RedisPass   string
	RedisDB     int
	MongoHost   string
	MongoPort   string
	MongoUser   string
	MongoPass   string
	SecretJWT   string
}

func Load() *Config {
	cfg := &Config{}

	if dbName := os.Getenv("DB_NAME"); dbName != "" {
		cfg.DBName = dbName
	}
	if dbUser := os.Getenv("DB_USER"); dbUser != "" {
		cfg.DBUser = dbUser
	}
	if dbPass := os.Getenv("DB_PASSWORD"); dbPass != "" {
		cfg.DBPass = dbPass
	}
	if dbHost := os.Getenv("DB_HOST"); dbHost != "" {
		cfg.DBHost = dbHost
	}
	if dbPort := os.Getenv("DB_PORT"); dbPort != "" {
		cfg.DBPort = dbPort
	}
	if redisHost := os.Getenv("REDIS_HOST"); redisHost != "" {
		cfg.RedisHost = redisHost
	}
	if redisPort := os.Getenv("REDIS_PORT"); redisPort != "" {
		cfg.RedisPort = redisPort
	}
	if redisDB := os.Getenv("REDIS_DB"); redisDB != "" {
		redisDBInt, _ := strconv.Atoi(redisDB)
		cfg.RedisDB = redisDBInt
	}
	if redisPass := os.Getenv("REDIS_PASSWORD"); redisPass != "" {
		cfg.RedisPass = redisPass
	}
	if mongoHost := os.Getenv("MONGO_HOST"); mongoHost != "" {
		cfg.MongoHost = mongoHost
	}
	if mongoPort := os.Getenv("MONGO_PORT"); mongoPort != "" {
		cfg.MongoPort = mongoPort
	}
	if mongoUser := os.Getenv("MONGO_USERNAME"); mongoUser != "" {
		cfg.MongoUser = mongoUser
	}
	if mongoPass := os.Getenv("MONGO_PASSWORD"); mongoPass != "" {
		cfg.MongoPass = mongoPass
	}
	if secretJWT := os.Getenv("JWT_SECRET_KEY"); secretJWT != "" {
		cfg.SecretJWT = secretJWT
	}
	if runAddr := os.Getenv("RUN_ADDRESS"); runAddr != "" {
		cfg.RunAddress = runAddr
	}

	return cfg
}

func (c *Config) GetPostgresURI() string {
	if c.DBHost == "" || c.DBPort == "" || c.DBUser == "" || c.DBName == "" {
		return ""
	}
	return fmt.Sprintf("postgres://%s:%s@%s:%s/%s?sslmode=disable",
		c.DBUser, c.DBPass, c.DBHost, c.DBPort, c.DBName)
}

func (c *Config) GetMongoURI() string {
	if c.MongoHost == "" || c.MongoPort == "" {
		return ""
	}
	userInfo := ""
	if c.MongoUser != "" && c.MongoPass != "" {
		userInfo = fmt.Sprintf("%s:%s@", c.MongoUser, c.MongoPass)
	} else if c.MongoUser != "" {
		userInfo = fmt.Sprintf("%s@", c.MongoUser)
	}
	return fmt.Sprintf("mongodb://%s%s:%s", userInfo, c.MongoHost, c.MongoPort)
}
