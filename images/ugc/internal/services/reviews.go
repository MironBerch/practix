package services

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
	"go.mongodb.org/mongo-driver/v2/bson"
	"go.mongodb.org/mongo-driver/v2/mongo"
	"go.mongodb.org/mongo-driver/v2/mongo/options"
	"ugc/internal/models"
)

type ReviewsService struct {
	mongo *mongo.Client
}

func NewReviewsService(mongo *mongo.Client) *ReviewsService {
	return &ReviewsService{mongo: mongo}
}

func (s *ReviewsService) Get(ctx context.Context, userID, filmworkID uuid.UUID) (*models.Review, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{
		"author_id":   models.UUIDToBinary(userID),
		"filmwork_id": models.UUIDToBinary(filmworkID),
	}
	var review models.Review
	err := db.Collection("reviews").FindOne(ctx, filter).Decode(&review)
	if err != nil {
		if errors.Is(err, mongo.ErrNoDocuments) {
			return nil, nil
		}
		return nil, err
	}
	return &review, nil
}

func (s *ReviewsService) Filter(ctx context.Context, filmworkID uuid.UUID, page, size int64) ([]models.Review, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"filmwork_id": models.UUIDToBinary(filmworkID)}
	opts := options.Find().SetSkip((page - 1) * size).SetLimit(size)
	cursor, err := db.Collection("reviews").Find(ctx, filter, opts)
	if err != nil {
		return nil, err
	}
	defer cursor.Close(ctx)

	var reviews []models.Review
	if err = cursor.All(ctx, &reviews); err != nil {
		return nil, err
	}
	return reviews, nil
}

func (s *ReviewsService) Update(ctx context.Context, userID, filmworkID uuid.UUID, text string) (*models.Review, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{
		"author_id":   models.UUIDToBinary(userID),
		"filmwork_id": models.UUIDToBinary(filmworkID),
	}
	update := bson.M{
		"$set": bson.M{"text": text},
		"$setOnInsert": bson.M{
			"_id":         models.UUIDToBinary(uuid.New()),
			"pub_date":    time.Now(),
			"rating":      bson.M{"votes": []bson.M{}},
			"author_id":   models.UUIDToBinary(userID),
			"filmwork_id": models.UUIDToBinary(filmworkID),
		},
	}
	opts := options.UpdateOne().SetUpsert(true)
	_, err := db.Collection("reviews").UpdateOne(ctx, filter, update, opts)
	if err != nil {
		return nil, err
	}

	var review models.Review
	err = db.Collection("reviews").FindOne(ctx, filter).Decode(&review)
	if err != nil {
		return nil, err
	}
	return &review, nil
}

func (s *ReviewsService) Remove(ctx context.Context, reviewID, userID, filmworkID uuid.UUID) error {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{
		"_id":         models.UUIDToBinary(reviewID),
		"author_id":   models.UUIDToBinary(userID),
		"filmwork_id": models.UUIDToBinary(filmworkID),
	}
	_, err := db.Collection("reviews").DeleteOne(ctx, filter)
	return err
}

func (s *ReviewsService) GetRating(ctx context.Context, reviewID, filmworkID uuid.UUID) (*models.ReviewRating, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{
		"_id":         models.UUIDToBinary(reviewID),
		"filmwork_id": models.UUIDToBinary(filmworkID),
	}
	var review struct {
		Rating models.ReviewRating `bson:"rating"`
	}
	err := db.Collection("reviews").FindOne(ctx, filter).Decode(&review)
	if err != nil {
		return nil, err
	}
	return &review.Rating, nil
}

func (s *ReviewsService) Rate(ctx context.Context, reviewID, userID, filmworkID uuid.UUID, score int) (*models.ReviewRating, error) {
	db := s.mongo.Database("ugc_database")
	reviewIDBin := models.UUIDToBinary(reviewID)
	//userIDBin := models.UUIDToBinary(userID)

	var review struct {
		Rating models.ReviewRating `bson:"rating"`
	}
	filter := bson.M{"_id": reviewIDBin}
	err := db.Collection("reviews").FindOne(ctx, filter).Decode(&review)
	if err != nil {
		return nil, err
	}

	votes := review.Rating.Votes
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
	_, err = db.Collection("reviews").UpdateOne(ctx, filter, update)
	if err != nil {
		return nil, err
	}

	var updated struct {
		Rating models.ReviewRating `bson:"rating"`
	}
	err = db.Collection("reviews").FindOne(ctx, filter).Decode(&updated)
	if err != nil {
		return nil, err
	}
	return &updated.Rating, nil
}

func (s *ReviewsService) Unrate(ctx context.Context, reviewID, filmworkID, userID uuid.UUID) (*models.ReviewRating, error) {
	db := s.mongo.Database("ugc_database")
	filter := bson.M{"_id": models.UUIDToBinary(reviewID)}
	update := bson.M{
		"$pull": bson.M{
			"rating.votes": bson.M{"user_id": models.UUIDToBinary(userID)},
		},
	}
	_, err := db.Collection("reviews").UpdateOne(ctx, filter, update)
	if err != nil {
		return nil, err
	}

	var updated struct {
		Rating models.ReviewRating `bson:"rating"`
	}
	err = db.Collection("reviews").FindOne(ctx, filter).Decode(&updated)
	if err != nil {
		return nil, err
	}
	return &updated.Rating, nil
}
