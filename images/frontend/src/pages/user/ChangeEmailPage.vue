<template>
  <div class="user-page">
    <h1>Change Email</h1>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="email">New Email</label>
        <input v-model="email" type="email" id="email" required />
      </div>
      <button type="submit" :disabled="loading">Change Email</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useAuth } from "../../composables/useAuth";
import { useRouter } from "vue-router";

const router = useRouter();

export default defineComponent({
  setup() {
    const { changeEmail, loading, error } = useAuth();
    const email = ref("");

    const handleSubmit = async () => {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) return;

      const response = await changeEmail({ email: email.value }, access_token);
      if (response) {
        // Redirect to confirmation page
        router.push({ name: "confirm-change-email" });
      }
    };

    return {
      email,
      handleSubmit,
      loading,
      error,
    };
  },
});
</script>

<style scoped>
@import '../../styles/auth-form-styles.css';
</style>
