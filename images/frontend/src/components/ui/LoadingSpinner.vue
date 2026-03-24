<template>
  <div class="loading-state">
    <div class="spinner"></div>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ message?: string }>(), {
  message: "Загрузка...",
});
</script>

<style scoped>
.loading-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 15px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-state p {
  margin: 0;
  font-size: 1em;
}
</style>
