<script setup>
import { ref, computed } from 'vue'
import { NeoButton, NeoCard, NeoSelect, NeoModal, NeoBadge } from '@/components/ui'

// Sample data for service requests
const serviceRequests = ref([
  {
    id: 1,
    customer_id: 1,
    customer_name: 'Alice Johnson',
    customer_phone: '555-123-4567',
    customer_address: '123 Main St, Apt 4B, New York, NY 10001',
    service_id: 1,
    service_name: 'House Cleaning',
    date_of_request: '2023-11-10',
    expected_date: '2023-11-15',
    date_of_completion: null,
    status: 'assigned',
    remarks: '',
    price: 75,
    description: 'Complete cleaning of 2BHK apartment including kitchen and bathrooms.',
  },
  {
    id: 2,
    customer_id: 2,
    customer_name: 'Bob Smith',
    customer_phone: '555-987-6543',
    customer_address: '456 Park Ave, Suite 201, New York, NY 10022',
    service_id: 1,
    service_name: 'House Cleaning',
    date_of_request: '2023-11-12',
    expected_date: '2023-11-16',
    date_of_completion: null,
    status: 'pending',
    remarks: '',
    price: 85,
    description: 'Deep cleaning of a studio apartment, including windows and balcony.',
  },
  {
    id: 3,
    customer_id: 3,
    customer_name: 'Charlie Davis',
    customer_phone: '555-456-7890',
    customer_address: '789 Broadway, New York, NY 10003',
    service_id: 1,
    service_name: 'House Cleaning',
    date_of_request: '2023-11-05',
    expected_date: '2023-11-08',
    date_of_completion: '2023-11-08',
    status: 'completed',
    remarks: 'Cleaned the entire apartment, including kitchen appliances and bathroom fixtures.',
    price: 70,
    description: 'Regular cleaning of 1BHK apartment. Please focus on kitchen and bathroom.',
  },
  {
    id: 4,
    customer_id: 4,
    customer_name: 'Diana Wilson',
    customer_phone: '555-789-0123',
    customer_address: '321 5th Ave, New York, NY 10016',
    service_id: 1,
    service_name: 'House Cleaning',
    date_of_request: '2023-10-28',
    expected_date: '2023-10-30',
    date_of_completion: null,
    status: 'rejected',
    remarks: 'Schedule conflict, unable to accommodate the requested date.',
    price: 95,
    description:
      'Move-out cleaning for a 3BHK apartment. Need to clean carpets and windows as well.',
  },
])

// State for selected request and completion form
const selectedRequest = ref(null)
const showRequestDetails = ref(false)
const completionRemarks = ref('')

// Filter state
const statusFilter = ref('all')

// Status options for filter
const statusOptions = [
  { value: 'all', label: 'All Requests' },
  { value: 'pending', label: 'Pending' },
  { value: 'assigned', label: 'Accepted' },
  { value: 'completed', label: 'Completed' },
  { value: 'rejected', label: 'Rejected' },
]

// Filtered requests based on status
const filteredRequests = computed(() => {
  if (statusFilter.value === 'all') {
    return serviceRequests.value
  }
  return serviceRequests.value.filter((request) => request.status === statusFilter.value)
})

// View details of a request
const viewRequestDetails = (request) => {
  selectedRequest.value = request
  completionRemarks.value = request.remarks || ''
  showRequestDetails.value = true
}

// Accept a service request
const acceptRequest = (requestId) => {
  const index = serviceRequests.value.findIndex((req) => req.id === requestId)
  if (index !== -1 && serviceRequests.value[index].status === 'pending') {
    serviceRequests.value[index] = {
      ...serviceRequests.value[index],
      status: 'assigned',
    }
    alert('Service request accepted successfully!')
    showRequestDetails.value = false
  }
}

// Reject a service request
const rejectRequest = (requestId) => {
  if (confirm('Are you sure you want to reject this service request?')) {
    const index = serviceRequests.value.findIndex((req) => req.id === requestId)
    if (index !== -1 && serviceRequests.value[index].status === 'pending') {
      serviceRequests.value[index] = {
        ...serviceRequests.value[index],
        status: 'rejected',
        remarks: 'Request rejected by professional',
      }
      alert('Service request rejected.')
      showRequestDetails.value = false
    }
  }
}

// Mark a service request as completed
const completeRequest = (requestId) => {
  if (!completionRemarks.value.trim()) {
    alert('Please provide completion remarks.')
    return
  }

  const index = serviceRequests.value.findIndex((req) => req.id === requestId)
  if (index !== -1 && serviceRequests.value[index].status === 'assigned') {
    serviceRequests.value[index] = {
      ...serviceRequests.value[index],
      status: 'completed',
      date_of_completion: new Date().toISOString().split('T')[0],
      remarks: completionRemarks.value.trim(),
    }
    alert('Service request marked as completed!')
    showRequestDetails.value = false
  }
}

// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'assigned':
      return 'primary'
    case 'completed':
      return 'success'
    case 'rejected':
      return 'danger'
    default:
      return 'secondary'
  }
}
</script>

<template>
  <div class="container py-4">
    <h1 class="page-title mb-4">Service Requests</h1>

    <!-- Status Filters -->
    <div class="mb-4">
      <NeoSelect v-model="statusFilter" :options="statusOptions" label="Filter by Status" />
    </div>

    <!-- Requests Table -->
    <NeoCard>
      <template #title>Service Requests</template>

      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Service</th>
              <th>Expected Date</th>
              <th>Status</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in filteredRequests" :key="request.id">
              <td># {{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.service_name }}</td>
              <td>{{ request.expected_date }}</td>
              <td>
                <NeoBadge :variant="getStatusBadgeClass(request.status)">
                  {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
                </NeoBadge>
              </td>
              <td>${{ request.price }}</td>
              <td>
                <NeoButton
                  variant="info"
                  size="sm"
                  @click="viewRequestDetails(request)"
                  class="me-1"
                >
                  <i class="bi bi-eye"></i>
                </NeoButton>

                <NeoButton
                  v-if="request.status === 'pending'"
                  variant="success"
                  size="sm"
                  @click="acceptRequest(request.id)"
                  class="me-1"
                >
                  <i class="bi bi-check-lg"></i>
                </NeoButton>

                <NeoButton
                  v-if="request.status === 'pending'"
                  variant="danger"
                  size="sm"
                  @click="rejectRequest(request.id)"
                >
                  <i class="bi bi-x-lg"></i>
                </NeoButton>
              </td>
            </tr>
            <tr v-if="filteredRequests.length === 0">
              <td colspan="7" class="text-center">No service requests found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </NeoCard>

    <!-- Request Details Modal -->
    <NeoModal
      v-model="showRequestDetails"
      :title="`Request #${selectedRequest?.id} Details`"
      size="lg"
    >
      <div v-if="selectedRequest" class="row">
        <div class="col-md-6">
          <h5>Customer Information</h5>
          <p><strong>Name:</strong> {{ selectedRequest.customer_name }}</p>
          <p><strong>Phone:</strong> {{ selectedRequest.customer_phone }}</p>
          <p><strong>Address:</strong> {{ selectedRequest.customer_address }}</p>

          <h5 class="mt-4">Service Details</h5>
          <p><strong>Service:</strong> {{ selectedRequest.service_name }}</p>
          <p><strong>Price:</strong> ${{ selectedRequest.price }}</p>
          <p><strong>Description:</strong> {{ selectedRequest.description }}</p>
        </div>

        <div class="col-md-6">
          <h5>Schedule</h5>
          <p><strong>Date Requested:</strong> {{ selectedRequest.date_of_request }}</p>
          <p><strong>Expected Date:</strong> {{ selectedRequest.expected_date }}</p>

          <div v-if="selectedRequest.date_of_completion">
            <p><strong>Date Completed:</strong> {{ selectedRequest.date_of_completion }}</p>
          </div>

          <p>
            <strong>Status:</strong>
            <NeoBadge :variant="getStatusBadgeClass(selectedRequest.status)" class="ms-2">
              {{ selectedRequest.status.charAt(0).toUpperCase() + selectedRequest.status.slice(1) }}
            </NeoBadge>
          </p>

          <div
            v-if="selectedRequest.status === 'completed' || selectedRequest.status === 'rejected'"
          >
            <h5 class="mt-4">Remarks</h5>
            <p>{{ selectedRequest.remarks }}</p>
          </div>

          <div v-if="selectedRequest.status === 'assigned'" class="mt-4">
            <h5>Complete Service</h5>
            <div class="mb-3">
              <label for="completion-remarks" class="form-label">Completion Remarks</label>
              <textarea
                id="completion-remarks"
                v-model="completionRemarks"
                class="form-control"
                rows="3"
                placeholder="Describe what was done"
              ></textarea>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showRequestDetails = false">Close</NeoButton>

        <template v-if="selectedRequest && selectedRequest.status === 'pending'">
          <NeoButton variant="success" @click="acceptRequest(selectedRequest.id)" class="ms-2">
            Accept Request
          </NeoButton>
          <NeoButton variant="danger" @click="rejectRequest(selectedRequest.id)" class="ms-2">
            Reject Request
          </NeoButton>
        </template>

        <NeoButton
          v-if="selectedRequest && selectedRequest.status === 'assigned'"
          variant="success"
          @click="completeRequest(selectedRequest.id)"
          class="ms-2"
        >
          Mark as Completed
        </NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
.modal.show {
  display: block;
}
</style>
