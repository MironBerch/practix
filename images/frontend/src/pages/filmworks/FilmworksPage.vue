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
              :key="genre.id"
              class="genre-checkbox"
            >
              <input
                type="checkbox"
                :id="`genre-${genre.id}`"
                :value="genre.name"
                v-model="selectedGenres"
                @change="handleGenreChange"
                class="genre-input"
              />
              <label :for="`genre-${genre.id}`" class="genre-label">
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

    <LoadingSpinner v-if="loading" message="Загрузка фильмов..." />

    <ErrorMessage v-if="error" :message="error" @retry="refreshData" />

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
      <FilmworkCard
        v-for="filmwork in filmworks"
        :key="filmwork.id"
        :id="filmwork.id"
        :title="filmwork.title"
        :rating="filmwork.rating"
        :genres="filmwork.genres"
        @click="navigateToFilmwork"
      />
    </div>

    <EmptyState
      v-if="!loading && !error && filmworks.length === 0"
      :message="emptyMessage"
    />

    <Pagination
      v-if="!loading && !error && filmworks.length > 0"
      :current-page="currentPage"
      @previous="previousPage"
      @next="nextPage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useMovies } from "../../composables/useMovies";
import FilmworkCard from "../../components/ui/FilmworkCard.vue";
import SearchInput from "../../components/ui/SearchInput.vue";
import Pagination from "../../components/ui/Pagination.vue";
import LoadingSpinner from "../../components/ui/LoadingSpinner.vue";
import ErrorMessage from "../../components/ui/ErrorMessage.vue";
import EmptyState from "../../components/ui/EmptyState.vue";
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

const navigateToFilmwork = (id: string) => {
  router.push(`/filmworks/${id}`);
};

const emptyMessage = computed(() => {
  if (isSearchMode.value) return "По вашему запросу ничего не найдено";
  if (selectedGenres.value.length > 0) return "По выбранным жанрам ничего не найдено";
  return "Нет доступных фильмов";
});

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
@import url('../../styles/pages/filmworks/filmworks.css');
</style>
