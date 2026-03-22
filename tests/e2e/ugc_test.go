package e2e

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

const ugcBaseURL = "http://localhost:8080"

type BookmarkRequest struct {
	FilmworkID string `json:"filmwork_id"`
}

type ReviewRequest struct {
	Text string `json:"text"`
}

type RatingRequest struct {
	Score int `json:"score"`
}

type Review struct {
	ID         uuid.UUID `json:"id"`
	AuthorID   uuid.UUID `json:"author_id"`
	FilmworkID uuid.UUID `json:"filmwork_id"`
	Text       string    `json:"text"`
	PubDate    time.Time `json:"pub_date"`
}

func getAuthToken(t *testing.T, email, password string) string {
	client := &http.Client{Timeout: 10 * time.Second}

	signupReq := map[string]string{
		"email":    email,
		"password": password,
	}
	jsonData, _ := json.Marshal(signupReq)
	resp, err := client.Post("http://localhost:5000/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Auth service not available: %v", err)
		return ""
	}
	resp.Body.Close()

	signinReq := map[string]string{
		"email":    email,
		"password": password,
	}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post("http://localhost:5000/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Auth service not available: %v", err)
		return ""
	}
	defer resp.Body.Close()

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)

	return authResp.AccessToken
}

func createFilmworkReview(t *testing.T, filmworkID string, accessToken string) (*Review, error) {
	client := &http.Client{Timeout: 10 * time.Second}
	reqBody := ReviewRequest{Text: "Great movie!"}
	jsonData, _ := json.Marshal(reqBody)

	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+accessToken)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return nil, err
	}
	defer resp.Body.Close()
	var reviewResp Review
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &reviewResp)
	return &reviewResp, nil
}

func TestUGCGetBookmarks(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc1@example.com", "password123")
	if token == "" {
		return
	}

	req, _ := http.NewRequest("GET", ugcBaseURL+"/ugc/api/v1/bookmarks", nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCBookmarkFilmwork(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc2@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	reqBody := BookmarkRequest{FilmworkID: filmworkID}
	jsonData, _ := json.Marshal(reqBody)

	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/bookmarks", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCUnbookmarkFilmwork(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc3@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"

	// First bookmark
	reqBody := BookmarkRequest{FilmworkID: filmworkID}
	jsonData, _ := json.Marshal(reqBody)
	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/bookmarks", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	req, _ = http.NewRequest("DELETE", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/bookmarks", nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCGetFilmworkRating(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc4@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	req, _ := http.NewRequest("GET", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/ratings", nil)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCRateFilmwork(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc5@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	reqBody := RatingRequest{Score: 5}
	jsonData, _ := json.Marshal(reqBody)

	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/ratings", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCUnrateFilmwork(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc6@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"

	reqBody := RatingRequest{Score: 5}
	jsonData, _ := json.Marshal(reqBody)
	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/ratings", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	req, _ = http.NewRequest("DELETE", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/ratings", nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCCreateReview(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc7@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	reqBody := ReviewRequest{Text: "Great movie!"}
	jsonData, _ := json.Marshal(reqBody)

	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCGetFilmworkReviews(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc8@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	req, _ := http.NewRequest("GET", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews", nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCDeleteReview(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc9@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	review, err := createFilmworkReview(t, filmworkID, token)
	if err != nil {
		return
	}

	req, _ := http.NewRequest("DELETE", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews/"+review.ID.String(), nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.True(t, resp.StatusCode == http.StatusNoContent)
}

func TestUGCRateReview(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc10@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	review, err := createFilmworkReview(t, filmworkID, token)
	if err != nil {
		return
	}
	reqBody := RatingRequest{Score: 10}
	jsonData, _ := json.Marshal(reqBody)

	req, _ := http.NewRequest("POST", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews/"+review.ID.String()+"/ratings", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+token)
	req.Header.Set("Content-Type", "application/json")

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCUnrateReview(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc11@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	review, err := createFilmworkReview(t, filmworkID, token)
	if err != nil {
		return
	}

	req, _ := http.NewRequest("DELETE", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews/"+review.ID.String()+"/ratings", nil)
	req.Header.Set("Authorization", "Bearer "+token)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestUGCGetReviewRating(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}
	token := getAuthToken(t, "ugc12@example.com", "password123")
	if token == "" {
		return
	}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	review, err := createFilmworkReview(t, filmworkID, token)
	if err != nil {
		return
	}

	req, _ := http.NewRequest("GET", ugcBaseURL+"/ugc/api/v1/filmworks/"+filmworkID+"/reviews/"+review.ID.String()+"/ratings", nil)

	resp, err := client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}
