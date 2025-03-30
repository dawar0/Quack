import { defineStore } from 'pinia'
import { serviceAPI } from '@/services/api'
import { toastService } from '@/services/toastService'

export const useServiceStore = defineStore('service', {
  state: () => ({
    services: [],
    loading: false,
    error: null,
    selectedService: null,
  }),

  getters: {
    serviceById: (state) => (id) => {
      return state.services.find((service) => service.id === id)
    },
  },

  actions: {
    async fetchServices() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceAPI.getAll()
        this.services = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch services:', err)
        this.error = err.response?.data?.message || 'Failed to fetch services'
        toastService.error('Failed to load services')
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchServiceById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await serviceAPI.getById(id)
        this.selectedService = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch service details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch service details'
        toastService.error('Failed to load service details')
        return false
      } finally {
        this.loading = false
      }
    },

    async createService(serviceData) {
      try {
        this.loading = true
        this.error = null
        await serviceAPI.create(serviceData)
        await this.fetchServices()
        toastService.success('Service created successfully')
        return true
      } catch (err) {
        console.error('Failed to create service:', err)
        this.error = err.response?.data?.message || 'Failed to create service'
        toastService.error(err.response?.data?.message || 'Failed to create service')
        return false
      } finally {
        this.loading = false
      }
    },

    async updateService(id, serviceData) {
      try {
        this.loading = true
        this.error = null
        await serviceAPI.update(id, serviceData)
        await this.fetchServices()
        toastService.success('Service updated successfully')
        return true
      } catch (err) {
        console.error('Failed to update service:', err)
        this.error = err.response?.data?.message || 'Failed to update service'
        toastService.error(err.response?.data?.message || 'Failed to update service')
        return false
      } finally {
        this.loading = false
      }
    },

    async deleteService(id) {
      try {
        this.loading = true
        this.error = null
        await serviceAPI.delete(id)
        await this.fetchServices()
        toastService.success('Service deleted successfully')
        return true
      } catch (err) {
        console.error('Failed to delete service:', err)
        this.error = err.response?.data?.message || 'Failed to delete service'
        if (err.response?.status === 400) {
          this.error = 'Cannot delete service that has existing requests'
          toastService.error('Cannot delete service that has existing requests')
        } else {
          toastService.error(err.response?.data?.message || 'Failed to delete service')
        }
        return false
      } finally {
        this.loading = false
      }
    },
  },
})
