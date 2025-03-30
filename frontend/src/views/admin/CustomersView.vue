<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { NeoButton, NeoCard, NeoInput, NeoModal, NeoBadge, NeoAlert } from '@/components/ui'
import { professionalAPI } from '@/services/api' // Import API for profile image URL function
import { toastService } from '@/services/toastService'

const adminStore = useAdminStore()

// State for customers
const customers = ref([])

// Search term for filtering
const searchTerm = ref('')

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmAction = ref(() => { })
const confirmMessage = ref('')

// Selected customer for viewing details
const selectedCustomer = ref(null)
const showCustomerDetails = ref(false)

// Fetch customers on component mount
onMounted(async () => {
  try {
    const success = await adminStore.fetchUsers()
    if (!success) {
      throw new Error(adminStore.error || 'Failed to fetch users')
    }
    console.log(adminStore.users)
    customers.value = adminStore.users.filter(user => user.role_ids && user.role_ids.includes(3)) // Filter customers
  } catch (error) {
    console.error('Error fetching customers:', error)
    toastService.error(error.message || 'Failed to load customers.')
  }
})

// Helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}

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
      customer.id.toString().toLowerCase().includes(search) ||
      customer.phone_number?.toLowerCase().includes(search)
    )
  })
})

// View customer details
const viewCustomerDetails = async (customer) => {
  try {
    await adminStore.fetchUserById(customer.id)
    selectedCustomer.value = adminStore.currentUser
    showCustomerDetails.value = true
  } catch (error) {
    toastService.error(error.response?.data?.message || 'Failed to fetch customer details.')
  }
}

// Toggle customer account status
const toggleCustomerStatus = (customer) => {
  const newStatus = customer.blocked ? 'unblock' : 'block'
  confirmMessage.value = `Are you sure you want to ${newStatus} this customer?`
  confirmAction.value = async () => {
    try {
      const response = await adminStore.updateUserStatus(customer.id, { blocked: !customer.blocked })
      customers.value = adminStore.users.filter(user => user.role_ids.includes(3))
      toastService.success(response.message || `Customer has been ${newStatus}ed.`)
    } catch (error) {
      toastService.error(error.response?.data?.message || `Failed to ${newStatus} customer.`)
    }
  }
  showConfirmModal.value = true
}

// Handle confirmation
const executeConfirmAction = () => {
  confirmAction.value()
  showConfirmModal.value = false
}

// Helper function to get status badge class
const getStatusBadgeClass = (blocked) => {
  return blocked ? 'danger' : 'success'
}

// Helper function to get status text
const getStatusText = (blocked) => {
  return blocked ? 'Blocked' : 'Active'
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
    <h2 class="mb-4 page-title">Customers</h2>

    <!-- Search and Filter -->
    <div class="row mb-4">
      <div class="col-md-6">
        <NeoInput v-model="searchTerm" placeholder="Search by name, email, phone or ID" label="Search" />
      </div>
      <div class="col-md-6 d-flex align-items-end">
        <div class="ms-auto">
          <span class="me-3"> <strong>Total:</strong> {{ customers.length }} customers </span>
          <span>
            <strong>Active:</strong>
            {{customers.filter((c) => c.blocked === false).length}} customers
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
              <th>Profile</th>
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
              <td colspan="9" class="text-center py-3">No customers found matching your search.</td>
            </tr>

            <tr v-for="customer in filteredCustomers" :key="customer.id">
              <td>
                <img :src="getProfileImageUrl(customer.profile_image)" alt="Profile" class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;" />
              </td>
              <td>{{ customer.name }}</td>
              <td>{{ customer.email }}</td>
              <td>{{ customer.phone_number }}</td>
              <td>{{ customer.date_created }}</td>
              <td>{{ customer.total_requests || 0 }}</td>
              <td>
                <NeoBadge :variant="getStatusBadgeClass(customer.blocked)">
                  {{ getStatusText(customer.blocked) }}
                </NeoBadge>
              </td>
              <td>
                <NeoButton variant="info" size="sm" @click="viewCustomerDetails(customer)" class="me-2">
                  <i class="bi bi-eye"></i>
                </NeoButton>
                <NeoButton :variant="customer.blocked ? 'success' : 'danger'" size="sm"
                  @click="toggleCustomerStatus(customer)">
                  <i class="bi" :class="customer.blocked ? 'bi-unlock' : 'bi-lock'"></i>
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
        <div class="col-md-4 text-center mb-4">
          <img :src="getProfileImageUrl(selectedCustomer.profile_image)" alt="Profile"
            class="rounded-circle img-fluid mb-3 border border-dark border-3"
            style="width: 150px; height: 150px; object-fit: cover;" />
        </div>
        <div class="col-md-4">
          <h5>Personal Information</h5>
          <p><strong>Customer ID:</strong> {{ selectedCustomer.id }}</p>
          <p><strong>Email:</strong> {{ selectedCustomer.email }}</p>
          <p><strong>Phone:</strong> {{ selectedCustomer.phone_number }}</p>
          <p><strong>Joined:</strong> {{ selectedCustomer.date_created }}</p>
          <p>
            <strong>Status:</strong>
            <NeoBadge :variant="getStatusBadgeClass(selectedCustomer.blocked)" class="ms-2">
              {{ getStatusText(selectedCustomer.blocked) }}
            </NeoBadge>
          </p>
        </div>
        <div class="col-md-4">
          <h5>Address</h5>
          <p>{{ selectedCustomer.address }}</p>

          <h5 class="mt-4">Request Summary</h5>
          <p><strong>Total Requests:</strong> {{ selectedCustomer.total_requests || 0 }}</p>
          <p><strong>Active Requests:</strong> {{ selectedCustomer.active_requests || 0 }}</p>
          <p><strong>Last Service:</strong> {{ selectedCustomer.last_service }}</p>
        </div>

        <!-- Service History -->
        <div class="col-12 mt-4">
          <h5>Service Request History</h5>
          <div class="table-responsive">
            <table class="table table-hover table-sm">
              <thead>
                <tr>
                  <th>Service</th>
                  <th>Date</th>
                  <th>Status</th>
                  <th>Amount</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="request in selectedCustomer.serviceHistory" :key="request.id">
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
        <NeoButton :variant="selectedCustomer?.blocked ? 'success' : 'danger'"
          @click="toggleCustomerStatus(selectedCustomer)" class="ms-2">
          <i class="bi me-1" :class="selectedCustomer?.blocked ? 'bi-unlock' : 'bi-lock'"></i>
          {{ selectedCustomer?.blocked ? 'Unblock Account' : 'Block Account' }}
        </NeoButton>
      </template>
    </NeoModal>

    <!-- Confirmation Modal -->
    <NeoModal v-model="showConfirmModal" title="Confirm Action">
      <NeoAlert variant="warning" class="mb-3">
        {{ confirmMessage }}
      </NeoAlert>
      <template #footer>
        <NeoButton variant="secondary" @click="showConfirmModal = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="executeConfirmAction" class="ms-2">
          Confirm
        </NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped></style>
