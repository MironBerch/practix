<template>
  <div class="confirm-change-email-page">
    <h1>Подтверждение смены email</h1>

    <div v-if="successMessage" class="success-message">
      <i class="icon-check"></i>
      {{ successMessage }}
    </div>

    <form v-else @submit.prevent="handleSubmit" class="confirmation-form">
      <div class="form-group">
        <label for="confirmation-code">Код подтверждения</label>
        <input
          v-model="confirmationCode"
          id="confirmation-code"
          type="text"
          required
          placeholder="Введите 6-значный код из письма"
          maxlength="6"
          @input="validateCode"
        />
        <div class="hint">Проверьте папку "Спам", если не видите письмо</div>
      </div>

      <button
        type="submit"
        :disabled="loading || !isCodeValid"
        class="submit-button"
      >
        <i v-if="loading" class="icon-spinner"></i>
        <span>{{ loading ? "Проверка..." : "Подтвердить смену email" }}</span>
      </button>

      <div v-if="errorMessage" class="error-message">
        <i class="icon-warning"></i>
        {{ errorMessage }}
      </div>
    </form>

    <div class="resend-section">
      <p>Не получили код?</p>
      <button
        @click="resendCode"
        :disabled="resendLoading || resendCooldown > 0"
        class="resend-button"
      >
        <i v-if="resendLoading" class="icon-spinner"></i>
        <span v-else>
          Отправить код повторно
          <span v-if="resendCooldown > 0">({{ resendCooldown }} сек)</span>
        </span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuth } from "../../composables/useAuth";

export default defineComponent({
  name: "ConfirmChangeEmailPage",

  setup() {
    const router = useRouter();
    const { confirmChangeEmail, resendChangeEmail, loading, error } = useAuth();

    const confirmationCode = ref("");
    const errorMessage = ref("");
    const successMessage = ref("");
    const resendLoading = ref(false);
    const resendCooldown = ref(0);
    const isCodeValid = ref(false);

    // Таймер для отсчета времени до повторной отправки
    let cooldownInterval: number;

    const validateCode = () => {
      isCodeValid.value = /^\d{6}$/.test(confirmationCode.value);
    };

    const startCooldown = () => {
      resendCooldown.value = 60; // 60 секунд
      cooldownInterval = setInterval(() => {
        resendCooldown.value--;
        if (resendCooldown.value <= 0) {
          clearInterval(cooldownInterval);
        }
      }, 1000);
    };

    const handleSubmit = async () => {
      errorMessage.value = "";

      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        errorMessage.value = "Требуется авторизация";
        return;
      }

      try {
        const response = await confirmChangeEmail(
          { code: confirmationCode.value },
          accessToken,
        );

        if (response) {
          successMessage.value = "Email успешно изменён!";
          setTimeout(() => {
            router.push({ name: "settings" });
          }, 2000);
        }
      } catch (err) {
        errorMessage.value =
          error.value || "Неверный код подтверждения. Попробуйте ещё раз.";
      }
    };

    const resendCode = async () => {
      resendLoading.value = true;
      errorMessage.value = "";

      const accessToken = localStorage.getItem("access_token");
      if (!accessToken) {
        errorMessage.value = "Требуется авторизация";
        resendLoading.value = false;
        return;
      }

      try {
        const response = await resendChangeEmail(accessToken);
        if (response) {
          successMessage.value =
            "Новый код подтверждения отправлен на ваш email!";
          startCooldown();
        }
      } catch (err) {
        errorMessage.value =
          error.value || "Ошибка при отправке кода. Попробуйте позже.";
      } finally {
        resendLoading.value = false;
      }
    };

    onMounted(() => {
      // При загрузке страницы сразу запускаем таймер
      startCooldown();
    });

    return {
      confirmationCode,
      errorMessage,
      successMessage,
      loading,
      resendLoading,
      resendCooldown,
      isCodeValid,
      handleSubmit,
      resendCode,
      validateCode,
    };
  },
});
</script>

<style scoped>
@import '../../styles/auth-form-styles.css';
</style>
