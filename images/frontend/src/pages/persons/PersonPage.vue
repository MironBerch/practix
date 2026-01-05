<template>
  <div class="person-page" v-if="person">
    <!-- Хлебные крошки -->
    <nav class="breadcrumb">
      <router-link to="/persons">Персоны</router-link>
      <span class="separator">/</span>
      <span>{{ person.name }}</span>
    </nav>

    <!-- Основная информация -->
    <div class="person-header">
      <div class="person-avatar-large">
        <div class="avatar-placeholder">{{ getInitials(person.name) }}</div>
      </div>
      <div class="person-info-main">
        <h1 class="person-name">{{ person.name }}</h1>
        <div class="person-roles">
          <span
            v-for="role in person.roles"
            :key="role"
            :class="['role-tag', getRoleClass(role)]"
          >
            {{ getRoleDisplayName(role) }}
          </span>
        </div>
        <div class="filmworks-count">
          Участвовал(а) в {{ person.filmwork_ids?.length || 0 }} фильмах
        </div>
      </div>
    </div>

    <!-- Фильмы персоны -->
    <div class="filmworks-section">
      <h2>Фильмы</h2>
      <div v-if="filmworksLoading" class="loading-state">
        <p>Загрузка фильмов...</p>
      </div>
      <div v-else-if="personFilmworks.length > 0" class="filmworks-grid">
        <router-link
          v-for="filmwork in personFilmworks"
          :key="filmwork.uuid"
          :to="`/filmworks/${filmwork.uuid}`"
          class="filmwork-card"
        >
          <div class="filmwork-poster">
            <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
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
            </div>
          </div>
        </router-link>
      </div>
      <div v-else class="empty-state">
        <p>Нет информации о фильмах</p>
      </div>
    </div>
  </div>

  <!-- Состояние загрузки -->
  <div v-else-if="loading" class="loading-state">
    <p>Загрузка информации о персоне...</p>
  </div>

  <!-- Сообщение об ошибке -->
  <div v-else-if="error" class="error-state">
    <p>Ошибка: {{ error }}</p>
    <button @click="loadPersonData" class="retry-button">
      Попробовать снова
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import { useMovies } from "../../composables/useMovies";
import type { Person, BaseFilmwork } from "../../types/types";

const route = useRoute();
const { getPerson, getFilmworksByPerson, loading, error } = useMovies();

// Реактивные данные
const person = ref<Person | null>(null);
const personFilmworks = ref<BaseFilmwork[]>([]);
const filmworksLoading = ref(false);

// Получение UUID из параметров маршрута
const personUuid = computed(() => route.params.uuid as string);

// Загрузка данных о персоне
const loadPersonData = async () => {
  const personData = await getPerson(personUuid.value);
  if (personData) {
    person.value = personData;
    await loadPersonFilmworks();
  }
};

// Загрузка фильмов персоны
const loadPersonFilmworks = async () => {
  filmworksLoading.value = true;
  try {
    const filmworksData = await getFilmworksByPerson(personUuid.value);
    if (filmworksData && Array.isArray(filmworksData)) {
      personFilmworks.value = filmworksData.flat() as BaseFilmwork[];
    } else {
      personFilmworks.value = [];
    }
  } catch (err) {
    console.error("Error loading person filmworks:", err);
    personFilmworks.value = [];
  } finally {
    filmworksLoading.value = false;
  }
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
  loadPersonData();
});
</script>

<style scoped>
@import '../../styles/pagess/person/person.css';
</style>
