import { defineStore } from 'pinia'
import { serviceRequestAPI } from '@/services/api'

export const useServiceRequestStore = defineStore('serviceRequest', {
  state: () => ({
    customerRequests: [],
    professionalRequests: [],
    assignedRequests: [],
    loading: false,
    error: null,
    selectedRequest: null,
    currentRequest: null,
    dashboardStats: {
      totalEarnings: 0,
      completedJobs: 0,
      pendingJobs: 0,
      acceptedJobs: 0,
    },
    activityFeed: [],
  }),

  getters: {
    totalRequests: (state) => state.customerRequests.length,
    completedJobs: (state) => state.dashboardStats.completedJobs,
    pendingJobs: (state) => state.dashboardStats.pendingJobs,
    activeJobs: (state) => state.dashboardStats.acceptedJobs,
    totalEarnings: (state) => state.dashboardStats.totalEarnings,
    recentActivity: (state) => state.activityFeed,
  },

  actions: {
    async fetchCustomerRequests() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getCustomerRequests()
        this.customerRequests = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch customer requests:', err)
        this.error = err.response?.data?.message || 'Failed to fetch customer requests'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchProfessionalRequests() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getProfessionalRequests()
        this.professionalRequests = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch professional requests:', err)
        this.error = err.response?.data?.message || 'Failed to fetch professional requests'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAssignedRequests() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getAssignedRequests()
        this.assignedRequests = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch assigned requests:', err)
        this.error = err.response?.data?.message || 'Failed to fetch assigned requests'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchRequestById(id, type = 'customer') {
      try {
        this.loading = true
        this.error = null
        const response = await (type === 'customer'
          ? serviceRequestAPI.getCustomerRequestById(id)
          : serviceRequestAPI.getProfessionalRequestById(id))
        this.selectedRequest = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch request details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch request details'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchCustomerRequestById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getCustomerRequestById(id)
        this.currentRequest = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch customer request details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch request details'
        return false
      } finally {
        this.loading = false
      }
    },

    async createServiceRequest(requestData) {
      try {
        this.loading = true
        this.error = null
        await serviceRequestAPI.createRequest(requestData)
        await this.fetchCustomerRequests()
        return true
      } catch (err) {
        console.error('Failed to create service request:', err)
        this.error = err.response?.data?.message || 'Failed to create service request'
        return false
      } finally {
        this.loading = false
      }
    },

    async takeActionOnRequest(actionData) {
      try {
        this.loading = true
        this.error = null
        await serviceRequestAPI.takeAction(actionData)

        // Fetch fresh data for all request lists
        await Promise.all([
          this.fetchCustomerRequests(),
          this.fetchProfessionalRequests(),
          this.fetchAssignedRequests(),
          this.fetchDashboardStats(),
        ])

        return true
      } catch (err) {
        console.error('Failed to take action on request:', err)
        this.error = err.response?.data?.message || 'Failed to take action on request'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchDashboardStats() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getDashboardStats()
        this.dashboardStats = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err)
        this.error = err.response?.data?.message || 'Failed to fetch dashboard stats'
        // Default values if API fails
        this.dashboardStats = {
          totalEarnings: this.assignedRequests
            .filter((req) => req.service_status === 'Completed')
            .reduce((sum, req) => sum + (req.service?.price || 0), 0),
          completedJobs: this.assignedRequests.filter((req) => req.service_status === 'Completed')
            .length,
          pendingJobs: this.professionalRequests.filter((req) => req.service_status === 'Pending')
            .length,
          acceptedJobs: this.assignedRequests.filter((req) => req.service_status === 'Accepted')
            .length,
        }
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchActivityFeed() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getActivityFeed()
        this.activityFeed = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch activity feed:', err)
        this.error = err.response?.data?.message || 'Failed to fetch activity feed'

        return false
      } finally {
        this.loading = false
      }
    },

    async fetchCustomerActivityFeed() {
      try {
        this.loading = true
        this.error = null
        const response = await serviceRequestAPI.getCustomerActivityFeed()
        this.activityFeed = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch customer activity feed:', err)
        this.error = err.response?.data?.message || 'Failed to fetch activity feed'
        // Generate default activity feed from customer requests if API fails

        return false
      } finally {
        this.loading = false
      }
    },
  },
})
