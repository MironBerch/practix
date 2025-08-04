<template>
  <div class="user-page">
    <h1>Change Password</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="oldPassword">Old Password</label>
        <input v-model="form.old_password" type="password" id="oldPassword" required>
      </div>
      <div class="form-group">
        <label for="newPassword">New Password</label>
        <input v-model="form.new_password" type="password" id="newPassword" required>
      </div>
      <button type="submit" :disabled="loading">Change Password</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref } from 'vue'
  import { useAuth } from '../../composables/useAuth'

  export default defineComponent(
    {
      setup() {
        const { passwordChange, loading, error } = useAuth()
        const form = ref({
          old_password: '',
          new_password: ''
        })

        const handleSubmit = async () => {
          const access_token = localStorage.getItem('access_token')
          if (!access_token) return
          
          const response = await passwordChange(form.value, access_token)
          if (response) {
            // Handle success (maybe show a message)
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
