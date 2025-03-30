import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { useAuthStore } from '@/stores/auth'

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
    {
      path: '/blocked',
      name: 'blocked',
      component: () => import('../views/auth/BlockedView.vue'),
    },
    {
      path: '/pending-approval',
      name: 'pending-approval',
      component: () => import('../views/auth/PendingApprovalView.vue'),
    },
    {
      path: '/disapproved',
      name: 'disapproved',
      component: () => import('../views/auth/DisapprovedView.vue'),
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
  const role = to.meta.role

  const authStore = useAuthStore()
  const isAuthenticated = authStore.isAuthenticated
  const userRoles = authStore.user?.roles
  const isBlocked = authStore.user?.blocked

  // Check if professional is pending approval or has been disapproved
  const isProfessionalPending =
    userRoles?.map((r) => r.name).includes('professional') && authStore.user?.status === 'pending'

  const isProfessionalDisapproved =
    userRoles?.map((r) => r.name).includes('professional') &&
    authStore.user?.status === 'disapproved'

  // If user is blocked and trying to access any protected route, redirect to blocked page
  if (isBlocked && requiresAuth) {
    next('/blocked')
    return
  }

  // If professional is pending approval and trying to access professional dashboard, redirect to pending approval page
  if (isProfessionalPending && to.path.startsWith('/professional')) {
    next('/pending-approval')
    return
  }

  // If professional is disapproved and trying to access professional dashboard, redirect to disapproved page
  if (isProfessionalDisapproved && to.path.startsWith('/professional')) {
    next('/disapproved')
    return
  }

  if (requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (role && !userRoles.map((r) => r.name).includes(role)) {
    next('/')
  } else {
    next()
  }
})

export default router
