<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAdminStore } from '@/stores/admin'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'
import { NeoButton, NeoCard, NeoIcon } from '@/components/ui'
import { professionalAPI } from '@/services/api'
import { toastService } from '@/services/toastService'

const router = useRouter()
const route = useRoute()
const adminStore = useAdminStore()
const currentRoute = computed(() => {
  return route.name || ''
})

// Menu items for navigation
const menuItems = [
  {
    label: 'Overview',
    route: '/admin',
    routeName: 'admin',
    icon: 'home',
  },
  {
    label: 'Services',
    route: '/admin/services',
    routeName: 'admin-services',
    icon: 'wrench',
  },
  {
    label: 'Professionals',
    route: '/admin/professionals',
    routeName: 'admin-professionals',
    icon: 'user-cog',
  },
  {
    label: 'Customers',
    route: '/admin/customers',
    routeName: 'admin-customers',
    icon: 'users',
  },
  {
    label: 'Reports',
    route: '/admin/reports',
    routeName: 'admin-reports',
    icon: 'bar-chart',
  },
]

// Dashboard statistics
const stats = ref([])

// Recent activity
const recentActivity = ref([])

// Helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}

// Helper function to format time ago
const formatTimeAgo = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))

  if (hours < 24) {
    return `${hours} hours ago`
  } else {
    return `${days} days ago`
  }
}

// Fetch dashboard data
const fetchDashboardData = async () => {
  try {
    await adminStore.fetchDashboardStats()

    // Update stats
    stats.value = [
      {
        id: 'customers',
        label: 'Total Customers',
        value: adminStore.dashboardStats.total_customers,
        variant: 'primary',
        route: '/admin/customers',
        icon: 'users',
      },
      {
        id: 'professionals',
        label: 'Total Professionals',
        value: adminStore.dashboardStats.total_professionals,
        variant: 'success',
        route: '/admin/professionals',
        icon: 'user-cog',
      },
      {
        id: 'activeServices',
        label: 'Active Services',
        value: adminStore.dashboardStats.active_services,
        variant: 'info',
        route: '/admin/services',
        icon: 'activity',
      },
      {
        id: 'pendingRequests',
        label: 'Pending Requests',
        value: adminStore.dashboardStats.pending_requests,
        variant: 'warning',
        route: '/admin/professionals',
        icon: 'clock',
      },
      {
        id: 'pendingApprovals',
        label: 'Pending Approvals',
        value: adminStore.dashboardStats.pending_approvals,
        variant: 'danger',
        route: '/admin/professionals',
        icon: 'user-check',
      },
      {
        id: 'completedServices',
        label: 'Completed Services',
        value: adminStore.dashboardStats.completed_services,
        variant: 'secondary',
        route: '/admin/services',
        icon: 'check-circle',
      },
    ]

    // Update recent activity
    recentActivity.value = adminStore.dashboardStats.recent_activity.map((activity) => ({
      ...activity,
      timeAgo: formatTimeAgo(activity.timestamp),
    }))
  } catch (error) {
    toastService.error(error.response?.data?.message || 'Failed to load dashboard data.')
  }
}

// Fetch data on component mount
onMounted(() => {
  if (currentRoute.value === 'admin') {
    fetchDashboardData()
  }
})

// Watch for route changes
watch(currentRoute, (newRoute) => {
  if (newRoute === 'admin') {
    fetchDashboardData()
  }
})
</script>

