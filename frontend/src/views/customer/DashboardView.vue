<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useServiceRequestStore } from '@/stores/serviceRequest'
import { useAuthStore } from '@/stores/auth'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'
import { NeoButton, NeoCard, NeoBadge, NeoIcon } from '@/components/ui'
import { toastService } from '@/services/toastService'
import { professionalAPI } from '@/services/api'

const router = useRouter()
const route = useRoute()
const serviceRequestStore = useServiceRequestStore()
const authStore = useAuthStore()

// Check if we're on the main customer route
const isMainDashboard = computed(() => route.path === '/customer')

// Customer sidebar menu items
const menuItems = [
  {
    label: 'Dashboard',
    route: '/customer',
    icon: 'layout-dashboard',
    exactPath: true,
  },
  {
    label: 'Service Requests',
    route: '/customer/requests',
    icon: 'clipboard-list',
  },
  {
    label: 'Profile',
    route: '/customer/profile',
    icon: 'user',
  },
]

// Customer data
const customerData = ref({
  name: '',
  email: '',
  phone: '',
  profileImage: '',
  joinDate: '',
  totalRequests: 0,
})

// Service requests
const serviceRequests = ref([])

// Dashboard stats
const stats = ref([])

// Recent activity
const recentActivity = ref([])

// Loading state
const isLoading = ref(false)

// Fetch data on component mount
const pollingInterval = ref(null);

onMounted(async () => {
  try {
    isLoading.value = true

    // Fetch customer data and service requests
    await Promise.all([
      authStore.fetchUser(),
      serviceRequestStore.fetchCustomerRequests(),
      serviceRequestStore.fetchCustomerActivityFeed(),
      serviceRequestStore.fetchCustomerStats()
    ])

    // Set profile data if user is available in the store
    if (authStore.user) {
      const profileImageUrl = authStore.user.profile_image
        ? professionalAPI.getProfilePictureUrl(authStore.user.profile_image)
        : 'https://avatar.iran.liara.run/public/11'

      customerData.value = {
        name: authStore.user.name,
        email: authStore.user.email,
        phone: authStore.user.phone,
        profileImage: profileImageUrl,
        joinDate: authStore.user.date_created,
        totalRequests: authStore.user.total_requests || 0,
      }
    }

    // Set service requests and update stats
    serviceRequests.value = serviceRequestStore.customerRequests
    calculateDashboardStats()

    // Set up polling to refresh data every 60 seconds
    pollingInterval.value = setInterval(async () => {
      if (isMainDashboard.value) {
        await Promise.all([
          serviceRequestStore.fetchCustomerRequests(),
          serviceRequestStore.fetchCustomerActivityFeed(),
          serviceRequestStore.fetchCustomerStats()
        ]);
        serviceRequests.value = serviceRequestStore.customerRequests;
        calculateDashboardStats();
      }
    }, 60000); // 60 seconds
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
    toastService.error('Failed to load dashboard data')
  } finally {
    isLoading.value = false
  }
})

// Clean up interval when component is unmounted
onUnmounted(() => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value);
  }
})

// Watch for route changes
watch(isMainDashboard, async (newValue) => {
  if (newValue) {
    await Promise.all([
      fetchCustomerData(),
      fetchServiceRequests()
    ])
  }
})

// Helper function to get the status badge variant
const getStatusBadgeVariant = (status) => {
  switch (status?.toLowerCase()) {
    case 'completed':
      return 'success'
    case 'assigned':
      return 'primary'
    case 'requested':
      return 'warning'
    case 'cancelled':
      return 'danger'
    case 'closed':
      return 'secondary'
    default:
      return 'info'
  }
}

// Fetch customer data
const fetchCustomerData = async () => {
  try {
    await authStore.fetchUser()
    const user = authStore.user

    const profileImageUrl = user.profile_image
      ? professionalAPI.getProfilePictureUrl(user.profile_image)
      : 'https://avatar.iran.liara.run/public/11'

    customerData.value = {
      name: user.name,
      email: user.email,
      phone: user.phone,
      profileImage: profileImageUrl,
      joinDate: user.date_created,
      totalRequests: user.total_requests || 0,
    }
  } catch (error) {
    console.error('Failed to load customer data:', error)
    toastService.error('Failed to load customer data.')
  }
}

// Fetch service requests
const fetchServiceRequests = async () => {
  try {
    await serviceRequestStore.fetchCustomerRequests()
    serviceRequests.value = serviceRequestStore.customerRequests

    // Update stats
    calculateDashboardStats()
  } catch (error) {
    console.error('Failed to fetch requests:', error)
    toastService.error('Failed to load service requests.')
  }
}

