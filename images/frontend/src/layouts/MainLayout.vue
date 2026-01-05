<script setup lang="ts">
import AppHeader from "../components/Header.vue";
</script>

<template>
  <div class="layout">
    <AppHeader />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
@import '../styles/layouts/main.css';
</style>
