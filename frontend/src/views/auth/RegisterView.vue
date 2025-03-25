<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoSelect from '@/components/ui/NeoSelect.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoAlert from '@/components/ui/NeoAlert.vue'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const role = ref('customer') // Default role
const phone = ref('')
const address = ref('')
const errorMessage = ref('')
const isLoading = ref(false)

// Additional fields for professionals
const serviceType = ref('')
const experience = ref('')
const description = ref('')

const serviceTypes = [
  { value: 'plumbing', label: 'Plumbing' },
  { value: 'electrical', label: 'Electrical' },
  { value: 'cleaning', label: 'Cleaning' },
  { value: 'gardening', label: 'Gardening' },
  { value: 'carpentry', label: 'Carpentry' },
  { value: 'painting', label: 'Painting' },
]

const register = async () => {
  // Basic validation
  if (!name.value || !email.value || !password.value || !confirmPassword.value) {
    errorMessage.value = 'Please fill in all required fields'
    return
  }

  if (password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  if (role.value === 'professional' && !serviceType.value) {
    errorMessage.value = 'Please select a service type'
    return
  }

  try {
    isLoading.value = true
    errorMessage.value = ''

    // This is a mock registration - in a real app, this would call an API
    // For demo purposes, we'll simulate success and redirect to login

    // If it's a professional, show a notification about approval process
    if (role.value === 'professional') {
      alert(
        'Thank you for registering as a service professional. Your account will be reviewed by an admin before approval.',
      )
    }

    router.push('/login')
  } catch (error) {
    errorMessage.value = error.message || 'Registration failed'
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
          <h2 class="text-center">REGISTER</h2>
        </template>

        <NeoAlert v-if="errorMessage" variant="danger">
          {{ errorMessage }}
        </NeoAlert>

        <form @submit.prevent="register" class="neo-form">
          <div class="mb-4">
            <label class="neobrutalism-label">REGISTER AS</label>
            <div class="d-flex gap-4 neo-radio-group">
              <div class="neo-radio">
                <input
                  class="neo-radio-input"
                  type="radio"
                  name="userRole"
                  id="customerRole"
                  value="customer"
                  v-model="role"
                />
                <label class="neo-radio-label" for="customerRole">CUSTOMER</label>
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
                <label class="neo-radio-label" for="professionalRole"> SERVICE PROFESSIONAL </label>
              </div>
            </div>
          </div>

          <div class="row">
            <div class="col-md-12">
              <NeoInput
                id="name"
                v-model="name"
                type="text"
                label="Full Name"
                placeholder="Enter your full name"
                required
                variant="primary"
              />
            </div>

            <div class="col-md-12">
              <NeoInput
                id="email"
                v-model="email"
                type="email"
                label="Email"
                placeholder="Enter your email"
                required
                variant="primary"
              />
            </div>
          </div>

          <div class="row">
            <div class="col-md-12">
              <NeoInput
                id="password"
                v-model="password"
                type="password"
                label="Password"
                placeholder="Enter your password"
                required
                variant="primary"
              />
            </div>

            <div class="col-md-12">
              <NeoInput
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                label="Confirm Password"
                placeholder="Confirm your password"
                required
                variant="primary"
              />
            </div>
          </div>

          <div class="row">
            <div class="col-md-12">
              <NeoInput
                id="phone"
                v-model="phone"
                type="tel"
                label="Phone Number"
                placeholder="Enter your phone number"
                variant="primary"
              />
            </div>

            <div class="col-md-12">
              <NeoInput
                id="address"
                v-model="address"
                type="text"
                label="Address"
                placeholder="Enter your address"
                variant="primary"
              />
            </div>
          </div>

          <!-- Professional specific fields -->
          <div v-if="role === 'professional'" class="neo-professional-section">
            <h5 class="neo-section-title">PROFESSIONAL DETAILS</h5>

            <NeoSelect
              id="serviceType"
              v-model="serviceType"
              :options="serviceTypes"
              label="Service Type"
              placeholder="Select a service type"
              required
              variant="primary"
            />
            <div class="neo-form-hint">A professional can only provide one type of service</div>

            <NeoInput
              id="experience"
              v-model="experience"
              type="number"
              label="Years of Experience"
              placeholder="Years of experience"
              min="0"
              variant="primary"
            />

            <div class="mb-3">
              <label for="description" class="neobrutalism-label">Professional Description</label>
              <textarea
                class="neo-textarea"
                id="description"
                v-model="description"
                rows="3"
                placeholder="Describe your services and expertise"
              ></textarea>
            </div>

            <div class="mb-3">
              <label for="documents" class="neobrutalism-label">
                Upload Documents for Verification
              </label>
              <input type="file" class="neo-file-input" id="documents" multiple />
              <div class="neo-form-hint">
                Upload identification and professional certification documents
              </div>
            </div>
          </div>

          <div class="d-grid gap-2 mt-4">
            <NeoButton type="submit" variant="success" size="lg" block :disabled="isLoading">
              <span
                v-if="isLoading"
                class="spinner-border spinner-border-sm"
                role="status"
                aria-hidden="true"
              ></span>
              {{ isLoading ? 'REGISTERING...' : 'REGISTER' }}
            </NeoButton>
          </div>
        </form>

        <div class="text-center mt-4 neo-link-container">
          <p>
            Already have an account? <router-link to="/login" class="neo-link">LOGIN</router-link>
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
  max-width: 800px;
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

.neo-professional-section {
  background: #ffd700;
  border: 3px solid #000;
  padding: 1.5rem;
  margin: 1.5rem 0;
  position: relative;
}

.neo-section-title {
  position: absolute;
  top: -15px;
  left: 20px;
  background: #ffd700;
  padding: 0 10px;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.neo-textarea {
  width: 100%;
  border: 3px solid #000;
  border-radius: 0;
  padding: 0.6rem 0.75rem;
  font-family: monospace;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.neo-textarea:focus {
  box-shadow: 5px 5px 0 #000;
  transform: translate(-3px, -3px);
  outline: none;
}

.neo-file-input {
  display: block;
  width: 100%;
  padding: 0.6rem 0.75rem;
  font-family: monospace;
  border: 3px solid #000;
  border-radius: 0;
  transition: all 0.2s ease;
  background-color: #fff;
}

.neo-file-input:focus {
  box-shadow: 5px 5px 0 #000;
  transform: translate(-3px, -3px);
  outline: none;
}

.neo-form-hint {
  margin-top: -10px;
  margin-bottom: 15px;
  font-weight: bold;
  font-size: 0.75rem;
  background: #fff;
  border: 2px solid #000;
  display: inline-block;
  padding: 2px 8px;
  text-transform: uppercase;
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
