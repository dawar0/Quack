<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoBadge from '@/components/ui/NeoBadge.vue'

const router = useRouter()
const route = useRoute()

// Check if we're on the main customer route
const isMainDashboard = computed(() => route.path === '/customer')

// Customer sidebar menu items
const menuItems = [
  {
    label: 'Dashboard',
    route: '/customer',
    icon: 'fas fa-tachometer-alt',
    exactPath: true,
  },

  {
    label: 'My Requests',
    route: '/customer/requests',
    icon: 'fas fa-clipboard-list',
  },
  {
    label: 'Profile',
    route: '/customer/profile',
    icon: 'fas fa-user',
  },
]

// Mock user data
const userData = ref({
  name: 'John Doe',
  email: 'john.doe@example.com',
  profileImage: 'https://randomuser.me/api/portraits/men/32.jpg',
  joinDate: '2023-01-15',
})

// Mock service request data
const serviceRequests = ref([
  {
    id: 'SR1001',
    serviceName: 'Plumbing',
    date: '2023-05-15',
    status: 'Completed',
    professional: 'Mike Smith',
  },
  {
    id: 'SR1002',
    serviceName: 'Electrical',
    date: '2023-05-20',
    status: 'Assigned',
    professional: 'Sarah Wilson',
  },
  {
    id: 'SR1003',
    serviceName: 'Cleaning',
    date: '2023-05-22',
    status: 'Requested',
    professional: null,
  },
  {
    id: 'SR1004',
    serviceName: 'Gardening',
    date: '2023-05-25',
    status: 'Cancelled',
    professional: null,
  },
])

// Dashboard stats formatted as an array for easier iteration
const stats = [
  {
    id: 1,
    label: 'Total Requests',
    value: serviceRequests.value.length,
    icon: 'fas fa-clipboard-list',
    variant: 'default',
  },
  {
    id: 2,
    label: 'Completed',
    value: serviceRequests.value.filter((req) => req.status === 'Completed').length,
    icon: 'fas fa-check-circle',
    variant: 'success',
  },
  {
    id: 3,
    label: 'In Progress',
    value: serviceRequests.value.filter((req) => req.status === 'Assigned').length,
    icon: 'fas fa-clock',
    variant: 'primary',
  },
  {
    id: 4,
    label: 'Pending',
    value: serviceRequests.value.filter((req) => req.status === 'Requested').length,
    icon: 'fas fa-hourglass-half',
    variant: 'warning',
  },
]

// Mock recent activity
const recentActivity = ref([
  { id: 1, type: 'service_request', action: 'created', service: 'Gardening', date: '3 days ago' },
  { id: 2, type: 'service_request', action: 'completed', service: 'Plumbing', date: '5 days ago' },
  {
    id: 3,
    type: 'payment',
    action: 'made',
    amount: '₹550',
    service: 'Plumbing',
    date: '5 days ago',
  },
  {
    id: 4,
    type: 'service_request',
    action: 'cancelled',
    service: 'Electrical',
    date: '1 week ago',
  },
])

// Helper function to get status badge variant
const getStatusVariant = (status) => {
  const statusVariants = {
    Completed: 'success',
    Assigned: 'primary',
    Requested: 'warning',
    Cancelled: 'danger',
  }
  return statusVariants[status] || 'secondary'
}

// Navigate to service requests page
const viewAllRequests = () => {
  router.push('/customer/requests')
}

// Navigate to browse services page
const browseServices = () => {
  router.push({ path: '/customer/requests', query: { openRequestModal: 'true' } })
}

// Mock upcoming appointments
const upcomingAppointments = ref([
  {
    id: 'A1001',
    service: 'Electrical',
    professional: 'Sarah Wilson',
    date: '2023-05-30',
    time: '10:00 - 12:00',
    address: '123 Main Street, Mumbai',
  },
])

// Handle logout action
const handleMenuAction = (item) => {
  if (item.label === 'Logout') {
    localStorage.removeItem('token')
    localStorage.removeItem('role')
    router.push('/login')
  }
}
</script>

