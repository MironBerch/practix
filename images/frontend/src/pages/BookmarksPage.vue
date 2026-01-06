<template>
  <div class="bookmarks-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1>Мои закладки</h1>
      <p v-if="bookmarksCount > 0">Найдено фильмов: {{ bookmarksCount }}</p>
      <p v-else>У вас пока нет фильмов в закладках</p>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="loading-state">
      <p>Загрузка закладок...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-if="error" class="error-state">
      <p>Ошибка: {{ error }}</p>
      <button @click="loadBookmarks" class="retry-button">
        Попробовать снова
      </button>
    </div>

    <!-- Сообщение о необходимости авторизации -->
    <div v-if="!isAuthenticated" class="auth-required">
      <h2>Для просмотра закладок необходимо авторизоваться</h2>
      <router-link to="/signin" class="auth-link">Войти в аккаунт</router-link>
    </div>

    <!-- Список фильмов в закладках -->
    <div
      v-if="isAuthenticated && !loading && !error && bookmarksCount > 0"
      class="bookmarks-grid"
    >
      <router-link
        v-for="filmwork in bookmarkedFilmworks"
        :key="filmwork.uuid"
        :to="`/filmworks/${filmwork.uuid}`"
        class="filmwork-card"
      >
        <div class="filmwork-poster">
          <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
          <div class="bookmark-indicator">★</div>
        </div>
        <div class="filmwork-info">
          <h3 class="filmwork-title">{{ filmwork.title }}</h3>
          <div class="filmwork-rating">
            <span class="rating-star">⭐</span>
            <span class="rating-value">{{
              filmwork.rating?.toFixed(1) || "0.0"
            }}</span>
          </div>
          <div
            v-if="filmwork.genres && filmwork.genres.length > 0"
            class="filmwork-genres"
          >
            <span
              v-for="genre in filmwork.genres.slice(0, 2)"
              :key="genre"
              class="genre-tag"
            >
              {{ genre }}
            </span>
            <span v-if="filmwork.genres.length > 2" class="genre-more">
              +{{ filmwork.genres.length - 2 }}
            </span>
          </div>
          <button
            @click.prevent="removeFromBookmarks(filmwork.uuid)"
            class="remove-bookmark-btn"
          >
            Удалить из закладок
          </button>
        </div>
      </router-link>
    </div>

    <!-- Сообщение о пустых закладках -->
    <div
      v-if="isAuthenticated && !loading && !error && bookmarksCount === 0"
      class="empty-bookmarks"
    >
      <div class="empty-state">
        <h2>Закладок пока нет</h2>
        <p>Добавляйте фильмы в закладки, чтобы легко находить их позже</p>
        <router-link to="/filmworks" class="explore-link"
          >Найти фильмы</router-link
        >
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useMovies } from "../composables/useMovies";
import { useUGC } from "../composables/useUGC";
import type { BaseFilmwork, FilmworkBookmark } from "../types/types";

const { getFilmwork, loading: moviesLoading } = useMovies();
const {
  getBookmarks,
  removeFilmworkFromBookmarks,
  loading: ugcLoading,
  error,
} = useUGC();

// Реактивные данные
const bookmarks = ref<FilmworkBookmark[]>([]);
const bookmarkedFilmworks = ref<BaseFilmwork[]>([]);
const removalLoading = ref<string | null>(null);

// Проверка аутентификации
const isAuthenticated = computed(() => {
  return !!localStorage.getItem("access_token");
});

// Количество закладок
const bookmarksCount = computed(() => bookmarkedFilmworks.value.length);

// Состояние загрузки
const loading = computed(() => moviesLoading.value || ugcLoading.value);

// Загрузка закладок
const loadBookmarks = async () => {
  if (!isAuthenticated.value) return;

  const token = localStorage.getItem("access_token");
  if (!token) return;

  try {
    const bookmarksData = await getBookmarks(token);
    if (bookmarksData && Array.isArray(bookmarksData)) {
      bookmarks.value = bookmarksData.flat() as FilmworkBookmark[];
      await loadBookmarkedFilmworks();
    } else {
      bookmarks.value = [];
      bookmarkedFilmworks.value = [];
    }
  } catch (err) {
    console.error("Error loading bookmarks:", err);
    bookmarks.value = [];
    bookmarkedFilmworks.value = [];
  }
};

// Загрузка информации о фильмах в закладках
const loadBookmarkedFilmworks = async () => {
  bookmarkedFilmworks.value = [];

  for (const bookmark of bookmarks.value) {
    try {
      const filmwork = await getFilmwork(bookmark.filmwork_id);
      if (filmwork) {
        bookmarkedFilmworks.value.push(filmwork);
      }
    } catch (err) {
      console.error(`Error loading filmwork ${bookmark.filmwork_id}:`, err);
    }
  }
};

// Удаление из закладок
const removeFromBookmarks = async (filmworkUuid: string) => {
  if (!isAuthenticated.value) return;

  const token = localStorage.getItem("access_token");
  if (!token) return;

  removalLoading.value = filmworkUuid;

  try {
    await removeFilmworkFromBookmarks(filmworkUuid, token);

    // Удаляем фильм из локального списка
    bookmarkedFilmworks.value = bookmarkedFilmworks.value.filter(
      (filmwork) => filmwork.uuid !== filmworkUuid,
    );

    // Обновляем список закладок
    bookmarks.value = bookmarks.value.filter(
      (bookmark) => bookmark.filmwork_id !== filmworkUuid,
    );
  } catch (err) {
    console.error("Error removing bookmark:", err);
  } finally {
    removalLoading.value = null;
  }
};

// Загрузка при монтировании
onMounted(() => {
  if (isAuthenticated.value) {
    loadBookmarks();
  }
});
</script>

<style scoped>
@import url('../styles/pages/bookmarks.css');
</style>
