<script setup>
import { ref, computed } from 'vue'
import { NeoButton, NeoCard, NeoInput, NeoModal } from '@/components/ui'

// Sample service data - in a real app, this would come from an API
const services = ref([
  {
    id: 1,
    name: 'House Cleaning',
    price: 75,
    time_required: '2 hours',
    description:
      'Complete house cleaning service including dusting, mopping, and bathroom cleaning.',
  },
  {
    id: 2,
    name: 'Plumbing',
    price: 120,
    time_required: '1-3 hours',
    description: 'Professional plumbing services for repairs, installations, and maintenance.',
  },
  {
    id: 3,
    name: 'Electrical Work',
    price: 150,
    time_required: '2-4 hours',
    description:
      'Licensed electricians for all your electrical needs, from repairs to installations.',
  },
  {
    id: 4,
    name: 'Gardening',
    price: 90,
    time_required: '3 hours',
    description: 'Complete garden maintenance including mowing, trimming, and planting.',
  },
  {
    id: 5,
    name: 'Painting',
    price: 200,
    time_required: '5-8 hours',
    description: 'Professional painting services for interior and exterior surfaces.',
  },
  {
    id: 6,
    name: 'Carpet Cleaning',
    price: 85,
    time_required: '2 hours',
    description: 'Deep carpet cleaning to remove stains, dirt, and allergens.',
  },
])

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

// Search functionality
const searchTerm = ref('')
const filteredServices = computed(() => {
  if (!searchTerm.value) return services.value

  const term = searchTerm.value.toLowerCase()
  return services.value.filter(
    (service) =>
      service.name.toLowerCase().includes(term) || service.description.toLowerCase().includes(term),
  )
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
const saveService = () => {
  // Validate form
  if (
    !currentService.value.name ||
    !currentService.value.price ||
    !currentService.value.time_required
  ) {
    alert('Please fill in all required fields')
    return
  }

  if (formMode.value === 'add') {
    // Create new service
    const newId = Math.max(0, ...services.value.map((s) => s.id)) + 1
    services.value.push({
      ...currentService.value,
      id: newId,
    })
    alert('Service created successfully!')
  } else {
    // Update existing service
    const index = services.value.findIndex((s) => s.id === currentService.value.id)
    if (index !== -1) {
      services.value[index] = { ...currentService.value }
      alert('Service updated successfully!')
    }
  }

  showForm.value = false
}

// Delete a service
const deleteService = (id) => {
  if (confirm('Are you sure you want to delete this service?')) {
    services.value = services.value.filter((service) => service.id !== id)
    alert('Service deleted successfully!')
  }
}
</script>

<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-2">
      <h1>Service Management</h1>
      <NeoButton @click="addService" variant="primary">
        <i class="bi bi-plus-circle me-2"></i> Add New Service
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
              <th>ID</th>
              <th>Name</th>
              <th>Price</th>
              <th>Time Required</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in filteredServices" :key="service.id">
              <td>{{ service.id }}</td>
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
                  <i class="bi bi-pencil"></i>
                </NeoButton>
                <NeoButton variant="danger" size="sm" @click="deleteService(service.id)">
                  <i class="bi bi-trash"></i>
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
        <NeoInput
          v-model="currentService.name"
          label="Service Name"
          placeholder="Enter service name"
          required
        />
      </div>

      <div class="mb-3">
        <NeoInput
          v-model="currentService.price"
          type="number"
          label="Price ($)"
          placeholder="Enter price"
          required
        />
      </div>

      <div class="mb-3">
        <NeoInput
          v-model="currentService.time_required"
          label="Time Required"
          placeholder="e.g. 2 hours, 1-3 hours"
          required
        />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
          id="description"
          v-model="currentService.description"
          class="form-control"
          rows="3"
          placeholder="Enter service description"
        ></textarea>
      </div>

      <template #footer>
        <NeoButton variant="secondary" @click="showForm = false">Cancel</NeoButton>
        <NeoButton variant="primary" @click="saveService" class="ms-2">Save</NeoButton>
      </template>
    </NeoModal>
  </div>
</template>

<style scoped>
.modal.show {
  display: block;
}
</style>
