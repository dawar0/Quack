<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'

const router = useRouter()

// Customer sidebar menu items
const menuItems = [
  {
    label: 'Dashboard',
    route: '/customer',
    icon: 'fas fa-tachometer-alt',
    exactPath: true,
  },
  {
    label: 'Services',
    route: '/customer/services',
    icon: 'fas fa-concierge-bell',
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
  {
    label: 'Logout',
    route: '#',
    icon: 'fas fa-sign-out-alt',
    action: true,
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

// Dashboard stats
const stats = {
  totalRequests: serviceRequests.value.length,
  completed: serviceRequests.value.filter((req) => req.status === 'Completed').length,
  inProgress: serviceRequests.value.filter((req) => req.status === 'Assigned').length,
  pending: serviceRequests.value.filter((req) => req.status === 'Requested').length,
  cancelled: serviceRequests.value.filter((req) => req.status === 'Cancelled').length,
}

// Mock notifications
const notifications = ref([
  {
    id: 1,
    message: 'Your service request SR1002 has been assigned to Sarah Wilson',
    time: '2 hours ago',
    read: false,
  },
  {
    id: 2,
    message: 'Your service request SR1001 has been marked as completed',
    time: '1 day ago',
    read: true,
  },
  {
    id: 3,
    message: 'Mike Smith has sent you a message regarding your plumbing service',
    time: '2 days ago',
    read: true,
  },
])

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

// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  const statusClasses = {
    Completed: 'bg-success',
    Assigned: 'bg-primary',
    Requested: 'bg-warning text-dark',
    Cancelled: 'bg-danger',
  }
  return statusClasses[status] || 'bg-secondary'
}

// Navigate to service requests page
const viewAllRequests = () => {
  router.push('/customer/requests')
}

// Navigate to browse services page
const browseServices = () => {
  router.push('/customer/services')
}

// Mark notification as read
const markAsRead = (notificationId) => {
  const notification = notifications.value.find((n) => n.id === notificationId)
  if (notification) {
    notification.read = true
  }
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
  <div class="container-fluid p-0">
    <div class="row m-0">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 p-0 sidebar-container d-md-block">
        <NeoDashboardSidebar
          :menuItems="menuItems"
          title="Customer"
          @item-action="handleMenuAction"
        />
      </div>

      <!-- Main Content -->
      <div class="col-md-9 col-lg-10 p-4">
        <div class="row mb-4">
          <div class="col">
            <h2>Dashboard</h2>
            <p class="text-muted">Welcome back, {{ userData.name }}</p>
          </div>
        </div>

        <!-- Stats Cards -->
        <div class="row mb-4">
          <div class="col-md-4 col-xl-3 mb-3">
            <div class="card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                  <div class="text-muted">Total Requests</div>
                  <div class="rounded-circle bg-primary bg-opacity-10 p-2">
                    <i class="fas fa-clipboard-list text-primary"></i>
                  </div>
                </div>
                <h3 class="mb-0">{{ stats.totalRequests }}</h3>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-xl-3 mb-3">
            <div class="card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                  <div class="text-muted">Completed</div>
                  <div class="rounded-circle bg-success bg-opacity-10 p-2">
                    <i class="fas fa-check-circle text-success"></i>
                  </div>
                </div>
                <h3 class="mb-0">{{ stats.completed }}</h3>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-xl-3 mb-3">
            <div class="card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                  <div class="text-muted">In Progress</div>
                  <div class="rounded-circle bg-primary bg-opacity-10 p-2">
                    <i class="fas fa-clock text-primary"></i>
                  </div>
                </div>
                <h3 class="mb-0">{{ stats.inProgress }}</h3>
              </div>
            </div>
          </div>

          <div class="col-md-4 col-xl-3 mb-3">
            <div class="card border-0 shadow-sm">
              <div class="card-body">
                <div class="d-flex justify-content-between mb-2">
                  <div class="text-muted">Pending</div>
                  <div class="rounded-circle bg-warning bg-opacity-10 p-2">
                    <i class="fas fa-hourglass-half text-warning"></i>
                  </div>
                </div>
                <h3 class="mb-0">{{ stats.pending }}</h3>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <!-- Left Column -->
          <div class="col-lg-8">
            <!-- Recent Service Requests -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">Recent Service Requests</h5>
                  <button class="btn btn-sm btn-outline-primary" @click="viewAllRequests">
                    View All
                  </button>
                </div>
              </div>
              <div class="card-body p-0">
                <div class="table-responsive">
                  <table class="table mb-0">
                    <thead class="table-light">
                      <tr>
                        <th>ID</th>
                        <th>Service</th>
                        <th>Date</th>
                        <th>Professional</th>
                        <th>Status</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="request in serviceRequests" :key="request.id">
                        <td>{{ request.id }}</td>
                        <td>{{ request.serviceName }}</td>
                        <td>{{ request.date }}</td>
                        <td>{{ request.professional || '—' }}</td>
                        <td>
                          <span :class="`badge ${getStatusBadgeClass(request.status)}`">
                            {{ request.status }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Upcoming Appointments -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white py-3">
                <h5 class="mb-0">Upcoming Appointments</h5>
              </div>
              <div class="card-body">
                <div v-if="upcomingAppointments.length === 0" class="text-center py-4">
                  <p class="text-muted mb-3">You have no upcoming appointments</p>
                  <button class="btn btn-primary" @click="browseServices">Book a Service</button>
                </div>

                <div
                  v-else
                  v-for="appointment in upcomingAppointments"
                  :key="appointment.id"
                  class="mb-3"
                >
                  <div class="card border-0 bg-light">
                    <div class="card-body">
                      <div class="d-flex justify-content-between mb-2">
                        <h6 class="mb-0">{{ appointment.service }} Service</h6>
                        <span class="badge bg-primary">Upcoming</span>
                      </div>
                      <div class="mb-2">
                        <i class="fas fa-user me-2 text-muted"></i>
                        <span>{{ appointment.professional }}</span>
                      </div>
                      <div class="mb-2">
                        <i class="fas fa-calendar me-2 text-muted"></i>
                        <span>{{ appointment.date }}</span>
                      </div>
                      <div class="mb-2">
                        <i class="fas fa-clock me-2 text-muted"></i>
                        <span>{{ appointment.time }}</span>
                      </div>
                      <div>
                        <i class="fas fa-map-marker-alt me-2 text-muted"></i>
                        <span>{{ appointment.address }}</span>
                      </div>
                      <div class="mt-3">
                        <button class="btn btn-sm btn-outline-secondary me-2">Reschedule</button>
                        <button class="btn btn-sm btn-outline-danger">Cancel</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white py-3">
                <h5 class="mb-0">Quick Actions</h5>
              </div>
              <div class="card-body">
                <div class="row">
                  <div class="col-md-4 mb-3">
                    <div class="d-grid">
                      <button class="btn btn-primary" @click="browseServices">
                        <i class="fas fa-plus-circle me-2"></i> Book a Service
                      </button>
                    </div>
                  </div>
                  <div class="col-md-4 mb-3">
                    <div class="d-grid">
                      <button class="btn btn-outline-primary" @click="viewAllRequests">
                        <i class="fas fa-list me-2"></i> View Requests
                      </button>
                    </div>
                  </div>
                  <div class="col-md-4 mb-3">
                    <div class="d-grid">
                      <button
                        class="btn btn-outline-primary"
                        @click="router.push('/customer/profile')"
                      >
                        <i class="fas fa-user me-2"></i> Edit Profile
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="col-lg-4">
            <!-- User Profile Card -->
            <div class="card shadow-sm mb-4">
              <div class="card-body text-center py-4">
                <img
                  :src="userData.profileImage"
                  alt="Profile picture"
                  class="rounded-circle img-fluid mb-3"
                  style="width: 100px; height: 100px; object-fit: cover"
                />
                <h5 class="mb-1">{{ userData.name }}</h5>
                <p class="text-muted">{{ userData.email }}</p>
                <p class="small text-muted">Member since {{ userData.joinDate }}</p>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="router.push('/customer/profile')"
                >
                  Edit Profile
                </button>
              </div>
            </div>

            <!-- Notifications -->
            <div class="card shadow-sm mb-4">
              <div class="card-header bg-white py-3">
                <div class="d-flex justify-content-between align-items-center">
                  <h5 class="mb-0">Notifications</h5>
                  <span class="badge bg-primary rounded-pill">
                    {{ notifications.filter((n) => !n.read).length }}
                  </span>
                </div>
              </div>
              <div class="card-body p-0">
                <div v-if="notifications.length === 0" class="text-center py-4">
                  <p class="text-muted mb-0">No notifications</p>
                </div>

                <div v-else class="list-group list-group-flush">
                  <div
                    v-for="notification in notifications"
                    :key="notification.id"
                    class="list-group-item list-group-item-action"
                    :class="{ 'bg-light': !notification.read }"
                  >
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1">{{ notification.message }}</h6>
                      <small v-if="!notification.read" class="badge bg-primary">New</small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                      <small class="text-muted">{{ notification.time }}</small>
                      <button
                        v-if="!notification.read"
                        class="btn btn-sm text-primary"
                        @click="markAsRead(notification.id)"
                      >
                        Mark as read
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Recent Activity -->
            <div class="card shadow-sm">
              <div class="card-header bg-white py-3">
                <h5 class="mb-0">Recent Activity</h5>
              </div>
              <div class="card-body p-0">
                <div class="list-group list-group-flush">
                  <div
                    v-for="activity in recentActivity"
                    :key="activity.id"
                    class="list-group-item"
                  >
                    <div
                      v-if="activity.type === 'service_request' && activity.action === 'created'"
                    >
                      <i class="fas fa-plus-circle text-primary me-2"></i>
                      <span>You requested a {{ activity.service }} service</span>
                    </div>
                    <div
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'completed'
                      "
                    >
                      <i class="fas fa-check-circle text-success me-2"></i>
                      <span>Your {{ activity.service }} service was completed</span>
                    </div>
                    <div v-else-if="activity.type === 'payment'">
                      <i class="fas fa-credit-card text-info me-2"></i>
                      <span
                        >You made a payment of {{ activity.amount }} for
                        {{ activity.service }}</span
                      >
                    </div>
                    <div
                      v-else-if="
                        activity.type === 'service_request' && activity.action === 'cancelled'
                      "
                    >
                      <i class="fas fa-times-circle text-danger me-2"></i>
                      <span>You cancelled a {{ activity.service }} service</span>
                    </div>
                    <div class="mt-1">
                      <small class="text-muted">{{ activity.date }}</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar-container {
  padding-left: 0;
  padding-right: 0;
}

@media (max-width: 767.98px) {
  .sidebar-container {
    margin-bottom: 20px;
  }
}
</style>
