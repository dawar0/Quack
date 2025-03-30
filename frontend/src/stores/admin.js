import { defineStore } from 'pinia'
import { adminAPI } from '@/services/api'
import { toastService } from '@/services/toastService'

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: [],
    roles: [],
    services: [],
    requests: [],
    loading: false,
    error: null,
    selectedItem: null,
    dashboardStats: {
      total_customers: 0,
      total_professionals: 0,
      active_services: 0,
      pending_requests: 0,
      pending_approvals: 0,
      completed_services: 0,
      recent_activity: [],
    },
    reports: {
      service_requests: [],
      service_types: [],
      professional_stats: {},
    },
  }),

  getters: {
    customers: (state) => state.users.filter((user) => user.role_ids.includes(3)),
    professionals: (state) => state.users.filter((user) => user.role_ids.includes(2)),
  },

  actions: {
    async fetchDashboardStats() {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getDashboardStats()
        this.dashboardStats = {
          ...response.data,
          recent_activity: response.data.recent_activity.map((activity) => ({
            ...activity,
            timeAgo: this.formatTimeAgo(activity.timestamp),
          })),
        }
        return true
      } catch (err) {
        console.error('Failed to fetch dashboard stats:', err)
        this.error = err.response?.data?.message || 'Failed to fetch dashboard stats'
        return false
      } finally {
        this.loading = false
      }
    },

    formatTimeAgo(timestamp) {
      const date = new Date(timestamp)
      const now = new Date()
      const diff = now - date
      const hours = Math.floor(diff / (1000 * 60 * 60))
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))

      if (hours < 24) {
        return `${hours} hours ago`
      } else {
        return `${days} days ago`
      }
    },

    async fetchUsers() {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getUsers()
        this.users = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch users:', err)
        this.error = err.response?.data?.message || 'Failed to fetch users'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUserById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getUserById(id)
        this.selectedItem = response.data

        return response
      } catch (err) {
        console.error('Failed to fetch user details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch user details'
        return false
      } finally {
        this.loading = false
      }
    },

    async updateUserStatus(userId, data) {
      try {
        this.loading = true
        this.error = null

        const updateData = {
          status: data.status,
          blocked: data.blocked,
        }

        // Add rejection reason if provided
        if (data.rejection_reason !== undefined) {
          updateData.rejection_reason = data.rejection_reason
        }

        await adminAPI.updateUserStatus(userId, updateData)
        await this.fetchUsers()

        // Show toast message based on status
        if (data.blocked) {
          toastService.warning(`User has been blocked`)
        } else if (data.status === 'approved') {
          toastService.success(`User has been approved`)
        } else if (data.status === 'disapproved') {
          toastService.error(`User has been disapproved`)
        }

        return true
      } catch (err) {
        console.error('Failed to update user status:', err)
        this.error = err.response?.data?.message || 'Failed to update user status'
        toastService.error(err.response?.data?.message || 'Failed to update user status')
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchRoles() {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getRoles()
        this.roles = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch roles:', err)
        this.error = err.response?.data?.message || 'Failed to fetch roles'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchRoleById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getRoleById(id)
        this.selectedItem = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch role details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch role details'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAdminServices() {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getAdminServices()
        this.services = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch services:', err)
        this.error = err.response?.data?.message || 'Failed to fetch services'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAdminServiceById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getAdminServiceById(id)
        this.selectedItem = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch service details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch service details'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAdminRequests() {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getAdminRequests()
        this.requests = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch requests:', err)
        this.error = err.response?.data?.message || 'Failed to fetch requests'
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchAdminRequestById(id) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getAdminRequestById(id)
        this.selectedItem = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch request details:', err)
        this.error = err.response?.data?.message || 'Failed to fetch request details'
        return false
      } finally {
        this.loading = false
      }
    },

    async updateRequestStatus(requestId, status) {
      try {
        this.loading = true
        this.error = null
        await adminAPI.updateRequestStatus(requestId, { status })
        await this.fetchAdminRequests()

        // Show toast message based on status
        if (status === 'assigned') {
          toastService.success('Service request has been assigned')
        } else if (status === 'completed') {
          toastService.success('Service request has been marked as completed')
        } else if (status === 'cancelled') {
          toastService.warning('Service request has been cancelled')
        }

        return true
      } catch (err) {
        console.error('Failed to update request status:', err)
        this.error = err.response?.data?.message || 'Failed to update request status'
        toastService.error(err.response?.data?.message || 'Failed to update request status')
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchReports(params) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.getReports(params)
        this.reports = response.data
        return true
      } catch (err) {
        console.error('Failed to fetch reports:', err)
        this.error = err.response?.data?.message || 'Failed to fetch reports'
        return false
      } finally {
        this.loading = false
      }
    },

    async exportReport(params) {
      try {
        this.loading = true
        this.error = null
        const response = await adminAPI.exportReport(params)

        toastService.success('Report exported successfully')
        return response
      } catch (err) {
        console.error('Failed to export report:', err)
        this.error = err.response?.data?.message || 'Failed to export report'
        toastService.error(err.response?.data?.message || 'Failed to export report')
        return false
      } finally {
        this.loading = false
      }
    },
  },
})
