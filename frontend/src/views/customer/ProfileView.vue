<script setup>
import { ref } from 'vue'

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
</script>

<template>
  <div class="container py-4">
    <h2 class="mb-4">My Profile</h2>

    <div class="row">
      <!-- Profile Information Card -->
      <div class="col-lg-8 mb-4">
        <div class="card shadow-sm">
          <div class="card-header bg-white py-3">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Profile Information</h5>
              <button
                class="btn"
                :class="isEditMode ? 'btn-outline-secondary' : 'btn-outline-primary'"
                @click="toggleEditMode"
              >
                {{ isEditMode ? 'Cancel' : 'Edit Profile' }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <!-- View Mode -->
            <div v-if="!isEditMode">
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Name</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.name }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.email }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Phone</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.phone }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.address }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Member Since</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ userData.joinDate }}</p>
                </div>
              </div>
            </div>

            <!-- Edit Mode -->
            <form v-else>
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input type="text" class="form-control" id="name" v-model="editableUserData.name" />
              </div>
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  v-model="editableUserData.email"
                />
              </div>
              <div class="mb-3">
                <label for="phone" class="form-label">Phone</label>
                <input
                  type="tel"
                  class="form-control"
                  id="phone"
                  v-model="editableUserData.phone"
                />
              </div>
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <textarea
                  class="form-control"
                  id="address"
                  rows="3"
                  v-model="editableUserData.address"
                ></textarea>
              </div>

              <div class="d-grid">
                <button type="button" class="btn btn-primary" @click="saveUserData">
                  Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <!-- Profile Picture and Security Card -->
      <div class="col-lg-4">
        <!-- Profile Picture Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-body text-center py-4">
            <img
              :src="userData.profileImage"
              alt="Profile picture"
              class="rounded-circle img-fluid mb-3"
              style="width: 150px; height: 150px; object-fit: cover"
            />
            <h5 class="mb-0">{{ userData.name }}</h5>
            <p class="text-muted mb-3">Customer ID: {{ userData.id }}</p>
            <button class="btn btn-sm btn-outline-primary">Change Picture</button>
          </div>
        </div>

        <!-- Security Card -->
        <div class="card shadow-sm">
          <div class="card-header bg-white py-3">
            <h5 class="mb-0">Security</h5>
          </div>
          <div class="card-body">
            <button class="btn btn-outline-primary w-100 mb-3" @click="togglePasswordForm">
              Change Password
            </button>

            <!-- Change Password Form -->
            <form v-if="showPasswordForm" class="mt-3">
              <div class="mb-3">
                <label for="currentPassword" class="form-label">Current Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="currentPassword"
                  v-model="currentPassword"
                  placeholder="Enter current password"
                />
              </div>
              <div class="mb-3">
                <label for="newPassword" class="form-label">New Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="newPassword"
                  v-model="newPassword"
                  placeholder="Enter new password"
                />
              </div>
              <div class="mb-3">
                <label for="confirmPassword" class="form-label">Confirm New Password</label>
                <input
                  type="password"
                  class="form-control"
                  id="confirmPassword"
                  v-model="confirmPassword"
                  placeholder="Confirm new password"
                />
              </div>
              <div class="d-grid">
                <button type="button" class="btn btn-primary" @click="changePassword">
                  Update Password
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
