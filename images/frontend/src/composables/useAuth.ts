import { ref } from "vue";
import type {
  SignInRequest,
  SignInResponse,
  ResendEmailResponse,
  SignUpRequest,
  MessageResponse,
  RefreshResponse,
  ChangeEmailRequest,
  UserSessionCollection,
  ChangePasswordRequest,
  User,
} from "../types/types";

const BASE_AUTH_API_URL = import.meta.env.VITE_AUTH_API_URL;
const API_URL = BASE_AUTH_API_URL + "/auth/api/v1";

export const useAuth = () => {
  const loading = ref(false);

  const error = ref<string | null>(null);

  const signUp = async (
    data: SignUpRequest,
  ): Promise<SignInResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to register");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const signIn = async (
    data: SignInRequest,
  ): Promise<SignInResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/signin`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed to login");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const signOut = async (
    access_token: string,
  ): Promise<ResendEmailResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed signout");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const refresh = async (
    refresh_token: string,
  ): Promise<RefreshResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/refresh`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${refresh_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed signout");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const changeEmail = async (
    data: ChangeEmailRequest,
    access_token: string,
  ): Promise<MessageResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/change_email`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed signout");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const passwordChange = async (
    data: ChangePasswordRequest,
    access_token: string,
  ): Promise<MessageResponse | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/password_change`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error("Failed signout");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getUserSessions = async (
    access_token: string,
  ): Promise<UserSessionCollection[] | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/user_sessions`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch pastes");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  const getUserInfo = async (access_token: string): Promise<User | null> => {
    try {
      loading.value = true;
      const response = await fetch(`${API_URL}/user_info`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${access_token}`,
        },
      });
      console.log(`Bearer ${access_token}`);

      if (!response.ok) {
        throw new Error("Failed to get user info");
      }

      return await response.json();
    } catch (err) {
      error.value = err instanceof Error ? err.message : "Unknown error";
      return null;
    } finally {
      loading.value = false;
    }
  };

  return {
    loading,
    error,
    signUp,
    signIn,
    signOut,
    refresh,
    changeEmail,
    passwordChange,
    getUserSessions,
    getUserInfo,
  };
};
