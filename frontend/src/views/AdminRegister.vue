<template>
  <div class="auth-page">
    <div class="auth-card">
      <h1>JIHC Clubs</h1>
      <h2>Admin Registration</h2>
      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Full Name</label>
          <input type="text" v-model="fullName" required />
        </div>
        <div class="form-group">
          <label>Email</label>
          <input type="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required minlength="6" />
        </div>
        <div class="form-group">
          <label>Secret Key</label>
          <input type="password" v-model="secretKey" required placeholder="Enter admin secret key" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading" style="width:100%">
          {{ loading ? 'Loading...' : 'Register as Admin' }}
        </button>
      </form>
      <p style="margin-top:16px;text-align:center">
        Already have admin account? <router-link to="/admin/login">Login</router-link>
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

const fullName = ref('')
const email = ref('')
const password = ref('')
const secretKey = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    const { data } = await api.post('/auth/admin/register', {
      full_name: fullName.value,
      email: email.value,
      password: password.value,
      secret_key: secretKey.value
    })
    authStore.setAuth(data)
    router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Registration failed'
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

