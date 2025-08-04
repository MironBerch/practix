<template>
  <div class="user-page">
    <h1>Your Sessions</h1>
    <div v-if="loading">Loading...</div>
    <div v-else>
      <div v-for="session in sessions" :key="session.id" class="session-item">
        <p><strong>Device:</strong> {{ session.user_device_type }}</p>
        <p><strong>Browser:</strong> {{ session.user_agent }}</p>
        <p><strong>Date:</strong> {{ session.date }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import { useAuth } from '../../composables/useAuth'

  export default defineComponent(
    {
      setup() {
        const { getUserSessions, loading, error } = useAuth()
        const sessions = ref([])

        onMounted(async () => {
          const data = await getUserSessions()
          if (data) {
            sessions.value = data
          }
        })

        return {
          sessions,
          loading,
          error
        }
      }
    }
  )
</script>
