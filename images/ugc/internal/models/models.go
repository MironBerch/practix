package models

import (
	"time"

	"github.com/google/uuid"
	"go.mongodb.org/mongo-driver/v2/bson"
)

type FilmworkBookmark struct {
	FilmworkID uuid.UUID `json:"filmwork_id" bson:"filmwork_id"`
}

type Text struct {
	Text string `json:"text" bson:"text"`
}

type Score struct {
	Score int `json:"score" validate:"min=1,max=10"`
}

type ReviewScore struct {
	Score int `json:"score" validate:"oneof=1 10"`
}

type Review struct {
	ID         uuid.UUID `json:"id" bson:"_id"`
	AuthorID   uuid.UUID `json:"author_id" bson:"author_id"`
	FilmworkID uuid.UUID `json:"filmwork_id" bson:"filmwork_id"`
	Text       string    `json:"text" bson:"text"`
	PubDate    time.Time `json:"pub_date" bson:"pub_date"`
}

type Vote struct {
	UserID uuid.UUID `json:"user_id" bson:"user_id"`
	Score  int       `json:"score" bson:"score"`
}

type Rating struct {
	AverageRating *float64 `json:"average_rating,omitempty" bson:"-"`
	Votes         []Vote   `json:"-" bson:"votes"`
}

type ReviewRating struct {
	Votes    []Vote `json:"-" bson:"votes"`
	Likes    int    `json:"likes" bson:"-"`
	Dislikes int    `json:"dislikes" bson:"-"`
	LikesSum int    `json:"likes_sum" bson:"-"`
}

func UUIDToBinary(id uuid.UUID) bson.Binary {
	return bson.Binary{Subtype: 0x00, Data: id[:]}
}

func BinaryToUUID(b bson.Binary) uuid.UUID {
	return uuid.UUID(b.Data)
}
