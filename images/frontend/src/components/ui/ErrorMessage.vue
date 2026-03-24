<template>
  <div class="error-state">
    <p>Ошибка: {{ message }}</p>
    <button @click="handleRetry" class="retry-button">
      Попробовать снова
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message: string;
}

const props = defineProps<Props>();

const emit = defineEmits<{
  retry: [];
}>();

const handleRetry = () => {
  emit("retry");
};
</script>

<style scoped>
.error-state {
  text-align: center;
  padding: 40px;
  color: #e74c3c;
}

.error-state p {
  margin: 0 0 15px;
  font-size: 1em;
}

.retry-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.retry-button:hover {
  background: #2980b9;
}
</style>
