package main

import (
	"context"
	"log"

	"github.com/labstack/echo/v5"
	"github.com/labstack/echo/v5/middleware"
	"ugc/internal/config"
	"ugc/internal/handlers"
	"ugc/internal/middlewares"
	"ugc/internal/services"
	"ugc/pkg/database"
	"ugc/internal/validator"
)

func main() {
	cfg, err := config.New()
	if err != nil {
		log.Fatalf("failed to load config: %v", err)
	}

	mongoUri := database.GetMongoURI(&cfg.Mongo)
	mongo, err := database.NewMongoDB(mongoUri)
	if err != nil {
		log.Fatalf("failed to connect to MongoDB: %v", err)
	}
	defer mongo.Disconnect(context.Background())

	authService := services.NewAuthService(&cfg.Auth)
	bookmarksService := services.NewBookmarksService(mongo)
	filmworksService := services.NewFilmworksService(mongo)
	reviewsService := services.NewReviewsService(mongo)

	bookmarksHandler := handlers.NewBookmarksHandler(bookmarksService)
	filmworksHandler := handlers.NewFilmworksHandler(filmworksService)
	reviewsHandler := handlers.NewReviewsHandler(reviewsService)

	e := echo.New()

	e.Validator = validator.New()

	e.Use(middleware.RequestLogger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "DELETE"},
		AllowHeaders:     []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		AllowCredentials: false,
		MaxAge:           300,
	}))

	authMiddleware := middlewares.NewAuthMiddleware(authService)

	apiV1 := e.Group("/ugc/api/v1")

	bookmarks := apiV1.Group("", authMiddleware.Auth)
	bookmarks.GET("/bookmarks", bookmarksHandler.GetBookmarks, middlewares.PaginatorMiddleware)
	bookmarks.POST("/filmworks/:filmwork_id/bookmarks", bookmarksHandler.BookmarkFilmwork)
	bookmarks.DELETE("/filmworks/:filmwork_id/bookmarks", bookmarksHandler.UnbookmarkFilmwork)

	filmworks := apiV1.Group("/filmworks")
	filmworks.GET("/:filmwork_id/ratings", filmworksHandler.GetFilmworkRating)
	filmworks.POST("/:filmwork_id/ratings", filmworksHandler.RateFilmwork, authMiddleware.Auth)
	filmworks.DELETE("/:filmwork_id/ratings", filmworksHandler.UnrateFilmwork, authMiddleware.Auth)

	reviews := apiV1.Group("/filmworks")
	reviews.GET("/:filmwork_id/reviews", reviewsHandler.GetFilmworkReviews, middlewares.PaginatorMiddleware)
	reviews.POST("/:filmwork_id/reviews", reviewsHandler.CreateFilmworkReview, authMiddleware.Auth)
	reviews.DELETE("/:filmwork_id/reviews/:review_id", reviewsHandler.DeleteFilmworkReview, authMiddleware.Auth)
	reviews.GET("/:filmwork_id/reviews/:review_id/ratings", reviewsHandler.GetReviewRating)
	reviews.POST("/:filmwork_id/reviews/:review_id/ratings", reviewsHandler.RateReview, authMiddleware.Auth)
	reviews.DELETE("/:filmwork_id/reviews/:review_id/ratings", reviewsHandler.UnrateReview, authMiddleware.Auth)

	addr := "0.0.0.0" + ":" + cfg.Server.Port
	if err := e.Start(addr); err != nil {
		log.Fatalf("failed to start server: %v", err)
	}
}
