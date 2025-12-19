<template>
  <div class="filmwork-detail" v-if="filmwork">
    <!-- Хлебные крошки -->
    <nav class="breadcrumb">
      <router-link to="/filmworks">Фильмы</router-link>
      <span class="separator">/</span>
      <span>{{ filmwork.title }}</span>
    </nav>

    <!-- Основная информация о фильме -->
    <div class="filmwork-header">
      <div class="poster-section">
        <div class="poster">
          <div class="poster-placeholder">{{ filmwork.title.charAt(0) }}</div>
        </div>
        <div class="actions">
          <button
            @click="toggleBookmark"
            :class="['bookmark-btn', { bookmarked: isBookmarked }]"
            :disabled="!isAuthenticated || bookmarkLoading"
          >
            <span v-if="bookmarkLoading">...</span>
            <span v-else-if="isBookmarked">★ В избранном</span>
            <span v-else>☆ Добавить в избранное</span>
          </button>

          <div class="rating-section">
            <h4>Рейтинг фильма</h4>
            <div class="average-rating" v-if="filmworkRating">
              Средний рейтинг:
              {{ filmworkRating.average_rating?.toFixed(1) || "Нет оценок" }}
            </div>
            <div class="user-rating">
              <span>Ваша оценка: </span>
              <select
                v-model="userRating"
                @change="handleRatingChange"
                :disabled="!isAuthenticated || ratingLoading"
                class="rating-select"
              >
                <option value="0">Не оценено</option>
                <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
              </select>
              <button
                v-if="userRating > 0"
                @click="removeRating"
                class="remove-rating-btn"
                :disabled="!isAuthenticated || ratingLoading"
              >
                <span v-if="ratingLoading">...</span>
                <span v-else>Удалить оценку</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="info-section">
        <h1 class="filmwork-title">{{ filmwork.title }}</h1>
        <div class="filmwork-rating">
          <span class="rating-star">⭐</span>
          <span class="rating-value">{{ filmwork.rating.toFixed(1) }}</span>
        </div>

        <div class="filmwork-description">
          <h3>Описание</h3>
          <p>{{ filmwork.description }}</p>
        </div>

        <div class="filmwork-genres">
          <h3>Жанры</h3>
          <div class="genres-list">
            <span
              v-for="genre in filmwork.genres"
              :key="genre"
              class="genre-tag"
            >
              {{ genre }}
            </span>
          </div>
        </div>

        <div class="filmwork-people">
          <div class="people-section">
            <h3>Режиссеры</h3>
            <div class="people-list">
              <span
                v-for="person in filmwork.directors"
                :key="person.uuid"
                class="person-name"
                @click="navigateToPerson(person.uuid)"
              >
                {{ person.name }}
              </span>
            </div>
          </div>

          <div class="people-section">
            <h3>Актеры</h3>
            <div class="people-list">
              <span
                v-for="person in filmwork.actors"
                :key="person.uuid"
                class="person-name"
                @click="navigateToPerson(person.uuid)"
              >
                {{ person.name }}
              </span>
            </div>
          </div>

          <div class="people-section">
            <h3>Сценаристы</h3>
            <div class="people-list">
              <span
                v-for="person in filmwork.writers"
                :key="person.uuid"
                class="person-name"
                @click="navigateToPerson(person.uuid)"
              >
                {{ person.name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Раздел отзывов -->
    <div class="reviews-section">
      <div class="reviews-header">
        <h2>Отзывы ({{ reviews.length }})</h2>
        <button
          v-if="isAuthenticated && !userReview"
          @click="showReviewForm = true"
          class="add-review-btn"
          :disabled="reviewLoading"
        >
          <span v-if="reviewLoading">...</span>
          <span v-else>Написать отзыв</span>
        </button>
        <button
          v-else-if="isAuthenticated && userReview"
          @click="deleteUserReview"
          class="delete-review-btn"
          :disabled="reviewLoading"
        >
          <span v-if="reviewLoading">...</span>
          <span v-else>Удалить мой отзыв</span>
        </button>
      </div>

      <!-- Форма добавления отзыва -->
      <div v-if="showReviewForm" class="review-form">
        <h3>Ваш отзыв</h3>
        <textarea
          v-model="newReviewText"
          placeholder="Напишите ваш отзыв..."
          class="review-textarea"
          rows="4"
          :disabled="reviewLoading"
        ></textarea>
        <div class="review-actions">
          <button
            @click="submitReview"
            class="submit-review-btn"
            :disabled="reviewLoading"
          >
            <span v-if="reviewLoading">Публикация...</span>
            <span v-else>Опубликовать</span>
          </button>
          <button
            @click="cancelReview"
            class="cancel-review-btn"
            :disabled="reviewLoading"
          >
            Отмена
          </button>
        </div>
      </div>

      <!-- Список отзывов -->
      <div v-if="!reviewsLoading && reviews.length > 0" class="reviews-list">
        <div v-for="review in reviews" :key="review.id" class="review-card">
          <div class="review-header">
            <span class="review-author"
              >Пользователь #{{ review.author_id.slice(-6) }}</span
            >
            <span class="review-date">{{ formatDate(review.pub_date) }}</span>
          </div>
          <p class="review-text">{{ review.text }}</p>

          <!-- Рейтинг отзыва -->
          <div class="review-rating">
            <div class="rating-stats" v-if="reviewRatings[review.id]">
              <span class="likes">👍 {{ reviewRatings[review.id].likes }}</span>
              <span class="dislikes"
                >👎 {{ reviewRatings[review.id].dislikes }}</span
              >
            </div>

            <div v-if="isAuthenticated" class="rating-actions">
              <button
                @click="rateReview(review.id, 10)"
                :class="[
                  'rate-btn',
                  'like-btn',
                  { active: userReviewRatings[review.id] === 10 },
                ]"
                :disabled="reviewRatingLoading[review.id]"
              >
                <span v-if="reviewRatingLoading[review.id]">...</span>
                <span v-else>👍</span>
              </button>
              <button
                @click="rateReview(review.id, 1)"
                :class="[
                  'rate-btn',
                  'dislike-btn',
                  { active: userReviewRatings[review.id] === 1 },
                ]"
                :disabled="reviewRatingLoading[review.id]"
              >
                <span v-if="reviewRatingLoading[review.id]">...</span>
                <span v-else>👎</span>
              </button>
              <button
                v-if="userReviewRatings[review.id]"
                @click="removeReviewRating(review.id)"
                class="remove-rating-btn"
                :disabled="reviewRatingLoading[review.id]"
              >
                <span v-if="reviewRatingLoading[review.id]">...</span>
                <span v-else>Убрать оценку</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!reviewsLoading" class="no-reviews">
        <p>Пока нет отзывов. Будьте первым!</p>
      </div>

      <div v-if="reviewsLoading" class="loading-reviews">
        <p>Загрузка отзывов...</p>
      </div>
    </div>

    <!-- Уведомления -->
    <div v-if="message" :class="['message', messageType]">
      {{ message }}
    </div>
  </div>

  <!-- Состояние загрузки -->
  <div v-else-if="loading" class="loading-state">
    <p>Загрузка информации о фильме...</p>
  </div>

  <!-- Сообщение об ошибке -->
  <div v-else-if="error" class="error-state">
    <p>Ошибка: {{ error }}</p>
    <button @click="loadFilmworkData" class="retry-button">
      Попробовать снова
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useMovies } from "../../composables/useMovies";
import { useUGC } from "../../composables/useUGC";
import type {
  Filmwork,
  Review,
  ReviewRating,
  Score,
  Text,
  ReviewScore,
} from "../../types/types";

