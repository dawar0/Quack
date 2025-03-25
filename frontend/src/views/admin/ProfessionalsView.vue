<script setup>
import { ref, computed } from 'vue'
import { NeoButton, NeoCard, NeoInput, NeoSelect, NeoModal, NeoBadge } from '@/components/ui'
import { toastService } from '@/services/toastService'

// Sample professionals data - in a real app, this would come from an API
const professionals = ref([
  {
    id: 1,
    name: 'John Smith',
    email: 'john.smith@example.com',
    phone: '555-123-4567',
    service_type: 'House Cleaning',
    experience: '5 years',
    date_created: '2023-08-15',
    status: 'approved',
    description: 'Experienced house cleaner specializing in deep cleaning and organization.',
  },
  {
    id: 2,
    name: 'Maria Garcia',
    email: 'maria.garcia@example.com',
    phone: '555-987-6543',
    service_type: 'House Cleaning',
    experience: '3 years',
    date_created: '2023-09-20',
    status: 'pending',
    description: 'Detail-oriented cleaner with focus on eco-friendly products and methods.',
  },
  {
    id: 3,
    name: 'Robert Johnson',
    email: 'robert.johnson@example.com',
    phone: '555-456-7890',
    service_type: 'Plumbing',
    experience: '8 years',
    date_created: '2023-07-05',
    status: 'approved',
    description: 'Licensed plumber with experience in residential and commercial projects.',
  },
  {
    id: 4,
    name: 'Sarah Lee',
    email: 'sarah.lee@example.com',
    phone: '555-789-0123',
    service_type: 'Electrical Work',
    experience: '6 years',
    date_created: '2023-10-10',
    status: 'blocked',
    description:
      'Certified electrician specializing in home rewiring and smart home installations.',
  },
  {
    id: 5,
    name: 'James Wilson',
    email: 'james.wilson@example.com',
    phone: '555-234-5678',
    service_type: 'Gardening',
    experience: '4 years',
    date_created: '2023-11-15',
    status: 'pending',
    description: 'Passionate gardener with expertise in sustainable garden design and maintenance.',
  },
])

// Search and filter functionality
const searchTerm = ref('')
const statusFilter = ref('all')

// Status options for filter
const statusOptions = [
  { value: 'all', label: 'All Professionals' },
  { value: 'pending', label: 'Pending Approval' },
  { value: 'approved', label: 'Approved' },
  { value: 'blocked', label: 'Blocked' },
  { value: 'disapproved', label: 'Disapproved' },
]

const filteredProfessionals = computed(() => {
  return professionals.value.filter((professional) => {
    // Apply search term filter
    if (
      searchTerm.value &&
      !professional.name.toLowerCase().includes(searchTerm.value.toLowerCase()) &&
      !professional.email.toLowerCase().includes(searchTerm.value.toLowerCase()) &&
      !professional.service_type.toLowerCase().includes(searchTerm.value.toLowerCase())
    ) {
      return false
    }

    // Apply status filter
    if (statusFilter.value !== 'all' && professional.status !== statusFilter.value) {
      return false
    }

    return true
  })
})

// Professional details modal
const showDetailsModal = ref(false)
const currentProfessional = ref(null)

const viewDetails = (professional) => {
  currentProfessional.value = professional
  showDetailsModal.value = true
}

// Reapprove a professional
const reapproveProfessional = (professional) => {
  const index = professionals.value.findIndex((p) => p.id === professional.id)
  if (index !== -1) {
    professionals.value[index] = {
      ...professional,
      status: 'approved',
    }
    toastService.success(`${professional.name} has been reapproved`)
  }
}

// Update existing functions to show toasts
const approveProfessional = (professional) => {
  const index = professionals.value.findIndex((p) => p.id === professional.id)
  if (index !== -1) {
    professionals.value[index] = {
      ...professional,
      status: 'approved',
    }
    toastService.success(`${professional.name} has been approved`)
  }
}

const disapproveProfessional = (professional) => {
  const index = professionals.value.findIndex((p) => p.id === professional.id)
  if (index !== -1) {
    professionals.value[index] = {
      ...professional,
      status: 'disapproved',
    }
    toastService.error(`${professional.name} has been disapproved`)
  }
}

