<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { NeoButton, NeoCard, NeoInput, NeoSelect, NeoModal, NeoBadge, NeoAlert, NeoIcon } from '@/components/ui'
import { adminAPI, professionalAPI } from '@/services/api'
import { toastService } from '@/services/toastService'

const adminStore = useAdminStore()

const professionals = ref([])
const professionalDocuments = ref([])
const loadingDocuments = ref(false)

const searchTerm = ref('')
const statusFilter = ref('all')
const statusOptions = [
  { value: 'all', label: 'All Professionals' },
  { value: 'pending', label: 'Pending Approval' },
  { value: 'approved', label: 'Approved' },
  { value: 'blocked', label: 'Blocked' },
  { value: 'disapproved', label: 'Disapproved' },
]

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmAction = ref(() => { })
const confirmMessage = ref('')

// Rejection reason modal state
const showRejectionModal = ref(false)
const rejectionReason = ref('')
const professionalToDisapprove = ref(null)

// Professional details modal
const showDetailsModal = ref(false)
const currentProfessional = ref(null)

// Fetch professionals on component mount
onMounted(async () => {
  try {
    await adminStore.fetchUsers()
    // Filter professionals and ensure we have all required fields
    professionals.value = adminStore.professionals.map(professional => ({
      ...professional,
      status: professional.status || 'pending',
      blocked: professional.blocked || false,
      service_type: professional.service_type || 'Not specified',
      experience: professional.experience || 'Not specified',
      date_created: professional.date_created || 'Not available'
    }))
  } catch (error) {
    console.error('Failed to load professionals:', error)
    toastService.error('Failed to load professionals.')
  }
})

const filteredProfessionals = computed(() => {
  return professionals.value.filter((professional) => {
    if (searchTerm.value) {
      const searchLower = searchTerm.value.toLowerCase()
      const nameMatch = professional.name?.toLowerCase().includes(searchLower)
      const emailMatch = professional.email?.toLowerCase().includes(searchLower)
      const serviceMatch = professional.service_type?.toLowerCase().includes(searchLower)

      if (!nameMatch && !emailMatch && !serviceMatch) {
        return false
      }
    }

    if (statusFilter.value !== 'all') {
      if (statusFilter.value === 'blocked' && !professional.blocked) {
        return false
      }
      if (statusFilter.value !== 'blocked' && professional.status !== statusFilter.value) {
        return false
      }
    }

    return true
  })
})

// Fetch professional documents
const fetchProfessionalDocuments = async (professionalId) => {
  loadingDocuments.value = true
  professionalDocuments.value = []

  try {
    const response = await adminAPI.getUserDocuments(professionalId)
    professionalDocuments.value = response.data
  } catch (error) {
    console.error('Failed to fetch documents:', error)
    toastService.error('Failed to fetch professional documents.')
  } finally {
    loadingDocuments.value = false
  }
}

// View professional details
const viewDetails = async (professional) => {
  try {
    await adminStore.fetchUserById(professional.id)
    currentProfessional.value = adminStore.selectedItem
    showDetailsModal.value = true

    // Fetch documents when viewing details
    await fetchProfessionalDocuments(professional.id)
  } catch (error) {
    toastService.error(error.response?.data?.message || 'Failed to fetch professional details.')
  }
}

// Get document status badge class
const getDocumentStatusBadgeClass = (document) => {
  if (document.verified) return 'success'
  if (document.rejected) return 'danger'
  return 'warning'
}

// Get document status text
const getDocumentStatusText = (document) => {
  if (document.verified) return 'Verified'
  if (document.rejected) return 'Rejected'
  return 'Pending'
}

// View document
const viewDocument = async (document) => {
  try {
    toastService.info('Downloading document...')
    const response = await adminAPI.downloadDocument(document.id)

    // Create a blob from the response data
    const blob = new Blob([response.data], {
      type: document.file_name.toLowerCase().endsWith('.pdf') ? 'application/pdf' : 'application/octet-stream'
    })
    const url = window.URL.createObjectURL(blob)

    // Open document in a new tab
    window.open(url, '_blank')

    // Clean up the URL object after the document is opened
    setTimeout(() => {
      window.URL.revokeObjectURL(url)
    }, 100)
  } catch (error) {
    console.error('Failed to download document:', error)
    toastService.error('Failed to download document')
  }
}

