import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
<<<<<<< HEAD

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token'))
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  const setAuth = (data) => {
    token.value = data.access_token
    user.value = data.user
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
=======
import api from '../services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(sessionStorage.getItem('token') || null)
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (email, password) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    
    const response = await api.post('/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    token.value = response.data.access_token
    sessionStorage.setItem('token', token.value)
    
    await fetchUser()
    
    return response.data
  }

  const register = async (userData) => {
    const response = await api.post('/register', userData)
    return response.data
>>>>>>> 694dc7c (the_last_update)
  }

  const logout = () => {
    token.value = null
    user.value = null
<<<<<<< HEAD
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isAuthenticated, isAdmin, setAuth, logout }
})
=======
    sessionStorage.removeItem('token')
  }

  const fetchUser = async () => {
    try {
      const response = await api.get('/me')
      user.value = response.data
      return response.data
    } catch (error) {
      if (error.response?.status === 401) {
        logout()
      }
      throw error
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser
  }
})


>>>>>>> 694dc7c (the_last_update)
