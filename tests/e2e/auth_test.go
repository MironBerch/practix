package e2e

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

const authBaseURL = "http://localhost:5000"

type SignupRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type SigninRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}

type AuthResponse struct {
	AccessToken  string `json:"access_token"`
	RefreshToken string `json:"refresh_token"`
}

func TestAuthSignup(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	reqBody := SignupRequest{
		Email:    "test@example.com",
		Password: "password123",
	}
	jsonData, _ := json.Marshal(reqBody)

	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusCreated, resp.StatusCode)
}

func TestAuthSignin(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	reqBody := SignupRequest{
		Email:    "signin@example.com",
		Password: "password123",
	}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{
		Email:    "signin@example.com",
		Password: "password123",
	}
	jsonData, _ = json.Marshal(signinReq)

	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)

	assert.NotEmpty(t, authResp.AccessToken)
	assert.NotEmpty(t, authResp.RefreshToken)
}

func TestAuthUserInfo(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	reqBody := SignupRequest{
		Email:    "userinfo@example.com",
		Password: "password123",
	}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{
		Email:    "userinfo@example.com",
		Password: "password123",
	}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)

	req, _ := http.NewRequest("GET", authBaseURL+"/auth/api/v1/user_info", nil)
	req.Header.Set("Authorization", "Bearer "+authResp.AccessToken)

	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAuthHealth(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Get(authBaseURL + "/auth/api/v1/health")
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}
