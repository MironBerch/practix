<template>
  <div class="filmwork-card" @click="handleClick">
    <div class="filmwork-poster">
      <div class="poster-placeholder">{{ title.charAt(0) }}</div>
      <div v-if="showBookmarkIndicator" class="bookmark-indicator">★</div>
    </div>
    <div class="filmwork-info">
      <h3 class="filmwork-title">{{ title }}</h3>
      <div class="filmwork-rating" v-if="showRating">
        <span class="rating-star">⭐</span>
        <span class="rating-value">{{ displayRating }}</span>
      </div>
      <div v-if="genres && genres.length > 0" class="filmwork-genres">
        <span v-for="genre in displayGenres" :key="genre" class="genre-tag">
          {{ genre }}
        </span>
        <span v-if="genres.length > maxGenres" class="genre-more">
          +{{ genres.length - maxGenres }}
        </span>
      </div>
      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  id: string;
  title: string;
  rating?: number | null;
  genres?: string[];
  maxGenres?: number;
  showRating?: boolean;
  showBookmarkIndicator?: boolean;
  clickable?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  maxGenres: 2,
  showRating: true,
  showBookmarkIndicator: false,
  clickable: true,
});

const emit = defineEmits<{
  click: [id: string];
}>();

const displayRating = computed(() => {
  return props.rating?.toFixed(1) || "0.0";
});

const displayGenres = computed(() => {
  return props.genres?.slice(0, props.maxGenres) || [];
});

const handleClick = () => {
  if (props.clickable) {
    emit("click", props.id);
  }
};
</script>

<style scoped>
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
  position: relative;
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

.bookmark-indicator {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  color: #f39c12;
}

.filmwork-info {
  text-align: center;
}

.filmwork-title {
  margin: 0 0 10px;
  font-size: 1.1em;
  font-weight: 600;
  color: #333;
  line-height: 1.3;
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
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8em;
}

.genre-more {
  color: #666;
  font-size: 0.8em;
}

@media (width <= 768px) {
  .filmwork-poster {
    height: 150px;
  }

  .poster-placeholder {
    font-size: 36px;
  }

  .filmwork-title {
    font-size: 1em;
  }
}
</style>
