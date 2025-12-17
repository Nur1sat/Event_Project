<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <div class="glass-card p-10">
        <h1 class="text-4xl font-semibold text-center text-gray-900 mb-2 tracking-tight">JIHC Clubs</h1>
        <h2 class="text-xl text-center text-gray-700 mb-8 font-medium">Login</h2>
        
        <div v-if="error" class="backdrop-blur-[20px] bg-red-500/20 rounded-2xl p-4 mb-6 border border-red-400/30">
          <p class="text-red-900 font-medium">{{ error }}</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Email</label>
            <input
              type="email"
              v-model="email"
              required
              autocomplete="email"
              placeholder="email@example.com"
              class="glass-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Password</label>
            <input
              type="password"
              v-model="password"
              required
              autocomplete="current-password"
              placeholder="Enter your password"
              class="glass-input w-full"
            />
          </div>
          
          <button type="submit" class="glass-btn glass-btn-primary w-full" :disabled="loading">
            {{ loading ? 'Please wait...' : 'Login' }}
          </button>
        </form>
        
        <div class="mt-8 text-center space-y-3">
            <p class="text-gray-700 text-sm">
            Not registered? 
            <router-link to="/register" class="text-blue-600 hover:text-blue-700 font-semibold">
              Register
            </router-link>
          </p>
            <p class="text-gray-700 text-sm">
            Are you an administrator? 
            <router-link to="/admin/login" class="text-blue-600 hover:text-blue-700 font-semibold">
              Admin Login
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const email = ref('')
    const password = ref('')
    const error = ref('')
    const loading = ref(false)
    
    const handleLogin = async () => {
      error.value = ''
      loading.value = true
      
      try {
        await authStore.login(email.value, password.value)
        router.push('/')
      } catch (err) {
        error.value = err.response?.data?.detail || 'An error occurred during login'
      } finally {
        loading.value = false
      }
    }
    
    return {
      email,
      password,
      error,
      loading,
      handleLogin
    }
  }
}
</script>

