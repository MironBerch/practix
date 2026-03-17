package services

import (
	"context"
	"errors"

	"github.com/google/uuid"
	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
	"ugc/internal/models"
)

type FilmworksService struct {
	mongo *mongo.Client
}

func NewFilmworksService(mongo *mongo.Client) *FilmworksService {
	return &FilmworksService{mongo: mongo}
}

func (s *FilmworksService) Get(ctx context.Context, filmworkID uuid.UUID) (*models.Rating, error) {
    db := s.mongo.Database("ugc_database")
    binID := models.UUIDToBinary(filmworkID)

    var filmwork struct {
        Rating models.Rating `bson:"rating"`
    }
    filter := bson.M{"_id": binID}
    err := db.Collection("filmworks").FindOne(ctx, filter).Decode(&filmwork)
    if err != nil {
        if errors.Is(err, mongo.ErrNoDocuments) {
            return nil, nil
        }
        return nil, err
    }
    return &filmwork.Rating, nil
}

func (s *FilmworksService) GetRating(ctx context.Context, filmworkID uuid.UUID) (*models.Rating, error) {
	return s.Get(ctx, filmworkID)
}

func (s *FilmworksService) Rate(ctx context.Context, filmworkID, userID uuid.UUID, score int) (*models.Rating, error) {
	db := s.mongo.Database("ugc_database")
	filmworkIDBin := models.UUIDToBinary(filmworkID)
	//userIDBin := models.UUIDToBinary(userID)

	var filmwork struct {
		Rating models.Rating `bson:"rating"`
	}
	filter := bson.M{"_id": filmworkIDBin}
	err := db.Collection("filmworks").FindOne(ctx, filter).Decode(&filmwork)
	if err != nil && !errors.Is(err, mongo.ErrNoDocuments) {
		return nil, err
	}

	votes := filmwork.Rating.Votes
	found := false
	for i, v := range votes {
		if v.UserID == userID {
			votes[i].Score = score
			found = true
			break
		}
	}
	if !found {
		votes = append(votes, models.Vote{UserID: userID, Score: score})
	}

	update := bson.M{"$set": bson.M{"rating.votes": votes}}
	opts := options.UpdateOne().SetUpsert(true)
	_, err = db.Collection("filmworks").UpdateOne(ctx, filter, update, opts)
	if err != nil {
		return nil, err
	}

	var updated struct {
		Rating models.Rating `bson:"rating"`
	}
	err = db.Collection("filmworks").FindOne(ctx, filter).Decode(&updated)
	if err != nil {
		return nil, err
	}
	return &updated.Rating, nil
}

func (s *FilmworksService) Unrate(ctx context.Context, filmworkID, userID uuid.UUID) (*models.Rating, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"_id": models.UUIDToBinary(filmworkID)}
	update := bson.M{
		"$pull": bson.M{
			"rating.votes": bson.M{"user_id": models.UUIDToBinary(userID)},
		},
	}
	_, err := db.Collection("filmworks").UpdateOne(ctx, filter, update)
	if err != nil {
		return nil, err
	}

	var updated struct {
		Rating models.Rating `bson:"rating"`
	}
	err = db.Collection("filmworks").FindOne(ctx, filter).Decode(&updated)
	if err != nil {
		return nil, err
	}
	return &updated.Rating, nil
}