// Calculate dashboard stats
const calculateDashboardStats = () => {
  // Update stats based on the fetched service requests
  stats.value = [
    {
      id: 1,
      label: 'Total Requests',
      value: serviceRequestStore.totalRequests,
      icon: 'clipboard-list',
      variant: 'primary',
    },
    {
      id: 2,
      label: 'Completed Jobs',
      value: serviceRequestStore.completedJobs,
      icon: 'check-circle',
      variant: 'success',
    },
    {
      id: 3,
      label: 'Pending Jobs',
      value: serviceRequestStore.pendingJobs,
      icon: 'clock',
      variant: 'warning',
    },
    {
      id: 5,
      label: 'Total Spent',
      value: `₹${serviceRequestStore.totalSpent.toFixed(2)}`,
      icon: 'indian-rupee',
      variant: 'danger',
    },
  ]

  // Update recent activity
  recentActivity.value = serviceRequestStore.recentActivity?.map(activity => ({
    ...activity,
  })) || []
}
</script>

<template>
  <div class="neo-brutalist">
    <div class="p-0 row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 sidebar-container ps-0 overflow-hidden">
        <NeoDashboardSidebar :menuItems="menuItems" title="Customer" />
      </div>

      <!-- Main Content -->
      <div class="col-md-9 col-lg-10 p-4 main-content">
        <div v-if="isMainDashboard">
          <!-- Dashboard Header -->
          <div class="header-section mb-4">
            <div>
              <h1 class="page-title mb-2">Dashboard</h1>
              <div class="welcome-tag">
                <span>Welcome Back, {{ customerData.name.split(' ')[0] }}!</span>
              </div>
            </div>
          </div>

          <!-- Profile Quick View -->
          <div class="profile-quick-view mb-4">
            <div class="profile-avatar">
              <img :src="customerData.profileImage" alt="Profile" />
            </div>
            <div class="profile-info">
              <h2>{{ customerData.name }}</h2>
              <div class="profile-email">{{ customerData.email }}</div>
            </div>
            <div class="profile-actions">
              <NeoButton variant="primary" size="sm" @click="router.push('/customer/profile')">
                <NeoIcon name="user" size="16" class="me-2" /> View Profile
              </NeoButton>
            </div>
          </div>

          <!-- Stats Grid -->
          <div class="stats-container">
            <NeoCard v-for="stat in stats" :key="stat.id" class="stat-card">
              <div class="stat-icon">
                <NeoIcon :name="stat.icon" size="24" />
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ stat.value }}</div>
                <div class="stat-label">{{ stat.label }}</div>
              </div>
            </NeoCard>
          </div>

          <!-- Dashboard Content -->
          <div class="row g-4">
            <!-- Recent Requests -->
            <div class="col-lg-7">
              <NeoCard class="h-100">
                <template #title>Recent Service Requests</template>
                <template #subtitle>
                  <div class="d-flex justify-content-end">
                    <NeoButton variant="link" @click="router.push('/customer/requests')">
                      View All
                    </NeoButton>
                  </div>
                </template>

                <div v-if="serviceRequests.length === 0" class="text-center py-4">
                  <div class="mb-3">
                    <NeoIcon name="clipboard-list" size="48" class="text-muted" />
                  </div>
                  <h4>No service requests yet</h4>
                  <p class="text-muted mb-3">Book your first service to get started</p>
                  <NeoButton variant="primary" @click="router.push('/customer/requests')">
                    Book a Service
                  </NeoButton>
                </div>

                <div v-else class="table-responsive">
                  <table class="table table-hover align-middle table-sm service-request-table">
                    <thead>
                      <tr>
                        <th>Service</th>
                        <th>Date</th>
                        <th>Status</th>
                        <th>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="request in serviceRequests.slice(0, 4)" :key="request.id"
                        @click="router.push(`/customer/requests?requestId=${request.id}`)" style="cursor: pointer"
                        class="active-row">
                        <td>
                          <div class="d-flex align-items-center">
                            <div class="service-icon me-2">
                              <NeoIcon name="wrench" size="20" />
                            </div>
                            <div>
                              <div class="service-name fw-bold">{{ request.service?.name }}</div>
                              <div class="service-price text-muted">₹{{ request.service?.price }}</div>
                            </div>
                          </div>
                        </td>
                        <td>{{ new Date(request.date_of_request).toLocaleDateString() }}</td>
                        <td>
                          <NeoBadge :variant="getStatusBadgeVariant(request.service_status)">
                            {{ request.service_status }}
                          </NeoBadge>
                        </td>
                        <td>
                          <NeoButton variant="link" size="sm"
                            @click.stop="router.push(`/customer/requests?requestId=${request.id}`)">
                            View
                          </NeoButton>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </NeoCard>
            </div>

            <!-- Recent Activity -->
            <div class="col-lg-5">
              <NeoCard class="h-100">
                <template #title>Recent Activity</template>

                <div v-if="recentActivity.length === 0" class="text-center py-4">
                  <div class="mb-3">
                    <NeoIcon name="activity" size="48" class="text-muted" />
                  </div>
                  <h4>No activity yet</h4>
                  <p class="text-muted">Your recent activities will appear here</p>
                </div>

                <div class="activity-feed">

                  <div v-for="activity in recentActivity" :key="activity.id">
                    <div v-if="activity.action" class="activity-item">
                      <div class="activity-icon">
                        <NeoIcon v-if="activity.action === 'accepted'" name="check-circle" />
                        <NeoIcon v-else-if="activity.action === 'completed'" name="check-circle" />
                        <NeoIcon v-else-if="activity.type === 'payment'" name="indian-rupee" />
                        <NeoIcon v-else-if="activity.action === 'canceled'" name="x-circle" />
                        <NeoIcon v-else name="info" />

                      </div>
                      <div class="activity-content">

                        <div class="activity-message">
                          <span v-if="activity.type === 'service_request' && activity.action === 'created'">
                            You requested a <strong>{{ activity.service }}</strong> service
                          </span>
                          <span v-else-if="
                            activity.type === 'service_request' && activity.action === 'completed'
                          ">
                            Your <strong>{{ activity.service }}</strong> service was completed
                          </span>
                          <span v-else-if="activity.type === 'payment'">
                            You made a payment of <strong>{{ activity.amount }}</strong> for
                            <strong>{{ activity.service }}</strong>
                          </span>
                          <span v-else-if="
                            activity.type === 'service_request' && activity.action === 'accepted'
                          ">
                            Your request for <strong>{{ activity.service }}</strong> service was accepted
                          </span>
                          <span v-else-if="
                            activity.type === 'service_request' && activity.action === 'canceled'
                          ">
                            You cancelled a <strong>{{ activity.service }}</strong> service
                          </span>

                        </div>

                      </div>
                    </div>

                  </div>
                </div>
              </NeoCard>
            </div>
          </div>

          <!-- Services by Category -->
          <div class="row mt-4">
            <div class="col-12">
              <NeoCard>
                <template #title>Services by Category</template>

                <div v-if="serviceRequestStore.servicesByCategory.length === 0" class="text-center py-4">
                  <div class="mb-3">
                    <NeoIcon name="pie-chart" size="48" class="text-muted" />
                  </div>
                  <h4>No service data yet</h4>
                  <p class="text-muted">Book services to see your category breakdown</p>
                </div>

                <div v-else class="row justify-content-center">
                  <div class="col-lg-8">
                    <div class="services-category-chart">
                      <div v-for="service in serviceRequestStore.servicesByCategory" :key="service.name"
                        class="service-category-item">
                        <div class="service-category-name">{{ service.name }}</div>
                        <div class="service-category-bar-container">
                          <div class="service-category-bar"
                            :style="{ width: `${(service.count / Math.max(...serviceRequestStore.servicesByCategory.map(s => s.count))) * 100}%` }">
                          </div>
                          <div class="service-category-count">{{ service.count }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </NeoCard>
            </div>
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
  background-image: radial-gradient(#000 1px, transparent 0);
  background-size: 20px 20px;
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
  border-right: 5px solid #000;
}

.main-content {
  padding: 2rem;
  overflow-y: auto;
  height: calc(100vh - 74px);
}

/* Header styling */
.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  position: relative;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 0.5rem;
  position: relative;
  display: inline-block;
  text-shadow: 3px 3px 0 #ff7f50;
  transform: skew(-5deg);
}

