import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('./pages/Home.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('./pages/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('./pages/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('./pages/AdminLogin.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin/register',
    name: 'AdminRegister',
    component: () => import('./pages/AdminRegister.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/events',
    name: 'EventsList',
    component: () => import('./pages/EventsList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/events/:id',
    name: 'EventDetails',
    component: () => import('./pages/EventDetails.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-events',
    name: 'MyEvents',
    component: () => import('./pages/MyEvents.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: () => import('./pages/Calendar.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-requests',
    name: 'MyRequests',
    component: () => import('./pages/MyRequests.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/event-request',
    name: 'EventRequest',
    component: () => import('./pages/EventRequest.vue'),
    meta: { requiresAuth: true, requiresStudent: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('./pages/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminPanel',
    component: () => import('./pages/AdminPanel.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      if (to.path.startsWith('/admin')) {
        next('/admin/login')
      } else {
        next('/login')
      }
      return
    }
    
    // Check if user data is loaded
    if (!authStore.user) {
      try {
        await authStore.fetchUser()
      } catch (error) {
        console.error('Failed to fetch user:', error)
        authStore.logout()
        next('/login')
        return
      }
    }
    
    // Check admin routes
    if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
      next('/admin/login')
      return
    }
    
    // Check student-only routes (event requests)
    if (to.meta.requiresStudent && authStore.user?.role === 'admin') {
      next('/admin')
      return
    }
    
    // Redirect non-admins trying to access /admin
    if (to.path === '/admin' && authStore.user?.role !== 'admin') {
      next('/admin/login')
      return
    }
    
    // Redirect admins trying to access /event-request
    if (to.path === '/event-request' && authStore.user?.role === 'admin') {
      next('/admin')
      return
    }
  }
  
  next()
})

export default router

