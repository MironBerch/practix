package e2e

import (
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

const asyncAPIBaseURL = "http://localhost:3000"

func TestAsyncAPIHealth(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Get(asyncAPIBaseURL + "/healthz")
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAsyncAPIGetGenres(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/genres")
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAsyncAPIGetGenreByID(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	genreID := "0b105f87-e0a5-45dc-8ce7-f8632088f390"
	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/genres/" + genreID)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.True(t, resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusNotFound)
}

func TestAsyncAPIGetPersons(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/persons")
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAsyncAPIGetPersonByID(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	personID := "0031feab-8f53-412a-8f53-47098a60ac73"
	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/persons/" + personID)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.True(t, resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusNotFound)
}

func TestAsyncAPIGetFilmworks(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/filmworks")
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAsyncAPIGetFilmworkByID(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	filmworkID := "2c132fb2-69a8-4ab3-aee7-399a0f607ade"
	resp, err := client.Get(asyncAPIBaseURL + "/movies/api/v1/filmworks/" + filmworkID)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.True(t, resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusNotFound)
}
