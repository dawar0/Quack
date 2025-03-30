<script setup>
import { ref, computed, onMounted } from 'vue'
import { useServiceRequestStore } from '@/stores/serviceRequest'
import { NeoButton, NeoCard, NeoSelect, NeoModal, NeoBadge, NeoAlert, NeoTabs } from '@/components/ui'
import { toastService } from '@/services/toastService'
import { professionalAPI } from '@/services/api'

const serviceRequestStore = useServiceRequestStore()

// State for service requests
const serviceRequests = ref([])
const assignedRequests = ref([])

// State for selected request and completion form
const selectedRequest = ref(null)
const showRequestDetails = ref(false)
const completionRemarks = ref('')

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmAction = ref(() => { })
const confirmMessage = ref('')

// Filter state
const statusFilter = ref('All')

// Tab state
const activeTab = ref('available')

// Define tabs for NeoTabs component
const tabs = [
  { value: 'available', label: 'Available Service Requests' },
  { value: 'myRequests', label: 'My Requests' }
]

// Status options for filter
const statusOptions = [
  { value: 'All', label: 'All Requests' },
  { value: 'Pending', label: 'Pending' },
  { value: 'Accepted', label: 'Accepted' },
  { value: 'Completed', label: 'Completed' },
  { value: 'Cancelled', label: 'Cancelled' },
]

// Filtered requests based on status
const filteredRequests = computed(() => {
  if (statusFilter.value.toLowerCase() === 'all') {
    return serviceRequests.value
  }
  return serviceRequests.value.filter((request) =>
    request.service_status.toLowerCase() === statusFilter.value.toLowerCase()
  )
})

// Filtered assigned requests based on status
const filteredAssignedRequests = computed(() => {
  if (statusFilter.value.toLowerCase() === 'all') {
    return assignedRequests.value
  }
  return assignedRequests.value.filter((request) =>
    request.service_status.toLowerCase() === statusFilter.value.toLowerCase()
  )
})

// Fetch requests on component mount
onMounted(async () => {
  try {
    await Promise.all([
      serviceRequestStore.fetchProfessionalRequests(),
      serviceRequestStore.fetchAssignedRequests()
    ])
    serviceRequests.value = serviceRequestStore.professionalRequests
    assignedRequests.value = serviceRequestStore.assignedRequests
  } catch (error) {
    console.error('Failed to fetch requests:', error)
    toastService.error('Failed to load service requests.')
  }
})

// View details of a request
const viewRequestDetails = async (request) => {
  try {
    await serviceRequestStore.fetchRequestById(request.id, 'professional')
    selectedRequest.value = serviceRequestStore.selectedRequest
    showRequestDetails.value = true
  } catch (error) {
    toastService.error(error.response?.data?.message || 'Failed to fetch request details.')
  }
}

// Accept a service request
const acceptRequest = (requestId) => {
  confirmMessage.value = 'Are you sure you want to accept this service request?'
  confirmAction.value = async () => {
    try {
      await serviceRequestStore.takeActionOnRequest({
        request_id: requestId,
        action: 'accept'
      })

      // Refresh both lists
      await Promise.all([
        serviceRequestStore.fetchProfessionalRequests(),
        serviceRequestStore.fetchAssignedRequests()
      ])

      serviceRequests.value = serviceRequestStore.professionalRequests
      assignedRequests.value = serviceRequestStore.assignedRequests

      toastService.success('Service request accepted successfully!')
      showRequestDetails.value = false
    } catch (error) {
      toastService.error(error.response?.data?.message || 'Failed to accept service request.')
    }
  }
  showConfirmModal.value = true
}

// Mark a service request as completed
const completeRequest = (requestId) => {

  confirmMessage.value = 'Are you sure you want to mark this service as completed?'
  confirmAction.value = async () => {
    try {
      await serviceRequestStore.takeActionOnRequest({
        request_id: requestId,
        action: 'complete',
        remarks: completionRemarks.value.trim()
      })

      // Refresh both lists
      await Promise.all([
        serviceRequestStore.fetchProfessionalRequests(),
        serviceRequestStore.fetchAssignedRequests()
      ])

      serviceRequests.value = serviceRequestStore.professionalRequests
      assignedRequests.value = serviceRequestStore.assignedRequests

      toastService.success('Service request marked as completed!')
      showRequestDetails.value = false
    } catch (error) {
      toastService.error(error.response?.data?.message || 'Failed to complete service request.')
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
const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'Pending':
      return 'info'
    case 'Accepted':
      return 'primary'
    case 'Completed':
      return 'success'
    case 'Cancelled':
      return 'danger'
    default:
      return 'secondary'
  }
}

const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}
</script>

