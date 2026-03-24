<template>
  <div class="pagination">
    <button
      :disabled="!canGoPrevious"
      @click="$emit('previous')"
      class="pagination-button"
    >
      Назад
    </button>
    <span class="pagination-info">Страница {{ currentPage }}</span>
    <button @click="$emit('next')" class="pagination-button">Вперед</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface Props {
  currentPage: number;
  hasNextPage?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  hasNextPage: true,
});

defineEmits<{
  previous: [];
  next: [];
}>();

const canGoPrevious = computed(() => props.currentPage > 1);
</script>

<style scoped>
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
  transition: background-color 0.3s ease;
}

.pagination-button:hover:not(:disabled) {
  background: #2980b9;
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
  .pagination {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
