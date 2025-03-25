<script setup>
import { ref } from 'vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoBadge from '@/components/ui/NeoBadge.vue'

// Sample professional data (would come from API in real implementation)
const professionalData = ref({
  id: 'P1001',
  name: 'Mike Smith',
  email: 'mike.smith@example.com',
  phone: '+91 9876543210',
  address: '456 Park Avenue, Mumbai, Maharashtra, 400001',
  joinDate: '2023-02-10',
  profileImage: 'https://randomuser.me/api/portraits/men/41.jpg',
  serviceType: 'Plumbing',
  experience: '8 years',
  hourlyRate: '₹500',
  description:
    'Experienced plumber with expertise in residential and commercial plumbing services. Specialized in fixing leaks, installing new plumbing systems, and handling emergency repairs.',
  status: 'Approved',
  rating: 4.8,
  completedJobs: 37,
})

// Edit mode state
const isEditMode = ref(false)
const editableUserData = ref({ ...professionalData.value })

// Toggle edit mode
const toggleEditMode = () => {
  if (isEditMode.value) {
    // If we're exiting edit mode, reset the editable data
    editableUserData.value = { ...professionalData.value }
  }
  isEditMode.value = !isEditMode.value
}

// Save user data changes
const saveUserData = () => {
  // In a real application, this would call an API to update user data
  professionalData.value = { ...editableUserData.value }
  isEditMode.value = false

  // Show success message (would use a toast/notification in real app)
  alert('Profile updated successfully')
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
    alert('Please fill all password fields')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    alert('New password and confirmation do not match')
    return
  }

  if (newPassword.value.length < 8) {
    alert('New password must be at least 8 characters long')
    return
  }

  // In a real application, this would call an API to change the password
  alert('Password changed successfully')

  // Reset form and hide it
  currentPassword.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  showPasswordForm.value = false
}

// Get status badge variant
const getStatusBadgeVariant = (status) => {
  const statusVariants = {
    Approved: 'success',
    Pending: 'warning',
    Blocked: 'danger',
  }
  return statusVariants[status] || 'secondary'
}
</script>

<template>
  <div class="container py-4 neo-brutalist">
    <h1 class="page-title mb-4">My Profile</h1>

    <div class="row g-4">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Basic Information Card -->
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
                  <p class="mb-0">{{ professionalData.name }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.email }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Phone</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.phone }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.address }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Service Type</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.serviceType }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Experience</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.experience }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Hourly Rate</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.hourlyRate }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Description</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.description }}</p>
                </div>
              </div>
            </div>

            <div class="p-3 bg-light border border-dark border-3">
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Status</p>
                </div>
                <div class="col-sm-9">
                  <NeoBadge :variant="getStatusBadgeVariant(professionalData.status)">
                    {{ professionalData.status }}
                  </NeoBadge>
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
              class="mb-3"
            />

            <NeoInput
              label="Experience"
              id="experience"
              v-model="editableUserData.experience"
              variant="primary"
              class="mb-3"
            />

            <NeoInput
              label="Hourly Rate"
              id="hourlyRate"
              v-model="editableUserData.hourlyRate"
              variant="primary"
              class="mb-3"
            />

            <NeoInput
              label="Description"
              id="description"
              v-model="editableUserData.description"
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
              :src="professionalData.profileImage"
              alt="Profile picture"
              class="rounded-circle img-fluid mb-3 border border-dark border-3"
              style="width: 150px; height: 150px; object-fit: cover"
            />
            <h5 class="mb-0 fw-bold text-uppercase">{{ professionalData.name }}</h5>
            <p class="mb-2 fw-bold">
              {{ professionalData.serviceType }}
            </p>
            <div class="d-flex justify-content-center gap-2 mb-3">
              <NeoBadge variant="primary">
                {{ professionalData.completedJobs }} Jobs Completed
              </NeoBadge>
              <NeoBadge :variant="getStatusBadgeVariant(professionalData.status)">
                {{ professionalData.status }}
              </NeoBadge>
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
              <NeoButton variant="success" @click="changePassword"> Update Password </NeoButton>
            </div>
          </form>
        </NeoCard>

        <!-- Stats Card -->
        <NeoCard variant="primary">
          <template #header>
            <h5 class="mb-0 fw-bold text-uppercase">Stats</h5>
          </template>

          <div class="border border-dark border-3 mb-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Total Jobs</span>
              <span>{{ professionalData.completedJobs }}</span>
            </div>
          </div>

          <div class="border border-dark border-3 mb-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Rating</span>
              <span class="text-warning">
                <i class="fas fa-star"></i> {{ professionalData.rating }}
              </span>
            </div>
          </div>

          <div class="border border-dark border-3 mb-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Member Since</span>
              <span>{{ professionalData.joinDate }}</span>
            </div>
          </div>

          <div class="border border-dark border-3">
            <div class="d-flex justify-content-between p-3 bg-light fw-bold">
              <span class="text-uppercase">Status</span>
              <NeoBadge :variant="getStatusBadgeVariant(professionalData.status)">
                {{ professionalData.status }}
              </NeoBadge>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.neo-brutalist {
  font-family: 'Inter', sans-serif;
}

.neo-brutalist h1 {
  font-size: 3rem;
  letter-spacing: -0.5px;
}

.fw-black {
  font-weight: 900;
}

.form-check-input {
  cursor: pointer;
}

.form-check-input:checked {
  background-color: #000;
  border-color: #000;
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
