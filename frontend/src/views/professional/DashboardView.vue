<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useServiceRequestStore } from '@/stores/serviceRequest'
import { professionalAPI } from '@/services/api'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'
import { NeoButton, NeoCard, NeoBadge, NeoAlert, NeoModal, NeoIcon } from '@/components/ui'

const router = useRouter()
const route = useRoute()
const serviceRequestStore = useServiceRequestStore()
const authStore = useAuthStore()

// Check if we're on the main professional route
const isMainDashboard = computed(() => route.path === '/professional')

// Professional sidebar menu items
const menuItems = [
  {
    label: 'Dashboard',
    route: '/professional',
    icon: 'layout-dashboard',
    exactPath: true,
  },
  {
    label: 'Service Requests',
    route: '/professional/requests',
    icon: 'clipboard-list',
  },
  {
    label: 'Profile',
    route: '/professional/profile',
    icon: 'user',
  },
]

// Professional data
const professionalData = ref({
  name: '',
  serviceType: '',
  experience: '',
  profileImage: '',
  rating: 0,
  joinDate: '',
  completedJobs: 0,
  status: '',
})

// Service requests
const serviceRequests = ref([])

// Dashboard stats
const stats = ref([])

// Recent activity
const recentActivity = ref([])

// Feedback modal state
const showFeedbackModal = ref(false)
const feedbackMessage = ref('')
const feedbackTitle = ref('')
const feedbackVariant = ref('info')

// Helper function to show feedback modal
const showFeedback = (title, message, variant = 'info') => {
  feedbackTitle.value = title
  feedbackMessage.value = message
  feedbackVariant.value = variant
  showFeedbackModal.value = true
}

// Fetch professional data
const fetchProfessionalData = async () => {
  try {
    const user = await authStore.user
    console.log(user)
    professionalData.value = {
      name: user.name,
      serviceType: user.service_type,
      experience: user.experience,
      profileImage: user.profile_image || `https://avatar.iran.liara.run/public/11`,
      rating: user.rating || 0,
      joinDate: user.date_created,
      completedJobs: user.completed_jobs || 0,
      status: user.status,
    }
  } catch (error) {
    console.error('Failed to fetch professional data:', error)
    showFeedback('Error', 'Failed to load professional data.', 'danger')
  }
}

// Fetch service requests
const fetchServiceRequests = async () => {
  try {
    await serviceRequestStore.fetchAssignedRequests()
    await serviceRequestStore.fetchProfessionalRequests()
    await serviceRequestStore.fetchDashboardStats()
    await serviceRequestStore.fetchActivityFeed()

    serviceRequests.value = serviceRequestStore.assignedRequests

    // Update stats
    stats.value = [
      {
        id: 1,
        label: 'Total Earnings',
        value: `₹${serviceRequestStore.totalEarnings}`,
        icon: 'indian-rupee',
        variant: 'success',
      },
      {
        id: 2,
        label: 'Completed Jobs',
        value: serviceRequestStore.completedJobs,
        icon: 'check-circle',
        variant: 'primary',
      },
      {
        id: 3,
        label: 'Pending Jobs',
        value: serviceRequestStore.pendingJobs,
        icon: 'clock',
        variant: 'warning',
      },
      {
        id: 4,
        label: 'Accepted Jobs',
        value: serviceRequestStore.activeJobs,
        icon: 'thumbs-up',
        variant: 'info',
      },
    ]

    // Update recent activity
    recentActivity.value = serviceRequestStore.recentActivity.map(activity => ({
      ...activity,
      timeAgo: formatTimeAgo(activity.timestamp)
    }))
  } catch (error) {
    console.error('Failed to fetch requests:', error)
    showFeedback('Error', 'Failed to load service requests.', 'danger')
  }
}

// Helper function to format time ago
const formatTimeAgo = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  if (hours < 1) {
    return 'just now'
  } else if (hours < 24) {
    return `${hours} hours ago`
  } else {
    return `${days} days ago`
  }

}

// Fetch data on component mount
onMounted(async () => {
  if (isMainDashboard.value) {
    await Promise.all([
      fetchProfessionalData(),
      fetchServiceRequests()
    ])
  }
})

// Watch for route changes
watch(isMainDashboard, async (newValue) => {
  if (newValue) {
    await Promise.all([
      fetchProfessionalData(),
      fetchServiceRequests()
    ])
  }
})


// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  const statusClasses = {
    Completed: 'success',
    Accepted: 'primary',
    Pending: 'warning',
    Rejected: 'danger',
  }
  return statusClasses[status] || 'secondary'
}

// Navigate to requests page
const viewAllRequests = () => {
  router.push('/professional/requests')
}

// Handle logout action
const handleMenuAction = (item) => {
  if (item.label === 'Logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    router.push('/login')
  }
}

// Add helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}
</script>