<template>
  <div class="neo-brutalist">
    <div class="dashboard-wrapper">
      <!-- Sidebar - Always visible -->
      <div class="sidebar-container">
        <NeoDashboardSidebar
          :menuItems="menuItems"
          title="Customer"
          @item-action="handleMenuAction"
        />
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Dashboard content - Only shown on main customer route -->
        <div v-if="isMainDashboard">
          <div class="header-section">
            <h1 class="page-title">Dashboard</h1>
            <div class="welcome-tag">
              <span>Welcome, {{ userData.name }}</span>
            </div>
          </div>

          <!-- Profile Quick View -->
          <div class="profile-quick-view">
            <div class="profile-avatar">
              <img :src="userData.profileImage" alt="Profile" />
            </div>
            <div class="profile-info">
              <h2>{{ userData.name }}</h2>
              <div class="profile-email">{{ userData.email }}</div>
              <div class="profile-join-date">Member since {{ userData.joinDate }}</div>
            </div>
            <div class="profile-actions">
              <NeoButton variant="dark" @click="router.push('/customer/profile')">
                Edit Profile
              </NeoButton>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="quick-actions-container">
            <NeoButton variant="primary" @click="browseServices" class="quick-action-button">
              <i class="fas fa-plus-circle"></i> Book a Service
            </NeoButton>

            <NeoButton variant="secondary" @click="viewAllRequests" class="quick-action-button">
              <i class="fas fa-list"></i> View All Requests
            </NeoButton>

            <NeoButton
              variant="info"
              @click="router.push('/customer/profile')"
              class="quick-action-button"
            >
              <i class="fas fa-user"></i> Edit Profile
            </NeoButton>
          </div>

          <!-- Stats Cards -->
          <div class="stats-container">
            <NeoCard v-for="stat in stats" :key="stat.id" :variant="stat.variant" class="stat-card">
              <div class="stat-content">
                <div class="stat-icon">
                  <i :class="stat.icon"></i>
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
                      <th>ID</th>
                      <th>Service</th>
                      <th>Date</th>
                      <th>Professional</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="request in serviceRequests" :key="request.id" class="request-row">
                      <td>
                        <div class="request-id">{{ request.id }}</div>
                      </td>
                      <td>{{ request.serviceName }}</td>
                      <td>{{ request.date }}</td>
                      <td>{{ request.professional || '—' }}</td>
                      <td>
                        <NeoBadge :variant="getStatusVariant(request.status)">
                          {{ request.status }}
                        </NeoBadge>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </NeoCard>

            <!-- Upcoming Appointments -->
            <NeoCard variant="warning" class="appointments-card">
              <template #header>
                <h5 class="card-title">Upcoming Appointments</h5>
              </template>

              <div v-if="upcomingAppointments.length === 0" class="no-appointments">
                <div class="empty-state">
                  <i class="fas fa-calendar-times"></i>
                  <p>No upcoming appointments</p>
                  <NeoButton variant="primary" size="sm" @click="browseServices"
                    >Book a Service</NeoButton
                  >
                </div>
              </div>

              <div v-else class="appointments-list">
                <div
                  v-for="appointment in upcomingAppointments"
                  :key="appointment.id"
                  class="appointment-item"
                >
                  <div class="appointment-header">
                    <h6 class="appointment-service">{{ appointment.service }} Service</h6>
                    <NeoBadge variant="primary">Upcoming</NeoBadge>
                  </div>
                  <div class="appointment-details">
                    <div class="appointment-detail">
                      <i class="fas fa-user"></i>
                      <span>{{ appointment.professional }}</span>
                    </div>
                    <div class="appointment-detail">
                      <i class="fas fa-calendar"></i>
                      <span>{{ appointment.date }}</span>
                    </div>
                    <div class="appointment-detail">
                      <i class="fas fa-clock"></i>
                      <span>{{ appointment.time }}</span>
                    </div>
                    <div class="appointment-detail">
                      <i class="fas fa-map-marker-alt"></i>
                      <span>{{ appointment.address }}</span>
                    </div>
                  </div>
                  <div class="appointment-actions">
                    <NeoButton variant="secondary" size="sm">Reschedule</NeoButton>
                    <NeoButton variant="danger" size="sm" outline>Cancel</NeoButton>
                  </div>
                </div>
              </div>
            </NeoCard>

            <!-- Recent Activity -->
            <NeoCard variant="danger" class="activity-card">
              <template #header>
                <h5 class="card-title">Recent Activity</h5>
              </template>

              <div class="activity-feed">
                <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                  <div class="activity-icon">
                    <i
                      v-if="activity.type === 'service_request' && activity.action === 'created'"
                      class="fas fa-plus-circle"
                    ></i>
                    <i
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'completed'
                      "
                      class="fas fa-check-circle"
                    ></i>
                    <i v-else-if="activity.type === 'payment'" class="fas fa-rupee-sign"></i>
                    <i
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'cancelled'
                      "
                      class="fas fa-times-circle"
                    ></i>
                  </div>
                  <div class="activity-content">
                    <div class="activity-message">
                      <span
                        v-if="activity.type === 'service_request' && activity.action === 'created'"
                      >
                        You requested a <strong>{{ activity.service }}</strong> service
                      </span>
                      <span
                        v-else-if="
                          activity.type === 'service_request' && activity.action === 'completed'
                        "
                      >
                        Your <strong>{{ activity.service }}</strong> service was completed
                      </span>
                      <span v-else-if="activity.type === 'payment'">
                        You made a payment of <strong>{{ activity.amount }}</strong> for
                        <strong>{{ activity.service }}</strong>
                      </span>
                      <span
                        v-else-if="
                          activity.type === 'service_request' && activity.action === 'cancelled'
                        "
                      >
                        You cancelled a <strong>{{ activity.service }}</strong> service
                      </span>
                    </div>
                    <div class="activity-time">{{ activity.date }}</div>
                  </div>
                </div>
              </div>
            </NeoCard>
          </div>
        </div>

        <!-- Child route content will be rendered here -->
        <router-view v-else></router-view>
      </div>
    </div>
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
}

