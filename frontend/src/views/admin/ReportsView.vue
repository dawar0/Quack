<script setup>
import { ref, computed } from 'vue'
import { NeoButton, NeoCard, NeoInput, NeoSelect, NeoBadge } from '@/components/ui'
import { toastService } from '@/services/toastService'
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

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

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

// Sample service request data for demonstration
const serviceRequestData = [
  { month: 'Jan', requested: 24, completed: 20, cancelled: 4 },
  { month: 'Feb', requested: 32, completed: 28, cancelled: 4 },
  { month: 'Mar', requested: 38, completed: 34, cancelled: 4 },
  { month: 'Apr', requested: 43, completed: 38, cancelled: 5 },
  { month: 'May', requested: 50, completed: 45, cancelled: 5 },
  { month: 'Jun', requested: 65, completed: 60, cancelled: 5 },
]

// Service Request Chart Data
const serviceRequestChartData = computed(() => {
  return {
    labels: serviceRequestData.map((item) => item.month),
    datasets: [
      {
        label: 'Requested',
        backgroundColor: '#ff7f50',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.map((item) => item.requested),
      },
      {
        label: 'Completed',
        backgroundColor: '#00ff7f',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.map((item) => item.completed),
      },
      {
        label: 'Cancelled',
        backgroundColor: '#ff5555',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceRequestData.map((item) => item.cancelled),
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

// Sample service type distribution data
const serviceTypeData = [
  { service: 'Plumbing', count: 75 },
  { service: 'Electrical', count: 90 },
  { service: 'Cleaning', count: 60 },
  { service: 'Gardening', count: 45 },
  { service: 'Carpentry', count: 30 },
  { service: 'Painting', count: 50 },
]

// Service Type Chart Data
const serviceTypeChartData = computed(() => {
  return {
    labels: serviceTypeData.map((item) => item.service),
    datasets: [
      {
        label: 'Service Count',
        backgroundColor: '#ffd700',
        borderColor: '#000',
        borderWidth: 2,
        data: serviceTypeData.map((item) => item.count),
      },
    ],
  }
})

// Professional Rating Chart Data
const professionalRatingData = [
  { rating: '5 stars', count: 15 },
  { rating: '4 stars', count: 25 },
  { rating: '3 stars', count: 5 },
  { rating: '2 stars', count: 2 },
  { rating: '1 star', count: 0 },
]

const professionalRatingChartData = computed(() => {
  return {
    labels: professionalRatingData.map((item) => item.rating),
    datasets: [
      {
        label: 'Professionals',
        backgroundColor: '#ffd700',
        borderColor: '#000',
        borderWidth: 2,
        data: professionalRatingData.map((item) => item.count),
      },
    ],
  }
})

// Generate CSV export
const exportReport = () => {
  if (!startDate.value || !endDate.value) {
    toastService.error('Please select both start and end dates')
    return
  }

  exportStatus.value = 'loading'

  // Simulate API call to generate report
  setTimeout(() => {
    exportStatus.value = 'success'
    toastService.success('Report generated successfully!')

    // In a real application, this would trigger a backend job through API
    // and then notify when the report is ready
  }, 2000)
}

// Set default date range to last 30 days
const setDefaultDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 30)

  endDate.value = end.toISOString().split('T')[0]
  startDate.value = start.toISOString().split('T')[0]
}

// Initialize with default date range
setDefaultDateRange()
</script>

<template>
  <div>
    <h1 class="mb-4 page-title">Reports</h1>

    <!-- Report Options -->
    <NeoCard class="mb-4">
      <template #title>Report Configuration</template>
      <div class="row g-3">
        <div class="col-md-4">
          <NeoSelect
            v-model="selectedReportType"
            :options="reportTypes.map((type) => ({ value: type.id, label: type.name }))"
            label="Report Type"
          />
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
                  <th>ID</th>
                  <th>Service</th>
                  <th>Customer</th>
                  <th>Professional</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>#1001</td>
                  <td>Plumbing</td>
                  <td>John Doe</td>
                  <td>Mike Smith</td>
                  <td>2023-05-25</td>
                  <td><NeoBadge variant="success">Completed</NeoBadge></td>
                  <td>₹550</td>
                </tr>
                <tr>
                  <td>#1002</td>
                  <td>Electrical</td>
                  <td>Jane Brown</td>
                  <td>Sarah Wilson</td>
                  <td>2023-05-24</td>
                  <td><NeoBadge variant="success">Completed</NeoBadge></td>
                  <td>₹650</td>
                </tr>
                <tr>
                  <td>#1003</td>
                  <td>Cleaning</td>
                  <td>Robert Johnson</td>
                  <td>Emily Davis</td>
                  <td>2023-05-24</td>
                  <td><NeoBadge variant="warning">Pending</NeoBadge></td>
                  <td>₹450</td>
                </tr>
                <tr>
                  <td>#1004</td>
                  <td>Gardening</td>
                  <td>Maria Garcia</td>
                  <td>--</td>
                  <td>2023-05-23</td>
                  <td><NeoBadge variant="primary">Assigned</NeoBadge></td>
                  <td>₹350</td>
                </tr>
                <tr>
                  <td>#1005</td>
                  <td>Carpentry</td>
                  <td>David Kim</td>
                  <td>Alex Thompson</td>
                  <td>2023-05-22</td>
                  <td><NeoBadge variant="danger">Cancelled</NeoBadge></td>
                  <td>₹700</td>
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
          <template #title>Professional Ratings Distribution</template>
          <div class="chart-container" style="height: 350px; position: relative">
            <Bar :data="professionalRatingChartData" :options="chartOptions" />
          </div>
        </NeoCard>
      </div>

      <div class="col-lg-4">
        <NeoCard>
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
            <div class="d-flex justify-content-between border-bottom border-dark py-2">
              <span>Blocked Professionals</span>
              <span class="fw-bold">2</span>
            </div>
            <div class="d-flex justify-content-between py-2">
              <span>Average Rating</span>
              <span class="fw-bold">4.3</span>
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
                <tr>
                  <td>John Doe</td>
                  <td>12</td>
                  <td>10</td>
                  <td>2</td>
                  <td>₹7,500</td>
                  <td>2023-05-25</td>
                </tr>
                <tr>
                  <td>Jane Brown</td>
                  <td>9</td>
                  <td>9</td>
                  <td>0</td>
                  <td>₹6,200</td>
                  <td>2023-05-24</td>
                </tr>
                <tr>
                  <td>Robert Johnson</td>
                  <td>7</td>
                  <td>5</td>
                  <td>2</td>
                  <td>₹4,500</td>
                  <td>2023-05-24</td>
                </tr>
                <tr>
                  <td>Maria Garcia</td>
                  <td>6</td>
                  <td>4</td>
                  <td>2</td>
                  <td>₹3,200</td>
                  <td>2023-05-23</td>
                </tr>
                <tr>
                  <td>David Kim</td>
                  <td>5</td>
                  <td>4</td>
                  <td>1</td>
                  <td>₹2,800</td>
                  <td>2023-05-22</td>
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
