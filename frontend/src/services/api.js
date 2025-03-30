import axios from 'axios'

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Important for handling cookies
})

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor for handling token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // If error is 401 and we haven't tried to refresh token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      // Skip token refresh for login/register routes - just return the error
      if (
        originalRequest.url?.includes('/auth/login') ||
        originalRequest.url?.includes('/auth/register')
      ) {
        return Promise.reject(error)
      }

      originalRequest._retry = true

      try {
        // Get refresh token from localStorage
        const refreshToken = localStorage.getItem('refresh_token')

        if (!refreshToken) {
          throw new Error('No refresh token available')
        }

        // Try to refresh the token
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/refresh`,
          {},
          {
            withCredentials: true,
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          },
        )

        if (response.data && response.data.access_token && response.data.refresh_token) {
          const { access_token, refresh_token } = response.data
          localStorage.setItem('access_token', access_token)
          localStorage.setItem('refresh_token', refresh_token)

          // Update the original request with new token
          originalRequest.headers.Authorization = `Bearer ${access_token}`
          return api(originalRequest)
        } else {
          throw new Error('Invalid token response')
        }
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError)
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  },
)

// Auth API endpoints
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (formData) =>
    api.post('/auth/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  logout: () => api.post('/auth/logout'),
  refresh: () => {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      return Promise.reject(new Error('No refresh token available'))
    }
    return api.post(
      '/auth/refresh',
      {},
      {
        headers: {
          Authorization: `Bearer ${refreshToken}`,
        },
      },
    )
  },
  getCurrentUser: () => api.get('/auth/me'),
}

// Service API endpoints
export const serviceAPI = {
  getAll: () => api.get('/service/'),
  getById: (id) => api.get(`/service/${id}`),
  create: (serviceData) => api.post('/service/', serviceData),
  update: (id, serviceData) => api.put(`/service/${id}`, serviceData),
  delete: (id) => api.delete(`/service/${id}`),
}

// Service Request API endpoints
export const serviceRequestAPI = {
  // Customer endpoints
  getCustomerRequests: () => api.get('/customer/requests'),
  getCustomerRequestById: (id) => api.get(`/customer/requests/${id}`),
  createRequest: (requestData) => api.post('/customer/requests', requestData),
  cancelRequest: (actionData) => api.post('/customer/requests/take_action', actionData),
  getCustomerActivityFeed: () => api.get('/customer/dashboard/activity'),

  // Professional endpoints
  getProfessionalRequests: () => api.get('/professional/requests'),
  getAssignedRequests: () => api.get('/professional/requests/assigned'),
  getProfessionalRequestById: (id) => api.get(`/professional/requests/${id}`),
  takeAction: (actionData) => api.post('/professional/requests/take_action', actionData),
  getDashboardStats: () => api.get('/professional/dashboard/stats'),
  getActivityFeed: () => api.get('/professional/dashboard/activity'),
}

// Admin API endpoints
export const adminAPI = {
  // Dashboard stats
  getDashboardStats: () => api.get('/admin/dashboard/stats'),

  // User management
  getUsers: () => api.get('/admin/users'),
  getUserById: (id) => api.get(`/admin/users/${id}`),
  updateUserStatus: (id, data) => api.patch(`/admin/users/${id}/status`, data),

  // Role management
  getRoles: () => api.get('/admin/roles'),
  getRoleById: (id) => api.get(`/admin/roles/${id}`),

  // Service management
  getAdminServices: () => api.get('/admin/services'),
  getAdminServiceById: (id) => api.get(`/admin/services/${id}`),

  // Service request management
  getAdminRequests: () => api.get('/admin/requests'),
  getAdminRequestById: (id) => api.get(`/admin/requests/${id}`),
  updateRequestStatus: (id, data) => api.patch(`/admin/requests/${id}/status`, data),

  // Document management
  getUserDocuments: (userId) => api.get(`/admin/users/${userId}/documents`),
  verifyDocument: (documentId) => api.patch(`/admin/documents/${documentId}/verify`),
  rejectDocument: (documentId) => api.patch(`/admin/documents/${documentId}/reject`),
  downloadDocument: (documentId) =>
    api.get(`/admin/documents/${documentId}/download`, {
      responseType: 'blob', // For file downloads
    }),

  // Reports management
  getReports: (params) => api.get('/admin/reports', { params }),
  exportReport: (params) =>
    api.get('/admin/reports/export', {
      params,
      responseType: 'blob', // For handling file downloads
    }),
}

// Professional API endpoints
export const professionalAPI = {
  updateProfile: (profileData) => api.put('/professional/profile', profileData),
  changePassword: (passwordData) => api.put('/professional/password', passwordData),
  updateProfilePicture: (formData) =>
    api.put('/professional/profile/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  getProfilePictureUrl: (filename) => {
    if (!filename) return null
    return `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/profile-images/${filename}`
  },
  // Document management endpoints
  getDocuments: () => api.get('/professional/documents'),
  uploadDocument: (formData) =>
    api.post('/professional/documents', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  deleteDocument: (documentId) => api.delete(`/professional/documents/${documentId}`),
  downloadDocument: (documentId) =>
    api.get(`/professional/documents/${documentId}/download`, {
      responseType: 'blob', // For file downloads
    }),
}

// Customer API endpoints
export const customerAPI = {
  getProfile: () => api.get('/customer/profile'),
  updateProfile: (profileData) => api.put('/customer/profile', profileData),
  changePassword: (passwordData) => api.put('/customer/password', passwordData),
  updateProfilePicture: (formData) =>
    api.put('/customer/profile/picture', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  getProfilePictureUrl: (filename) => {
    if (!filename) return null
    return `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/auth/profile-images/${filename}`
  },
  deleteAccount: () => api.delete('/customer/account'),
}

export default api
