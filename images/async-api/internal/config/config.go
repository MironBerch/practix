package config

import (
	"os"
	"strconv"
)

type Config struct {
	RunAddress           string
	RedisHost            string
	RedisPort            string
	RedisPass            string
	RedisDB              int
	ElasticHost            string
	ElasticPort            string
	ElasticUser            string
	ElasticPass            string
}

func Load() *Config {
	cfg := &Config{}
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
	if elasticHost := os.Getenv("ELASTIC_HOST"); elasticHost != "" {
		cfg.ElasticHost = elasticHost
	}
	if elasticPort := os.Getenv("ELASTIC_PORT"); elasticPort != "" {
		cfg.ElasticPort = elasticPort
	}
	if elasticUser := os.Getenv("ELASTIC_USERNAME"); elasticUser != "" {
		cfg.ElasticUser = elasticUser
	}
	if elasticPass := os.Getenv("ELASTIC_PASSWORD"); elasticPass != "" {
		cfg.ElasticPass = elasticPass
	}
	if runAddr := os.Getenv("RUN_ADDRESS"); runAddr != "" {
		cfg.RunAddress = runAddr
	}

	return cfg
}
