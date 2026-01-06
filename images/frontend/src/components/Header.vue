<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../composables/useAuth";

const router = useRouter();
const { signOut } = useAuth();
const isDropdownOpen = ref(false);
const dropdownRef = ref<HTMLElement | null>(null);
const avatarRef = ref<HTMLElement | null>(null);

// Проверяем авторизацию пользователя
const isAuthenticated = computed(() => {
  return !!localStorage.getItem("access_token");
});

// Переключение дропдауна
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

// Закрытие дропдауна
const closeDropdown = () => {
  isDropdownOpen.value = false;
};

// Обработка клика вне области
const handleClickOutside = (event: MouseEvent) => {
  if (
    dropdownRef.value &&
    avatarRef.value &&
    !dropdownRef.value.contains(event.target as Node) &&
    !avatarRef.value.contains(event.target as Node)
  ) {
    closeDropdown();
  }
};

// Выход из аккаунта
const handleLogout = async () => {
  const access_token = localStorage.getItem("access_token");
  if (!access_token) return;

  await signOut(access_token);
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push({ name: "signin" });
};

// Добавляем обработчик клика при монтировании
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

// Убираем обработчик при размонтировании
onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>

<template>
  <header class="header">
    <div class="navbar">
      <h2 class="logo">PRACTIX</h2>

      <ul class="nav-links">
        <li>
          <router-link to="/filmworks" class="nav-link">Movies</router-link>
        </li>
        <li>
          <router-link to="/persons" class="nav-link">Persons</router-link>
        </li>
        <li>
          <router-link to="/bookmarks" class="nav-link">My List</router-link>
        </li>
      </ul>

      <div class="nav-right">
        <!-- Для авторизованных пользователей - аватарка и dropdown -->
        <div v-if="isAuthenticated" class="avatar-container">
          <div ref="avatarRef" class="avatar" @click="toggleDropdown">
            <svg
              class="user-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
          </div>

          <div v-if="isDropdownOpen" ref="dropdownRef" class="dropdown-menu">
            <router-link
              to="/settings"
              class="dropdown-item"
              @click="closeDropdown"
              >Settings</router-link
            >
            <div class="dropdown-divider"></div>
            <button @click="handleLogout" class="dropdown-item logout">
              Log Out
            </button>
          </div>
        </div>

        <!-- Для неавторизованных пользователей - ссылки на вход и регистрацию -->
        <div v-else class="auth-links">
          <router-link :to="{ name: 'signin' }" class="auth-link signin">
            Войти
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
@import url('../styles/components/header.css');
</style>