const route = useRoute();
const router = useRouter();
const { getFilmwork, loading, error } = useMovies();
const {
  addFilmworkToBookmarks,
  removeFilmworkFromBookmarks,
  getBookmarks,
  getFilmworkRating,
  addFilmworkRating,
  deleteFilmworkRating,
  getFilmworkReviews,
  addFilmworkReview,
  deleteFilmworkReview,
  getFilmworkReviewRating,
  addFilmworkReviewRating,
  deleteFilmworkReviewRating,
} = useUGC();

// Реактивные данные
const filmwork = ref<Filmwork | null>(null);
const isBookmarked = ref(false);
const filmworkRating = ref<{ average_rating: number | null } | null>(null);
const userRating = ref(0);
const reviews = ref<Review[]>([]);
const reviewRatings = ref<{ [key: string]: ReviewRating }>({});
const userReviewRatings = ref<{ [key: string]: 1 | 10 }>({});
const showReviewForm = ref(false);
const newReviewText = ref("");
const message = ref("");
const messageType = ref<"success" | "error">("success");

// Состояния загрузки
const bookmarkLoading = ref(false);
const ratingLoading = ref(false);
const reviewLoading = ref(false);
const reviewsLoading = ref(false);
const reviewRatingLoading = ref<{ [key: string]: boolean }>({});

// Получение UUID из параметров маршрута
const filmworkUuid = computed(() => route.params.uuid as string);

