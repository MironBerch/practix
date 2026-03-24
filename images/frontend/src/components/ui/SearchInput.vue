<template>
  <div class="search-control">
    <input
      v-model="modelValue"
      type="text"
      :placeholder="placeholder"
      @input="handleInput"
      class="search-input"
    />
    <button
      v-if="modelValue && showClear"
      @click="clearSearch"
      class="clear-button"
      type="button"
    >
      ×
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue?: string;
  placeholder?: string;
  debounceMs?: number;
  showClear?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: "",
  placeholder: "Поиск...",
  debounceMs: 300,
  showClear: true,
});

const emit = defineEmits<{
  "update:modelValue": [value: string];
  search: [value: string];
}>();

let debounceTimer: ReturnType<typeof setTimeout> | null = null;

const handleInput = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }
  debounceTimer = setTimeout(() => {
    emit("search", props.modelValue);
  }, props.debounceMs);
};

const clearSearch = () => {
  emit("update:modelValue", "");
  emit("search", "");
};
</script>

<style scoped>
.search-control {
  position: relative;
  display: flex;
  align-items: center;
}

.search-input {
  padding: 8px 35px 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 250px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #3498db;
}

.clear-button {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.clear-button:hover {
  color: #333;
}

@media (width <= 768px) {
  .search-input {
    min-width: auto;
    width: 100%;
  }
}
</style>
