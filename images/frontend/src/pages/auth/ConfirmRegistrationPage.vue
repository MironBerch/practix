<template>
  <div class="auth-page">
    <h1>Confirm Registration</h1>
    <p>Please enter the 6-digit verification code sent to your email</p>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="code">Verification Code</label>
        <input
          v-model="code"
          type="text"
          id="code"
          required
          maxlength="6"
          placeholder="123456"
          @input="validateCode"
        >
        <p v-if="code.length > 0 && !isValidCode" class="input-hint">
          Code must be exactly 6 digits
        </p>
      </div>
      
      <button 
        type="submit" 
        :disabled="loading || !isValidCode"
        class="submit-btn"
      >
        <span v-if="loading">Verifying...</span>
        <span v-else>Confirm Registration</span>
      </button>
      
      <p v-if="error" class="error-message">
        {{ error }}
      </p>
    </form>
    
    <div class="resend-section">
      <p>Didn't receive a code?</p>
      <button
        @click="handleResend"
        :disabled="resendLoading || resendCooldown > 0"
        class="resend-btn"
      >
        <template v-if="resendLoading">Sending...</template>
        <template v-else>
          Resend Code 
          <span v-if="resendCooldown > 0">({{ resendCooldown }}s)</span>
        </template>
      </button>
      
      <p v-if="resendSuccess" class="success-message">
        New verification code has been sent!
      </p>
    </div>
  </div>
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuth } from '../../composables/useAuth'

  export default defineComponent({
    name: 'ConfirmRegistrationPage',
    
    setup() {
      const router = useRouter()
      const route = useRoute()
      const { 
        confirmRegistration, 
        resendConfirmRegistrationEmail,
        loading, 
        error 
      } = useAuth()
      
      const code = ref('')
      const temp_token = ref(route.query.temp_token as string)
      const isValidCode = ref(false)
      const resendLoading = ref(false)
      const resendSuccess = ref(false)
      const resendCooldown = ref(0)
      
      let cooldownTimer: number

      // Validate code format (6 digits)
      const validateCode = () => {
        isValidCode.value = /^\d{6}$/.test(code.value)
      }

      // Handle code submission
      const handleSubmit = async () => {
        if (!isValidCode.value) return
        
        const response = await confirmRegistration(
          { code: code.value }, 
          temp_token.value
        )
        
        if (response) {
          router.push({ 
            name: 'signin',
            query: { registered: 'true' } // Добавляем параметр для отображения успешного сообщения
          })
        }
      }

      // Handle resend code
      const handleResend = async () => {
        resendLoading.value = true
        resendSuccess.value = false
        error.value = null
        
        try {
          const response = await resendConfirmRegistrationEmail(temp_token.value)
          if (response) {
            resendSuccess.value = true
            startCooldown()
          }
        } finally {
          resendLoading.value = false
        }
      }

      // Start cooldown timer (60 seconds)
      const startCooldown = () => {
        resendCooldown.value = 60
        clearInterval(cooldownTimer)
        cooldownTimer = setInterval(() => {
          resendCooldown.value--
          if (resendCooldown.value <= 0) {
            clearInterval(cooldownTimer)
          }
        }, 1000)
      }

      onMounted(() => {
        if (!temp_token.value) {
          router.push({ name: 'signup' })
        }
        startCooldown() // Initial cooldown
      })

      return {
        code,
        temp_token,
        isValidCode,
        loading,
        error,
        resendLoading,
        resendSuccess,
        resendCooldown,
        handleSubmit,
        handleResend,
        validateCode
      }
    }
  })
</script>
