<script setup>
import { ref } from 'vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoBadge from '@/components/ui/NeoBadge.vue'
import NeoModal from '@/components/ui/NeoModal.vue'

// Sample user data (would come from API in real implementation)
const userData = ref({
  id: 'C1001',
  name: 'John Doe',
  email: 'john.doe@example.com',
  phone: '+91 9876543210',
  address: '123 Main Street, Mumbai, Maharashtra, 400001',
  joinDate: '2023-01-15',
  profileImage: 'https://randomuser.me/api/portraits/men/32.jpg',
})

// Edit mode state
const isEditMode = ref(false)
const editableUserData = ref({ ...userData.value })

// Modal states
const showSuccessModal = ref(false)
const showPasswordSuccessModal = ref(false)
const showPasswordErrorModal = ref(false)
const passwordErrorMessage = ref('')

// Toggle edit mode
const toggleEditMode = () => {
  if (isEditMode.value) {
    // If we're exiting edit mode, reset the editable data
    editableUserData.value = { ...userData.value }
  }
  isEditMode.value = !isEditMode.value
}

// Save user data changes
const saveUserData = () => {
  // In a real application, this would call an API to update user data
  userData.value = { ...editableUserData.value }
  isEditMode.value = false

  // Show success message
  showSuccessModal.value = true
}

// Change password
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showPasswordForm = ref(false)

// Toggle password form visibility
const togglePasswordForm = () => {
  showPasswordForm.value = !showPasswordForm.value

  if (!showPasswordForm.value) {
    // Reset form when hiding
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
  }
}

// Change password functionality
const changePassword = () => {
  // Validation
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    passwordErrorMessage.value = 'Please fill all password fields'
    showPasswordErrorModal.value = true
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    passwordErrorMessage.value = 'New password and confirmation do not match'
    showPasswordErrorModal.value = true
    return
  }

  if (newPassword.value.length < 8) {
    passwordErrorMessage.value = 'New password must be at least 8 characters long'
    showPasswordErrorModal.value = true
    return
  }

  // In a real application, this would call an API to change the password
  showPasswordSuccessModal.value = true

  // Reset form and hide it
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  showPasswordForm.value = false
}
</script>

