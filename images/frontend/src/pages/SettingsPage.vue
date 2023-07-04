<template>
    <div class="settings-page">
        <div class="settings-header">
            <h1>Настройки аккаунта</h1>
            <p>Управление вашими персональными данными и настройками безопасности</p>
        </div>

        <div class="settings-content">
            <!-- Безопасность -->
            <div class="settings-section">
                <h2>Безопасность</h2>
                <div class="settings-cards">
                    <router-link to="/change-email" class="settings-card">
                        <div class="card-icon">📧</div>
                        <div class="card-content">
                            <h3>Изменить email</h3>
                            <p>Обновите ваш адрес электронной почты</p>
                        </div>
                        <div class="card-arrow">→</div>
                    </router-link>

                    <router-link to="/change-password" class="settings-card">
                        <div class="card-icon">🔒</div>
                        <div class="card-content">
                            <h3>Изменить пароль</h3>
                            <p>Установите новый пароль для вашего аккаунта</p>
                        </div>
                        <div class="card-arrow">→</div>
                    </router-link>

                    <router-link to="/sessions" class="settings-card">
                        <div class="card-icon">💻</div>
                        <div class="card-content">
                            <h3>Активные сессии</h3>
                            <p>Просмотр и управление устройствами, на которых выполнен вход</p>
                        </div>
                        <div class="card-arrow">→</div>
                    </router-link>
                </div>
            </div>

            <!-- Действия -->
            <div class="settings-section">
                <h2>Действия</h2>
                <div class="settings-cards">
                    <button 
                        @click="handleSignOut"
                        :disabled="signOutLoading"
                        class="settings-card danger"
                    >
                        <div class="card-icon">🚪</div>
                        <div class="card-content">
                            <h3>Выйти из аккаунта</h3>
                            <p>Завершите текущую сессию на этом устройстве</p>
                        </div>
                        <div class="card-arrow">
                            <span v-if="signOutLoading">...</span>
                            <span v-else>→</span>
                        </div>
                    </button>
                </div>
            </div>

            <!-- Информация о пользователе -->
            <div class="settings-section">
                <h2>Информация об аккаунте</h2>
                <div v-if="userInfoLoading" class="loading-info">
                    <p>Загрузка информации...</p>
                </div>
                <div v-else-if="userInfo" class="account-info">
                    <div class="info-item">
                        <span class="info-label">ID пользователя:</span>
                        <span class="info-value">{{ userInfo.user_id }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Email:</span>
                        <span class="info-value">{{ userInfo.user_email }}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Дата регистрации:</span>
                        <span class="info-value">{{ userInfo.user_created_at }}</span>
                    </div>
                </div>
                <div v-else class="error-info">
                    <p>Не удалось загрузить информацию о пользователе</p>
                    <button @click="loadUserInfo" class="retry-button">Попробовать снова</button>
                </div>
            </div>
        </div>

        <!-- Уведомления -->
        <div v-if="message" :class="['message', messageType]">
            {{ message }}
        </div>
    </div>
</template>

<script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import { useAuth } from '../composables/useAuth'
    import type { User } from '../types/types'

    const router = useRouter()
    const { signOut, getUserInfo, loading } = useAuth()

    const userInfo = ref<User | null>(null)
    const userInfoLoading = ref(false)
    const signOutLoading = ref(false)
    const message = ref('')
    const messageType = ref<'success' | 'error'>('success')

    // Загрузка информации о пользователе
    const loadUserInfo = async () => {
        const token = localStorage.getItem('access_token')
        if (!token) {
            router.push('/auth/signin')
            return
        }

        userInfoLoading.value = true
        try {
            const userData = await getUserInfo(token)
            if (userData) {
                userInfo.value = userData
                // Сохраняем email в localStorage для использования в других компонентах
                localStorage.setItem('user_email', userData.user_email)
            }
        } catch (err) {
            console.error('Error loading user info:', err)
            showMessage('Ошибка при загрузке информации о пользователе', 'error')
        } finally {
            userInfoLoading.value = false
        }
    }

    // Выход из аккаунта
    const handleSignOut = async () => {
        const token = localStorage.getItem('access_token')
        if (!token) {
            router.push('/auth/signin')
            return
        }

        signOutLoading.value = true
        try {
            await signOut(token)
            
            // Очищаем localStorage
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user_email')
            
            // Перенаправляем на страницу входа
            router.push('/auth/signin')
        } catch (err) {
            console.error('Error during sign out:', err)
            showMessage('Ошибка при выходе из аккаунта', 'error')
        } finally {
            signOutLoading.value = false
        }
    }

    const showMessage = (text: string, type: 'success' | 'error' = 'success') => {
        message.value = text
        messageType.value = type
        setTimeout(() => {
            message.value = ''
        }, 3000)
    }

    // Загрузка данных при монтировании
    onMounted(() => {
        loadUserInfo()
    })
</script>

<style scoped>
    .settings-page {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }

    .settings-header {
        text-align: center;
        margin-bottom: 40px;
    }

    .settings-header h1 {
        margin: 0 0 10px 0;
        color: #333;
        font-size: 2.5em;
    }

    .settings-header p {
        margin: 0;
        color: #666;
        font-size: 1.1em;
    }

    .settings-content {
        display: flex;
        flex-direction: column;
        gap: 40px;
    }

    .settings-section h2 {
        margin: 0 0 20px 0;
        color: #333;
        font-size: 1.5em;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
    }

    .settings-cards {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .settings-card {
        display: flex;
        align-items: center;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 12px;
        padding: 20px;
        text-decoration: none;
        color: inherit;
        transition: all 0.3s ease;
        cursor: pointer;
        gap: 15px;
    }

    .settings-card:hover {
        border-color: #3498db;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.1);
        transform: translateY(-2px);
        text-decoration: none;
        color: inherit;
    }

    .settings-card.danger:hover {
        border-color: #e74c3c;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.1);
    }

    .settings-card:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
    }

    .settings-card:disabled:hover {
        border-color: #e0e0e0;
        box-shadow: none;
        transform: none;
    }

    .card-icon {
        font-size: 24px;
        width: 50px;
        height: 50px;
        background: #f8f9fa;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    .card-content {
        flex: 1;
    }

    .card-content h3 {
        margin: 0 0 5px 0;
        color: #333;
        font-size: 1.2em;
        font-weight: 600;
    }

    .card-content p {
        margin: 0;
        color: #666;
        font-size: 0.95em;
        line-height: 1.4;
    }

    .card-arrow {
        color: #999;
        font-size: 1.2em;
        font-weight: bold;
    }

    .account-info {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 25px;
    }

    .info-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #e9ecef;
    }

    .info-item:last-child {
        border-bottom: none;
    }

    .info-label {
        font-weight: 600;
        color: #333;
    }

    .info-value {
        color: #666;
        font-family: 'Courier New', monospace;
        word-break: break-all;
    }

    .loading-info {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 40px;
        text-align: center;
        color: #666;
    }

    .error-info {
        background: #fdf2f2;
        border: 1px solid #f5c6cb;
        border-radius: 12px;
        padding: 30px;
        text-align: center;
        color: #721c24;
    }

    .error-info p {
        margin: 0 0 15px 0;
    }

    .retry-button {
        background: #3498db;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }

    .retry-button:hover {
        background: #2980b9;
    }

    .message {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 8px;
        color: white;
        font-weight: 600;
        z-index: 1000;
        max-width: 300px;
    }

    .message.success {
        background: #27ae60;
    }

    .message.error {
        background: #e74c3c;
    }

    @media (max-width: 768px) {
        .settings-page {
            padding: 15px;
        }

        .settings-header h1 {
            font-size: 2em;
        }

        .settings-card {
            padding: 15px;
        }

        .card-icon {
            width: 40px;
            height: 40px;
            font-size: 20px;
        }

        .info-item {
            flex-direction: column;
            align-items: flex-start;
            gap: 5px;
        }

        .info-value {
            word-break: break-all;
        }
    }

    @media (max-width: 480px) {
        .settings-header h1 {
            font-size: 1.8em;
        }

        .settings-card {
            flex-direction: column;
            text-align: center;
            gap: 12px;
        }

        .card-content h3 {
            font-size: 1.1em;
        }
    }
</style>