<template>
  <div class="neo-brutalist">
    <div class="p-0 row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 sidebar-container ps-0 overflow-hidden">
        <NeoDashboardSidebar :menuItems="menuItems" title="Admin" />
      </div>

      <!-- Main Content -->
      <div class="col-md-9 col-lg-10 p-4 main-content">
        <div v-if="currentRoute === 'admin'">
          <!-- Stats Grid -->
          <h1 class="mb-4 page-title">Activity</h1>
          <div class="stats-grid">
            <NeoCard v-for="stat in stats" :key="stat.id" class="stat-card dashboard-card">
              <div class="stat-card-content">
                <div class="stat-icon">
                  <NeoIcon :name="stat.icon" size="32" />
                </div>
                <div class="stat-info">
                  <h6 class="stat-label">{{ stat.label }}</h6>
                  <h1 class="stat-value">{{ stat.value }}</h1>
                </div>
              </div>
              <template #footer>
                <router-link :to="stat.route" class="text-decoration-none">
                  <NeoButton size="sm" variant="ghost" class="w-100">
                    View Details
                    <NeoIcon name="arrow-right" size="16" class="ms-2" />
                  </NeoButton>
                </router-link>
              </template>
            </NeoCard>
          </div>

          <!-- Recent Activity Section -->
          <div class="row mt-4 container">
            <div class="col-12">
              <NeoCard>
                <template #header>
                  <div class="d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Recent Activity</h5>
                    <NeoButton variant="ghost" size="sm" @click="router.push('/admin/reports')">
                      View All
                      <NeoIcon name="arrow-right" size="16" class="ms-2" />
                    </NeoButton>
                  </div>
                </template>
                <div class="list-group list-group-flush">
                  <a v-for="activity in recentActivity" :key="activity.id" href="#"
                    class="list-group-item list-group-item-action border-0">
                    <div class="d-flex w-100 justify-content-between align-items-center">
                      <div class="d-flex align-items-center">
                        <div class="activity-profile me-3">
                          <img v-if="activity.type === 'service_request'"
                            :src="getProfileImageUrl(activity.customer_profile_image)" alt="Customer"
                            class="rounded-circle" style="width: 40px; height: 40px; object-fit: cover;" />
                          <img v-else-if="activity.type === 'user_registration'"
                            :src="getProfileImageUrl(activity.user_profile_image)" alt="User" class="rounded-circle"
                            style="width: 40px; height: 40px; object-fit: cover;" />
                        </div>
                        <div>
                          <h6 class="mb-1 fw-bold">{{ activity.title }}</h6>
                          <p class="mb-0 text-muted">{{ activity.description }}</p>
                        </div>
                      </div>
                      <small class="text-muted">{{ activity.timeAgo }}</small>
                    </div>
                  </a>
                </div>
              </NeoCard>
            </div>
          </div>
        </div>

        <!-- Child routes content -->
        <router-view v-else></router-view>
      </div>
    </div>
  </div>
</template>

<style scoped>
.h-screen {
  height: 100vh;
}

.main-content {
  overflow-y: auto;
  height: calc(100vh - 74px);
}

.neo-brutalist {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
}

.sidebar-container {
  padding-left: 0;
  padding-right: 0;
  min-height: 100vh;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(300px, 1fr));
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: minmax(300px, 1fr);
  }
}

.stat-card {
  height: 100%;
  transition: all 0.3s ease;
  border: 3px solid var(--bs-primary);
  box-shadow: 4px 4px 0px 0px var(--bs-primary);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 6px 6px 0px 0px var(--bs-primary);
}

.stat-card-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
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

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.stat-trend {
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.trend-up {
  color: var(--bs-success);
}

.trend-down {
  color: var(--bs-danger);
}

.dashboard-card {
  border: 4px solid #ff7f50;
  box-shadow: 5px 5px 0px 0px #ff7f50;
}

.dashboard-card h1 {
  font-size: 3.5rem;
  line-height: 1;
  letter-spacing: -1px;
}

.neo-brutalist .list-group-item {
  transition: all 0.2s ease;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.neo-brutalist .list-group-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  transform: translateX(4px);
}

.activity-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background-color: rgba(var(--bs-primary-rgb), 0.1);
  color: var(--bs-primary);
  font-size: 1.25rem;
}

.neo-brutalist .fs-4 {
  letter-spacing: 1px;
}
</style>