// Handle professional status changes
const handleStatusChange = async (professional, newStatus) => {
  if (newStatus === 'disapproved') {
    // Show rejection reason modal
    professionalToDisapprove.value = professional
    rejectionReason.value = ''
    showRejectionModal.value = true
    return
  }

  confirmMessage.value = `Are you sure you want to ${newStatus} this professional?`
  confirmAction.value = async () => {
    try {
      await adminStore.updateUserStatus(professional.id, {
        status: newStatus,
        blocked: professional.blocked
      })
      professionals.value = adminStore.professionals
      toastService.success(`Professional ${professional.name} has been ${newStatus}.`)
    } catch (error) {
      console.error('Error updating status:', error)
      toastService.error(error.response?.data?.message || `Failed to ${newStatus} professional.`)
    }
  }
  showConfirmModal.value = true
}

// Submit rejection reason and disapprove professional
const submitDisapproval = async () => {
  try {
    if (!professionalToDisapprove.value) return

    await adminStore.updateUserStatus(professionalToDisapprove.value.id, {
      status: 'disapproved',
      blocked: professionalToDisapprove.value.blocked,
      rejection_reason: rejectionReason.value
    })

    professionals.value = adminStore.professionals
    showRejectionModal.value = false
    toastService.success(`Professional ${professionalToDisapprove.value.name} has been disapproved.`)
  } catch (error) {
    console.error('Error disapproving professional:', error)
    toastService.error(error.response?.data?.message || 'Failed to disapprove professional.')
  }
}

