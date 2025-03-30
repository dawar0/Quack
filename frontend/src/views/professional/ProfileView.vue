<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { professionalAPI } from '@/services/api'
import { toastService } from '@/services/toastService'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoInput from '@/components/ui/NeoInput.vue'
import NeoIcon from '@/components/ui/NeoIcon.vue'

const authStore = useAuthStore()

// Professional data from auth store
const professionalData = ref({
  id: '',
  name: '',
  email: '',
  phone: '',
  joinDate: '',
  profileImage: '',
  serviceType: '',
  experience: '',
  description: '',
  status: '',
  rating: 0,
  completedJobs: 0,
})

// Document management
const documents = ref([])

// Edit mode state
const isEditMode = ref(false)
const editableUserData = ref({ ...professionalData.value })

// Change password
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showPasswordForm = ref(false)

// File input reference
const profilePictureInput = ref(null)

// Helper function to show feedback using toast service
const showFeedback = (title, message, variant = 'info') => {
  // Map variant to toast type
  const typeMap = {
    'success': 'success',
    'danger': 'error',
    'warning': 'warning',
    'info': 'info'
  }
  const type = typeMap[variant] || 'info'

  // Show toast with appropriate type
  toastService[type](`${title}: ${message}`)
}

// Initialize professional data from auth store
const initializeData = () => {
  const user = authStore.user
  if (user) {
    let profileImageUrl = user.profile_image
      ? professionalAPI.getProfilePictureUrl(user.profile_image)
      : 'https://avatar.iran.liara.run/public/11'

    professionalData.value = {
      id: user.id,
      name: user.name || '',
      email: user.email || '',
      phone: user.phone_number || '',
      joinDate: user.date_created || '',
      profileImage: profileImageUrl,
      serviceType: user.service_type || '',
      experience: user.experience || '',
      description: user.description || '',
      status: user.status || '',
      rating: user.rating || 0,
      completedJobs: user.completed_jobs || 0,
    }
    editableUserData.value = { ...professionalData.value }
  }
}

// Toggle edit mode
const toggleEditMode = () => {
  if (isEditMode.value) {
    // If we're exiting edit mode, reset the editable data
    editableUserData.value = { ...professionalData.value }
  }
  isEditMode.value = !isEditMode.value
}

// Save user data changes
const saveUserData = async () => {
  try {
    await professionalAPI.updateProfile({
      name: editableUserData.value.name,
      phone_number: editableUserData.value.phone,
      experience: editableUserData.value.experience,
      description: editableUserData.value.description,
    })

    // Update local data
    professionalData.value = { ...editableUserData.value }
    isEditMode.value = false

    // Refresh user data in auth store
    await authStore.fetchUser()

    showFeedback('Success', 'Profile updated successfully', 'success')
  } catch (error) {
    console.error('Failed to update profile:', error)
    showFeedback('Error', error.response?.data?.message || 'Failed to update profile', 'danger')
  }
}

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
const changePassword = async () => {
  // Validation
  if (!currentPassword.value || !newPassword.value || !confirmPassword.value) {
    showFeedback('Error', 'Please fill all password fields', 'danger')
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    showFeedback('Error', 'New password and confirmation do not match', 'danger')
    return
  }

  if (newPassword.value.length < 8) {
    showFeedback('Error', 'New password must be at least 8 characters long', 'danger')
    return
  }

  try {
    await professionalAPI.changePassword({
      current_password: currentPassword.value,
      new_password: newPassword.value,
    })

    // Reset form and hide it
    currentPassword.value = ''
    newPassword.value = ''
    confirmPassword.value = ''
    showPasswordForm.value = false

    showFeedback('Success', 'Password changed successfully', 'success')
  } catch (error) {
    console.error('Failed to change password:', error)
    showFeedback('Error', error.response?.data?.message || 'Failed to change password', 'danger')
  }
}

// Handle profile picture change
const handleProfilePictureChange = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    const formData = new FormData()
    formData.append('profile_picture', file)

    await professionalAPI.updateProfilePicture(formData)

    // Refresh user data in auth store
    await authStore.fetchUser()
    // Reinitialize with updated profile image
    initializeData()

    showFeedback('Success', 'Profile picture updated successfully', 'success')
  } catch (error) {
    console.error('Failed to update profile picture:', error)
    showFeedback('Error', error.response?.data?.message || 'Failed to update profile picture', 'danger')
  }
}

