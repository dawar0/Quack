<script setup>
import { ref, computed, onMounted } from 'vue'
import { useServiceStore } from '@/stores/service'
import { NeoButton, NeoCard, NeoInput, NeoModal, NeoAlert, NeoTextarea, NeoIcon } from '@/components/ui'
import { toastService } from '@/services/toastService'

const serviceStore = useServiceStore()

// State for services
const services = ref([])
const isLoading = ref(false)

// Form state for adding/editing a service
const formMode = ref('add') // 'add' or 'edit'
const showForm = ref(false)
const currentService = ref({
  id: null,
  name: '',
  price: '',
  time_required: '',
  description: '',
})

// Confirmation modal state
const showConfirmModal = ref(false)
const confirmAction = ref(() => { })
const confirmMessage = ref('')

// Search functionality
const searchTerm = ref('')

// Fetch services on component mount
onMounted(async () => {
  try {
    isLoading.value = true
    await serviceStore.fetchServices()
    services.value = serviceStore.services
  } catch (error) {
    console.error('Failed to fetch services:', error)
    toastService.error('Failed to load services.')
  } finally {
    isLoading.value = false
  }
})

// Filter services based on search term
const filteredServices = computed(() => {
  return services.value.filter(service => {
    return !searchTerm.value ||
      service.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      service.description.toLowerCase().includes(searchTerm.value.toLowerCase())
  })
})

// Start adding a new service
const addService = () => {
  formMode.value = 'add'
  currentService.value = {
    id: null,
    name: '',
    price: '',
    time_required: '',
    description: '',
  }
  showForm.value = true
}

// Start editing an existing service
const editService = (service) => {
  formMode.value = 'edit'
  currentService.value = { ...service }
  showForm.value = true
}

// Save the current service (add or update)
const saveService = async () => {
  // Validate form
  if (
    !currentService.value.name ||
    !currentService.value.price ||
    !currentService.value.time_required
  ) {
    toastService.error('Please fill in all required fields.')
    return
  }

  try {
    if (formMode.value === 'add') {
      // Create new service
      await serviceStore.createService({
        name: currentService.value.name,
        price: Number(currentService.value.price),
        time_required: currentService.value.time_required,
        description: currentService.value.description
      })
      toastService.success('Service created successfully!')
    } else {
      // Update existing service
      await serviceStore.updateService(currentService.value.id, {
        name: currentService.value.name,
        price: Number(currentService.value.price),
        time_required: currentService.value.time_required,
        description: currentService.value.description
      })
      toastService.success('Service updated successfully!')
    }
    services.value = serviceStore.services
    showForm.value = false
  } catch (error) {
    toastService.error(error.response?.data?.message || 'Failed to save service.')
  }
}

// Delete a service
const deleteService = (id) => {
  confirmMessage.value = 'Are you sure you want to delete this service?'
  confirmAction.value = async () => {
    try {
      const success = await serviceStore.deleteService(id)
      if (success) {
        services.value = serviceStore.services
        toastService.success('Service deleted successfully!')
      } else {
        toastService.error(serviceStore.error || 'Failed to delete service.')
      }
    } catch (error) {
      console.error('Failed to delete service:', error)
      toastService.error(serviceStore.error || 'Failed to delete service.')
    }
  }
  showConfirmModal.value = true
}

// Handle confirmation
const executeConfirmAction = () => {
  confirmAction.value()
  showConfirmModal.value = false
}
</script>

<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h1 class="page-title">Management</h1>
      <NeoButton @click="addService" variant="primary">
        <NeoIcon name="plus-circle" size="20" class="me-2" />
        Add New Service
      </NeoButton>
    </div>

    <!-- Search -->
    <div class="mb-4">
      <NeoInput v-model="searchTerm" placeholder="Search services..." label="Search" />
    </div>

    <!-- Services Table -->
    <NeoCard>
      <template #title>Services</template>

      <div class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Name</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id">
              <td>{{ service.name }}</td>
              <td>${{ service.price }}</td>
              <td>{{ service.time_required }}</td>
              <td>
                {{
                  service.description.length > 50
                    ? service.description.substring(0, 50) + '...'
                    : service.description
                }}
              </td>
              <td>
                <NeoButton variant="info" size="sm" @click="editService(service)" class="me-1">
                  <NeoIcon name="pencil" size="16" />
                </NeoButton>
                <NeoButton variant="danger" size="sm" @click="deleteService(service.id)">
                  <NeoIcon name="trash" size="16" />
                </NeoButton>
              </td>
            </tr>
            <tr v-if="filteredServices.length === 0">
              <td colspan="6" class="text-center">No services found</td>
            </tr>
          </tbody>
        </table>
      </div>
    </NeoCard>

    <!-- Add/Edit Service Modal -->
    <NeoModal v-model="showForm" :title="formMode === 'add' ? 'Add New Service' : 'Edit Service'">
      <div class="mb-3">
        <NeoInput v-model="currentService.name" label="Service Name" placeholder="Enter service name" required />
      </div>

      <div class="mb-3">
        <NeoInput v-model="currentService.price" type="number" label="Price ($)" placeholder="Enter price" required />
      </div>

      <div class="mb-3">
        <NeoInput v-model="currentService.time_required" label="Time Required" placeholder="e.g. 2 hours, 1-3 hours"
          required />
      </div>

      <div class="mb-3">
        <NeoTextarea v-model="currentService.description" label="Description" placeholder="Enter service description"
          required />
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showForm = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="saveService" class="ms-2">Save</NeoButton>
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