/* Header styling */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
}

.welcome-tag {
  transform: rotate(-3deg);
}

.welcome-tag span {
  background-color: #fff;
  padding: 0.5rem 1rem;
  border: 3px solid #000;
  box-shadow: 4px 4px 0 #000;
  font-weight: 700;
  display: inline-block;
}

/* Profile quick view */
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
  object-fit: cover;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  font-weight: 900;
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
}

.profile-email {
  font-weight: 700;
  color: #ff7f50;
  margin-bottom: 0.25rem;
  letter-spacing: 0.5px;
}

.profile-join-date {
  font-size: 0.875rem;
  font-weight: 700;
  color: #555;
}

.profile-actions {
  z-index: 1;
}

/* Stats container */
.stats-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
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
  font-size: 2rem;
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

/* Content grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: auto auto;
  gap: 1.5rem;
}

/* Card stylings */
.service-requests-card {
  grid-column: 1 / -1;
  border: 4px solid #000;
  box-shadow: 8px 8px 0 #000;
}

.activity-card,
.appointments-card,
.notifications-card {
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

/* Table styling */
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

/* Appointments styling */
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

/* Notifications styling */
.no-notifications {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.notifications-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.notification-item {
  padding: 1rem;
  background-color: white;
  border: 2px solid #000;
  transition: transform 0.2s ease;
}

.notification-item.unread {
  border-left: 5px solid #ff7f50;
  background-color: rgba(255, 127, 80, 0.1);
}

.notification-item:hover {
  transform: translateX(5px);
}

.notification-message {
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.notification-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-time {
  font-size: 0.875rem;
  font-weight: 700;
  color: #555;
}

/* Activity styling */
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

.activity-icon {
  width: 40px;
  height: 40px;
  border: 2px solid #000;
  background: #f8f8f8;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.activity-item:nth-child(1) .activity-icon {
  color: #ff7f50;
}

.activity-item:nth-child(2) .activity-icon {
  color: #00ff7f;
}

.activity-item:nth-child(3) .activity-icon {
  color: #ffd700;
}

.activity-item:nth-child(4) .activity-icon {
  color: #ff5555;
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

/* Quick actions */
.quick-actions-container {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.quick-action-button {
  border: 3px solid #000;
  box-shadow: 5px 5px 0 #000;
  padding: 1rem;
  text-transform: uppercase;
  font-weight: bold;
  letter-spacing: 0.5px;
}

/* Custom scrollbar */
.activity-feed::-webkit-scrollbar,
.notifications-list::-webkit-scrollbar {
  width: 10px;
}

.activity-feed::-webkit-scrollbar-track,
.notifications-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border: 2px solid #000;
}

.activity-feed::-webkit-scrollbar-thumb,
.notifications-list::-webkit-scrollbar-thumb {
  background: #ff7f50;
  border: 2px solid #000;
}

.activity-feed::-webkit-scrollbar-thumb:hover,
.notifications-list::-webkit-scrollbar-thumb:hover {
  background: #ff5722;
}

/* Responsive styling */
@media (max-width: 1200px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

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
    border-bottom: 4px solid #ff7f50;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 2rem;
  }

  .profile-quick-view {
    flex-direction: column;
    text-align: center;
  }

  .profile-avatar {
    margin: 0 auto 1rem;
  }

  .profile-actions {
    width: 100%;
    margin-top: 1rem;
  }

  .quick-actions-container {
    grid-template-columns: 1fr;
    margin-bottom: 2rem;
  }
}
</style>
