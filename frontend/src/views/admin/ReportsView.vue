<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { NeoButton, NeoCard, NeoInput, NeoSelect, NeoBadge } from '@/components/ui'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { professionalAPI } from '@/services/api' // Import API for profile image URLs
import { toastService } from '@/services/toastService'

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const adminStore = useAdminStore()

// Report types
const reportTypes = [
  { id: 'service', name: 'Service Requests Report' },
  { id: 'professional', name: 'Service Professionals Report' },
  { id: 'customer', name: 'Customer Activity Report' },
]

// Selected report type
const selectedReportType = ref('service')

// Date range for reports
const startDate = ref('')
const endDate = ref('')

// Status of export
const exportStatus = ref('idle') // idle, loading, success, error

// Report data
const serviceRequestData = ref([])
const serviceTypeData = ref([])

// Recent service requests
const recentRequests = computed(() => {
  return adminStore.requests.slice(0, 5) // Show only the 5 most recent requests
})

// Fetch report data
const fetchReportData = async () => {
  try {
    exportStatus.value = 'loading'
    const success = await adminStore.fetchReports({
      type: selectedReportType.value,
      start_date: startDate.value,
      end_date: endDate.value
    })

    if (success) {
      // Update chart data based on report type
      switch (selectedReportType.value) {
        case 'service':
          serviceRequestData.value = adminStore.reports.service_requests
          serviceTypeData.value = adminStore.reports.service_types
          break
        case 'professional':
          // Handle professional report data
          break
        case 'customer':
          // Handle customer report data
          break
      }

      // Fetch recent requests
      await adminStore.fetchAdminRequests()

      exportStatus.value = 'success'
      toastService.success('Report data loaded successfully.')
    } else {
      throw new Error(adminStore.error || 'Failed to load report data')
    }
  } catch (error) {
    exportStatus.value = 'error'
    toastService.error(error.message || 'Failed to load report data.')
  }
}

// Service Request Chart Data
const serviceRequestChartData = computed(() => {
  return {
    labels: serviceRequestData.value.map((item) => item.month),
    datasets: [
      {
        label: 'Requested',
        backgroundColor: '#ff7f50',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.value.map((item) => item.requested),
      },
      {
        label: 'Completed',
        backgroundColor: '#00ff7f',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.value.map((item) => item.completed),
      },
      {
        label: 'Cancelled',
        backgroundColor: '#ff5555',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.value.map((item) => item.cancelled),
      },
    ],
  }
})

// Chart options with neobrutalist style
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
        borderColor: '#000',
        tickColor: '#000',
      },
      ticks: {
        color: '#000',
        font: {
          weight: 'bold',
        },
      },
    },
    y: {
      grid: {
        color: 'rgba(0, 0, 0, 0.1)',
        borderColor: '#000',
        tickColor: '#000',
      },
      ticks: {
        color: '#000',
        font: {
          weight: 'bold',
        },
      },
    },
  },
  plugins: {
    legend: {
      labels: {
        color: '#000',
        font: {
          weight: 'bold',
        },
      },
    },
  },
}

// Service Type Chart Data
const serviceTypeChartData = computed(() => {
  return {
    labels: serviceTypeData.value.map((item) => item.service),
    datasets: [
      {
        label: 'Service Count',
        backgroundColor: '#ffd700',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceTypeData.value.map((item) => item.count),
      },
    ],
  }
})

// Generate CSV export
const exportReport = async () => {
  if (!startDate.value || !endDate.value) {
    toastService.error('Please select both start and end dates.')
    return
  }

  try {
    exportStatus.value = 'loading'
    const success = await adminStore.exportReport({
      type: selectedReportType.value,
      start_date: startDate.value,
      end_date: endDate.value
    })

    if (success) {
      exportStatus.value = 'success'
      toastService.success('Report exported successfully!')
    } else {
      throw new Error(adminStore.error || 'Failed to export report')
    }
  } catch (error) {
    exportStatus.value = 'error'
    toastService.error(error.message || 'Failed to export report.')
  }
}

// Set default date range to last 30 days
const setDefaultDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)

  endDate.value = end.toISOString().split('T')[0]
  startDate.value = start.toISOString().split('T')[0]
}

// Initialize with default date range and fetch data
onMounted(() => {
  setDefaultDateRange()
  fetchReportData()
})

// Watch for report type changes
watch(selectedReportType, () => {
  fetchReportData()
})

// Watch for date range changes
watch([startDate, endDate], () => {
  if (startDate.value && endDate.value) {
    fetchReportData()
  }
})

// Add this helper function before the template
const getStatusVariant = (status) => {
  switch (status?.toLowerCase()) {
    case 'accepted':
      return 'success'
    case 'pending':
      return 'warning'
    case 'completed':
      return 'primary'
    case 'rejected':
      return 'danger'
    default:
      return 'secondary'
  }
}

// Helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}
</script>