<template>
  <div class="container py-4">
    <h1 class="page-title mb-4">Service Requests</h1>

    <!-- Neo Brutalist Tabs -->
    <NeoTabs v-model="activeTab" :tabs="tabs" />

    <!-- Status Filters -->
    <div class="mb-4">
      <NeoSelect v-model="statusFilter" :options="statusOptions" label="Filter by Status" :model-value="statusFilter" />
    </div>

    <!-- Available Service Requests Tab -->
    <div v-if="activeTab === 'available'">
      <NeoCard>
        <template #title>Available Service Requests</template>

        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Customer</th>
                <th>Service</th>
                <th>Date</th>
                <th>Status</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in filteredRequests" :key="request.id">
                <td>
                  <div class="d-flex align-items-center">
                    <img :src="getProfileImageUrl(request.customer.profile_image)" alt="Customer"
                      class="rounded-circle me-2" style="width: 32px; height: 32px; object-fit: cover;" />
                    <span>{{ request.customer.name }}</span>
                  </div>
                </td>
                <td>{{ request.service.name }}</td>
                <td>{{ new Date(request.date_of_request).toLocaleDateString() }}</td>
                <td>
                  <NeoBadge :variant="getStatusBadgeClass(request.service_status)">
                    {{ request.service_status }}
                  </NeoBadge>
                </td>
                <td>${{ request.service.price }}</td>
                <td>
                  <NeoButton variant="info" size="sm" @click="viewRequestDetails(request)" class="me-1">
                    <i class="bi bi-eye"></i>
                  </NeoButton>

                  <NeoButton v-if="request.service_status === 'Pending'" variant="success" size="sm"
                    @click="acceptRequest(request.id)" class="me-1">
                    <i class="bi bi-check-lg"></i>
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
    </div>

    <!-- My Requests Tab -->
    <div v-if="activeTab === 'myRequests'">
      <NeoCard>
        <template #title>My Requests</template>

        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Customer</th>
                <th>Service</th>
                <th>Date</th>
                <th>Status</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="request in filteredAssignedRequests" :key="request.id">
                <td>
                  <div class="d-flex align-items-center">
                    <img :src="getProfileImageUrl(request.customer.profile_image)" alt="Customer"
                      class="rounded-circle me-2" style="width: 32px; height: 32px; object-fit: cover;" />
                    <span>{{ request.customer.name }}</span>
                  </div>
                </td>
                <td>{{ request.service.name }}</td>
                <td>{{ new Date(request.date_of_request).toLocaleDateString() }}</td>
                <td>
                  <NeoBadge :variant="getStatusBadgeClass(request.service_status)">
                    {{ request.service_status }}
                  </NeoBadge>
                </td>
                <td>${{ request.service.price }}</td>
                <td>
                  <NeoButton variant="info" size="sm" @click="viewRequestDetails(request)" class="me-1">
                    <i class="bi bi-eye"></i>
                  </NeoButton>

                  <NeoButton v-if="request.service_status === 'Accepted'" variant="success" size="sm"
                    @click="completeRequest(request.id)" class="me-1">
                    <i class="bi bi-check-circle"></i>
                  </NeoButton>
                </td>
              </tr>
              <tr v-if="filteredAssignedRequests.length === 0">
                <td colspan="7" class="text-center">No assigned requests found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </NeoCard>
    </div>

    <!-- Request Details Modal -->
    <NeoModal v-model="showRequestDetails" :title="`Request #${selectedRequest?.id} Details`" size="lg">
      <div v-if="selectedRequest" class="row">
        <div class="col-md-6">
          <h5>Customer Information</h5>
          <p><strong>Name:</strong> {{ selectedRequest.customer.name }}</p>
          <p><strong>Phone:</strong> {{ selectedRequest.customer.phone_number }}</p>

          <h5 class="mt-4">Service Details</h5>
          <p><strong>Service:</strong> {{ selectedRequest.service.name }}</p>
          <p><strong>Price:</strong> ${{ selectedRequest.service.price }}</p>
          <p><strong>Description:</strong> {{ selectedRequest.service.description }}</p>
        </div>

        <div class="col-md-6">
          <h5>Schedule</h5>
          <p><strong>Date Requested:</strong> {{ new Date(selectedRequest.date_of_request).toLocaleDateString() }}</p>
          <p><strong>Preferred Date:</strong> {{ new Date(selectedRequest.preferred_date).toLocaleDateString() }}</p>

          <div v-if="selectedRequest.date_of_completion">
            <p><strong>Date Completed:</strong> {{ new Date(selectedRequest.date_of_completion).toLocaleDateString() }}
            </p>
          </div>

          <p>
            <strong>Status:</strong>
            <NeoBadge :variant="getStatusBadgeClass(selectedRequest.service_status)" class="ms-2">
              {{ selectedRequest.service_status.charAt(0).toUpperCase() + selectedRequest.service_status.slice(1) }}
            </NeoBadge>
          </p>

          <div>
            <h5 class="mt-4">Remarks</h5>
            <p>{{ selectedRequest.remarks }}</p>
          </div>

          <div v-if="selectedRequest.service_status === 'Accepted'">
            <h5 class="mt-4">Completion Form</h5>
            <div class="mb-3">
              <label for="completionRemarks" class="form-label">Completion Remarks</label>
              <textarea id="completionRemarks" v-model="completionRemarks" class="form-control" rows="3"></textarea>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showRequestDetails = false">Close</NeoButton>

        <template v-if="selectedRequest && activeTab === 'available' && selectedRequest.service_status === 'Pending'">
          <NeoButton variant="success" @click="acceptRequest(selectedRequest.id)" class="ms-2">
            Accept Request
          </NeoButton>
        </template>

        <NeoButton v-if="selectedRequest && selectedRequest.service_status === 'Accepted'" variant="success"
          @click="completeRequest(selectedRequest.id)" class="ms-2">
          Mark as Completed
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

<style scoped>
.modal.show {
  display: block;
}
</style>
