import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/services/api'
import { toastService } from '@/services/toastService'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: ref(null),
    access_token: ref(null),
    refresh_token: ref(null),
    error: ref(null),
    loading: ref(false),
  }),

  getters: {
    isAuthenticated: (state) => !!state.access_token,
    isAdmin: (state) => state.user?.roles?.some((role) => role.name === 'admin'),
    isProfessional: (state) => state.user?.roles?.some((role) => role.name === 'professional'),
    isCustomer: (state) => state.user?.roles?.some((role) => role.name === 'customer'),
    isBlocked: (state) => state.user?.blocked,
    isApproved: (state) => state.user?.status === 'approved',
    isPending: (state) => state.user?.status === 'pending',
    isDisapproved: (state) => state.user?.status === 'disapproved',
  },

  actions: {
    async initialize() {
      console.log('Initializing auth store')
      const access_token = localStorage.getItem('access_token')
      const refresh_token = localStorage.getItem('refresh_token')
      if (access_token && refresh_token) {
        this.access_token = access_token
        this.refresh_token = refresh_token
        await this.fetchUser()
      }
    },

    async login(credentials) {
      try {
        this.loading = true
        this.error = null
        const response = await authAPI.login(credentials)
        const { access_token, refresh_token } = response.data
        this.access_token = access_token
        this.refresh_token = refresh_token
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)
        await this.fetchUser()
        return true
      } catch (err) {
        console.error('Login error:', err)
        this.error = err.response?.data?.message || 'Login failed'
        return false
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      try {
        const formData = new FormData()

        // Add user data
        Object.keys(userData).forEach((key) => {
          if (key !== 'documents') {
            formData.append(key, userData[key])
          }
        })

        // Add documents if any
        if (userData.documents) {
          userData.documents.forEach((doc, index) => {
            formData.append(`document_${index}`, doc.file)
            formData.append(`document_type_${index}`, doc.type)
          })
        }

        const response = await authAPI.register(formData)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || 'Registration failed'
        throw error
      }
    },

    async logout() {
      this.user = null
      this.access_token = null
      this.refresh_token = null
      this.error = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      toastService.info('You have been logged out')
    },

    async fetchUser() {
      try {
        const response = await authAPI.getCurrentUser()
        this.user = response.data
      } catch (err) {
        console.error('Failed to fetch user:', err)
        this.error = err.response?.data?.message || 'Failed to fetch user data'
        toastService.error('Session expired. Please log in again.')
        await this.logout()
      }
    },
  },

  persist: {
    key: 'auth-store',
    storage: localStorage,
    paths: ['user', 'access_token', 'refresh_token'],
  },
})
