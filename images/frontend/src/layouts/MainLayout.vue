<script setup lang="ts">
  import AppHeader from '../components/Header.vue'
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
  .layout {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    margin: 0 10px;
  }

  .main-content {
    flex: 1;
    padding: 2rem;
    background-color: #f5f5f5;
  }

  @media (min-width: 1280px) {
    .layout {
      width: 1280px;
      margin: 0 auto;
    }
  }

  @media (max-width: 768px) {
    .main-content {
      padding: 1rem;
    }
    
    .layout {
      margin: 0 5px;
    }
  }
</style>
