package services

import (
	"context"

	"github.com/google/uuid"
	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
	"ugc/internal/models"
)

type BookmarksService struct {
	mongo *mongo.Client
}

func NewBookmarksService(mongo *mongo.Client) *BookmarksService {
	return &BookmarksService{mongo: mongo}
}

func (s *BookmarksService) Filter(ctx context.Context, userID uuid.UUID, page, size int64) ([]models.FilmworkBookmark, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"_id": models.UUIDToBinary(userID)}
	skip := (page - 1) * size
	opts := options.Find().
		SetProjection(bson.M{"bookmarks": 1}).
		SetSkip(skip).
		SetLimit(size)
	cursor, err := db.Collection("users").Find(ctx, filter, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)
	var results []struct {
		Bookmarks []struct {
			FilmworkID bson.Binary `bson:"filmwork_id"`
		} `bson:"bookmarks"`
	}
	err = cursor.All(ctx, &results)
	if err != nil {
		return nil, err
	}
	if len(results) == 0 {
		return []models.FilmworkBookmark{}, nil
	}
	bookmarksData := results[0]
	bookmarks := make([]models.FilmworkBookmark, len(bookmarksData.Bookmarks))
	for i, b := range bookmarksData.Bookmarks {
		bookmarks[i] = models.FilmworkBookmark{
			FilmworkID: models.BinaryToUUID(b.FilmworkID),
		}
	}
	return bookmarks, nil
}

func (s *BookmarksService) Update(ctx context.Context, userID, filmworkID uuid.UUID) (*models.FilmworkBookmark, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"_id": models.UUIDToBinary(userID)}
	update := bson.M{
		"$addToSet": bson.M{
			"bookmarks": bson.M{"filmwork_id": models.UUIDToBinary(filmworkID)},
		},
	}
	opts := options.UpdateOne().SetUpsert(true)
	_, err := db.Collection("users").UpdateOne(ctx, filter, update, opts)
	if err != nil {
		return nil, err
	}
	return &models.FilmworkBookmark{FilmworkID: filmworkID}, nil
}

func (s *BookmarksService) Remove(ctx context.Context, userID, filmworkID uuid.UUID) (*models.FilmworkBookmark, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"_id": models.UUIDToBinary(userID)}
	update := bson.M{
		"$pull": bson.M{
			"bookmarks": bson.M{"filmwork_id": models.UUIDToBinary(filmworkID)},
		},
	}
	_, err := db.Collection("users").UpdateOne(ctx, filter, update)
	if err != nil {
		return nil, err
	}
	return &models.FilmworkBookmark{FilmworkID: filmworkID}, nil
}
