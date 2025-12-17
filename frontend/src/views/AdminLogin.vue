<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>JIHC Clubs</h1>
      <h2>Admin Login</h2>
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading" style="width:100%">
          {{ loading ? 'Loading...' : 'Login as Admin' }}
        </button>
      </form>
      <p style="margin-top:16px;text-align:center">
        Need admin account? <router-link to="/admin/register">Register as Admin</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const { data } = await api.post('/auth/login', {
      email: email.value,
      password: password.value
    })
    if (data.user.role !== 'admin') {
      error.value = 'This account is not an admin'
      return
    }
    authStore.setAuth(data)
    router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1e293b;
}
.auth-card {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.3);
  width: 100%;
  max-width: 400px;
}
.auth-card h1 {
  text-align: center;
  color: #dc2626;
  margin-bottom: 8px;
}
.auth-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #374151;
}
</style>