.welcome-tag {
  transform: rotate(-5deg);
}

.welcome-tag span {
  background-color: #ffff00;
  padding: 0.5rem 1rem;
  border: 4px solid #000;
  box-shadow: 6px 6px 0 #000;
  font-weight: 700;
  display: inline-block;
  transform: skew(-3deg);
}

/* Profile quick view */
.profile-quick-view {
  background: white;
  border: 5px solid #000;
  margin-bottom: 2rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 12px 12px 0 #000;
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
  background-color: rgba(255, 127, 80, 0.3);
  clip-path: polygon(100% 0, 0 0, 100% 100%);
  z-index: 0;
}

.profile-quick-view::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 30%;
  height: 100%;
  background-color: rgba(0, 255, 255, 0.2);
  clip-path: polygon(0 100%, 0 30%, 100% 100%);
  z-index: 0;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border: 4px solid #000;
  border-radius: 0;
  overflow: hidden;
  transform: rotate(-5deg);
  box-shadow: 6px 6px 0 #000;
  z-index: 1;
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  flex: 1;
  z-index: 1;
}

.profile-info h2 {
  font-weight: 900;
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
  transform: skew(-3deg);
}

.profile-email {
  font-weight: 700;
  color: #ff7f50;
  margin-bottom: 0.25rem;
  letter-spacing: 0.5px;
  text-decoration: underline;
}

