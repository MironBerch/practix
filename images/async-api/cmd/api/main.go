package main

import (
	"async-api/internal/config"
	"async-api/internal/domain/filmwork"
	"async-api/internal/domain/genre"
	"async-api/internal/domain/person"
	"async-api/pkg/database"
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func healthzHandler(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{"message": "ok"})
}

func main() {
	cfg := config.Load()

	esClient, err := database.SetupElasticClient(*cfg)
	if err != nil {
		log.Fatal("Failed to setup Elasticsearch client:", err)
	}

	genreRepo := genre.NewGenreRepository(esClient)
	genreService := genre.NewGenreService(genreRepo)
	genreHandler := genre.NewGenreHandler(genreService)

	personRepo := person.NewPersonRepository(esClient)
	personService := person.NewPersonService(personRepo)
	personHandler := person.NewPersonHandler(personService)

	filmworkRepo := filmwork.NewFilmworkRepository(esClient)
	filmworkService := filmwork.NewFilmworkService(filmworkRepo)
	filmworkHandler := filmwork.NewFilmworkHandler(filmworkService)

	router := gin.Default()

	router.Use(cors.New(cors.Config{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders: []string{"Content-Type", "Authorization"},
	}))

	router.GET("/healthz", healthzHandler)

	genreHandler.RegisterRoutes(router)
	personHandler.RegisterRoutes(router)
	filmworkHandler.RegisterRoutes(router)

	srv := &http.Server{
		Addr:    ":" + cfg.RunAddress,
		Handler: router,
	}

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		log.Printf("Server starting on port %s", cfg.RunAddress)
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server error: %v", err)
		}
	}()

	<-quit
	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		log.Fatal("Server forced to shutdown:", err)
	}

	log.Println("Server stopped")
}