<template>
  <div class="neo-brutalist">
    <div class="dashboard-wrapper">
      <!-- Sidebar - Always visible -->
      <div class="sidebar-container">
        <NeoDashboardSidebar :menuItems="menuItems" title="Professional" @item-action="handleMenuAction" />
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Dashboard content - Only shown on main professional route -->
        <div v-if="isMainDashboard">
          <div class="header-section">
            <h1 class="page-title">Dashboard</h1>

          </div>

          <!-- Profile Quick View -->
          <div class="profile-quick-view">
            <div class="profile-avatar">
              <img :src="professionalData.profileImage" alt="Profile" />
            </div>
            <div class="profile-info">
              <h2>{{ professionalData.name }}</h2>
              <div class="service-type">{{ professionalData.serviceType }}</div>
            </div>
            <div class="profile-actions">
              <NeoButton variant="primary" @click="router.push('/professional/profile')">
                Edit Profile
              </NeoButton>
            </div>
          </div>

          <!-- Stats Cards -->
          <div class="stats-container">
            <NeoCard v-for="stat in stats" :key="stat.id" :variant="stat.variant" class="stat-card">
              <div class="stat-content">
                <div class="stat-icon">
                  <NeoIcon :name="stat.icon" size="32" />
                </div>
                <div class="stat-details">
                  <div class="stat-label">{{ stat.label }}</div>
                  <div class="stat-value">{{ stat.value }}</div>
                </div>
              </div>
            </NeoCard>
          </div>

          <!-- Main Content Grid -->
          <div class="content-grid">
            <!-- Recent Service Requests -->
            <NeoCard class="service-requests-card">
              <template #header>
                <div class="card-header-content">
                  <h5 class="card-title">Recent Service Requests</h5>
                  <NeoButton variant="dark" size="sm" @click="viewAllRequests">
                    View All
                  </NeoButton>
                </div>
              </template>

              <div class="table-wrapper">
                <table class="request-table">
                  <thead>
                    <tr>
                      <th>Customer</th>
                      <th>Service</th>
                      <th>Date</th>
                      <th>Status</th>
                      <th>Time Required</th>
                      <th>Amount</th>
                      <th>Remarks</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="request in serviceRequests" :key="request.id" class="request-row">
                      <td>
                        <div class="d-flex align-items-center">
                          <img :src="getProfileImageUrl(request.customer.profile_image)" alt="Customer"
                            class="rounded-circle me-2" style="width: 32px; height: 32px; object-fit: cover;" />
                          <span>{{ request.customer.name }}</span>
                        </div>
                      </td>
                      <td>{{ request.service.name }}</td>
                      <td>{{ new Date(request.date_of_request).toLocaleDateString() }}</td>
                      <td>
                        <NeoBadge :variant="getStatusBadgeClass(request.service_status)">
                          {{ request.service_status }}
                        </NeoBadge>
                      </td>
                      <td>{{ request.service.time_required }}</td>
                      <td class="amount">{{ request.service?.price || 0 }}</td>
                      <td class="remarks">{{ request.remarks }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </NeoCard>

            <!-- Activity Feed -->
            <NeoCard variant="danger" class="activity-card">
              <template #header>
                <h5 class="card-title">Activity Feed</h5>
              </template>

              <div class="activity-feed">
                <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                  <div class="activity-avatar">
                    <img :src="getProfileImageUrl(activity.customer_profile_image)" alt="Customer"
                      class="rounded-circle"
                      style="width: 40px; height: 40px; object-fit: cover; border: 2px solid #000;" />
                  </div>
                  <div class="activity-content">
                    <div class="activity-message">
                      <span v-if="activity.type === 'service_request' && activity.action === 'accepted'">
                        You accepted a request from <strong>{{ activity.customer }}</strong>
                      </span>
                      <span v-else-if="
                        activity.type === 'service_request' && activity.action === 'completed'
                      ">
                        You completed a service for <strong>{{ activity.customer }}</strong>
                      </span>
                      <span v-else-if="activity.type === 'payment'">
                        Payment of <strong>{{ activity.amount }}</strong> received from
                        <strong>{{ activity.customer }}</strong>
                      </span>
                      <span v-else-if="
                        activity.type === 'service_request' && activity.action === 'rejected'
                      ">
                        You rejected a request from <strong>{{ activity.customer }}</strong>
                      </span>
                    </div>
                    <div class="activity-time">{{ activity.timeAgo }}</div>
                  </div>
                </div>
              </div>
            </NeoCard>
          </div>
        </div>

        <!-- Child route content - Shown when on child routes -->
        <router-view v-else></router-view>
      </div>
    </div>

    <!-- Feedback Modal -->
    <NeoModal v-model="showFeedbackModal" :title="feedbackTitle">
      <NeoAlert :variant="feedbackVariant" class="mb-0">
        {{ feedbackMessage }}
      </NeoAlert>
      <template #footer>
        <NeoButton variant="secondary" @click="showFeedbackModal = false">Close</NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
.neo-brutalist {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-wrapper {
  display: grid;
  grid-template-columns: 250px 1fr;
  min-height: 100vh;
}

.sidebar-container {
  min-height: 100vh;
  background-color: white;
  position: sticky;
  top: 0;
  height: 100vh;
}

.main-content {
  padding: 2rem;
  overflow-y: auto;
  height: calc(100vh - 74px);
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.status-badge {
  transform: rotate(-3deg);
}

/* Profile Quick View */
.profile-quick-view {
  background: white;
  border: 4px solid #000;
  margin-bottom: 2rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 8px 8px 0 #000;
  position: relative;
  overflow: hidden;
}

.profile-quick-view::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 30%;
  height: 100%;
  background-color: rgba(255, 127, 80, 0.2);
  clip-path: polygon(100% 0, 0 0, 100% 100%);
  z-index: 0;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border: 3px solid #000;
  border-radius: 0;
  overflow: hidden;
  transform: rotate(-3deg);
  box-shadow: 4px 4px 0 #000;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  font-weight: 900;
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
}

.service-type {
  font-weight: 700;
  color: #ff7f50;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-actions {
  z-index: 1;
}

/* Stats Cards Container */
.stats-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 1200px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

.stat-card {
  border: 4px solid #000;
  box-shadow: 8px 8px 0 #000;
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
}

.stat-content {
  display: flex;
  align-items: center;
  padding: 1rem;
}

.stat-icon {
  margin-right: 1rem;
  border: 3px solid #000;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotate(-5deg);
}

.stat-details {
  flex: 1;
}

.stat-label {
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  line-height: 1;
}

/* Main Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

.service-requests-card {
  grid-column: 1 / -1;
  border: 4px solid #000;
  box-shadow: 8px 8px 0 #000;
}

.activity-card {
  border: 4px solid #000;
  box-shadow: 8px 8px 0 #000;
}

.appointments-card {
  border: 4px solid #000;
  box-shadow: 8px 8px 0 #000;
}

.card-header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.card-title {
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

/* Table Styling */
.table-wrapper {
  overflow-x: auto;
}

.request-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

.request-table th {
  font-weight: 900;
  text-transform: uppercase;
  padding: 1rem;
  border-bottom: 3px solid #000;
  letter-spacing: 0.5px;
  text-align: left;
}

.request-table td {
  padding: 1rem;
  border-bottom: 2px solid rgba(0, 0, 0, 0.2);
  font-weight: 500;
}

.request-row {
  transition: all 0.2s ease;
}

.request-row:hover {
  background-color: rgba(0, 0, 0, 0.05);
  transform: translateX(4px);
}

.request-id {
  font-weight: 800;
  padding: 0.25rem 0.5rem;
  background-color: #f0f0f0;
  border: 2px solid #000;
  display: inline-block;
}

.amount {
  font-weight: 800;
}

.remarks {
  font-weight: 500;
}

/* Activity Feed */
.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 400px;
  overflow-y: auto;
  padding: 0.5rem;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  background: white;
  padding: 1rem;
  border: 2px solid #000;
  transition: transform 0.2s ease;
}

.activity-item:hover {
  transform: translateX(5px);
}

.activity-avatar {
  margin-right: 1rem;
  width: 40px;
  height: 40px;
  overflow: hidden;
  flex-shrink: 0;
}

.activity-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 2px solid #000;
}