// Download document
const downloadDocument = async (doc) => {
  try {
    const response = await professionalAPI.downloadDocument(doc.id)

    // Create a blob from the response data
    const blob = new Blob([response.data], { type: response.headers['content-type'] })

    // Create a download link and trigger it
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', doc.file_name)
    document.body.appendChild(link)
    link.click()

    // Clean up
    window.URL.revokeObjectURL(url)
    link.remove()

    showFeedback('Success', 'Document download started', 'success')
  } catch (error) {
    console.error('Failed to download document:', error)
    showFeedback('Error', 'Failed to download document', 'danger')
  }
}

// Document management functions
const loadDocuments = async () => {
  try {
    const response = await professionalAPI.getDocuments()
    documents.value = response.data
  } catch (error) {
    console.error('Failed to load documents:', error)
    showFeedback('Error', 'Failed to load documents', 'danger')
  }
}


// Initialize data on component mount
onMounted(() => {
  initializeData()
  loadDocuments()
})
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
                <NeoIcon :name="isEditMode ? 'x' : 'edit'" size="16" class="me-1" />
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
                  <p class="mb-0 fw-bold text-uppercase">Description</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.description }}</p>
                </div>
              </div>
            </div>

          </div>

          <!-- Edit Mode -->
          <form v-else>
            <NeoInput label="Name" id="name" v-model="editableUserData.name" variant="primary" class="mb-3" />

            <NeoInput label="Phone" id="phone" type="tel" v-model="editableUserData.phone" variant="primary"
              class="mb-3" />

            <NeoInput label="Experience" id="experience" v-model="editableUserData.experience" variant="primary"
              class="mb-3" />

            <NeoInput label="Description" id="description" v-model="editableUserData.description" variant="primary"
              class="mb-4" />

            <div class="d-grid">
              <NeoButton variant="success" size="lg" @click="saveUserData">
                <NeoIcon name="save" size="16" class="me-1" />
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
            <img :src="`${professionalData.profileImage}?timestamp=${Date.now()}`" alt="Profile picture"
              class="rounded-circle img-fluid mb-3 border border-dark border-3"
              style="width: 150px; height: 150px; object-fit: cover" />
            <h5 class="mb-0 fw-bold text-uppercase">{{ professionalData.name }}</h5>
            <p class="mb-2 fw-bold">
              {{ professionalData.serviceType }}
            </p>

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

        <!-- Security Card -->
        <NeoCard class="mb-4" variant="danger">
          <template #header>
            <h5 class="mb-0 fw-bold text-uppercase">Security</h5>
          </template>

          <NeoButton variant="dark" class="w-100 mb-3" @click="togglePasswordForm">
            <NeoIcon name="lock" size="16" class="me-1" />
            Change Password
          </NeoButton>

          <!-- Change Password Form -->
          <form v-if="showPasswordForm" class="mt-3">
            <NeoInput label="Current Password" id="currentPassword" type="password" v-model="currentPassword"
              placeholder="Enter current password" variant="danger" class="mb-3" />

            <NeoInput label="New Password" id="newPassword" type="password" v-model="newPassword"
              placeholder="Enter new password" variant="danger" class="mb-3" />

            <NeoInput label="Confirm New Password" id="confirmPassword" type="password" v-model="confirmPassword"
              placeholder="Confirm new password" variant="danger" class="mb-3" />

            <div class="d-grid">
              <NeoButton variant="success" @click="changePassword">
                <NeoIcon name="check" size="16" class="me-1" />
                Update Password
              </NeoButton>
            </div>
          </form>
        </NeoCard>

        <!-- Documents Card -->
        <NeoCard class="mb-4" variant="warning">
          <template #header>
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0 fw-bold text-uppercase">Documents</h5>
            </div>
          </template>

          <div v-if="documents.length === 0" class="text-center py-4">
            <p class="mb-0">No documents uploaded yet</p>
          </div>

          <div v-else>
            <div v-for="doc in documents" :key="doc.id" class="mb-3">
              <div class="border border-dark border-3 p-3 bg-light">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h6 class="mb-0 text-uppercase">{{ doc.document_type }}</h6>
                </div>
                <p class="mb-2">{{ doc.file_name }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    Uploaded: {{ new Date(doc.upload_date).toLocaleDateString() }}
                  </small>
                  <NeoButton variant="primary" size="sm" @click="downloadDocument(doc)">
                    <NeoIcon name="download" size="14" class="me-1" />
                    Download
                  </NeoButton>
                </div>
              </div>
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
