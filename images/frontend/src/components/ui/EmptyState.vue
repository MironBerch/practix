<template>
  <div class="empty-state">
    <div v-if="icon" class="empty-icon">{{ icon }}</div>
    <h3 v-if="title">{{ title }}</h3>
    <p>{{ message }}</p>
    <slot name="action"></slot>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    message: string;
    title?: string;
    icon?: string;
  }>(),
  {
    message: "Нет данных",
  },
);
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.empty-state h3 {
  margin: 0 0 10px;
  color: #333;
}

.empty-state p {
  margin: 0;
  font-size: 1em;
}
</style>
