package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/go-chi/cors"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"

	"auth/config"
	"auth/internal/domain/auth"
	"auth/internal/domain/user"
	"auth/pkg/database"
)

func main() {
	cfg := config.Load()

	db, err := database.NewPostgres(cfg.GetPostgresURI())
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	if err := database.Migrate(cfg.GetPostgresURI()); err != nil {
		log.Fatal("Failed to run migrations:", err)
	}

	cache := database.NewRedis(cfg.RedisHost, cfg.RedisPort, cfg.RedisPass, cfg.RedisDB)
	defer cache.Close()

	mongo, err := database.NewMongoDB(cfg.GetMongoURI())
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer mongo.Disconnect(context.Background())

	authService := auth.New(cfg.SecretJWT, cache)

	userRepo := user.NewRepository(db, mongo)
	userService := user.NewService(userRepo, authService)
	userHandler := user.NewHandler(userService)

	r := chi.NewRouter()

	r.Use(middleware.RequestID)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)
	r.Use(middleware.Compress(5))

    r.Use(cors.Handler(cors.Options{
        AllowedOrigins:   []string{"https://*", "http://*"},
        AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"},
        AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
        AllowCredentials: true,
        MaxAge:           300,
    }))

	r.Get("/auth/api/v1/health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		response := map[string]string{"status": "ok"}
		if err := json.NewEncoder(w).Encode(response); err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
	})

	r.Group(func(r chi.Router) {
		r.Post("/auth/api/v1/signup", userHandler.Signup)
		r.Post("/auth/api/v1/signin", userHandler.Signin)
	})

	r.Group(func(r chi.Router) {
		r.Use(auth.Middleware(authService))

		r.Post("/auth/api/v1/logout", userHandler.Logout)
		r.Post("/auth/api/v1/refresh", userHandler.Refresh)
		r.Get("/auth/api/v1/user_info", userHandler.UserInfo)
		r.Post("/auth/api/v1/password_change", userHandler.PasswordChange)
		r.Post("/auth/api/v1/change_email", userHandler.ChangeEmail)
		r.Get("/auth/api/v1/user_sessions", userHandler.UserSessions)
	})

	srv := &http.Server{
		Addr:    ":" + cfg.RunAddress,
		Handler: r,
	}

	done := make(chan os.Signal, 1)
	signal.Notify(done, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		log.Printf("Server starting on %s", cfg.RunAddress)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal("Server error:", err)
		}
	}()

	<-done
	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server shutdown error:", err)
	}

	log.Println("Server stopped")
}