// Проверка аутентификации через localStorage
const isAuthenticated = computed(() => {
  const accessToken = localStorage.getItem("access_token");
  return !!accessToken;
});

// Получение access token
const getAccessToken = (): string | null => {
  return localStorage.getItem("access_token");
};

// Получение отзыва текущего пользователя
const userReview = computed(() => {
  // В реальном приложении нужно сравнивать с ID текущего пользователя
  // Для демонстрации будем считать, что у нас есть способ получить user_id
  const currentUserId = getCurrentUserId();
  return reviews.value.find((review) => review.author_id === currentUserId);
});

// Заглушка для получения ID текущего пользователя
const getCurrentUserId = (): string => {
  // В реальном приложении нужно декодировать JWT токен или получить ID из store
  // Здесь используем заглушку
  return "current-user-id";
};

// Загрузка данных о фильме
const loadFilmworkData = async () => {
  const filmworkData = await getFilmwork(filmworkUuid.value);
  if (filmworkData) {
    filmwork.value = filmworkData;
    await loadAdditionalData();
  }
};

// Загрузка дополнительных данных (закладки, рейтинги, отзывы)
const loadAdditionalData = async () => {
  // Загрузка рейтинга фильма (доступно без аутентификации)
  filmworkRating.value = await getFilmworkRating(filmworkUuid.value);

  // Загрузка отзывов (доступно без аутентификации)
  await loadReviews();

  // Загрузка данных, требующих аутентификации
  if (isAuthenticated.value) {
    await loadAuthenticatedData();
  }
};

// Загрузка отзывов
const loadReviews = async () => {
  reviewsLoading.value = true;
  try {
    const reviewsData = await getFilmworkReviews(filmworkUuid.value);
    if (reviewsData) {
      reviews.value = reviewsData;

      // Загрузка рейтингов для каждого отзыва
      for (const review of reviews.value) {
        const rating = await getFilmworkReviewRating(
          filmworkUuid.value,
          review.id,
        );
        if (rating) {
          reviewRatings.value[review.id] = rating;
        }
      }
    }
  } catch (err) {
    console.error("Error loading reviews:", err);
  } finally {
    reviewsLoading.value = false;
  }
};

// Загрузка данных, требующих аутентификации
const loadAuthenticatedData = async () => {
  const token = getAccessToken();
  if (!token) return;

  try {
    // Загрузка закладок
    const bookmarks = await getBookmarks(token);
    if (bookmarks && Array.isArray(bookmarks)) {
      isBookmarked.value = bookmarks.some(
        (bookmark: any) => bookmark.filmwork_id === filmworkUuid.value,
      );
    }

    // Здесь можно добавить загрузку рейтинга пользователя для фильма
    // и рейтингов пользователя для отзывов, если API поддерживает
  } catch (err) {
    console.error("Error loading authenticated data:", err);
    // Если токен невалидный, очищаем его
    if (err instanceof Error && err.message.includes("401")) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
    }
  }
};

