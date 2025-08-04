<template>
  <div class="auth-page">
    <h1>Sign In</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">Email</label>
        <input v-model="form.email" type="email" id="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="form.password" type="password" id="password" required>
      </div>
      <button type="submit" :disabled="loading">Sign In</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
    <p>Don't have an account? <router-link to="/auth/signup">Sign Up</router-link></p>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuth } from '../../composables/useAuth'

  export default defineComponent(
    {
      setup() {
        const router = useRouter()
        const { signIn, loading, error } = useAuth()
        
        const form = ref({
          email: '',
          password: ''
        })

        const handleSubmit = async () => {
          const response = await signIn(form.value)
          if (response) {
            router.push({ 
              name: 'confirm-2fa',
              query: { temp_token: response.temp_token }
            })
          }
        }

        return {
          form,
          handleSubmit,
          loading,
          error
        }
      }
    }
  )
</script>
