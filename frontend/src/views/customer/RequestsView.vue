<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useServiceRequestStore } from '@/stores/serviceRequest'
import { useServiceStore } from '@/stores/service'
import {
  NeoButton,
  NeoCard,
  NeoInput,
  NeoSelect,
  NeoModal,
  NeoBadge,
  NeoAlert,
  NeoIcon,
  NeoTextarea,
} from '@/components/ui'
import { toastService } from '@/services/toastService'
import { serviceRequestAPI } from '@/services/api'


const route = useRoute()
const serviceRequestStore = useServiceRequestStore()
const serviceStore = useServiceStore()

// State for service requests
const serviceRequests = ref([])
const services = ref([])

// State for new request form
const showNewRequestForm = ref(false)
const newRequest = ref({
  service_id: '',
  preferred_date: '',
  location_pin_code: '',
  remarks: '',
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
const confirmAction = ref(() => { })
const confirmMessage = ref('')

// Filter state
const statusFilter = ref('all')

// Status options for filter
const statusOptions = [
  { value: 'all', label: 'All Requests' },
  { value: 'pending', label: 'Pending' },
  { value: 'accepted', label: 'Accepted' },
  { value: 'completed', label: 'Completed' },
]

// Filtered requests based on status
const filteredRequests = computed(() => {
  if (statusFilter.value === 'all') {
    return serviceRequests.value
  }
  return serviceRequests.value.filter((request) => request.service_status &&
    request.service_status.toLowerCase() === statusFilter.value.toLowerCase())
})

// Helper function to format service request data
const formatServiceRequests = (requests) => {
  return requests.map(request => {
    // Format dates for display
    const formattedRequest = { ...request };

    // Format date of request
    if (formattedRequest.date_of_request) {
      formattedRequest.date_of_request = new Date(formattedRequest.date_of_request).toLocaleDateString();
    }

    // Format date of completion
    if (formattedRequest.date_of_completion) {
      formattedRequest.date_of_completion = new Date(formattedRequest.date_of_completion).toLocaleDateString();
    }

    // Format preferred date
    if (formattedRequest.preferred_date) {
      formattedRequest.expected_date = new Date(formattedRequest.preferred_date).toLocaleDateString();
    }

    // Extract service details
    if (formattedRequest.service) {
      formattedRequest.service_name = formattedRequest.service.name;
      formattedRequest.price = formattedRequest.service.price;
      formattedRequest.description = formattedRequest.service.description;
    }

    // Extract professional name if available
    if (formattedRequest.professional) {
      formattedRequest.professional_name = formattedRequest.professional.name;
    }

    return formattedRequest;
  });
};

// Fetch services and requests on component mount
onMounted(async () => {
  try {
    await Promise.all([
      serviceStore.fetchServices(),
      serviceRequestStore.fetchCustomerRequests()
    ])
    services.value = serviceStore.services

    // Process service requests data
    serviceRequests.value = formatServiceRequests(serviceRequestStore.customerRequests);
  } catch (error) {
    console.error('Error loading data:', error);
    showFeedback('Error', 'Failed to load services and requests.', 'danger')
    toastService.error('Failed to load services and requests.')
  }
})

// Create a new service request
const createServiceRequest = async () => {
  // Validate form
  if (!newRequest.value.service_id || !newRequest.value.preferred_date) {
    showFeedback('Error', 'Please fill in all required fields.', 'danger')
    toastService.error('Please fill in all required fields.')
    return
  }

  try {
    await serviceRequestStore.createServiceRequest({
      service_id: Number(newRequest.value.service_id),
      preferred_date: newRequest.value.preferred_date,
      location_pin_code: newRequest.value.location_pin_code,
      remarks: newRequest.value.remarks
    })

    // Get updated service requests from store
    await serviceRequestStore.fetchCustomerRequests()

    // Process service requests data
    serviceRequests.value = formatServiceRequests(serviceRequestStore.customerRequests);

    // Reset form and close modal
    newRequest.value = {
      service_id: '',
      preferred_date: '',
      location_pin_code: '',
      remarks: ''
    }
    showNewRequestForm.value = false

    toastService.success('Service request created successfully!')
  } catch (error) {
    console.error('Error creating request:', error);
    showFeedback('Error', error.response?.data?.message || 'Failed to create service request.', 'danger')
    toastService.error(error.response?.data?.message || 'Failed to create service request.')
  }
}

// Helper function to show feedback modal
const showFeedback = (title, message, variant = 'info') => {
  feedbackTitle.value = title
  feedbackMessage.value = message
  feedbackVariant.value = variant
  showFeedbackModal.value = true
}

// View details of a request
const viewRequestDetails = async (request) => {
  try {
    await serviceRequestStore.fetchCustomerRequestById(request.id)
    const currentRequest = serviceRequestStore.currentRequest;

    // Format the request details for display
    selectedRequest.value = {
      ...currentRequest,
      date_of_request: currentRequest.date_of_request ?
        new Date(currentRequest.date_of_request).toLocaleDateString() : '',
      date_of_completion: currentRequest.date_of_completion ?
        new Date(currentRequest.date_of_completion).toLocaleDateString() : '',
      expected_date: currentRequest.preferred_date ?
        new Date(currentRequest.preferred_date).toLocaleDateString() : '',
      service_name: currentRequest.service?.name || '',
      price: currentRequest.service?.price || 0,
      description: currentRequest.service?.description || '',
      professional_name: currentRequest.professional?.name || ''
    };

    showRequestDetails.value = true
  } catch (error) {
    console.error('Error fetching request details:', error);
    showFeedback('Error', error.response?.data?.message || 'Failed to fetch request details.', 'danger')
    toastService.error(error.response?.data?.message || 'Failed to fetch request details.')
  }
}

// Cancel a service request
const cancelServiceRequest = (requestId) => {
  confirmMessage.value = 'Are you sure you want to cancel this service request?'
  confirmAction.value = async () => {
    try {
      await serviceRequestAPI.cancelRequest({
        request_id: requestId,
        action: 'cancel'
      })

      // Refresh the service requests
      await serviceRequestStore.fetchCustomerRequests()

      // Process service requests data
      serviceRequests.value = formatServiceRequests(serviceRequestStore.customerRequests);

      showFeedback('Success', 'Service request cancelled successfully.', 'success')
      toastService.success('Service request cancelled successfully.')
      showRequestDetails.value = false
    } catch (error) {
      console.error('Error cancelling request:', error);
      showFeedback('Error', error.response?.data?.message || 'Failed to cancel service request.', 'danger')
      toastService.error(error.response?.data?.message || 'Failed to cancel service request.')
    }
  }
  showConfirmModal.value = true
}

// Helper function to get status badge class
const getStatusBadgeClass = (status) => {
  const normalizedStatus = status ? status.toLowerCase() : '';
  switch (normalizedStatus) {
    case 'accepted':
      return 'info'
    case 'pending':
      return 'primary'
    case 'completed':
      return 'success'
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
  try {
    if (typeof confirmAction.value === 'function') {
      confirmAction.value()
    } else {
      console.error('confirmAction is not a function', confirmAction.value)
      showFeedback('Error', 'An error occurred processing your request', 'danger')
    }
  } catch (error) {
    console.error('Error in executeConfirmAction:', error)
    showFeedback('Error', 'An error occurred processing your request', 'danger')
  } finally {
    showConfirmModal.value = false
  }
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
        <NeoIcon name="plus-circle" size="20" class="me-2" />
        New Service Request
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
            <NeoBadge :variant="getStatusBadgeClass(request.service_status)" class="ms-2">
              {{ request.service_status ? request.service_status.charAt(0).toUpperCase() +
                request.service_status.slice(1) : 'Unknown' }}
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
            <NeoButton variant="primary" size="sm" @click="viewRequestDetails(request)">
              <NeoIcon name="eye" size="16" class="me-1" />
              View Details
            </NeoButton>

            <NeoButton v-if="request.service_status &&
              ['pending'].includes(request.service_status.toLowerCase())" @click="cancelServiceRequest(request.id)"
              variant="danger" size="sm">
              <NeoIcon name="x-circle" size="16" class="me-1" />
              Cancel Request
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
        <NeoSelect v-model="newRequest.service_id"
          :options="services.map((s) => ({ value: s.id, label: `${s.name} ($${s.price})` }))" label="Select Service"
          required />
      </div>

      <div class="mb-3">
        <NeoInput v-model="newRequest.preferred_date" type="date" label="Preferred Date" :min="minDate()" required />
      </div>

      <div class="mb-3">
        <label for="location_pin_code" class="form-label">Location Pin Code</label>
        <NeoInput id="location_pin_code" v-model="newRequest.location_pin_code" placeholder="Enter location pin code"
          required />
      </div>

      <div class="mb-3">
        <label for="remarks" class="form-label">Remarks</label>
        <NeoTextarea id="remarks" v-model="newRequest.remarks" rows="3" placeholder="Enter remarks" required />
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showNewRequestForm = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="createServiceRequest" class="ms-2">Submit Request</NeoButton>
      </template>
    </NeoModal>

    <!-- Request Details Modal -->
    <NeoModal v-model="showRequestDetails" :title="`Request #${selectedRequest?.id} Details`" size="lg">
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
            <NeoBadge :variant="getStatusBadgeClass(selectedRequest.service_status)" class="ms-2">
              {{ selectedRequest.service_status ? selectedRequest.service_status.charAt(0).toUpperCase() +
                selectedRequest.service_status.slice(1) :
                'Unknown' }}
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

          <div v-if="selectedRequest.service_status === 'completed'">
            <h5 class="mt-4">Service Remarks</h5>
            <p>{{ selectedRequest.remarks }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showRequestDetails = false">Close</NeoButton>

        <NeoButton v-if="selectedRequest && selectedRequest.service_status &&
          ['requested', 'assigned'].includes(selectedRequest.service_status.toLowerCase())" variant="danger"
          @click="cancelServiceRequest(selectedRequest.id)" class="ms-2">
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
