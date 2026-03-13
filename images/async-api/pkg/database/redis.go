package database

import (
	"github.com/redis/go-redis/v9"
)

func NewRedis(host, port, pass string, db int) *redis.Client {
	rdb := redis.NewClient(&redis.Options{
		Addr:     host + ":" + port,
		Password: pass,
		DB:       db,
	})
	return rdb
}