.profile-join-date {
  font-size: 0.875rem;
  font-weight: 700;
  color: #555;
  background-color: #e6e6e6;
  display: inline-block;
  padding: 2px 6px;
  border: 2px solid #000;
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
  box-shadow: 10px 10px 0 #000;
  transition: transform 0.2s ease;
  background: white;
  overflow: hidden;
  position: relative;
}

.stat-card::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 40px;
  height: 40px;
  background-color: #ff7f50;
  clip-path: polygon(100% 0, 0 100%, 100% 100%);
}

.stat-card:hover {
  transform: translateY(-7px);
}

.stat-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background-color: #ff7f50;
  border: 3px solid #000;
  margin-bottom: 1rem;
  transform: rotate(-8deg);
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  margin-bottom: 0.25rem;
  transform: skew(-3deg);
}

.stat-label {
  font-weight: 700;
  color: #000;
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background-color: #e6e6e6;
  display: inline-block;
  padding: 2px 6px;
  transform: rotate(-2deg);
}

/* Service request table */
.service-request-table {
  border: 3px solid #000;
}

.service-request-table th {
  font-weight: 800;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  background-color: #000;
  color: white;
  padding: 12px;
}

.service-request-table td {
  border-bottom: 2px solid #000;
  padding: 12px;
}

.service-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #ff7f50;
  border: 2px solid #000;
  transform: rotate(-3deg);
}

.service-name {
  font-weight: 700;
}

.service-price {
  font-size: 0.875rem;
  background-color: #e6e6e6;
  display: inline-block;
  padding: 1px 5px;
  border: 1px solid #000;
}

.active-row {
  transition: all 0.2s ease;
}

.active-row:hover {
  background-color: rgba(255, 127, 80, 0.2);
  transform: translateX(8px);
}

/* Activity feed */
.activity-feed {
  max-height: 400px;
  overflow-y: auto;
  border: 3px solid #000;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 3px solid #000;
  transition: all 0.2s ease;
}

.activity-item:hover {
  background-color: rgba(255, 127, 80, 0.15);
  transform: translateX(5px);
}

.activity-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #ff7f50;
  border: 2px solid #000;
  flex-shrink: 0;
  transform: rotate(-5deg);
}

.activity-content {
  flex: 1;
}

.activity-message {
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.activity-message strong {
  background-color: #e6e6e6;
  padding: 0 4px;
  border: 1px solid #000;
  display: inline-block;
  transform: skew(-3deg);
}

.activity-date {
  font-size: 0.75rem;
  color: #000;
  font-weight: 600;
  background-color: #ffff00;
  display: inline-block;
  padding: 1px 5px;
  border: 1px solid #000;
  transform: rotate(-1deg);
}

@media (max-width: 1200px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }

  .profile-quick-view {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* Services by Category Styles */
.services-category-chart {
  margin-top: 1rem;
  border: 3px solid #000;
  padding: 1rem;
  background-color: white;
  box-shadow: 8px 8px 0 #000;
}

.service-category-item {
  display: flex;
  margin-bottom: 1rem;
  align-items: center;
  padding: 0.75rem;
  border: 2px solid #000;
  background-color: #f9f9f9;
}

.service-category-item:nth-child(odd) {
  transform: rotate(-1deg);
}

.service-category-item:nth-child(even) {
  transform: rotate(1deg);
}

.service-category-name {
  flex: 0 0 150px;
  font-weight: 700;
  background-color: #ffff00;
  padding: 3px 8px;
  border: 2px solid #000;
  transform: skew(-5deg);
}

.service-category-bar-container {
  flex: 1;
  display: flex;
  align-items: center;
  height: 30px;
  background-color: white;
  border: 2px solid #000;
  margin-left: 10px;
}

.service-category-bar {
  height: 100%;
  background-color: #ff7f50;
  border-right: 2px solid #000;
  position: relative;
  min-width: 20px;
  transition: width 0.3s ease;
}

.service-category-count {
  margin-left: 10px;
  font-weight: bold;
  background-color: white;
  border: 2px solid #000;
  padding: 2px 8px;
  transform: rotate(-3deg);
}
</style>
