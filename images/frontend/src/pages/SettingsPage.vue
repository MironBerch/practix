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
              <p>
                Просмотр и управление устройствами, на которых выполнен вход
              </p>
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
          <button @click="loadUserInfo" class="retry-button">
            Попробовать снова
          </button>
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
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";
import type { User } from "../types/types";

const router = useRouter();
const { signOut, getUserInfo } = useAuth();

const userInfo = ref<User | null>(null);
const userInfoLoading = ref(false);
const signOutLoading = ref(false);
const message = ref("");
const messageType = ref<"success" | "error">("success");

// Загрузка информации о пользователе
const loadUserInfo = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    router.push("/auth/signin");
    return;
  }

  userInfoLoading.value = true;
  try {
    const userData = await getUserInfo(token);
    if (userData) {
      userInfo.value = userData;
      // Сохраняем email в localStorage для использования в других компонентах
      localStorage.setItem("user_email", userData.user_email);
    }
  } catch (err) {
    console.error("Error loading user info:", err);
    showMessage("Ошибка при загрузке информации о пользователе", "error");
  } finally {
    userInfoLoading.value = false;
  }
};

// Выход из аккаунта
const handleSignOut = async () => {
  const token = localStorage.getItem("access_token");
  if (!token) {
    router.push("/auth/signin");
    return;
  }

  signOutLoading.value = true;
  try {
    await signOut(token);

    // Очищаем localStorage
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_email");

    // Перенаправляем на страницу входа
    router.push("/auth/signin");
  } catch (err) {
    console.error("Error during sign out:", err);
    showMessage("Ошибка при выходе из аккаунта", "error");
  } finally {
    signOutLoading.value = false;
  }
};

const showMessage = (text: string, type: "success" | "error" = "success") => {
  message.value = text;
  messageType.value = type;
  setTimeout(() => {
    message.value = "";
  }, 3000);
};

// Загрузка данных при монтировании
onMounted(() => {
  loadUserInfo();
});
</script>

<style scoped>
@import url('../styles/pages/settings.css');
</style>
