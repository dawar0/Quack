<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  NeoButton,
  NeoCard,
  NeoInput,
  NeoSelect,
  NeoModal,
  NeoBadge,
  NeoAlert,
} from '@/components/ui'

const route = useRoute()

// Sample data for service requests
const serviceRequests = ref([
  {
    id: 1,
    service_id: 1,
    service_name: 'House Cleaning',
    professional_id: 1,
    professional_name: 'John Smith',
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
    service_id: 3,
    service_name: 'Electrical Work',
    professional_id: 4,
    professional_name: 'Sarah Lee',
    date_of_request: '2023-11-05',
    expected_date: '2023-11-08',
    date_of_completion: '2023-11-08',
    status: 'completed',
    remarks: 'Fixed wiring issues in kitchen and installed new light fixtures in living room.',
    price: 150,
    description: 'Need to fix some wiring issues in the kitchen and install new light fixtures.',
  },
  {
    id: 3,
    service_id: 2,
    service_name: 'Plumbing',
    professional_id: 3,
    professional_name: 'Robert Johnson',
    date_of_request: '2023-10-25',
    expected_date: '2023-10-28',
    date_of_completion: '2023-10-28',
    status: 'closed',
    remarks: 'Fixed leaking pipe under sink and installed new faucet in bathroom.',
    price: 120,
    description:
      'Leaking pipe under the sink needs fixing. Also need to install a new faucet in the bathroom.',
  },
  {
    id: 4,
    service_id: 4,
    service_name: 'Gardening',
    professional_id: null,
    professional_name: null,
    date_of_request: '2023-11-12',
    expected_date: '2023-11-18',
    date_of_completion: null,
    status: 'requested',
    remarks: '',
    price: 90,
    description:
      'Need full garden maintenance including mowing, trimming, and planting new seasonal flowers.',
  },
])

// Sample data for available services
const services = ref([
  { id: 1, name: 'House Cleaning', price: 75 },
  { id: 2, name: 'Plumbing', price: 120 },
  { id: 3, name: 'Electrical Work', price: 150 },
  { id: 4, name: 'Gardening', price: 90 },
  { id: 5, name: 'Painting', price: 200 },
  { id: 6, name: 'Carpet Cleaning', price: 85 },
])

// State for new request form
const showNewRequestForm = ref(false)
const newRequest = ref({
  service_id: '',
  expected_date: '',
  description: '',
})

// State for request details modal
const showRequestDetails = ref(false)
const selectedRequest = ref(null)

// Feedback modal state
const showFeedbackModal = ref(false)
const feedbackMessage = ref('')
const feedbackTitle = ref('')
const feedbackVariant = ref('info')

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmAction = ref(() => {})
const confirmMessage = ref('')

// Filter state
const statusFilter = ref('all')

// Status options for filter
const statusOptions = [
  { value: 'all', label: 'All Requests' },
  { value: 'requested', label: 'Requested' },
  { value: 'assigned', label: 'Assigned' },
  { value: 'completed', label: 'Completed' },
  { value: 'closed', label: 'Closed' },
]

// Filtered requests based on status
const filteredRequests = computed(() => {
  if (statusFilter.value === 'all') {
    return serviceRequests.value
  }
  return serviceRequests.value.filter((request) => request.status === statusFilter.value)
})

// Create a new service request
const createServiceRequest = () => {
  // Validate form
  if (
    !newRequest.value.service_id ||
    !newRequest.value.expected_date ||
    !newRequest.value.description
  ) {
    showFeedback('Error', 'Please fill in all required fields.', 'danger')
    return
  }

  // Get service details
  const service = services.value.find(
    (s) => s.id === Number.parseInt(newRequest.value.service_id, 10),
  )
  if (!service) {
    showFeedback('Error', 'Invalid service selected.', 'danger')
    return
  }

  // Create request
  const newId = Math.max(0, ...serviceRequests.value.map((r) => r.id)) + 1
  const newServiceRequest = {
    id: newId,
    service_id: Number.parseInt(newRequest.value.service_id, 10),
    service_name: service.name,
    professional_id: null,
    professional_name: null,
    date_of_request: new Date().toISOString().split('T')[0],
    expected_date: newRequest.value.expected_date,
    date_of_completion: null,
    status: 'requested',
    remarks: '',
    price: service.price,
    description: newRequest.value.description,
  }

  serviceRequests.value.push(newServiceRequest)

  // Reset form and close modal
  newRequest.value = {
    service_id: '',
    expected_date: '',
    description: '',
  }
  showNewRequestForm.value = false

  showFeedback('Success', 'Service request created successfully!', 'success')
}

// Helper function to show feedback modal
const showFeedback = (title, message, variant = 'info') => {
  feedbackTitle.value = title
  feedbackMessage.value = message
  feedbackVariant.value = variant
  showFeedbackModal.value = true
}

// View details of a request
const viewRequestDetails = (request) => {
  selectedRequest.value = request
  showRequestDetails.value = true
}

// Close a completed service
const closeServiceRequest = (requestId) => {
  const index = serviceRequests.value.findIndex((req) => req.id === requestId)
  if (index !== -1 && serviceRequests.value[index].status === 'completed') {
    serviceRequests.value[index] = {
      ...serviceRequests.value[index],
      status: 'closed',
    }
    showFeedback('Success', 'Service request marked as closed.', 'success')
    showRequestDetails.value = false
  }
}

