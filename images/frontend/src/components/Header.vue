<script setup lang="ts">
  import { ref, onMounted, onUnmounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuth } from '../composables/useAuth'

  const router = useRouter()
  const { signOut } = useAuth()
  const isDropdownOpen = ref(false)
  const dropdownRef = ref<HTMLElement | null>(null)
  const avatarRef = ref<HTMLElement | null>(null)

  // Переключение дропдауна
  const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value
  }

  // Закрытие дропдауна
  const closeDropdown = () => {
    isDropdownOpen.value = false
  }

  // Обработка клика вне области
  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.value && 
      avatarRef.value &&
      !dropdownRef.value.contains(event.target as Node) &&
      !avatarRef.value.contains(event.target as Node)
    ) {
      closeDropdown()
    }
  }

  // Выход из аккаунта
  const handleLogout = async () => {
    const access_token = localStorage.getItem('access_token')
    if (!access_token) return
    
    await signOut(access_token)
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push({ name: 'signin' })
  }

  // Добавляем обработчик клика при монтировании
  onMounted(() => {
    document.addEventListener('click', handleClickOutside)
  })

  // Убираем обработчик при размонтировании
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
  })
</script>

<template>
  <header class="header">
    <div class="navbar">
      <h2 class="logo">PRACTIX</h2>
      
      <ul class="nav-links">
        <li><router-link to="/" class="nav-link">Home</router-link></li>
        <li><router-link to="/filmworks" class="nav-link">TV Shows</router-link></li>
        <li><router-link to="/filmworks" class="nav-link">Movies</router-link></li>
        <li><router-link to="/filmworks" class="nav-link">Latest</router-link></li>
        <li><router-link to="/bookmarks" class="nav-link">My List</router-link></li>
      </ul>

      <div class="nav-right">
        <form class="search-form">
          <input type="text" placeholder="Search..." class="search-input">
          <button type="submit" class="search-button">
            <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
            </svg>
          </button>
        </form>

        <div class="avatar-container">
          <div 
            ref="avatarRef"
            class="avatar" 
            @click="toggleDropdown"
          >
            <svg class="user-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
          </div>
          
          <div 
            v-if="isDropdownOpen" 
            ref="dropdownRef"
            class="dropdown-menu"
          >
            <router-link to="/settings" class="dropdown-item" @click="closeDropdown">Settings</router-link>
            <div class="dropdown-divider"></div>
            <button @click="handleLogout" class="dropdown-item logout">Log Out</button>
          </div>
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
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
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

  .search-form {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
  }

  .search-input {
    background: transparent;
    border: none;
    color: #fff;
    padding: 0.5rem 1rem;
    width: 200px;
    outline: none;
  }

  .search-input::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }

  .search-button {
    background: transparent;
    border: none;
    color: #fff;
    padding: 0.5rem;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .search-button:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .search-icon, .bell-icon, .user-icon {
    width: 20px;
    height: 20px;
  }

  .notification-icon {
    position: relative;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 50%;
    transition: background-color 0.3s ease;
  }

  .notification-icon:hover {
    background: rgba(255, 255, 255, 0.1);
  }

  .notification-dot {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 8px;
    height: 8px;
    background-color: #e50914;
    border-radius: 50%;
    border: 2px solid #000;
  }

  .avatar-container {
    position: relative;
  }

  .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.3);
    cursor: pointer;
  }

  .avatar:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
  }

  .avatar.active {
    background: rgba(255, 255, 255, 0.2);
    border-color: #e50914;
  }

  .dropdown-menu {
    position: absolute;
    top: 100%;
    right: 0;
    background: #fff;
    border-radius: 4px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
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

  /* Адаптивность */
  @media (max-width: 768px) {
    .navbar {
      padding: 1rem;
      flex-wrap: wrap;
    }
    
    .nav-links {
      gap: 1rem;
    }
    
    .search-input {
      width: 150px;
    }
  }

  @media (max-width: 480px) {
    .nav-links {
      display: none;
    }
    
    .search-form {
      display: none;
    }
  }
</style>
