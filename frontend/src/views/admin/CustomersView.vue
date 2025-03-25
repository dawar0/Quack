<script setup>
import { ref, computed } from 'vue'
import { NeoButton, NeoCard, NeoInput, NeoModal, NeoBadge } from '@/components/ui'
import { toastService } from '@/services/toastService'

// Sample customers data
const customers = ref([
  {
    id: 'C1001',
    name: 'John Doe',
    email: 'john.doe@example.com',
    phone: '+91 9876543210',
    address: '123 Main Street, Mumbai, Maharashtra, 400001',
    date_joined: '2023-01-15',
    total_requests: 12,
    active_requests: 2,
    last_service: '2023-05-25',
    status: 'Active',
  },
  {
    id: 'C1002',
    name: 'Jane Brown',
    email: 'jane.brown@example.com',
    phone: '+91 9876543211',
    address: '456 Park Avenue, Delhi, Delhi, 110001',
    date_joined: '2023-02-20',
    total_requests: 9,
    active_requests: 1,
    last_service: '2023-05-24',
    status: 'Active',
  },
  {
    id: 'C1003',
    name: 'Robert Johnson',
    email: 'robert.johnson@example.com',
    phone: '+91 9876543212',
    address: '789 Circle Road, Bangalore, Karnataka, 560001',
    date_joined: '2023-03-05',
    total_requests: 7,
    active_requests: 1,
    last_service: '2023-05-24',
    status: 'Active',
  },
  {
    id: 'C1004',
    name: 'Maria Garcia',
    email: 'maria.garcia@example.com',
    phone: '+91 9876543213',
    address: '101 Ridge Lane, Chennai, Tamil Nadu, 600001',
    date_joined: '2023-03-15',
    total_requests: 6,
    active_requests: 1,
    last_service: '2023-05-23',
    status: 'Active',
  },
  {
    id: 'C1005',
    name: 'David Kim',
    email: 'david.kim@example.com',
    phone: '+91 9876543214',
    address: '202 Valley Road, Hyderabad, Telangana, 500001',
    date_joined: '2023-04-10',
    total_requests: 5,
    active_requests: 0,
    last_service: '2023-05-22',
    status: 'Inactive',
  },
])

// Search term for filtering
const searchTerm = ref('')

// Computed property for filtered customers
const filteredCustomers = computed(() => {
  if (!searchTerm.value) {
    return customers.value
  }

  const search = searchTerm.value.toLowerCase()
  return customers.value.filter((customer) => {
    return (
      customer.name.toLowerCase().includes(search) ||
      customer.email.toLowerCase().includes(search) ||
      customer.id.toLowerCase().includes(search) ||
      customer.phone.toLowerCase().includes(search)
    )
  })
})

// Selected customer for viewing details
const selectedCustomer = ref(null)
const showCustomerDetails = ref(false)

// View customer details
const viewCustomerDetails = (customer) => {
  selectedCustomer.value = { ...customer }

  // In a real app, we would fetch more details from the API
  // Mocking service history
  selectedCustomer.value.serviceHistory = [
    { id: 'SR1001', service: 'Plumbing', date: '2023-05-25', status: 'Completed', amount: '₹550' },
    { id: 'SR1002', service: 'Electrical', date: '2023-05-20', status: 'Assigned', amount: '₹650' },
    { id: 'SR1003', service: 'Cleaning', date: '2023-05-10', status: 'Completed', amount: '₹450' },
    { id: 'SR1004', service: 'Gardening', date: '2023-04-25', status: 'Cancelled', amount: '₹350' },
  ]

  showCustomerDetails.value = true
}

// Toggle customer account status
const toggleCustomerStatus = (customer) => {
  customer.status = customer.status === 'Active' ? 'Inactive' : 'Active'

  // In a real app, this would send a request to the API
  toastService.success(`Customer ${customer.name}'s status changed to ${customer.status}`)
}

// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  return status === 'Active' ? 'success' : 'secondary'
}

// Helper function to get request status badge class
const getRequestStatusBadgeClass = (status) => {
  const statusClasses = {
    Completed: 'success',
    Assigned: 'primary',
    Requested: 'warning',
    Cancelled: 'danger',
    Closed: 'secondary',
  }
  return statusClasses[status] || 'secondary'
}
</script>