<template>
  <div>
    <h1 class="mb-4 page-title">Reports</h1>

    <!-- Report Options -->
    <NeoCard class="mb-4">
      <template #title>Report Configuration</template>
      <div class="row g-3">
        <div class="col-md-4">
          <NeoSelect v-model="selectedReportType"
            :options="reportTypes.map((type) => ({ value: type.id, label: type.name }))" label="Report Type" />
        </div>
        <div class="col-md-4">
          <NeoInput type="date" v-model="startDate" label="Start Date" />
        </div>
        <div class="col-md-4">
          <NeoInput type="date" v-model="endDate" label="End Date" />
        </div>
      </div>

      <div class="mt-4">
        <NeoButton variant="primary" @click="exportReport" :disabled="exportStatus === 'loading'">
          <i class="bi bi-download me-2"></i>
          <span v-if="exportStatus !== 'loading'">Export as CSV</span>
          <span v-else>Processing...</span>
        </NeoButton>
      </div>
    </NeoCard>

    <!-- Service Request Report -->
    <div v-if="selectedReportType === 'service'" class="row g-4">
      <!-- Service Requests Chart -->
      <div class="col-lg-8">
        <NeoCard class="h-100">
          <template #title>Service Requests (Last 6 Months)</template>
          <div class="chart-container" style="height: 350px; position: relative">
            <Bar :data="serviceRequestChartData" :options="chartOptions" />
          </div>
        </NeoCard>
      </div>

      <!-- Service Type Distribution -->
      <div class="col-lg-4">
        <NeoCard class="h-100">
          <template #title>Service Type Distribution</template>
          <div class="chart-container" style="height: 350px; position: relative">
            <Bar :data="serviceTypeChartData" :options="chartOptions" />
          </div>
        </NeoCard>
      </div>

      <!-- Recent Service Requests -->
      <div class="col-12">
        <NeoCard>
          <template #title>Recent Service Requests</template>
          <template #subtitle>
            <div class="d-flex justify-content-end">
              <NeoButton variant="primary" size="sm">
                <i class="bi bi-eye me-1"></i> View All
              </NeoButton>
            </div>
          </template>

          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Service</th>
                  <th>Customer</th>
                  <th>Professional</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in recentRequests" :key="request.id">
                  <td>{{ request.service?.name || 'N/A' }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="getProfileImageUrl(request.customer?.profile_image)" alt="Customer"
                        class="rounded-circle me-2" style="width: 32px; height: 32px; object-fit: cover;" />
                      <span>{{ request.customer?.name || 'N/A' }}</span>
                    </div>
                  </td>
                  <td>{{ request.professional?.name || '--' }}</td>
                  <td>{{ new Date(request.date_of_request).toLocaleDateString() }}</td>
                  <td>
                    <NeoBadge :variant="getStatusVariant(request.service_status)">
                      {{ request.service_status }}
                    </NeoBadge>
                  </td>
                  <td>₹{{ request.service?.price || 0 }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </NeoCard>
      </div>
    </div>

    <!-- Professional Report -->
    <div v-if="selectedReportType === 'professional'" class="row g-4">
      <div class="col-lg-8">
        <NeoCard class="h-100">
          <template #title>Professional Statistics</template>
          <div class="d-flex flex-column">
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Total Professionals</span>
              <span class="fw-bold">47</span>
            </div>
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Pending Approvals</span>
              <span class="fw-bold">3</span>
            </div>
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Active Professionals</span>
              <span class="fw-bold">42</span>
            </div>
            <div class="d-flex justify-content-between py-2">
              <span>Blocked Professionals</span>
              <span class="fw-bold">2</span>
            </div>
          </div>
        </NeoCard>
      </div>

      <div class="col-lg-4">
        <NeoCard>
          <template #title>Professional Activity</template>
          <div class="d-flex flex-column">
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Total Services</span>
              <span class="fw-bold">156</span>
            </div>
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Completed Services</span>
              <span class="fw-bold">142</span>
            </div>
            <div class="d-flex justify-content-between py-2">
              <span>Active Services</span>
              <span class="fw-bold">14</span>
            </div>
          </div>
        </NeoCard>
      </div>
    </div>

    <!-- Customer Report -->
    <div v-if="selectedReportType === 'customer'" class="row g-4">
      <div class="col-12">
        <NeoCard>
          <template #title>Top Customers (by Service Requests)</template>
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Customer</th>
                  <th>Total Requests</th>
                  <th>Completed</th>
                  <th>Cancelled</th>
                  <th>Total Spent</th>
                  <th>Last Request</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="customer in customerActivity" :key="customer.customer">
                  <td>
                    <div class="d-flex align-items-center">
                      <img :src="getProfileImageUrl(customer.profile_image)" alt="Profile" class="rounded-circle me-2"
                        style="width: 40px; height: 40px; object-fit: cover;" />
                      <span>{{ customer.customer }}</span>
                    </div>
                  </td>
                  <td>{{ customer.total_requests }}</td>
                  <td>{{ customer.completed }}</td>
                  <td>{{ customer.cancelled }}</td>
                  <td>₹{{ customer.total_spent }}</td>
                  <td>{{ customer.last_request }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </NeoCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.list-group-item {
  border-width: 2px;
  margin-bottom: 0.5rem;
}

thead th {
  text-transform: uppercase;
  font-weight: 600;
}

.progress {
  height: 8px;
  border-radius: 0;
  border: 1px solid #000;
}

.progress-bar {
  border-radius: 0;
}

/* Chart container */
.chart-container {
  position: relative;
  margin: auto;
  padding: 10px;
}
</style>