<template>
  <div class="container py-4 neo-brutalist">
    <h1 class="page-title mb-4">My Profile</h1>

    <div class="row g-4">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Profile Information Card -->
        <NeoCard class="mb-4" variant="primary">
          <template #header>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold text-uppercase">Profile Information</h5>
              <NeoButton :variant="isEditMode ? 'dark' : 'success'" @click="toggleEditMode">
                {{ isEditMode ? 'Cancel' : 'Edit Profile' }}
              </NeoButton>
            </div>
          </template>

          <!-- View Mode -->
          <div v-if="!isEditMode">
            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Name</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.name }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.email }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Phone</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.phone }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.address }}</p>
                </div>
              </div>
            </div>

            <div class="p-3 bg-light border border-dark border-3">
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Member Since</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.joinDate }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Edit Mode -->
          <form v-else>
            <NeoInput
              label="Name"
              id="name"
              v-model="editableUserData.name"
              variant="primary"
              class="mb-3"
            />

            <NeoInput
              label="Email"
              id="email"
              type="email"
              v-model="editableUserData.email"
              variant="primary"
              class="mb-3"
            />

            <NeoInput
              label="Phone"
              id="phone"
              type="tel"
              v-model="editableUserData.phone"
              variant="primary"
              class="mb-3"
            />

            <NeoInput
              label="Address"
              id="address"
              v-model="editableUserData.address"
              variant="primary"
              class="mb-4"
            />

            <div class="d-grid">
              <NeoButton variant="success" size="lg" @click="saveUserData">
                Save Changes
              </NeoButton>
            </div>
          </form>
        </NeoCard>
      </div>

      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Profile Picture Card -->
        <NeoCard class="mb-4" variant="success">
          <div class="text-center py-4">
            <img
              :src="userData.profileImage"
              alt="Profile picture"
              class="rounded-circle img-fluid mb-3 border border-dark border-3"
              style="width: 150px; height: 150px; object-fit: cover"
            />
            <h5 class="mb-0 fw-bold text-uppercase">{{ userData.name }}</h5>
            <p class="mb-2 fw-bold">Customer</p>
            <div class="d-flex justify-content-center gap-2 mb-3">
              <NeoBadge variant="primary"> ID: {{ userData.id }} </NeoBadge>
            </div>
            <NeoButton variant="dark">Change Picture</NeoButton>
          </div>
        </NeoCard>

        <!-- Security Card -->
        <NeoCard class="mb-4" variant="danger">
          <template #header>
            <h5 class="mb-0 fw-bold text-uppercase">Security</h5>
          </template>

          <NeoButton variant="dark" class="w-100 mb-3" @click="togglePasswordForm">
            Change Password
          </NeoButton>

          <!-- Change Password Form -->
          <form v-if="showPasswordForm" class="mt-3">
            <NeoInput
              label="Current Password"
              id="currentPassword"
              type="password"
              v-model="currentPassword"
              placeholder="Enter current password"
              variant="danger"
              class="mb-3"
            />

            <NeoInput
              label="New Password"
              id="newPassword"
              type="password"
              v-model="newPassword"
              placeholder="Enter new password"
              variant="danger"
              class="mb-3"
            />

            <NeoInput
              label="Confirm New Password"
              id="confirmPassword"
              type="password"
              v-model="confirmPassword"
              placeholder="Confirm new password"
              variant="danger"
              class="mb-3"
            />

            <div class="d-grid">
              <NeoButton variant="success" @click="changePassword">Update Password</NeoButton>
            </div>
          </form>
        </NeoCard>

        <!-- Stats Card -->
        <NeoCard variant="primary">
          <template #header>
            <h5 class="mb-0 fw-bold text-uppercase">Account Info</h5>
          </template>

          <div class="border border-dark border-3 mb-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">ID</span>
              <span>{{ userData.id }}</span>
            </div>
          </div>

          <div class="border border-dark border-3 mb-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Status</span>
              <NeoBadge variant="success">Active</NeoBadge>
            </div>
          </div>

          <div class="border border-dark border-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Member Since</span>
              <span>{{ userData.joinDate }}</span>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>

    <!-- Success Modal for Profile Update -->
    <NeoModal v-model="showSuccessModal" title="Success" size="sm">
      <div class="text-center">
        <i class="bi bi-check-circle text-success" style="font-size: 3rem"></i>
        <p class="mt-3">Profile updated successfully!</p>
      </div>
      <template #footer>
        <NeoButton variant="success" @click="showSuccessModal = false">OK</NeoButton>
      </template>
    </NeoModal>

    <!-- Success Modal for Password Change -->
    <NeoModal v-model="showPasswordSuccessModal" title="Success" size="sm">
      <div class="text-center">
        <i class="bi bi-check-circle text-success" style="font-size: 3rem"></i>
        <p class="mt-3">Password changed successfully!</p>
      </div>
      <template #footer>
        <NeoButton variant="success" @click="showPasswordSuccessModal = false">OK</NeoButton>
      </template>
    </NeoModal>

    <!-- Error Modal for Password Validation -->
    <NeoModal v-model="showPasswordErrorModal" title="Error" size="sm">
      <div class="text-center">
        <i class="bi bi-exclamation-triangle text-danger" style="font-size: 3rem"></i>
        <p class="mt-3">{{ passwordErrorMessage }}</p>
      </div>
      <template #footer>
        <NeoButton variant="danger" @click="showPasswordErrorModal = false">OK</NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
.neo-brutalist {
  font-family: 'Inter', sans-serif;
}

.page-title {
  font-size: 3rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
  margin-bottom: 2rem;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 0;
  width: 80px;
  height: 6px;
  background-color: #ff7f50;
}

.fw-black {
  font-weight: 900;
}

/* Override table styles */
.table {
  --bs-table-bg: transparent;
  --bs-table-border-color: #000;
}

.table-bordered {
  border-collapse: separate;
  border-spacing: 0;
}

.table > :not(caption) > * > * {
  padding: 0.75rem;
}

.table > thead {
  vertical-align: bottom;
}

.table > thead th {
  font-weight: bold;
  letter-spacing: 1px;
}
</style>