.activity-content {
  flex: 1;
}

.activity-message {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.activity-time {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

/* Appointments */
.no-appointments {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.empty-state {
  font-weight: 700;
}

.empty-state i {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.appointments-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.appointment-item {
  background: white;
  border: 2px solid #000;
  padding: 1rem;
}

.appointment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.appointment-service {
  font-weight: 800;
  font-size: 1.1rem;
  margin: 0;
  text-transform: uppercase;
}

.appointment-details {
  margin-bottom: 1rem;
}

.appointment-detail {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.appointment-detail i {
  width: 20px;
  margin-right: 0.5rem;
}

.appointment-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1rem;
}

/* Custom scrollbar */
.activity-feed::-webkit-scrollbar {
  width: 10px;
}

.activity-feed::-webkit-scrollbar-track {
  background: #f1f1f1;
  border: 2px solid #000;
}

.activity-feed::-webkit-scrollbar-thumb {
  background: #ff7f50;
  border: 2px solid #000;
}

.activity-feed::-webkit-scrollbar-thumb:hover {
  background: #ff5722;
}

/* Responsive adjustments */
@media (max-width: 992px) {
  .dashboard-wrapper {
    grid-template-columns: 1fr;
  }

  .sidebar-container {
    position: relative;
    height: auto;
    min-height: auto;
    border-right: none;
    background-color: white;
  }

  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 576px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .profile-quick-view {
    flex-direction: column;
    text-align: center;
  }

  .profile-actions {
    width: 100%;
    margin-top: 1rem;
  }
}
</style>
