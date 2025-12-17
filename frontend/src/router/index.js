import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/AdminLogin.vue'),
    meta: { public: true }
  },
  {
    path: '/admin/register',
    name: 'AdminRegister',
    component: () => import('../views/AdminRegister.vue'),
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Events',
    component: () => import('../views/Events.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/my-activities',
    name: 'MyActivities',
    component: () => import('../views/MyActivities.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')
  const isAuthenticated = !!token
  const isAdmin = user?.role === 'admin'
  
  // Public routes (admin login/register) - always accessible
  if (to.meta.public) {
    next()
    return
  }
  
  // Guest routes (login/register) - redirect if already logged in
  if (to.meta.guest) {
    if (isAuthenticated) {
      next(isAdmin ? '/admin' : '/')
    } else {
      next()
    }
    return
  }
  
  // Protected routes
  if (to.meta.requiresAuth && !isAuthenticated) {
    // If trying to access /admin without auth, redirect to admin login
    if (to.path === '/admin' || to.path.startsWith('/admin')) {
      next('/admin/login')
    } else {
      next('/login')
    }
    return
  }
  
  // Admin routes - if authenticated but not admin
  if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
    return
  }
  
  next()
})

export default router
