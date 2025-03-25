<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoAlert from '@/components/ui/NeoAlert.vue'

const router = useRouter()
const email = ref('')
const password = ref('')
const role = ref('customer') // Default role
const errorMessage = ref('')
const isLoading = ref(false)

const login = async () => {
  // Basic validation
  if (!email.value || !password.value) {
    errorMessage.value = 'Please fill in all fields'
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''

    // This is a mock authentication - in a real app, this would call an API
    // For demo purposes, we'll simulate success and store in localStorage
    const mockToken = 'mock-jwt-token'
    localStorage.setItem('token', mockToken)
    localStorage.setItem('role', role.value)

    // Navigate based on role
    if (role.value === 'admin') {
      router.push('/admin')
    } else if (role.value === 'professional') {
      router.push('/professional')
    } else {
      router.push('/customer')
    }
  } catch (error) {
    errorMessage.value = error.message || 'Login failed'
  } finally {
    isLoading.value = false
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

        <NeoAlert v-if="errorMessage" variant="danger">
          {{ errorMessage }}
        </NeoAlert>

        <form @submit.prevent="login" class="neo-form">
          <NeoInput
            id="email"
            v-model="email"
            type="email"
            label="Email"
            placeholder="Enter your email"
            required
            variant="primary"
          />

          <NeoInput
            id="password"
            v-model="password"
            type="password"
            label="Password"
            placeholder="Enter your password"
            required
            variant="primary"
          />

          <div class="mb-4">
            <label class="neobrutalism-label">LOGIN AS</label>
            <div class="d-flex justify-content-between neo-radio-group">
              <div class="neo-radio">
                <input
                  class="neo-radio-input"
                  type="radio"
                  name="userRole"
                  id="customerRole"
                  value="customer"
                  v-model="role"
                />
                <label class="neo-radio-label" for="customerRole"> Customer </label>
              </div>
              <div class="neo-radio">
                <input
                  class="neo-radio-input"
                  type="radio"
                  name="userRole"
                  id="professionalRole"
                  value="professional"
                  v-model="role"
                />
                <label class="neo-radio-label" for="professionalRole"> Professional </label>
              </div>
              <div class="neo-radio">
                <input
                  class="neo-radio-input"
                  type="radio"
                  name="userRole"
                  id="adminRole"
                  value="admin"
                  v-model="role"
                />
                <label class="neo-radio-label" for="adminRole"> Admin </label>
              </div>
            </div>
          </div>

          <div class="d-grid gap-2">
            <NeoButton type="submit" variant="success" size="lg" block :disabled="isLoading">
              <span
                v-if="isLoading"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              {{ isLoading ? 'LOGGING IN...' : 'LOGIN' }}
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

.neobrutalism-label {
  font-weight: bold;
  text-transform: uppercase;
  font-size: 0.9rem;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
  display: block;
}

.neo-radio-group {
  background: #fff;
  border: 3px solid #000;
  padding: 1rem;
}

.neo-radio {
  position: relative;
  margin-right: 1rem;
}

.neo-radio-input {
  appearance: none;
  -webkit-appearance: none;
  width: 1.5rem;
  height: 1.5rem;
  border: 3px solid #000;
  border-radius: 0;
  background-color: #fff;
  margin-right: 0.5rem;
  vertical-align: middle;
  position: relative;
  cursor: pointer;
}

.neo-radio-input:checked {
  background-color: #ff7f50;
}

.neo-radio-input:checked:after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0.5rem;
  height: 0.5rem;
  background-color: #000;
}

.neo-radio-input:focus {
  box-shadow: 3px 3px 0 #000;
  outline: none;
}

.neo-radio-label {
  font-weight: bold;
  cursor: pointer;
  text-transform: uppercase;
  font-size: 0.85rem;
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