const toggleBlockStatus = (professional) => {
  const index = professionals.value.findIndex((p) => p.id === professional.id)
  if (index !== -1) {
    const newStatus = professional.status === 'blocked' ? 'approved' : 'blocked'
    professionals.value[index] = {
      ...professional,
      status: newStatus,
    }
    if (newStatus === 'blocked') {
      toastService.error(`${professional.name} has been blocked`)
    } else {
      toastService.success(`${professional.name} has been unblocked`)
    }
  }
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
</script>

<template>
  <div class="container py-4">
    <h1 class="mb-2">Service Professionals</h1>

    <!-- Filters & Search -->
    <div class="row mb-2">
      <div class="col-md-6">
        <NeoInput v-model="searchTerm" placeholder="Search professionals..." label="Search" />
      </div>
      <div class="col-md-6">
        <NeoSelect v-model="statusFilter" :options="statusOptions" label="Filter by Status" />
      </div>
    </div>

    <!-- Professionals Table -->
    <NeoCard>
      <template #title>Service Professionals</template>

      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Service Type</th>
              <th>Experience</th>
              <th>Date Joined</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in filteredProfessionals" :key="professional.id">
              <td>{{ professional.id }}</td>
              <td>{{ professional.name }}</td>
              <td>{{ professional.service_type }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.date_created }}</td>
              <td>
                <NeoBadge :variant="getStatusBadgeClass(professional.status)">
                  {{ professional.status.charAt(0).toUpperCase() + professional.status.slice(1) }}
                </NeoBadge>
              </td>
              <td>
                <NeoButton variant="info" size="sm" @click="viewDetails(professional)" class="me-1">
                  <i class="bi bi-eye"></i>
                </NeoButton>

                <NeoButton
                  v-if="professional.status === 'pending'"
                  variant="success"
                  size="sm"
                  @click="approveProfessional(professional)"
                  class="me-1"
                >
                  <i class="bi bi-check-lg"></i>
                </NeoButton>
                <NeoButton
                  v-if="professional.status === 'pending'"
                  variant="danger"
                  size="sm"
                  @click="disapproveProfessional(professional)"
                  class="me-1"
                >
                  <i class="bi bi-x-lg"></i>
                </NeoButton>
                <NeoButton
                  v-if="professional.status === 'disapproved'"
                  variant="success"
                  size="sm"
                  @click="reapproveProfessional(professional)"
                  class="me-1"
                >
                  <i class="bi bi-check-lg"></i>
                </NeoButton>

                <NeoButton
                  :variant="professional.status === 'blocked' ? 'warning' : 'danger'"
                  size="sm"
                  @click="toggleBlockStatus(professional)"
                >
                  <i :class="professional.status === 'blocked' ? 'bi bi-unlock' : 'bi bi-lock'"></i>
                </NeoButton>
              </td>
            </tr>
            <tr v-if="filteredProfessionals.length === 0">
              <td colspan="7" class="text-center">No professionals found</td>
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
        </div>
        <div class="col-md-6">
          <h5>About</h5>
          <p>{{ currentProfessional.description }}</p>

          <h5 class="mt-4">Verification Documents</h5>
          <div class="d-flex gap-2 mb-3">
            <div class="border p-2 text-center">
              <i class="bi bi-file-earmark-text display-4"></i>
              <p class="mb-0">ID Proof</p>
            </div>
            <div class="border p-2 text-center">
              <i class="bi bi-file-earmark-text display-4"></i>
              <p class="mb-0">Certificate</p>
            </div>
            <div class="border p-2 text-center">
              <i class="bi bi-file-earmark-text display-4"></i>
              <p class="mb-0">Address Proof</p>
            </div>
          </div>

          <h5 class="mt-4">Recent Service History</h5>
          <div class="list-group">
            <div class="list-group-item d-flex justify-content-between align-items-center">
              Service #1245
              <NeoBadge variant="success" size="sm">Completed</NeoBadge>
            </div>
            <div class="list-group-item d-flex justify-content-between align-items-center">
              Service #1189
              <NeoBadge variant="success" size="sm">Completed</NeoBadge>
            </div>
            <div class="list-group-item d-flex justify-content-between align-items-center">
              Service #1023
              <NeoBadge variant="success" size="sm">Completed</NeoBadge>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showDetailsModal = false">Close</NeoButton>

        <template v-if="currentProfessional">
          <template v-if="currentProfessional.status === 'pending'">
            <NeoButton
              variant="success"
              @click="approveProfessional(currentProfessional)"
              class="ms-2"
            >
              Approve Professional
            </NeoButton>
            <NeoButton
              variant="danger"
              @click="disapproveProfessional(currentProfessional)"
              class="ms-2"
            >
              Disapprove Professional
            </NeoButton>
          </template>

          <template v-if="currentProfessional.status === 'disapproved'">
            <NeoButton
              variant="success"
              @click="reapproveProfessional(currentProfessional)"
              class="ms-2"
            >
              Reapprove Professional
            </NeoButton>
          </template>

          <template
            v-if="
              currentProfessional.status !== 'pending' &&
              currentProfessional.status !== 'disapproved'
            "
          >
            <NeoButton
              :variant="currentProfessional.status === 'blocked' ? 'warning' : 'danger'"
              @click="toggleBlockStatus(currentProfessional)"
              class="ms-2"
            >
              {{
                currentProfessional.status === 'blocked'
                  ? 'Unblock Professional'
                  : 'Block Professional'
              }}
            </NeoButton>
          </template>
        </template>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
.modal.show {
  display: block;
}
</style>
