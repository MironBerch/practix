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
        <li><router-link to="/" class="nav-link">Home</router-link></li>
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
.header {
  width: 100%;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #000;
  color: #fff;
  padding: 1rem 2rem;
  position: relative;
  box-shadow: 0 2px 10px rgb(0 0 0 / 30%);
}

.logo {
  color: #fff;
  font-size: 1.8rem;
  font-weight: bold;
  margin: 0;
}

.nav-links {
  display: flex;
  list-style: none;
  align-items: center;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
  padding: 0.5rem 0;
}

.nav-link:hover {
  color: #e50914;
}

.nav-link.router-link-active {
  color: #e50914;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-icon {
  width: 20px;
  height: 20px;
}

.avatar-container {
  position: relative;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgb(255 255 255 / 10%);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  border: 2px solid rgb(255 255 255 / 30%);
  cursor: pointer;
}

.avatar:hover {
  background: rgb(255 255 255 / 20%);
  border-color: rgb(255 255 255 / 50%);
}

.avatar.active {
  background: rgb(255 255 255 / 20%);
  border-color: #e50914;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 4px 20px rgb(0 0 0 / 30%);
  min-width: 180px;
  z-index: 1000;
  margin-top: 0.5rem;
  overflow: hidden;
  animation: dropdownFadeIn 0.2s ease-out;
}

@keyframes dropdownFadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dropdown-item {
  display: block;
  padding: 0.75rem 1rem;
  color: #000;
  text-decoration: none;
  transition: background-color 0.3s ease;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  font-size: 0.9rem;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f5f5f5;
}

.dropdown-divider {
  height: 1px;
  background: #e0e0e0;
  margin: 0.25rem 0;
}

.logout {
  color: #e50914;
  font-weight: 500;
}

/* Стили для ссылок авторизации */
.auth-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.auth-link {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.auth-link.signin {
  background: transparent;
  border: 1px solid rgb(255 255 255 / 30%);
}

.auth-link.signin:hover {
  background: rgb(255 255 255 / 10%);
  border-color: rgb(255 255 255 / 50%);
}

/* Адаптивность */
@media (width <= 768px) {
  .navbar {
    padding: 1rem;
    flex-wrap: wrap;
  }

  .nav-links {
    gap: 1rem;
  }

  .auth-links {
    gap: 0.5rem;
  }

  .auth-link {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}

@media (width <= 480px) {
  .nav-links {
    display: none;
  }

  .auth-links {
    flex-direction: column;
    gap: 0.5rem;
  }

  .auth-link {
    text-align: center;
    padding: 0.5rem;
    font-size: 0.8rem;
  }
}
</style>
