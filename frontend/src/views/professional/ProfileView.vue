<script setup>
import { ref } from 'vue'

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
  availability: {
    monday: { available: true, start: '09:00', end: '18:00' },
    tuesday: { available: true, start: '09:00', end: '18:00' },
    wednesday: { available: true, start: '09:00', end: '18:00' },
    thursday: { available: true, start: '09:00', end: '18:00' },
    friday: { available: true, start: '09:00', end: '18:00' },
    saturday: { available: true, start: '10:00', end: '16:00' },
    sunday: { available: false, start: '', end: '' },
  },
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

// Update availability settings
const showAvailabilityForm = ref(false)
const editableAvailability = ref({ ...professionalData.value.availability })

// Toggle availability form visibility
const toggleAvailabilityForm = () => {
  showAvailabilityForm.value = !showAvailabilityForm.value

  if (showAvailabilityForm.value) {
    // Make a copy of the current availability when showing the form
    editableAvailability.value = JSON.parse(JSON.stringify(professionalData.value.availability))
  }
}

// Save availability changes
const saveAvailability = () => {
  // In a real application, this would call an API to update availability
  professionalData.value.availability = JSON.parse(JSON.stringify(editableAvailability.value))
  showAvailabilityForm.value = false

  // Show success message
  alert('Availability updated successfully')
}

// Mock reviews
const reviews = [
  {
    id: 1,
    customer: 'John Doe',
    rating: 5,
    date: '2023-05-10',
    comment: 'Excellent service! Fixed my leaking pipe quickly and professionally.',
  },
  {
    id: 2,
    customer: 'Sarah Johnson',
    rating: 4,
    date: '2023-04-25',
    comment: 'Good work, arrived on time and completed the job efficiently.',
  },
  {
    id: 3,
    customer: 'David Brown',
    rating: 5,
    date: '2023-04-12',
    comment: 'Very professional and knowledgeable. Would definitely recommend.',
  },
]

// Get status badge class
const getStatusBadgeClass = (status) => {
  const statusClasses = {
    Approved: 'bg-success',
    Pending: 'bg-warning text-dark',
    Blocked: 'bg-danger',
  }
  return statusClasses[status] || 'bg-secondary'
}
</script>

