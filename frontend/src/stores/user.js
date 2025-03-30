import { defineStore } from 'pinia'
import api from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    profile: null,
    isLoading: false,
    error: null,
  }),

  actions: {
    async updateUserProfile(profileData) {
      this.isLoading = true
      this.error = null

      try {
        const response = await api.put('/user/profile', profileData)
        this.profile = response.data
        return this.profile
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to update profile'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Change password
    async changePassword(passwordData) {
      this.isLoading = true
      this.error = null

      try {
        await api.post('/user/change-password', passwordData)
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to change password'
        throw error
      } finally {
        this.isLoading = false
      }
    },

    // Delete account
    async deleteAccount() {
      this.isLoading = true
      this.error = null

      try {
        await api.delete('/user/account')
      } catch (error) {
        this.error = error.response?.data?.message || 'Failed to delete account'
        throw error
      } finally {
        this.isLoading = false
      }
    },
  },
})
