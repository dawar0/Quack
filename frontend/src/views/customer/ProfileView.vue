<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import {
  NeoCard,
  NeoButton,
  NeoInput,
  NeoAlert,
  NeoModal,
  NeoBadge,
  NeoIcon
} from '@/components/ui'
import { toastService } from '@/services/toastService'
import { customerAPI } from '@/services/api' // Import customer API

// Store for auth operations
const authStore = useAuthStore()

// User profile data
const profile = ref({
  id: null,
  name: '',
  email: '',
  phone_number: '',
  address: '',
  profileImage: 'https://avatar.iran.liara.run/public/11', // Default fallback
  joinDate: '',
})

// Edit mode state
const isEditMode = ref(false)
const isLoading = ref(false)
const error = ref(null)

// Form for editing profile data
const editForm = ref({
  name: '',
  phone_number: '',
  address: '',
})

// State for modals
const showConfirmModal = ref(false)
const confirmAction = ref(null)
const confirmMessage = ref('')
const showFeedbackModal = ref(false)
const feedbackTitle = ref('')
const feedbackMessage = ref('')

// Change password state
const showChangePasswordModal = ref(false)
const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
})
const passwordError = ref(null)
const passwordLoading = ref(false)

// File input reference for profile picture
const profilePictureInput = ref(null)

// Helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  // Check if customerAPI exists and has the getProfilePictureUrl method
  if (customerAPI && typeof customerAPI.getProfilePictureUrl === 'function') {
    return filename ? customerAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
  }
  // Fallback if API not available
  return 'https://avatar.iran.liara.run/public/11'
}

// Fetch user profile on component mount
onMounted(async () => {
  try {
    isLoading.value = true
    await authStore.fetchUser()

    // Set profile data
    if (authStore.user) {
      // Safely get profile image URL with error handling
      let profileImageUrl = 'https://avatar.iran.liara.run/public/11'
      try {
        profileImageUrl = getProfileImageUrl(authStore.user.profile_image)
      } catch (imageErr) {
        console.error('Error loading profile image:', imageErr)
      }

      profile.value = {
        ...authStore.user,
        profileImage: profileImageUrl,
        joinDate: authStore.user.date_created || '',
      }

      // Initialize edit form with current profile data
      editForm.value = {
        name: profile.value.name || '',
        phone_number: profile.value.phone_number || '',
        address: profile.value.address || '',
      }
    }
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load profile data'
    toastService.error('Failed to load profile data')
  } finally {
    isLoading.value = false
  }
})

// Toggle edit mode
const toggleEditMode = () => {
  if (isEditMode.value) {
    // Reset form to original values
    editForm.value = {
      name: profile.value.name || '',
      phone_number: profile.value.phone_number || '',
      address: profile.value.address || '',
    }
  }
  isEditMode.value = !isEditMode.value
  error.value = null
}

// Save profile changes
const saveProfile = async () => {
  try {
    isLoading.value = true
    error.value = null

    // Validate form fields
    if (!editForm.value.name) {
      error.value = 'Name is required'
      toastService.error('Name is required')
      return
    }

    // Use the customer API to update profile
    await customerAPI.updateProfile({
      name: editForm.value.name,
      phone_number: editForm.value.phone_number,
      address: editForm.value.address,
    })

    // Update local state
    profile.value = {
      ...profile.value,
      name: editForm.value.name,
      phone_number: editForm.value.phone_number,
      address: editForm.value.address,
    }

    // Refresh user data in auth store
    await authStore.fetchUser()

    // Exit edit mode
    isEditMode.value = false

    // Show success message
    toastService.success('Profile updated successfully!')
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || 'Failed to update profile'
    toastService.error(err.response?.data?.message || 'Failed to update profile')
  } finally {
    isLoading.value = false
  }
}

// Open change password modal
const openChangePasswordModal = () => {
  // Reset form
  passwordForm.value = {
    currentPassword: '',
    newPassword: '',
    confirmPassword: '',
  }
  passwordError.value = null
  showChangePasswordModal.value = true
}