<template>
  <div class="container py-4">
    <h2 class="mb-4">My Profile</h2>

    <div class="row">
      <!-- Left Column -->
      <div class="col-lg-8">
        <!-- Basic Information Card -->
        <div class="card shadow-sm mb-4">
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
                  <p class="mb-0">{{ professionalData.name }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Email</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.email }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Phone</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.phone }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Address</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.address }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Service Type</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.serviceType }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Experience</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.experience }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Hourly Rate</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.hourlyRate }}</p>
                </div>
              </div>
              <hr />
              <div class="row mb-3">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Description</p>
                </div>
                <div class="col-sm-9">
                  <p class="mb-0">{{ professionalData.description }}</p>
                </div>
              </div>
              <hr />
              <div class="row">
                <div class="col-sm-3">
                  <p class="mb-0 text-muted">Status</p>
                </div>
                <div class="col-sm-9">
                  <span :class="`badge ${getStatusBadgeClass(professionalData.status)}`">
                    {{ professionalData.status }}
                  </span>
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
                  rows="2"
                  v-model="editableUserData.address"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="experience" class="form-label">Experience</label>
                <input
                  type="text"
                  class="form-control"
                  id="experience"
                  v-model="editableUserData.experience"
                />
              </div>
              <div class="mb-3">
                <label for="hourlyRate" class="form-label">Hourly Rate</label>
                <input
                  type="text"
                  class="form-control"
                  id="hourlyRate"
                  v-model="editableUserData.hourlyRate"
                />
              </div>
              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="description"
                  rows="3"
                  v-model="editableUserData.description"
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

        <!-- Availability Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-header bg-white py-3">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Availability</h5>
              <button
                class="btn"
                :class="showAvailabilityForm ? 'btn-outline-secondary' : 'btn-outline-primary'"
                @click="toggleAvailabilityForm"
              >
                {{ showAvailabilityForm ? 'Cancel' : 'Set Availability' }}
              </button>
            </div>
          </div>
          <div class="card-body">
            <!-- View Mode -->
            <div v-if="!showAvailabilityForm">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Day</th>
                      <th>Available</th>
                      <th>Hours</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(availability, day) in professionalData.availability" :key="day">
                      <td class="text-capitalize">{{ day }}</td>
                      <td>
                        <span :class="availability.available ? 'text-success' : 'text-danger'">
                          {{ availability.available ? 'Yes' : 'No' }}
                        </span>
                      </td>
                      <td>
                        {{
                          availability.available
                            ? `${availability.start} - ${availability.end}`
                            : '-'
                        }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Edit Mode -->
            <form v-else>
              <div class="mb-3" v-for="(availability, day) in editableAvailability" :key="day">
                <div class="card mb-2">
                  <div class="card-body">
                    <div class="form-check form-switch mb-2">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        :id="`available-${day}`"
                        v-model="editableAvailability[day].available"
                      />
                      <label class="form-check-label text-capitalize" :for="`available-${day}`">
                        {{ day }}
                      </label>
                    </div>

                    <div class="row g-2" v-if="editableAvailability[day].available">
                      <div class="col-6">
                        <label :for="`start-${day}`" class="form-label small">Start Time</label>
                        <input
                          type="time"
                          class="form-control"
                          :id="`start-${day}`"
                          v-model="editableAvailability[day].start"
                        />
                      </div>
                      <div class="col-6">
                        <label :for="`end-${day}`" class="form-label small">End Time</label>
                        <input
                          type="time"
                          class="form-control"
                          :id="`end-${day}`"
                          v-model="editableAvailability[day].end"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="d-grid">
                <button type="button" class="btn btn-primary" @click="saveAvailability">
                  Save Availability
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Reviews Card -->
        <div class="card shadow-sm">
          <div class="card-header bg-white py-3">
            <div class="d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Customer Reviews</h5>
              <div class="d-flex align-items-center">
                <div class="text-warning me-2">
                  <i class="fas fa-star"></i>
                  {{ professionalData.rating }}
                </div>
                <span class="badge bg-light text-dark"> {{ reviews.length }} reviews </span>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div v-if="reviews.length === 0" class="text-center py-4">
              <p class="text-muted mb-0">No reviews yet</p>
            </div>

            <div v-else>
              <div v-for="review in reviews" :key="review.id" class="mb-3">
                <div class="d-flex justify-content-between">
                  <h6 class="mb-1">{{ review.customer }}</h6>
                  <small class="text-muted">{{ review.date }}</small>
                </div>
                <div class="mb-2">
                  <span class="text-warning">
                    <span v-for="i in 5" :key="i">
                      <i class="fas" :class="i <= review.rating ? 'fa-star' : 'fa-star-o'"></i>
                    </span>
                  </span>
                </div>
                <p class="mb-0">{{ review.comment }}</p>
                <hr v-if="review !== reviews[reviews.length - 1]" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column -->
      <div class="col-lg-4">
        <!-- Profile Picture Card -->
        <div class="card shadow-sm mb-4">
          <div class="card-body text-center py-4">
            <img
              :src="professionalData.profileImage"
              alt="Profile picture"
              class="rounded-circle img-fluid mb-3"
              style="width: 150px; height: 150px; object-fit: cover"
            />
            <h5 class="mb-0">{{ professionalData.name }}</h5>
            <p class="text-muted mb-2">
              {{ professionalData.serviceType }}
            </p>
            <p class="d-flex justify-content-center gap-2 mb-3">
              <span class="badge bg-primary"
                >{{ professionalData.completedJobs }} Jobs Completed</span
              >
              <span :class="`badge ${getStatusBadgeClass(professionalData.status)}`">
                {{ professionalData.status }}
              </span>
            </p>
            <button class="btn btn-sm btn-outline-primary">Change Picture</button>
          </div>
        </div>

        <!-- Security Card -->
        <div class="card shadow-sm mb-4">
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

        <!-- Stats Card -->
        <div class="card shadow-sm">
          <div class="card-header bg-white py-3">
            <h5 class="mb-0">Stats</h5>
          </div>
          <div class="card-body">
            <div class="d-flex justify-content-between border-bottom py-2">
              <span>Total Jobs</span>
              <span class="fw-bold">{{ professionalData.completedJobs }}</span>
            </div>
            <div class="d-flex justify-content-between border-bottom py-2">
              <span>Rating</span>
              <span class="fw-bold text-warning">
                <i class="fas fa-star"></i> {{ professionalData.rating }}
              </span>
            </div>
            <div class="d-flex justify-content-between border-bottom py-2">
              <span>Member Since</span>
              <span class="fw-bold">{{ professionalData.joinDate }}</span>
            </div>
            <div class="d-flex justify-content-between py-2">
              <span>Status</span>
              <span :class="`badge ${getStatusBadgeClass(professionalData.status)}`">
                {{ professionalData.status }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