// Handle professional block status
const toggleBlockStatus = async (professional) => {
  const newStatus = professional.blocked ? 'unblock' : 'block'
  confirmMessage.value = `Are you sure you want to ${newStatus} this professional?`
  confirmAction.value = async () => {
    try {
      await adminStore.updateUserStatus(professional.id, {
        blocked: !professional.blocked,
        status: professional.status
      })
      professionals.value = adminStore.professionals
      toastService.success(`Professional ${professional.name} has been ${newStatus}ed.`)
    } catch (error) {
      console.error('Error updating block status:', error)
      toastService.error(error.response?.data?.message || `Failed to ${newStatus} professional.`)
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
    case 'approved':
      return 'success'
    case 'pending':
      return 'warning'
    case 'blocked':
      return 'danger'
    case 'disapproved':
      return 'danger'
    default:
      return 'secondary'
  }
}

// Helper function to get profile image URL
const getProfileImageUrl = (filename) => {
  return filename ? professionalAPI.getProfilePictureUrl(filename) : 'https://avatar.iran.liara.run/public/11'
}

professionals.value = adminStore.professionals || []
</script>

<template>
  <div class="container">
    <h1 class="mb-4 page-title">Professionals</h1>

    <!-- Filters & Search -->
    <div class="row mb-2">
      <div class="col-md-6">
        <NeoInput v-model="searchTerm" placeholder="Search professionals..." label="Search" />
      </div>
      <div class="col-md-6">
        <NeoSelect v-model="statusFilter" :options="statusOptions" :model-value="statusFilter"
          label="Filter by Status" />
      </div>
    </div>

    <!-- Professionals Table -->
    <NeoCard>
      <template #title>Service Professionals</template>

      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Profile</th>
              <th>Name</th>
              <th>Email</th>
              <th>Service Type</th>
              <th>Experience</th>
              <th>Date Joined</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in filteredProfessionals" :key="professional.id">
              <td>
                <img :src="getProfileImageUrl(professional.profile_image)" alt="Profile" class="rounded-circle"
                  style="width: 40px; height: 40px; object-fit: cover;" />
              </td>
              <td>{{ professional.name }}</td>
              <td>{{ professional.email }}</td>
              <td>{{ professional.service_type }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.date_created }}</td>
              <td>
                <NeoBadge :variant="getStatusBadgeClass(professional.blocked ? 'blocked' : professional.status)">
                  {{ professional.blocked ? 'blocked' : professional.status }}
                </NeoBadge>
              </td>
              <td>
                <NeoButton variant="info" size="sm" @click="viewDetails(professional)" class="me-1">
                  <NeoIcon name="eye" size="16" />
                </NeoButton>

                <NeoButton v-if="professional.status === 'pending'" variant="success" size="sm"
                  @click="handleStatusChange(professional, 'approved')" class="me-1">
                  <NeoIcon name="check" size="16" />
                </NeoButton>
                <NeoButton v-if="professional.status === 'pending'" variant="danger" size="sm"
                  @click="handleStatusChange(professional, 'disapproved')" class="me-1">
                  <NeoIcon name="x" size="16" />
                </NeoButton>
                <NeoButton v-if="professional.status === 'disapproved'" variant="success" size="sm"
                  @click="handleStatusChange(professional, 'approved')" class="me-1">
                  <NeoIcon name="check" size="16" />
                </NeoButton>
                <NeoButton :variant="professional.blocked ? 'success' : 'danger'" size="sm"
                  @click="toggleBlockStatus(professional)">
                  <NeoIcon :name="professional.blocked ? 'unlock' : 'lock'" size="16" />
                </NeoButton>
              </td>
            </tr>
            <tr v-if="filteredProfessionals.length === 0">
              <td colspan="8" class="text-center">No professionals found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </NeoCard>

    <!-- Professional Details Modal -->
    <NeoModal v-model="showDetailsModal" :title="currentProfessional?.name" size="lg">
      <div v-if="currentProfessional" class="row">
        <div class="col-md-6">
          <h5>Personal Information</h5>
          <p><strong>Email:</strong> {{ currentProfessional.email }}</p>
          <p><strong>Phone:</strong> {{ currentProfessional.phone }}</p>
          <p><strong>Service:</strong> {{ currentProfessional.service_type }}</p>
          <p><strong>Experience:</strong> {{ currentProfessional.experience }}</p>
          <p><strong>Joined:</strong> {{ currentProfessional.date_created }}</p>
          <p>
            <strong>Status:</strong>
            <NeoBadge :variant="getStatusBadgeClass(currentProfessional.status)" class="ms-2">
              {{
                currentProfessional.status.charAt(0).toUpperCase() +
                currentProfessional.status.slice(1)
              }}
            </NeoBadge>
          </p>
          <div v-if="currentProfessional.status === 'disapproved' && currentProfessional.rejection_reason"
            class="mt-3 p-3 border border-danger bg-light">
            <h6 class="text-danger">Rejection Reason:</h6>
            <p class="mb-0">{{ currentProfessional.rejection_reason }}</p>
          </div>
        </div>
        <div class="col-md-6">
          <h5>About</h5>
          <p>{{ currentProfessional.description }}</p>

          <h5 class="mt-4">Verification Documents</h5>
          <div v-if="loadingDocuments" class="text-center py-4">
            <div class="spinner-border" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2">Loading documents...</p>
          </div>

          <div v-else-if="professionalDocuments.length === 0" class="text-center py-4">
            <p class="mb-0">No documents uploaded yet</p>
          </div>

          <div v-else>
            <div v-for="doc in professionalDocuments" :key="doc.id" class="mb-3">
              <div class="border border-dark border-3 p-3 bg-light">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <h6 class="mb-0 text-uppercase">{{ doc.document_type }}</h6>
                  <NeoBadge :variant="getDocumentStatusBadgeClass(doc)">
                    {{ getDocumentStatusText(doc) }}
                  </NeoBadge>
                </div>
                <p class="mb-2">{{ doc.file_name }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">
                    Uploaded: {{ new Date(doc.upload_date).toLocaleDateString() }}
                  </small>
                  <div>
                    <NeoButton variant="primary" size="sm" @click="viewDocument(doc)">
                      View Document
                    </NeoButton>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showDetailsModal = false">Close</NeoButton>

        <template v-if="currentProfessional">
          <template v-if="currentProfessional.status === 'pending'">
            <NeoButton variant="success" @click="handleStatusChange(currentProfessional, 'approved')" class="ms-2">
              Approve Professional
            </NeoButton>
            <NeoButton variant="danger" @click="handleStatusChange(currentProfessional, 'disapproved')" class="ms-2">
              Disapprove Professional
            </NeoButton>
          </template>

          <template v-if="currentProfessional.status === 'disapproved'">
            <NeoButton variant="success" @click="handleStatusChange(currentProfessional, 'approved')" class="ms-2">
              Reapprove Professional
            </NeoButton>
          </template>

          <template v-if="
            currentProfessional.status !== 'pending' &&
            currentProfessional.status !== 'disapproved'
          ">
            <NeoButton :variant="currentProfessional.blocked ? 'success' : 'danger'"
              @click="toggleBlockStatus(currentProfessional)" class="ms-2">
              {{
                currentProfessional.blocked
                  ? 'Unblock Professional'
                  : 'Block Professional'
              }}
            </NeoButton>
          </template>
        </template>
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

    <!-- Rejection Reason Modal -->
    <NeoModal v-model="showRejectionModal" title="Rejection Reason">
      <NeoInput v-model="rejectionReason" placeholder="Enter rejection reason" label="Reason" />
      <template #footer>
        <NeoButton variant="secondary" @click="showRejectionModal = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="submitDisapproval" class="ms-2">
          Submit
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
