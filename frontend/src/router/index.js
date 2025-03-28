import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/auth/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/auth/RegisterView.vue'),
    },
    // Admin routes
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/DashboardView.vue'),
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'services',
          name: 'admin-services',
          component: () => import('../views/admin/ServicesView.vue'),
        },
        {
          path: 'professionals',
          name: 'admin-professionals',
          component: () => import('../views/admin/ProfessionalsView.vue'),
        },
        {
          path: 'customers',
          name: 'admin-customers',
          component: () => import('../views/admin/CustomersView.vue'),
        },
        {
          path: 'reports',
          name: 'admin-reports',
          component: () => import('../views/admin/ReportsView.vue'),
        },
      ],
    },
    // Professional routes
    {
      path: '/professional',
      name: 'professional',
      component: () => import('../views/professional/DashboardView.vue'),
      meta: { requiresAuth: true, role: 'professional' },
      children: [
        {
          path: 'requests',
          name: 'professional-requests',
          component: () => import('../views/professional/RequestsView.vue'),
        },
        {
          path: 'profile',
          name: 'professional-profile',
          component: () => import('../views/professional/ProfileView.vue'),
        },
      ],
    },
    // Customer routes
    {
      path: '/customer',
      name: 'customer',
      component: () => import('../views/customer/DashboardView.vue'),
      meta: { requiresAuth: true, role: 'customer' },
      children: [
        {
          path: 'requests',
          name: 'customer-requests',
          component: () => import('../views/customer/RequestsView.vue'),
        },
        {
          path: 'profile',
          name: 'customer-profile',
          component: () => import('../views/customer/ProfileView.vue'),
        },
      ],
    },
  ],
})

// Navigation guard to check authentication and role
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const role = to.matched.find((record) => record.meta.role)?.meta.role

  // This will need to be implemented with actual auth logic
  const isAuthenticated = localStorage.getItem('token') !== null
  const userRole = localStorage.getItem('role')

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (role && role !== userRole) {
    next('/')
  } else {
    next()
  }
})

export default router