// Cancel a service request
const cancelServiceRequest = (requestId) => {
  confirmMessage.value = 'Are you sure you want to cancel this service request?'
  confirmAction.value = () => {
    const index = serviceRequests.value.findIndex((req) => req.id === requestId)
    if (index !== -1 && ['requested', 'assigned'].includes(serviceRequests.value[index].status)) {
      serviceRequests.value.splice(index, 1)
      showFeedback('Success', 'Service request cancelled successfully.', 'success')
      showRequestDetails.value = false
    }
  }
  showConfirmModal.value = true
}

// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'requested':
      return 'info'
    case 'assigned':
      return 'primary'
    case 'completed':
      return 'success'
    case 'closed':
      return 'secondary'
    case 'cancelled':
      return 'danger'
    default:
      return 'secondary'
  }
}

// Function to set minimum date for expected date input
const minDate = () => {
  const today = new Date()
  return today.toISOString().split('T')[0]
}

// Handle confirmation
const executeConfirmAction = () => {
  confirmAction.value()
  showConfirmModal.value = false
}

// Check for query parameter on mount
onMounted(() => {
  if (route.query.openRequestModal === 'true') {
    showNewRequestForm.value = true
  }
})
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h1 class="page-title">My Service Requests</h1>
      <NeoButton @click="showNewRequestForm = true" variant="primary">
        <i class="bi bi-plus-circle me-2"></i> New Service Request
      </NeoButton>
    </div>

    <!-- Status Filters -->
    <div class="mb-4">
      <NeoSelect v-model="statusFilter" :options="statusOptions" label="Filter by Status" />
    </div>

    <!-- Requests List -->
    <div class="row g-4">
      <div v-for="request in filteredRequests" :key="request.id" class="col-md-6">
        <NeoCard>
          <template #title>
            {{ request.service_name }}
            <NeoBadge :variant="getStatusBadgeClass(request.status)" class="ms-2">
              {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
            </NeoBadge>
          </template>

          <template #subtitle>
            <div class="d-flex justify-content-between">
              <div>Request #{{ request.id }}</div>
              <div>${{ request.price }}</div>
            </div>
          </template>

          <p>{{ request.description }}</p>

          <div class="d-flex justify-content-between align-items-center mb-3">
            <div><strong>Requested:</strong> {{ request.date_of_request }}</div>
            <div><strong>Expected:</strong> {{ request.expected_date }}</div>
          </div>

          <div class="d-flex justify-content-between">
            <NeoButton @click="viewRequestDetails(request)" variant="info" size="sm">
              <i class="bi bi-eye me-1"></i> View Details
            </NeoButton>

            <NeoButton
              v-if="['requested', 'assigned'].includes(request.status)"
              @click="cancelServiceRequest(request.id)"
              variant="danger"
              size="sm"
            >
              <i class="bi bi-x-circle me-1"></i> Cancel Request
            </NeoButton>
          </div>
        </NeoCard>
      </div>

      <div v-if="filteredRequests.length === 0" class="col-12">
        <NeoAlert variant="info"> No service requests found with the selected filter. </NeoAlert>
      </div>
    </div>

    <!-- New Request Modal -->
    <NeoModal v-model="showNewRequestForm" title="New Service Request">
      <div class="mb-3">
        <NeoSelect
          v-model="newRequest.service_id"
          :options="services.map((s) => ({ value: s.id, label: `${s.name} ($${s.price})` }))"
          label="Select Service"
          required
        />
      </div>

      <div class="mb-3">
        <NeoInput
          v-model="newRequest.expected_date"
          type="date"
          label="Expected Date"
          :min="minDate()"
          required
        />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          id="description"
          v-model="newRequest.description"
          class="form-control"
          rows="3"
          placeholder="Describe what you need"
          required
        ></textarea>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showNewRequestForm = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="createServiceRequest" class="ms-2"
          >Submit Request</NeoButton
        >
      </template>
    </NeoModal>

    <!-- Request Details Modal -->
    <NeoModal
      v-model="showRequestDetails"
      :title="`Request #${selectedRequest?.id} Details`"
      size="lg"
    >
      <div v-if="selectedRequest" class="row">
        <div class="col-md-6">
          <h5>Service Information</h5>
          <p><strong>Service:</strong> {{ selectedRequest.service_name }}</p>
          <p><strong>Price:</strong> ${{ selectedRequest.price }}</p>
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
        </div>

        <div class="col-md-6">
          <h5>Request Details</h5>
          <p>{{ selectedRequest.description }}</p>

          <div v-if="selectedRequest.professional_name">
            <h5 class="mt-4">Assigned Professional</h5>
            <p><strong>Name:</strong> {{ selectedRequest.professional_name }}</p>
          </div>

          <div v-if="selectedRequest.status === 'completed' || selectedRequest.status === 'closed'">
            <h5 class="mt-4">Service Remarks</h5>
            <p>{{ selectedRequest.remarks }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showRequestDetails = false">Close</NeoButton>

        <NeoButton
          v-if="selectedRequest && selectedRequest.status === 'completed'"
          variant="success"
          @click="closeServiceRequest(selectedRequest.id)"
          class="ms-2"
        >
          Mark as Closed
        </NeoButton>

        <NeoButton
          v-if="selectedRequest && ['requested', 'assigned'].includes(selectedRequest.status)"
          variant="danger"
          @click="cancelServiceRequest(selectedRequest.id)"
          class="ms-2"
        >
          Cancel Request
        </NeoButton>
      </template>
    </NeoModal>

    <!-- Feedback Modal -->
    <NeoModal v-model="showFeedbackModal" :title="feedbackTitle">
      <NeoAlert :variant="feedbackVariant" class="mb-0">
        {{ feedbackMessage }}
      </NeoAlert>
      <template #footer>
        <NeoButton variant="secondary" @click="showFeedbackModal = false">Close</NeoButton>
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
