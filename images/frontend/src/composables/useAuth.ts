import { ref } from 'vue';
import type { SignInRequest, SignInResponse, Confirm2StepVerificationRequest, Confirm2StepVerificationResponse, ResendEmailResponse, SignUpRequest, MessageResponse, RefreshResponse, ChangeEmailRequest, UserSessionCollection, ChangePasswordRequest } from '../types/types';

const BASE_AUTH_API_URL = import.meta.env.BASE_AUTH_API_URL;
const API_URL = BASE_AUTH_API_URL + '/auth/api/v1';

export const useAuth = () => {
    const loading = ref(false);

    const error = ref<string | null>(null);

    const signUp = async (data: SignUpRequest): Promise<SignInResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/signup`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed to register');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const signIn = async (data: SignInRequest): Promise<SignInResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/signin`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed to login');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const confirmRegistration = async (data: Confirm2StepVerificationRequest, temp_token: string): Promise<Confirm2StepVerificationResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/confirm_registration`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${temp_token}`,
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed confirm registration');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const confirm2StepVerification = async (data: Confirm2StepVerificationRequest, temp_token: string): Promise<Confirm2StepVerificationResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/confirm_2_step_verification`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${temp_token}`,
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed confirm 2 step verification');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const resendConfirmRegistrationEmail = async (temp_token: string): Promise<ResendEmailResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/resend_confirm_registration_email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${temp_token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error('Failed resend email');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const resend2StepVerificationEmail = async (temp_token: string): Promise<ResendEmailResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/resend_2_step_verification_email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${temp_token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error('Failed resend email');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const signOut = async (access_token: string): Promise<ResendEmailResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/logout`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error('Failed signout');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const refresh = async (refresh_token: string): Promise<RefreshResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/refresh`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${refresh_token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error('Failed signout');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const changeEmail = async (data: ChangeEmailRequest, access_token: string): Promise<MessageResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/change_email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed signout');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const resendChangeEmail = async (temp_token: string): Promise<MessageResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/resend_change_email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${temp_token}`,
                    },
                },
            );

            if (!response.ok) {
                throw new Error('Failed resend email');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const confirmChangeEmail = async (data: Confirm2StepVerificationRequest, access_token: string): Promise<MessageResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/confirm_change_email`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed signout');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const passwordChange = async (data: ChangePasswordRequest, access_token: string): Promise<MessageResponse | null> => {
        try {
            loading.value = true;
            const response = await fetch(
                `${API_URL}/password_change`,
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${access_token}`,
                    },
                    body: JSON.stringify(data),
                },
            );

            if (!response.ok) {
                throw new Error('Failed signout');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
            return null;
        } finally {
            loading.value = false;
        }
    }

    const getUserSessions = async (): Promise<UserSessionCollection[] | null> => {
        try {
            loading.value = true;
            const response = await fetch(`${API_URL}/user_sessions`);

            if (!response.ok) {
                throw new Error('Failed to fetch pastes');
            }

            return await response.json();
        } catch (err) {
            error.value = err instanceof Error ? err.message : 'Unknown error';
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
        confirmRegistration,
        confirm2StepVerification,
        resendConfirmRegistrationEmail,
        resend2StepVerificationEmail,
        signOut,
        refresh,
        changeEmail,
        resendChangeEmail,
        confirmChangeEmail,
        passwordChange,
        getUserSessions,
    };
};
