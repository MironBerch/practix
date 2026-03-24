<template>
  <div class="bookmarks-page">
    <!-- Заголовок -->
    <div class="page-header">
      <h1>Мои закладки</h1>
      <p v-if="bookmarksCount > 0">Найдено фильмов: {{ bookmarksCount }}</p>
      <p v-else>У вас пока нет фильмов в закладках</p>
    </div>

    <!-- Состояние загрузки -->
    <LoadingSpinner v-if="loading" message="Загрузка закладок..." />

    <!-- Сообщение об ошибке -->
    <ErrorMessage v-if="error" :message="error" @retry="loadBookmarks" />

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
      <FilmworkCard
        v-for="filmwork in bookmarkedFilmworks"
        :key="filmwork.id"
        :id="filmwork.id"
        :title="filmwork.title"
        :rating="filmwork.rating"
        :genres="filmwork.genres"
        :show-bookmark-indicator="true"
        @click="(id) => $router.push(`/filmworks/${id}`)"
      >
        <template #actions>
          <button
            @click.stop.prevent="removeFromBookmarks(filmwork.id)"
            class="remove-bookmark-btn"
          >
            Удалить из закладок
          </button>
        </template>
      </FilmworkCard>
    </div>

    <!-- Сообщение о пустых закладках -->
    <EmptyState
      v-if="isAuthenticated && !loading && !error && bookmarksCount === 0"
      message="Закладок пока нет"
    >
      <template #action>
        <router-link to="/filmworks" class="explore-link"
          >Найти фильмы</router-link
        >
      </template>
    </EmptyState>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useMovies } from "../composables/useMovies";
import { useUGC } from "../composables/useUGC";
import FilmworkCard from "../components/ui/FilmworkCard.vue";
import LoadingSpinner from "../components/ui/LoadingSpinner.vue";
import ErrorMessage from "../components/ui/ErrorMessage.vue";
import EmptyState from "../components/ui/EmptyState.vue";
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
      (filmwork) => filmwork.id !== filmworkUuid,
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
