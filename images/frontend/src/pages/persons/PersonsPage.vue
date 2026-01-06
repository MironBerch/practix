<template>
  <div class="persons-page">
    <!-- Заголовок и управление -->
    <div class="page-header">
      <h1>Актеры и режиссеры</h1>
      <div class="controls">
        <div class="search-control">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск по имени..."
            @input="handleSearch"
            class="search-input"
          />
        </div>
        <div class="filter-control">
          <select
            v-model="roleFilter"
            @change="handleFilterChange"
            class="filter-select"
          >
            <option value="">Все роли</option>
            <option value="actor">Актеры</option>
            <option value="director">Режиссеры</option>
            <option value="writer">Сценаристы</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="loading-state">
      <p>Загрузка персон...</p>
    </div>

    <!-- Сообщение об ошибке -->
    <div v-if="error" class="error-state">
      <p>Ошибка: {{ error }}</p>
      <button @click="refreshData" class="retry-button">
        Попробовать снова
      </button>
    </div>

    <!-- Результаты поиска -->
    <div v-if="isSearchMode && filteredPersons.length > 0" class="search-info">
      <h2>Результаты поиска для "{{ searchQuery }}"</h2>
      <p>Найдено персон: {{ filteredPersons.length }}</p>
      <button @click="clearSearch" class="clear-search-button">
        Показать всех
      </button>
    </div>

    <!-- Список персон -->
    <div v-if="!loading && !error" class="persons-grid">
      <router-link
        v-for="person in filteredPersons"
        :key="person.uuid"
        :to="`/persons/${person.uuid}`"
        class="person-card"
      >
        <div class="person-avatar">
          <div class="avatar-placeholder">{{ getInitials(person.name) }}</div>
        </div>
        <div class="person-info">
          <h3 class="person-name">{{ person.name }}</h3>
          <div class="person-roles">
            <span
              v-for="role in person.roles.slice(0, 3)"
              :key="role"
              :class="['role-tag', getRoleClass(role)]"
            >
              {{ getRoleDisplayName(role) }}
            </span>
            <span v-if="person.roles.length > 3" class="role-more">
              +{{ person.roles.length - 3 }}
            </span>
          </div>
          <div class="person-filmworks">
            <span class="filmworks-count">
              Участвовал(а) в {{ person.filmwork_ids?.length || 0 }} фильмах
            </span>
          </div>
        </div>
      </router-link>
    </div>

    <!-- Сообщение о пустом состоянии -->
    <div
      v-if="!loading && !error && filteredPersons.length === 0"
      class="empty-state"
    >
      <p v-if="isSearchMode">По вашему запросу ничего не найдено</p>
      <p v-else-if="roleFilter">Нет персон с выбранной ролью</p>
      <p v-else>Нет доступных персон</p>
    </div>

    <!-- Пагинация -->
    <div
      v-if="!loading && !error && filteredPersons.length > 0"
      class="pagination"
    >
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
import { ref, onMounted, watch, computed } from "vue";
import { useMovies } from "../../composables/useMovies";
import type { Person } from "../../types/types";

const { loading, error, getPersons, searchPersons } = useMovies();

// Реактивные данные
const persons = ref<Person[]>([]);
const searchQuery = ref("");
const roleFilter = ref("");
const currentPage = ref(1);
const pageSize = ref(24);
const isSearchMode = ref(false);

// Загрузка данных
const loadPersons = async () => {
  try {
    let result;
    if (isSearchMode.value && searchQuery.value.trim()) {
      result = await searchPersons(
        searchQuery.value,
        currentPage.value,
        pageSize.value,
      );
    } else {
      result = await getPersons(currentPage.value, pageSize.value);
    }

    if (result && Array.isArray(result)) {
      persons.value = result.flat() as Person[];
    } else {
      persons.value = [];
    }
  } catch (err) {
    console.error("Error loading persons:", err);
    persons.value = [];
  }
};

// Отфильтрованные персоны по роли
const filteredPersons = computed(() => {
  if (!roleFilter.value) {
    return persons.value;
  }

  return persons.value.filter((person) =>
    person.roles?.some((role) =>
      role.toLowerCase().includes(roleFilter.value.toLowerCase()),
    ),
  );
});

// Обработчики событий
const handleSearch = () => {
  isSearchMode.value = searchQuery.value.trim().length > 0;
  currentPage.value = 1;
  loadPersons();
};

const handleFilterChange = () => {
  currentPage.value = 1;
  // Фильтрация происходит на клиенте, поэтому не нужно перезагружать данные
};

const clearSearch = () => {
  searchQuery.value = "";
  roleFilter.value = "";
  isSearchMode.value = false;
  currentPage.value = 1;
  loadPersons();
};

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    loadPersons();
  }
};

const nextPage = () => {
  currentPage.value++;
  loadPersons();
};

const refreshData = () => {
  loadPersons();
};

// Вспомогательные функции
const getInitials = (name: string) => {
  return name
    .split(" ")
    .map((part) => part.charAt(0))
    .join("")
    .toUpperCase()
    .slice(0, 2);
};

const getRoleClass = (role: string) => {
  const roleLower = role.toLowerCase();
  if (roleLower.includes("actor") || roleLower.includes("актер")) {
    return "role-actor";
  } else if (roleLower.includes("director") || roleLower.includes("режиссер")) {
    return "role-director";
  } else if (roleLower.includes("writer") || roleLower.includes("сценарист")) {
    return "role-writer";
  } else if (roleLower.includes("producer") || roleLower.includes("продюсер")) {
    return "role-producer";
  }
  return "role-other";
};

const getRoleDisplayName = (role: string) => {
  const roleLower = role.toLowerCase();
  if (roleLower.includes("actor") || roleLower.includes("актер")) {
    return "Актер";
  } else if (roleLower.includes("director") || roleLower.includes("режиссер")) {
    return "Режиссер";
  } else if (roleLower.includes("writer") || roleLower.includes("сценарист")) {
    return "Сценарист";
  } else if (roleLower.includes("producer") || roleLower.includes("продюсер")) {
    return "Продюсер";
  }
  return role;
};

// Загрузка при монтировании
onMounted(() => {
  loadPersons();
});

// Наблюдатель для пагинации
watch([currentPage], () => {
  loadPersons();
});
</script>

<style scoped>
@import url('../../styles/pages/persons/persons.css');
</style>