<template>
  <div class="container-fluid py-4">
    <h2 class="mb-4">CUSTOMERS</h2>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-md-6">
        <NeoInput
          v-model="searchTerm"
          placeholder="Search by name, email, phone or ID"
          label="Search"
        />
      </div>
      <div class="col-md-6 d-flex align-items-end">
        <div class="ms-auto">
          <span class="me-3"> <strong>Total:</strong> {{ customers.length }} customers </span>
          <span>
            <strong>Active:</strong>
            {{ customers.filter((c) => c.status === 'Active').length }} customers
          </span>
        </div>
      </div>
    </div>

    <!-- Customers Table -->
    <NeoCard>
      <template #title>Customer Directory</template>

      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Joined</th>
              <th>Requests</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredCustomers.length === 0">
              <td colspan="8" class="text-center py-3">No customers found matching your search.</td>
            </tr>

            <tr v-for="customer in filteredCustomers" :key="customer.id">
              <td>{{ customer.id }}</td>
              <td>{{ customer.name }}</td>
              <td>{{ customer.email }}</td>
              <td>{{ customer.phone }}</td>
              <td>{{ customer.date_joined }}</td>
              <td>{{ customer.total_requests }}</td>
              <td>
                <NeoBadge :variant="getStatusBadgeClass(customer.status)">
                  {{ customer.status }}
                </NeoBadge>
              </td>
              <td>
                <NeoButton
                  variant="info"
                  size="sm"
                  @click="viewCustomerDetails(customer)"
                  class="me-2"
                >
                  <i class="bi bi-eye"></i>
                </NeoButton>
                <NeoButton
                  :variant="customer.status === 'Active' ? 'danger' : 'success'"
                  size="sm"
                  @click="toggleCustomerStatus(customer)"
                >
                  <i class="bi" :class="customer.status === 'Active' ? 'bi-lock' : 'bi-unlock'"></i>
                </NeoButton>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </NeoCard>

    <!-- Customer Details Modal -->
    <NeoModal v-model="showCustomerDetails" :title="selectedCustomer?.name" size="lg">
      <div v-if="selectedCustomer" class="row">
        <div class="col-md-6">
          <h5>Personal Information</h5>
          <p><strong>Customer ID:</strong> {{ selectedCustomer.id }}</p>
          <p><strong>Email:</strong> {{ selectedCustomer.email }}</p>
          <p><strong>Phone:</strong> {{ selectedCustomer.phone }}</p>
          <p><strong>Joined:</strong> {{ selectedCustomer.date_joined }}</p>
          <p>
            <strong>Status:</strong>
            <NeoBadge :variant="getStatusBadgeClass(selectedCustomer.status)" class="ms-2">
              {{ selectedCustomer.status }}
            </NeoBadge>
          </p>
        </div>
        <div class="col-md-6">
          <h5>Address</h5>
          <p>{{ selectedCustomer.address }}</p>

          <h5 class="mt-4">Request Summary</h5>
          <p><strong>Total Requests:</strong> {{ selectedCustomer.total_requests }}</p>
          <p><strong>Active Requests:</strong> {{ selectedCustomer.active_requests }}</p>
          <p><strong>Last Service:</strong> {{ selectedCustomer.last_service }}</p>
        </div>

        <!-- Service History -->
        <div class="col-12 mt-4">
          <h5>Service Request History</h5>
          <div class="table-responsive">
            <table class="table table-hover table-sm">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Service</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in selectedCustomer.serviceHistory" :key="request.id">
                  <td>{{ request.id }}</td>
                  <td>{{ request.service }}</td>
                  <td>{{ request.date }}</td>
                  <td>
                    <NeoBadge :variant="getRequestStatusBadgeClass(request.status)" size="sm">
                      {{ request.status }}
                    </NeoBadge>
                  </td>
                  <td>{{ request.amount }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showCustomerDetails = false">
          <i class="bi bi-x-lg me-1"></i> Close
        </NeoButton>
        <NeoButton
          :variant="selectedCustomer?.status === 'Active' ? 'danger' : 'success'"
          @click="toggleCustomerStatus(selectedCustomer)"
          class="ms-2"
        >
          <i
            class="bi me-1"
            :class="selectedCustomer?.status === 'Active' ? 'bi-lock' : 'bi-unlock'"
          ></i>
          {{ selectedCustomer?.status === 'Active' ? 'Deactivate Account' : 'Activate Account' }}
        </NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
h2 {
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  position: relative;
  display: inline-block;
  padding-bottom: 5px;
}

h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  height: 4px;
  width: 100%;
  background: #000;
}
</style>
