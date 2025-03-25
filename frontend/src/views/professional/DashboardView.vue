<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'
import NeoCard from '@/components/ui/NeoCard.vue'
import NeoButton from '@/components/ui/NeoButton.vue'
import NeoBadge from '@/components/ui/NeoBadge.vue'

const router = useRouter()

// Professional sidebar menu items
const menuItems = [
  {
    label: 'Dashboard',
    route: '/professional',
    icon: 'fas fa-tachometer-alt',
    exactPath: true,
  },
  {
    label: 'Service Requests',
    route: '/professional/requests',
    icon: 'fas fa-clipboard-list',
  },
  {
    label: 'Profile',
    route: '/professional/profile',
    icon: 'fas fa-user',
  },
]

// Mock professional data
const professionalData = ref({
  name: 'Mike Smith',
  serviceType: 'Plumbing',
  experience: '8 years',
  profileImage: 'https://randomuser.me/api/portraits/men/41.jpg',
  joinDate: '2023-02-10',
  completedJobs: 37,
  status: 'Approved',
})

// Mock service request data
const serviceRequests = ref([
  {
    id: 'SR2001',
    customer: 'John Doe',
    serviceName: 'Plumbing',
    date: '2023-05-15',
    status: 'Completed',
    amount: '₹550',
  },
  {
    id: 'SR2002',
    customer: 'Jane Brown',
    serviceName: 'Plumbing',
    date: '2023-05-20',
    status: 'Accepted',
    amount: '₹650',
  },
  {
    id: 'SR2003',
    customer: 'Robert Johnson',
    serviceName: 'Plumbing',
    date: '2023-05-22',
    status: 'Pending',
    amount: '₹450',
  },
  {
    id: 'SR2004',
    customer: 'Maria Garcia',
    serviceName: 'Plumbing',
    date: '2023-05-25',
    status: 'Rejected',
    amount: '₹350',
  },
])

// Dashboard stats
const stats = [
  {
    id: 1,
    label: 'Total Earnings',
    value: '₹16,500',
    icon: 'fas fa-rupee-sign',
    variant: 'success',
  },
  {
    id: 2,
    label: 'Completed Jobs',
    value: '37',
    icon: 'fas fa-check-circle',
    variant: 'primary',
  },
  {
    id: 3,
    label: 'Pending Jobs',
    value: serviceRequests.value.filter((req) => req.status === 'Pending').length.toString(),
    icon: 'fas fa-clock',
    variant: 'warning',
  },
  {
    id: 4,
    label: 'Accepted Jobs',
    value: serviceRequests.value.filter((req) => req.status === 'Accepted').length.toString(),
    icon: 'fas fa-thumbs-up',
    variant: 'info',
  },
]

// Mock upcoming appointments
const upcomingAppointments = ref([
  {
    id: 'A2001',
    customer: 'Jane Brown',
    service: 'Plumbing',
    date: '2023-05-30',
    time: '10:00 - 12:00',
    address: '456 Park Avenue, Mumbai',
  },
])

// Mock recent activity
const recentActivity = ref([
  {
    id: 1,
    type: 'service_request',
    action: 'accepted',
    customer: 'Jane Brown',
    service: 'Plumbing',
    date: '1 day ago',
  },
  {
    id: 2,
    type: 'service_request',
    action: 'completed',
    customer: 'John Doe',
    service: 'Plumbing',
    date: '3 days ago',
  },
  {
    id: 3,
    type: 'payment',
    action: 'received',
    amount: '₹550',
    customer: 'John Doe',
    date: '3 days ago',
  },
  {
    id: 4,
    type: 'service_request',
    action: 'rejected',
    customer: 'Maria Garcia',
    service: 'Plumbing',
    date: '5 days ago',
  },
])

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
</script>

