<template>
  <div class="user-page">
    <h1>Ваши сессии</h1>
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div v-for="session in sessions" :key="session.id" class="session-item">
        <p><strong>Устройство:</strong> {{ session.user_device_type }}</p>
        <p><strong>Браузер:</strong> {{ session.user_agent }}</p>
        <p><strong>Дата:</strong> {{ session.event_date }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useAuth } from "../../composables/useAuth";

const token = localStorage.getItem("access_token");

export default defineComponent({
  setup() {
    const { getUserSessions, loading, error } = useAuth();
    const sessions = ref([]);

    onMounted(async () => {
      const data = await getUserSessions(token);
      if (data) {
        sessions.value = data;
      }
    });

    return {
      sessions,
      loading,
      error,
    };
  },
});
</script>

<style scoped>
@import url('../../styles/pages/auth/auth-form-styles.css');
</style>