// Управление закладками
const toggleBookmark = async () => {
  if (!isAuthenticated.value) {
    showMessage(
      "Для добавления в избранное необходимо авторизоваться",
      "error",
    );
    return;
  }

  const token = getAccessToken();
  if (!token) return;

  bookmarkLoading.value = true;
  try {
    if (isBookmarked.value) {
      await removeFilmworkFromBookmarks(filmworkUuid.value, token);
      isBookmarked.value = false;
      showMessage("Фильм удален из избранного");
    } else {
      await addFilmworkToBookmarks(filmworkUuid.value, token);
      isBookmarked.value = true;
      showMessage("Фильм добавлен в избранное");
    }
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при обновлении закладки: ${errorMessage}`, "error");

    // Если ошибка аутентификации, перенаправляем на страницу входа
    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    bookmarkLoading.value = false;
  }
};

// Управление рейтингом фильма
const handleRatingChange = async () => {
  if (!isAuthenticated.value) {
    showMessage("Для оценки фильма необходимо авторизоваться", "error");
    return;
  }

  const token = getAccessToken();
  if (!token) return;

  ratingLoading.value = true;
  try {
    if (userRating.value > 0) {
      const score: Score = { score: userRating.value };
      await addFilmworkRating(filmworkUuid.value, token, score);
      showMessage("Оценка добавлена");

      // Обновляем средний рейтинг
      filmworkRating.value = await getFilmworkRating(filmworkUuid.value);
    }
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при добавлении оценки: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    ratingLoading.value = false;
  }
};

const removeRating = async () => {
  if (!isAuthenticated.value) return;

  const token = getAccessToken();
  if (!token) return;

  ratingLoading.value = true;
  try {
    await deleteFilmworkRating(filmworkUuid.value, token);
    userRating.value = 0;
    showMessage("Оценка удалена");

    // Обновляем средний рейтинг
    filmworkRating.value = await getFilmworkRating(filmworkUuid.value);
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при удалении оценки: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    ratingLoading.value = false;
  }
};

// Управление отзывами
const submitReview = async () => {
  if (!isAuthenticated.value) {
    showMessage("Для добавления отзыва необходимо авторизоваться", "error");
    return;
  }

  const token = getAccessToken();
  if (!token) return;

  if (!newReviewText.value.trim()) {
    showMessage("Отзыв не может быть пустым", "error");
    return;
  }

  reviewLoading.value = true;
  try {
    const text: Text = { text: newReviewText.value };
    await addFilmworkReview(filmworkUuid.value, token, text);
    showReviewForm.value = false;
    newReviewText.value = "";
    showMessage("Отзыв добавлен");

    // Перезагружаем отзывы
    await loadReviews();
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при добавлении отзыва: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    reviewLoading.value = false;
  }
};

const cancelReview = () => {
  showReviewForm.value = false;
  newReviewText.value = "";
};

const deleteUserReview = async () => {
  if (!userReview.value) return;

  const token = getAccessToken();
  if (!token) return;

  reviewLoading.value = true;
  try {
    await deleteFilmworkReview(filmworkUuid.value, userReview.value.id, token);
    showMessage("Отзыв удален");

    // Перезагружаем отзывы
    await loadReviews();
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при удалении отзыва: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    reviewLoading.value = false;
  }
};

// Управление рейтингом отзывов
const rateReview = async (reviewId: string, score: 1 | 10) => {
  if (!isAuthenticated.value) {
    showMessage("Для оценки отзыва необходимо авторизоваться", "error");
    return;
  }

  const token = getAccessToken();
  if (!token) return;

  reviewRatingLoading.value[reviewId] = true;
  try {
    const reviewScore: ReviewScore = { score };
    await addFilmworkReviewRating(
      filmworkUuid.value,
      token,
      reviewScore,
      reviewId,
    );
    userReviewRatings.value[reviewId] = score;
    showMessage("Оценка отзыва добавлена");

    // Обновляем рейтинг отзыва
    const rating = await getFilmworkReviewRating(filmworkUuid.value, reviewId);
    if (rating) {
      reviewRatings.value[reviewId] = rating;
    }
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при оценке отзыва: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    reviewRatingLoading.value[reviewId] = false;
  }
};

const removeReviewRating = async (reviewId: string) => {
  if (!isAuthenticated.value) return;

  const token = getAccessToken();
  if (!token) return;

  reviewRatingLoading.value[reviewId] = true;
  try {
    await deleteFilmworkReviewRating(filmworkUuid.value, token, reviewId);
    delete userReviewRatings.value[reviewId];
    showMessage("Оценка отзыва удалена");

    // Обновляем рейтинг отзыва
    const rating = await getFilmworkReviewRating(filmworkUuid.value, reviewId);
    if (rating) {
      reviewRatings.value[reviewId] = rating;
    }
  } catch (err) {
    const errorMessage =
      err instanceof Error ? err.message : "Неизвестная ошибка";
    showMessage(`Ошибка при удалении оценки отзыва: ${errorMessage}`, "error");

    if (errorMessage.includes("401")) {
      handleAuthError();
    }
  } finally {
    reviewRatingLoading.value[reviewId] = false;
  }
};

// Обработка ошибок аутентификации
const handleAuthError = () => {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  showMessage("Сессия истекла. Пожалуйста, войдите снова.", "error");
  // Перенаправление на страницу входа можно добавить здесь
  // router.push('/signin')
};

// Вспомогательные функции
const navigateToPerson = (personUuid: string) => {
  router.push(`/persons/${personUuid}`);
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("ru-RU");
};

const showMessage = (text: string, type: "success" | "error" = "success") => {
  message.value = text;
  messageType.value = type;
  setTimeout(() => {
    message.value = "";
  }, 3000);
};

// Загрузка при монтировании
onMounted(() => {
  loadFilmworkData();
});
</script>

<style scoped>
/* Стили остаются такими же как в предыдущей версии, но добавляем состояния загрузки */
.loading-reviews {
  text-align: center;
  padding: 20px;
  color: #666;
}

.rate-btn:disabled,
.bookmark-btn:disabled,
.rating-select:disabled,
.remove-rating-btn:disabled,
.add-review-btn:disabled,
.delete-review-btn:disabled,
.submit-review-btn:disabled,
.cancel-review-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Остальные стили остаются без изменений */
.filmwork-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.breadcrumb {
  margin-bottom: 20px;
  font-size: 14px;
  color: #666;
}

.breadcrumb a {
  color: #3498db;
  text-decoration: none;
}

.breadcrumb a:hover {
  text-decoration: underline;
}

.separator {
  margin: 0 8px;
}

.filmwork-header {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 40px;
  margin-bottom: 40px;
}

.poster-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.poster {
  width: 100%;
  height: 400px;
  background: #f5f5f5;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.poster-placeholder {
  font-size: 72px;
  color: #ccc;
  font-weight: bold;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bookmark-btn {
  padding: 12px 20px;
  border: 2px solid #3498db;
  background: white;
  color: #3498db;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.bookmark-btn:hover:not(:disabled) {
  background: #3498db;
  color: white;
}

.bookmark-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.bookmark-btn.bookmarked {
  background: #f39c12;
  border-color: #f39c12;
  color: white;
}

.rating-section {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background: #fafafa;
}

.rating-section h4 {
  margin: 0 0 15px;
  color: #333;
}

.average-rating {
  font-size: 18px;
  font-weight: 600;
  color: #f39c12;
  margin-bottom: 15px;
}

.user-rating {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.rating-select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.remove-rating-btn {
  padding: 6px 12px;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.remove-rating-btn:hover:not(:disabled) {
  background: #c0392b;
}

.remove-rating-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filmwork-title {
  font-size: 2.5em;
  margin: 0;
  color: #333;
}

.filmwork-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1.2em;
}

.rating-star {
  font-size: 1.4em;
}

.rating-value {
  font-weight: 600;
  color: #f39c12;
}

.filmwork-description h3,
.filmwork-genres h3,
.people-section h3 {
  margin: 0 0 10px;
  color: #333;
  font-size: 1.2em;
}

.filmwork-description p {
  line-height: 1.6;
  color: #666;
  margin: 0;
}

.genres-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.genre-tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 0.9em;
}

.filmwork-people {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.people-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.person-name {
  background: #f8f9fa;
  color: #495057;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.person-name:hover {
  background: #e9ecef;
}

.reviews-section {
  border-top: 2px solid #e0e0e0;
  padding-top: 30px;
}

.reviews-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.reviews-header h2 {
  margin: 0;
  color: #333;
}

.add-review-btn,
.delete-review-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.add-review-btn {
  background: #27ae60;
  color: white;
}

.add-review-btn:hover:not(:disabled) {
  background: #219a52;
}

.delete-review-btn {
  background: #e74c3c;
  color: white;
}

.delete-review-btn:hover:not(:disabled) {
  background: #c0392b;
}

.review-form {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.review-form h3 {
  margin: 0 0 15px;
  color: #333;
}

.review-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  font-family: inherit;
}

.review-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.submit-review-btn,
.cancel-review-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-review-btn {
  background: #3498db;
  color: white;
}

.submit-review-btn:hover:not(:disabled) {
  background: #2980b9;
}

.cancel-review-btn {
  background: #95a5a6;
  color: white;
}

.cancel-review-btn:hover:not(:disabled) {
  background: #7f8c8d;
}

.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.review-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background: white;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #666;
}

.review-text {
  line-height: 1.6;
  margin: 0 0 15px;
  color: #333;
}

.review-rating {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f0f0f0;
}

.rating-stats {
  display: flex;
  gap: 15px;
}

.likes {
  color: #27ae60;
}

.dislikes {
  color: #e74c3c;
}

.rating-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.rate-btn {
  padding: 6px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.rate-btn:hover:not(:disabled) {
  background: #f8f9fa;
}

.rate-btn.active {
  border-color: #3498db;
  background: #3498db;
  color: white;
}

.no-reviews {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #fafafa;
  border-radius: 8px;
}

.message {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 15px 20px;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  z-index: 1000;
  max-width: 300px;
}

.message.success {
  background: #27ae60;
}

.message.error {
  background: #e74c3c;
}

.loading-state,
.error-state {
  text-align: center;
  padding: 60px 20px;
  color: #666;
}

.error-state {
  color: #e74c3c;
}

.retry-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
}

.retry-button:hover {
  background: #2980b9;
}

@media (width <= 768px) {
  .filmwork-header {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .poster {
    height: 300px;
  }

  .filmwork-title {
    font-size: 2em;
  }

  .reviews-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .review-rating {
    flex-direction: column;
    gap: 10px;
    align-items: flex-start;
  }

  .user-rating {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
