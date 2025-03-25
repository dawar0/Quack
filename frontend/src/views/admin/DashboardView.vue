<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import NeoDashboardSidebar from '@/components/dashboard/NeoDashboardSidebar.vue'

const router = useRouter()
const currentRoute = computed(() => router.currentRoute.value.name)

// Menu items for navigation
const menuItems = [
  {
    label: 'Overview',
    route: '/admin',
    routeName: 'admin',
    icon: 'fas fa-home',
  },
  {
    label: 'Services',
    route: '/admin/services',
    routeName: 'admin-services',
    icon: 'fas fa-tools',
  },
  {
    label: 'Professionals',
    route: '/admin/professionals',
    routeName: 'admin-professionals',
    icon: 'fas fa-user-tie',
  },
  {
    label: 'Customers',
    route: '/admin/customers',
    routeName: 'admin-customers',
    icon: 'fas fa-users',
  },
  {
    label: 'Reports',
    route: '/admin/reports',
    routeName: 'admin-reports',
    icon: 'fas fa-chart-bar',
  },
]

// Dashboard statistics (would come from an API in a real application)
const stats = [
  {
    id: 'customers',
    label: 'Total Customers',
    value: '1,234',
    variant: 'primary',
    route: '/admin/customers',
  },
  {
    id: 'professionals',
    label: 'Total Professionals',
    value: '567',
    variant: 'success',
    route: '/admin/professionals',
  },
  {
    id: 'activeServices',
    label: 'Active Services',
    value: '89',
    variant: 'info',
    route: '/admin/services',
  },
  {
    id: 'pendingRequests',
    label: 'Pending Requests',
    value: '45',
    variant: 'warning',
    route: '/admin/professionals',
  },
  {
    id: 'pendingApprovals',
    label: 'Pending Approvals',
    value: '23',
    variant: 'danger',
    route: '/admin/professionals',
  },
  {
    id: 'completedServices',
    label: 'Completed Services',
    value: '2,345',
    variant: 'secondary',
    route: '/admin/services',
  },
]
</script>

<template>
  <div class="neo-brutalist">
    <div class="p-0 row">
      <!-- Sidebar -->
      <div class="col-md-3 col-lg-2 sidebar-container ps-0 overflow-hidden">
        <NeoDashboardSidebar :menuItems="menuItems" title="Admin" />
      </div>

      <!-- Main Content -->
      <div class="col-md-9 col-lg-10 p-4">
        <!-- If we're on the main admin page, show dashboard overview -->
        <div v-if="currentRoute === 'admin'">
          <!-- Stats Grid -->
          <h1 class="py-4 container">Activity</h1>
          <div class="stats-grid">
            <NeoCard
              v-for="stat in stats"
              :key="stat.id"
              :variant="stat.variant"
              class="stat-card dashboard-card"
            >
              <div class="d-flex justify-content-between align-items-center">
                <div class="p-2">
                  <h6 class="fw-bold text-uppercase">{{ stat.label }}</h6>
                  <h1 class="mb-0 fw-black display-4">{{ stat.value }}</h1>
                </div>
              </div>
              <template #footer>
                <router-link :to="stat.route" class="text-decoration-none">
                  <NeoButton :variant="stat.variant" size="sm" outline>View Details</NeoButton>
                </router-link>
              </template>
            </NeoCard>
          </div>

          <!-- Recent Activity Section -->
          <div class="row mt-4 container">
            <div class="col-12">
              <NeoCard>
                <template #header>
                  <h5 class="mb-0 fw-bold text-uppercase">Recent Activity</h5>
                </template>
                <div class="list-group list-group-flush">
                  <a href="#" class="list-group-item list-group-item-action border-0">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1 fw-bold">New professional registration</h6>
                      <small class="text-muted">3 hours ago</small>
                    </div>
                    <p class="mb-1">John Doe registered as an Electrical service provider</p>
                  </a>
                  <a href="#" class="list-group-item list-group-item-action border-0">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1 fw-bold">Service request completed</h6>
                      <small class="text-muted">5 hours ago</small>
                    </div>
                    <p class="mb-1">Plumbing service request #1234 was completed</p>
                  </a>
                  <a href="#" class="list-group-item list-group-item-action border-0">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1 fw-bold">New customer registration</h6>
                      <small class="text-muted">1 day ago</small>
                    </div>
                    <p class="mb-1">Jane Smith registered as a new customer</p>
                  </a>
                  <a href="#" class="list-group-item list-group-item-action border-0">
                    <div class="d-flex w-100 justify-content-between">
                      <h6 class="mb-1 fw-bold">New service added</h6>
                      <small class="text-muted">1 day ago</small>
                    </div>
                    <p class="mb-1">Admin added 'Home Painting' as a new service</p>
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
.neo-brutalist {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
}

.sidebar-container {
  padding-left: 0;
  padding-right: 0;
  min-height: 100vh;
  border-right: 4px solid #ff7f50;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(250px, 300px));
  gap: 1.5rem;
  margin-bottom: 2rem;
  justify-content: center;
}

@media (max-width: 992px) {
  .stats-grid {
    grid-template-columns: repeat(2, minmax(250px, 300px));
  }
}

@media (max-width: 576px) {
  .stats-grid {
    grid-template-columns: minmax(250px, 300px);
  }
}

.stat-card {
  height: 100%;
  transition: transform 0.2s ease;
  width: 100%;
}

.stat-card:hover {
  transform: translateY(-4px);
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
}

.neo-brutalist .list-group-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  transform: translateX(4px);
}

.neo-brutalist .fs-4 {
  letter-spacing: 1px;
}
</style>
