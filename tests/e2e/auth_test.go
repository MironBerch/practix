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

func TestAuthLogout(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	email := "logout@example.com"
	password := "password123"
	reqBody := SignupRequest{Email: email, Password: password}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{Email: email, Password: password}
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

	req, _ := http.NewRequest("POST", authBaseURL+"/auth/api/v1/logout", nil)
	req.Header.Set("Authorization", "Bearer "+authResp.AccessToken)
	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAuthRefresh(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	email := "refresh@example.com"
	password := "password123"
	reqBody := SignupRequest{Email: email, Password: password}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{Email: email, Password: password}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)
	resp.Body.Close()

	req, _ := http.NewRequest("POST", authBaseURL+"/auth/api/v1/refresh", nil)
	req.Header.Set("Authorization", "Bearer "+authResp.RefreshToken)
	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAuthPasswordChange(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	email := "pwdchange@example.com"
	password := "password123"
	reqBody := SignupRequest{Email: email, Password: password}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{Email: email, Password: password}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)
	resp.Body.Close()

	type PasswordChangeRequest struct {
		OldPassword string `json:"old_password"`
		NewPassword string `json:"new_password"`
	}
	pwdReq := PasswordChangeRequest{OldPassword: password, NewPassword: "newpassword123"}
	jsonData, _ = json.Marshal(pwdReq)
	req, _ := http.NewRequest("POST", authBaseURL+"/auth/api/v1/password_change", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+authResp.AccessToken)
	req.Header.Set("Content-Type", "application/json")
	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAuthChangeEmail(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	email := "changeemail@example.com"
	password := "password123"
	reqBody := SignupRequest{Email: email, Password: password}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{Email: email, Password: password}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)
	resp.Body.Close()

	type ChangeEmailRequest struct {
		Email string `json:"email"`
	}
	emailReq := ChangeEmailRequest{Email: "newemail@example.com"}
	jsonData, _ = json.Marshal(emailReq)
	req, _ := http.NewRequest("POST", authBaseURL+"/auth/api/v1/change_email", bytes.NewBuffer(jsonData))
	req.Header.Set("Authorization", "Bearer "+authResp.AccessToken)
	req.Header.Set("Content-Type", "application/json")
	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}

func TestAuthUserSessions(t *testing.T) {
	client := &http.Client{Timeout: 10 * time.Second}

	email := "sessions@example.com"
	password := "password123"
	reqBody := SignupRequest{Email: email, Password: password}
	jsonData, _ := json.Marshal(reqBody)
	resp, err := client.Post(authBaseURL+"/auth/api/v1/signup", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	resp.Body.Close()

	signinReq := SigninRequest{Email: email, Password: password}
	jsonData, _ = json.Marshal(signinReq)
	resp, err = client.Post(authBaseURL+"/auth/api/v1/signin", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}

	var authResp AuthResponse
	body, _ := io.ReadAll(resp.Body)
	json.Unmarshal(body, &authResp)
	resp.Body.Close()

	req, _ := http.NewRequest("GET", authBaseURL+"/auth/api/v1/user_sessions", nil)
	req.Header.Set("Authorization", "Bearer "+authResp.AccessToken)
	resp, err = client.Do(req)
	if err != nil {
		t.Skipf("Service not available: %v", err)
		return
	}
	defer resp.Body.Close()

	assert.Equal(t, http.StatusOK, resp.StatusCode)
}
