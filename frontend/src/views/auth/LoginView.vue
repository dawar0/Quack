<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoAlert from '@/components/ui/NeoAlert.vue'
import { toastService } from '@/services/toastService'

const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const login = async (event) => {
  // Ensure we prevent default
  event.preventDefault()

  if (!email.value || !password.value) {
    error.value = 'Please fill in all fields'
    toastService.error('Please fill in all fields')
    return
  }

  try {
    loading.value = true
    error.value = null
    const success = await authStore.login({
      email: email.value,
      password: password.value
    })
    if (success && authStore.user) {
      const user = authStore.user
      toastService.success(`Welcome back, ${user.name || 'User'}!`)

      if (user.roles && user.roles.length > 0) {
        const roleNames = user.roles.map(role => role.name)
        if (roleNames.includes('admin')) {
          router.push('/admin')
        } else if (roleNames.includes('professional')) {
          router.push('/professional')
        } else if (roleNames.includes('customer')) {
          router.push('/customer')
        } else {
          error.value = 'Invalid user role'
          toastService.error('Invalid user role')
          await authStore.logout()
        }
      } else {
        error.value = 'User has no assigned roles'
        toastService.error('User has no assigned roles')
        await authStore.logout()
      }
    } else {
      error.value = authStore.error || 'Login failed'
      toastService.error(authStore.error || 'Login failed')
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = authStore.error || err.response?.data?.message || 'An unexpected error occurred'
    toastService.error(authStore.error || err.response?.data?.message || 'An unexpected error occurred')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="neo-container">
    <div class="neo-card-container">
      <NeoCard variant="primary">
        <template #title>
          <h2 class="text-center">LOGIN</h2>
        </template>

        <NeoAlert v-if="error" variant="danger">
          {{ error }}
        </NeoAlert>

        <form @submit.prevent="login($event)" class="neo-form">
          <NeoInput id="email" v-model="email" type="email" label="Email" placeholder="Enter your email" required
            variant="primary" />

          <NeoInput id="password" v-model="password" type="password" label="Password" placeholder="Enter your password"
            required variant="primary" />

          <div class="d-grid gap-2">
            <NeoButton type="submit" variant="success" size="lg" block :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ loading ? 'LOGGING IN...' : 'LOGIN' }}
            </NeoButton>
          </div>
        </form>

        <div class="text-center mt-4 neo-link-container">
          <p class="mb-0">
            Don't have an account?
            <router-link to="/register" class="neo-link">REGISTER</router-link>
          </p>
        </div>
      </NeoCard>
    </div>
  </div>
</template>

<style scoped>
.neo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.neo-card-container {
  width: 100%;
  max-width: 500px;
}

.neo-form {
  padding: 1rem 0;
}

.neo-link-container {
  background: #fff;
  border: 3px solid #000;
  padding: 0.75rem;
  margin-top: 1.5rem;
  font-weight: bold;
}

.neo-link {
  font-weight: 900;
  color: #ff7f50;
  text-decoration: none;
  position: relative;
  padding-bottom: 2px;
  border-bottom: 3px solid #000;
  transition: all 0.2s;
}

.neo-link:hover {
  color: #ff5555;
  transform: translateY(-2px);
  display: inline-block;
}
</style>