// Change password
const changePassword = async () => {
  try {
    passwordLoading.value = true
    passwordError.value = null

    // Validate form
    if (!passwordForm.value.currentPassword || !passwordForm.value.newPassword || !passwordForm.value.confirmPassword) {
      passwordError.value = 'All fields are required'
      toastService.error('All password fields are required')
      return
    }

    if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
      passwordError.value = 'New passwords do not match'
      toastService.error('New passwords do not match')
      return
    }

    if (passwordForm.value.newPassword.length < 8) {
      passwordError.value = 'New password must be at least 8 characters long'
      toastService.error('New password must be at least 8 characters long')
      return
    }

    // Call API to change password using customerAPI
    await customerAPI.changePassword({
      current_password: passwordForm.value.currentPassword,
      new_password: passwordForm.value.newPassword
    })

    // Close modal and show success message
    showChangePasswordModal.value = false
    toastService.success('Password changed successfully!')
  } catch (err) {
    console.error(err)
    passwordError.value = err.response?.data?.message || 'Failed to change password'
    toastService.error(err.response?.data?.message || 'Failed to change password')
  } finally {
    passwordLoading.value = false
  }
}

// Handle profile picture change
const handleProfilePictureChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    const formData = new FormData()
    formData.append('profile_picture', file)

    // Use the customerAPI.updateProfilePicture method
    await customerAPI.updateProfilePicture(formData)

    // Refresh user data in auth store
    await authStore.fetchUser()

    // Update profile image in UI with timestamp to prevent caching
    if (authStore.user && authStore.user.profile_image) {
      profile.value.profileImage = getProfileImageUrl(authStore.user.profile_image)
    }

    toastService.success('Profile picture updated successfully!')
  } catch (err) {
    console.error('Failed to update profile picture:', err)
    toastService.error(err.response?.data?.message || 'Failed to update profile picture')
  }
}



// Delete account confirmation and handling
const confirmDeleteAccount = () => {
  confirmMessage.value = 'Are you sure you want to delete your account? This action cannot be undone.'
  confirmAction.value = deleteAccount
  showConfirmModal.value = true
}

// Delete account
const deleteAccount = async () => {
  try {
    isLoading.value = true

    // Use customerAPI to delete account
    await customerAPI.deleteAccount()

    // Show success message and logout
    toastService.success('Your account has been successfully deleted')

    // Logout after account deletion
    setTimeout(() => {
      authStore.logout()
    }, 2000)
  } catch (err) {
    console.error(err)
    toastService.error(err.response?.data?.message || 'Failed to delete account')
  } finally {
    isLoading.value = false
    showConfirmModal.value = false
  }
}
</script>

