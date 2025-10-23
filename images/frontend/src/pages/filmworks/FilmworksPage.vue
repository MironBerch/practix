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

    <!-- Список фильмов -->
    <div v-if="!loading && !error" class="filmworks-grid">
      <div
        v-for="filmwork in filmworks"
        :key="filmwork.uuid"
        class="filmwork-card"
        @click="navigateToFilmwork(filmwork.uuid)"
      >
        <div class="filmwork-poster">
          <!-- Здесь может быть постер фильма -->
          <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
        </div>
        <div class="filmwork-info">
          <h3 class="filmwork-title">{{ filmwork.title }}</h3>
          <div class="filmwork-rating">
            <span class="rating-star">⭐</span>
            <span class="rating-value">{{ filmwork.rating.toFixed(1) }}</span>
          </div>
          <div v-if="filmwork.genres" class="filmwork-genres">
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
import type { BaseFilmwork } from "../../types/types";

const router = useRouter();
const { loading, error, getFilmworks, searchFilmworks } = useMovies();

// Реактивные данные
const filmworks = ref<BaseFilmwork[]>([]);
const searchQuery = ref("");
const sortBy = ref("");
const currentPage = ref(1);
const pageSize = ref(20);
const isSearchMode = ref(false);

// Загрузка данных
const loadFilmworks = async () => {
  if (isSearchMode.value && searchQuery.value.trim()) {
    const result = await searchFilmworks(
      searchQuery.value,
      currentPage.value,
      pageSize.value,
    );
    filmworks.value = Array.isArray(result) ? result.flat() : [];
  } else {
    const result = await getFilmworks(
      sortBy.value,
      currentPage.value,
      pageSize.value,
    );
    filmworks.value = Array.isArray(result) ? result.flat() : [];
  }
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
});

// Наблюдатель для пагинации
watch([currentPage], () => {
  loadFilmworks();
});
</script>

<style scoped>
.filmworks-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 20px;
}

.controls {
  display: flex;
  gap: 15px;
  align-items: center;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 250px;
}

.sort-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.filmworks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.filmwork-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.filmwork-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgb(0 0 0 / 10%);
}

.filmwork-poster {
  width: 100%;
  height: 200px;
  background: #f5f5f5;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 15px;
}

.poster-placeholder {
  font-size: 48px;
  color: #ccc;
  font-weight: bold;
}

.filmwork-info {
  text-align: center;
}

.filmwork-title {
  margin: 0 0 10px;
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
}

.filmwork-rating {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  margin-bottom: 10px;
}

.rating-star {
  font-size: 1.2em;
}

.rating-value {
  font-weight: 600;
  color: #f39c12;
}

.filmwork-genres {
  display: flex;
  justify-content: center;
  gap: 5px;
  flex-wrap: wrap;
}

.genre-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8em;
}

.genre-more {
  color: #666;
  font-size: 0.8em;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error-state {
  color: #e74c3c;
}

.retry-button,
.clear-search-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.retry-button:hover,
.clear-search-button:hover {
  background: #2980b9;
}

.search-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 4px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 30px;
}

.pagination-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.pagination-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.pagination-info {
  font-weight: 600;
  color: #333;
}

@media (width <= 768px) {
  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .controls {
    flex-direction: column;
  }

  .search-input {
    min-width: auto;
  }

  .filmworks-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .search-info {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}
</style>
