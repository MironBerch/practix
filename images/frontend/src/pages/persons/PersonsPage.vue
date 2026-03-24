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
    <LoadingSpinner v-if="loading" message="Загрузка персон..." />

    <!-- Сообщение об ошибке -->
    <ErrorMessage v-if="error" :message="error" @retry="refreshData" />

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
        :key="person.id"
        :to="`/persons/${person.id}`"
        custom
        v-slot="{ navigate }"
      >
        <PersonCard
          :id="person.id"
          :name="person.name"
          :roles="person.roles"
          :filmwork-count="person.filmwork_ids?.length || 0"
          @click="navigate"
        />
      </router-link>
    </div>

    <!-- Сообщение о пустом состоянии -->
    <EmptyState
      v-if="!loading && !error && filteredPersons.length === 0"
      :message="emptyMessage"
    />

    <!-- Пагинация -->
    <Pagination
      v-if="!loading && !error && filteredPersons.length > 0"
      :current-page="currentPage"
      @previous="previousPage"
      @next="nextPage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from "vue";
import { useMovies } from "../../composables/useMovies";
import PersonCard from "../../components/ui/PersonCard.vue";
import SearchInput from "../../components/ui/SearchInput.vue";
import Pagination from "../../components/ui/Pagination.vue";
import LoadingSpinner from "../../components/ui/LoadingSpinner.vue";
import ErrorMessage from "../../components/ui/ErrorMessage.vue";
import EmptyState from "../../components/ui/EmptyState.vue";
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

const emptyMessage = computed(() => {
  if (isSearchMode.value) return "По вашему запросу ничего не найдено";
  if (roleFilter.value) return "Нет персон с выбранной ролью";
  return "Нет доступных персон";
});

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