<template>
  <div class="neo-brutalist">
    <div class="dashboard-wrapper">
      <!-- Sidebar -->
      <div class="sidebar-container">
        <NeoDashboardSidebar
          :menuItems="menuItems"
          title="Professional"
          @item-action="handleMenuAction"
        />
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <div class="header-section">
          <h1 class="page-title">Dashboard</h1>
          <div class="status-badge">
            <NeoBadge :variant="getStatusBadgeClass(professionalData.status)" size="lg">
              {{ professionalData.status }}
            </NeoBadge>
          </div>
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
                <NeoButton variant="dark" size="sm" @click="viewAllRequests"> View All </NeoButton>
              </div>
            </template>

            <div class="table-wrapper">
              <table class="request-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Customer</th>
                    <th>Service</th>
                    <th>Date</th>
                    <th>Status</th>
                    <th>Amount</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="request in serviceRequests" :key="request.id" class="request-row">
                    <td>
                      <div class="request-id">{{ request.id }}</div>
                    </td>
                    <td>{{ request.customer }}</td>
                    <td>{{ request.serviceName }}</td>
                    <td>{{ request.date }}</td>
                    <td>
                      <NeoBadge :variant="getStatusBadgeClass(request.status)">
                        {{ request.status }}
                      </NeoBadge>
                    </td>
                    <td class="amount">{{ request.amount }}</td>
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
                <div class="activity-icon">
                  <i
                    v-if="activity.type === 'service_request' && activity.action === 'accepted'"
                    class="fas fa-check-circle"
                  ></i>
                  <i
                    v-else-if="
                      activity.type === 'service_request' && activity.action === 'completed'
                    "
                    class="fas fa-check-double"
                  ></i>
                  <i v-else-if="activity.type === 'payment'" class="fas fa-rupee-sign"></i>
                  <i
                    v-else-if="
                      activity.type === 'service_request' && activity.action === 'rejected'
                    "
                    class="fas fa-times-circle"
                  ></i>
                </div>
                <div class="activity-content">
                  <div class="activity-message">
                    <span
                      v-if="activity.type === 'service_request' && activity.action === 'accepted'"
                    >
                      You accepted a request from <strong>{{ activity.customer }}</strong>
                    </span>
                    <span
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'completed'
                      "
                    >
                      You completed a service for <strong>{{ activity.customer }}</strong>
                    </span>
                    <span v-else-if="activity.type === 'payment'">
                      Payment of <strong>{{ activity.amount }}</strong> received from
                      <strong>{{ activity.customer }}</strong>
                    </span>
                    <span
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'rejected'
                      "
                    >
                      You rejected a request from <strong>{{ activity.customer }}</strong>
                    </span>
                  </div>
                  <div class="activity-time">{{ activity.date }}</div>
                </div>
              </div>
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
              </div>
            </div>

            <div v-else class="appointments-list">
              <div
                v-for="appointment in upcomingAppointments"
                :key="appointment.id"
                class="appointment-item"
              >
                <div class="appointment-header">
                  <h6 class="appointment-service">{{ appointment.service }}</h6>
                  <NeoBadge variant="primary">Upcoming</NeoBadge>
                </div>
                <div class="appointment-details">
                  <div class="appointment-detail">
                    <i class="fas fa-user"></i>
                    <span>{{ appointment.customer }}</span>
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
                  <NeoButton variant="dark" size="sm">Get Directions</NeoButton>
                  <NeoButton variant="danger" size="sm" outline>Cancel</NeoButton>
                </div>
              </div>
            </div>
          </NeoCard>
        </div>
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
  border-right: 4px solid #ff7f50;
  min-height: 100vh;
  position: sticky;
  top: 0;
  height: 100vh;
}

.main-content {
  padding: 2rem;
}

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
  color: #000;
  letter-spacing: -1px;
  position: relative;
  display: inline-block;
}

.page-title::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 4px;
  background-color: #ff7f50;
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

.service-type {
  font-weight: 700;
  color: #ff7f50;
  margin-bottom: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.rating {
  font-weight: 700;
  color: #ffc107;
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
    background-color: white;
    border-right: none;
    border-bottom: 4px solid #ff7f50;
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