<template>
  <div class="container py-4 neo-brutalist">
    <h1 class="page-title mb-4">My Profile</h1>

    <div class="row g-4">
      <!-- Main Profile Card -->
      <div class="col-lg-8">
        <NeoCard variant="primary">
          <template #header>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold text-uppercase">Profile Information</h5>
              <NeoButton :variant="isEditMode ? 'dark' : 'success'" @click="toggleEditMode">
                <NeoIcon :name="isEditMode ? 'x' : 'edit'" size="16" class="me-1" />
                {{ isEditMode ? 'Cancel' : 'Edit Profile' }}
              </NeoButton>
            </div>
          </template>

          <!-- Profile information in view mode -->
          <div v-if="!isEditMode">
            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Name</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ profile.name }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ profile.email }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Phone</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ profile.phone_number }}</p>
                </div>
              </div>
            </div>

            <div class="mb-4 p-3 bg-light border border-dark border-3">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 fw-bold text-uppercase">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ profile.address }}</p>
                </div>
              </div>
            </div>


          </div>

          <!-- Profile information in edit mode -->
          <form v-else>
            <NeoInput label="Name" id="name" v-model="editForm.name" variant="primary" class="mb-3" />

            <NeoInput label="Email" id="email" type="email" v-model="profile.email" variant="primary" class="mb-3"
              disabled />

            <NeoInput label="Phone" id="phone" type="tel" v-model="editForm.phone_number" variant="primary"
              class="mb-3" />

            <NeoInput label="Address" id="address" v-model="editForm.address" variant="primary" class="mb-4" />

            <div class="d-grid">
              <NeoButton variant="success" size="lg" @click="saveProfile">
                <NeoIcon name="save" size="16" class="me-1" />
                Save Changes
              </NeoButton>
            </div>
          </form>
        </NeoCard>
      </div>

      <!-- Side Profile Card with Picture and Actions -->
      <div class="col-lg-4">
        <!-- Profile Picture Card -->
        <NeoCard variant="success">
          <div class="text-center py-4">
            <img :src="`${profile.profileImage}?timestamp=${Date.now()}`" alt="Profile picture"
              class="rounded-circle img-fluid mb-3 border border-dark border-3"
              style="width: 150px; height: 150px; object-fit: cover" />
            <h5 class="mb-0 fw-bold text-uppercase">{{ profile.name }}</h5>
            <p class="mb-2 fw-bold">Customer</p>
            <div class="d-flex justify-content-center gap-2 mb-3">
              <NeoBadge variant="primary"> ID: {{ profile.id }} </NeoBadge>
            </div>

            <div class="position-relative d-inline-block">
              <input type="file" accept="image/*" class="d-none" ref="profilePictureInput"
                @change="handleProfilePictureChange" />
              <NeoButton variant="dark" @click="profilePictureInput.click()">
                <NeoIcon name="camera" size="16" class="me-1" />
                Change Picture
              </NeoButton>
            </div>
          </div>
        </NeoCard>

        <!-- Account Actions (Security) -->
        <NeoCard variant="danger" class="mt-4">
          <template #header>
            <h5 class="mb-0 fw-bold text-uppercase">Security</h5>
          </template>

          <NeoButton variant="dark" class="w-100 mb-3" @click="openChangePasswordModal">
            <NeoIcon name="lock" size="16" class="me-1" />
            Change Password
          </NeoButton>

          <!-- Delete Account Button -->
          <NeoButton variant="danger" class="w-100" @click="confirmDeleteAccount()">
            <NeoIcon name="trash" size="16" class="me-1" />
            Delete Account
          </NeoButton>
        </NeoCard>


      </div>
    </div>

    <!-- Change Password Modal -->
    <NeoModal v-model="showChangePasswordModal" title="Change Password">
      <NeoAlert v-if="passwordError" variant="danger" class="mb-3">
        {{ passwordError }}
      </NeoAlert>

      <NeoInput label="Current Password" id="currentPassword" type="password" v-model="passwordForm.currentPassword"
        placeholder="Enter current password" variant="danger" class="mb-3" />

      <NeoInput label="New Password" id="newPassword" type="password" v-model="passwordForm.newPassword"
        placeholder="Enter new password" variant="danger" class="mb-3" />

      <NeoInput label="Confirm New Password" id="confirmPassword" type="password" v-model="passwordForm.confirmPassword"
        placeholder="Confirm new password" variant="danger" class="mb-3" />

      <template #footer>
        <NeoButton variant="secondary" @click="showChangePasswordModal = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="changePassword">Change Password</NeoButton>
      </template>
    </NeoModal>

    <!-- Feedback Modal -->
    <NeoModal v-model="showFeedbackModal" :title="feedbackTitle" size="sm">
      <div class="text-center">
        <NeoIcon name="check-circle" size="48" class="text-success" />
        <p class="mt-3">{{ feedbackMessage }}</p>
      </div>
      <template #footer>
        <NeoButton variant="success" @click="showFeedbackModal = false">OK</NeoButton>
      </template>
    </NeoModal>

    <!-- Confirm Modal -->
    <NeoModal v-model="showConfirmModal" title="Confirm Action">
      <NeoAlert variant="warning" class="mb-0">
        {{ confirmMessage }}
      </NeoAlert>
      <template #footer>
        <NeoButton variant="secondary" @click="showConfirmModal = false">Cancel</NeoButton>
        <NeoButton variant="danger" @click="confirmAction">Yes, Continue</NeoButton>
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

.table> :not(caption)>*>* {
  padding: 0.75rem;
}

.table>thead {
  vertical-align: bottom;
}

.table>thead th {
  font-weight: bold;
  letter-spacing: 1px;
}
</style>
