<template>
  <div class="filmworks-page">
    <!-- Заголовок и управление -->
    <div class="page-header">
      <h1>Фильмы</h1>
      <div class="controls">
        <div class="search-control">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск фильмов..."
            @input="handleSearch"
            class="search-input"
          />
        </div>
        <div class="sort-control">
          <select
            v-model="sortBy"
            @change="handleSortChange"
            class="sort-select"
          >
            <option value="">Без сортировки</option>
            <option value="rating">По рейтингу</option>
            <option value="title">По названию</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Фильтры по жанрам в аккордеоне -->
    <div class="filters-accordion">
      <div class="accordion-header" @click="toggleFilters">
        <div class="accordion-title">
          <h3>Фильтры по жанрам</h3>
          <span class="selected-count" v-if="selectedGenres.length > 0">
            ({{ selectedGenres.length }} выбрано)
          </span>
        </div>
        <div class="accordion-arrow" :class="{ 'accordion-arrow--open': showFilters }">
          ▼
        </div>
      </div>
      
      <transition name="filters-slide">
        <div v-if="showFilters" class="filters-section">
          <div class="genres-filter">
            <div
              v-for="genre in availableGenres"
              :key="genre.uuid"
              class="genre-checkbox"
            >
              <input
                type="checkbox"
                :id="`genre-${genre.uuid}`"
                :value="genre.name"
                v-model="selectedGenres"
                @change="handleGenreChange"
                class="genre-input"
              />
              <label :for="`genre-${genre.uuid}`" class="genre-label">
                {{ genre.name }}
              </label>
            </div>
          </div>
          <div class="filters-actions" v-if="selectedGenres.length > 0">
            <button @click="clearGenres" class="clear-filters-button">
              Очистить все
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="loading-state">
      <p>Загрузка фильмов...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-if="error" class="error-state">
      <p>Ошибка: {{ error }}</p>
      <button @click="refreshData" class="retry-button">
        Попробовать снова
      </button>
    </div>

    <!-- Результаты поиска -->
    <div v-if="isSearchMode && filmworks.length > 0" class="search-info">
      <h2>Результаты поиска для "{{ searchQuery }}"</h2>
      <button @click="clearSearch" class="clear-search-button">
        Показать все фильмы
      </button>
    </div>

    <!-- Выбранные жанры -->
    <div v-if="selectedGenres.length > 0" class="active-filters">
      <span class="active-filters-label">Выбранные жанры:</span>
      <span
        v-for="genre in selectedGenres"
        :key="genre"
        class="active-filter-tag"
      >
        {{ genre }}
        <button @click="removeGenre(genre)" class="remove-genre-button">
          ×
        </button>
      </span>
    </div>

    <!-- Список фильмов -->
    <div v-if="!loading && !error" class="filmworks-grid">
      <div
        v-for="filmwork in filmworks"
        :key="filmwork.uuid"
        class="filmwork-card"
        @click="navigateToFilmwork(filmwork.uuid)"
      >
        <div class="filmwork-poster">
          <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
        </div>
        <div class="filmwork-info">
          <h3 class="filmwork-title">{{ filmwork.title }}</h3>
          <div class="filmwork-rating">
            <span class="rating-star">⭐</span>
            <span class="rating-value">{{ filmwork.rating?.toFixed(1) || '0.0' }}</span>
          </div>
          <div v-if="filmwork.genres && filmwork.genres.length > 0" class="filmwork-genres">
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
        </div>
      </div>
    </div>

    <!-- Сообщение о пустом состоянии -->
    <div
      v-if="!loading && !error && filmworks.length === 0"
      class="empty-state"
    >
      <p v-if="isSearchMode">По вашему запросу ничего не найдено</p>
      <p v-else-if="selectedGenres.length > 0">По выбранным жанрам ничего не найдено</p>
      <p v-else>Нет доступных фильмов</p>
    </div>

    <!-- Пагинация -->
    <div v-if="!loading && !error && filmworks.length > 0" class="pagination">
      <button
        :disabled="currentPage === 1"
        @click="previousPage"
        class="pagination-button"
      >
        Назад
      </button>
      <span class="pagination-info">Страница {{ currentPage }}</span>
      <button @click="nextPage" class="pagination-button">Вперед</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useMovies } from "../../composables/useMovies";
import type { BaseFilmwork, Genre } from "../../types/types";

const router = useRouter();
const { loading, error, getFilmworks, searchFilmworks, getGenres } = useMovies();

// Реактивные данные
const filmworks = ref<BaseFilmwork[]>([]);
const availableGenres = ref<Genre[]>([]);
const selectedGenres = ref<string[]>([]);
const searchQuery = ref("");
const sortBy = ref("");
const currentPage = ref(1);
const pageSize = ref(20);
const isSearchMode = ref(false);
const showFilters = ref(false);

// Загрузка данных
const loadFilmworks = async () => {
  if (isSearchMode.value && searchQuery.value.trim()) {
    const result = await searchFilmworks(
      searchQuery.value,
      currentPage.value,
      pageSize.value,
      selectedGenres.value
    );
    filmworks.value = Array.isArray(result) ? result.flat() : [];
  } else {
    const result = await getFilmworks(
      sortBy.value,
      currentPage.value,
      pageSize.value,
      selectedGenres.value
    );
    filmworks.value = Array.isArray(result) ? result.flat() : [];
  }
};

// Загрузка жанров
const loadGenres = async () => {
  const result = await getGenres();
  if (result) {
    availableGenres.value = Array.isArray(result) ? result.flat() : [];
  }
};

// Переключение видимости фильтров
const toggleFilters = () => {
  showFilters.value = !showFilters.value;
};

// Обработчики событий
const handleSearch = () => {
  isSearchMode.value = searchQuery.value.trim().length > 0;
  currentPage.value = 1;
  loadFilmworks();
};

const handleSortChange = () => {
  currentPage.value = 1;
  loadFilmworks();
};

const handleGenreChange = () => {
  currentPage.value = 1;
  loadFilmworks();
};

const removeGenre = (genre: string) => {
  selectedGenres.value = selectedGenres.value.filter(g => g !== genre);
  currentPage.value = 1;
  loadFilmworks();
};

const clearGenres = () => {
  selectedGenres.value = [];
  currentPage.value = 1;
  loadFilmworks();
};

const clearSearch = () => {
  searchQuery.value = "";
  isSearchMode.value = false;
  currentPage.value = 1;
  loadFilmworks();
};

const navigateToFilmwork = (uuid: string) => {
  router.push(`/filmworks/${uuid}`);
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadFilmworks();
  }
};

const nextPage = () => {
  currentPage.value++;
  loadFilmworks();
};

const refreshData = () => {
  loadFilmworks();
};

// Загрузка при монтировании
onMounted(() => {
  loadFilmworks();
  loadGenres();
});

// Наблюдатель для пагинации
watch([currentPage], () => {
  loadFilmworks();
});
</script>

<style scoped>
@import '../../styles/pages/filmworks/filmworks.css';
</style>
