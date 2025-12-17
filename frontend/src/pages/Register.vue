<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <div class="glass-card p-10">
        <h1 class="text-4xl font-semibold text-center text-gray-900 mb-2 tracking-tight">JIHC Clubs</h1>
        <h2 class="text-xl text-center text-gray-700 mb-8 font-medium">Register</h2>
        
        <div v-if="error" class="backdrop-blur-[20px] bg-red-500/20 rounded-2xl p-4 mb-6 border border-red-400/30">
          <p class="text-red-900 font-medium">{{ error }}</p>
        </div>
        <div v-if="success" class="backdrop-blur-[20px] bg-green-500/20 rounded-2xl p-4 mb-6 border border-green-400/30">
          <p class="text-green-900 font-medium">{{ success }}</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Full Name</label>
            <input
              type="text"
              v-model="fullName"
              required
              autocomplete="name"
              placeholder="Enter your full name"
              class="glass-input w-full"
            />
          </div>
          
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
            <label class="block text-sm font-semibold text-gray-800 mb-2">Group</label>
            <input
              type="text"
              v-model="group"
              required
              autocomplete="organization"
              placeholder="Example: 1F1"
              class="glass-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Role</label>
            <select v-model="role" required class="glass-input w-full">
              <option value="student">Student</option>
              <option value="admin">Administrator</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Password</label>
            <input
              type="password"
              v-model="password"
              required
              autocomplete="new-password"
              placeholder="Enter password"
              minlength="6"
              class="glass-input w-full"
            />
          </div>
          
          <button type="submit" class="glass-btn glass-btn-primary w-full" :disabled="loading">
            {{ loading ? 'Please wait...' : 'Register' }}
          </button>
        </form>
        
        <p class="mt-8 text-center text-gray-700 text-sm">
          Already registered? 
          <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-semibold">
            Login
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const fullName = ref('')
    const email = ref('')
    const group = ref('')
    const role = ref('student')
    const password = ref('')
    const error = ref('')
    const success = ref('')
    const loading = ref(false)
    
    const handleRegister = async () => {
      error.value = ''
      success.value = ''
      loading.value = true
      
      try {
        await authStore.register({
          full_name: fullName.value,
          email: email.value,
          group: group.value,
          role: role.value,
          password: password.value
        })
        
        success.value = 'Registration successful! Redirecting to login page...'
        setTimeout(() => {
          router.push('/login')
        }, 1500)
      } catch (err) {
        error.value = err.response?.data?.detail || 'An error occurred during registration'
      } finally {
        loading.value = false
      }
    }
    
    return {
      fullName,
      email,
      group,
      role,
      password,
      error,
      success,
      loading,
      handleRegister
    }
  }
}
</script>

