<template>
  <div>
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/change-email">Change Email</router-link>
        <router-link to="/change-password">Change Password</router-link>
        <router-link to="/sessions">Sessions</router-link>
        <button @click="handleLogout">Logout</button>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script lang="ts">
  import { defineComponent } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuth } from '../composables/useAuth'

  export default defineComponent(
    {
      setup() {
        const router = useRouter()
        const { signOut } = useAuth()

        const handleLogout = async () => {
          const access_token = localStorage.getItem('access_token')
          if (!access_token) return
          
          await signOut(access_token)
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          router.push({ name: 'signin' })
        }

        return {
          handleLogout
        }
      }
    }
  )
</script>
