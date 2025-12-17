<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <div class="glass-card p-10">
        <h1 class="text-4xl font-semibold text-center text-gray-900 mb-2 tracking-tight">JIHC Клубтар</h1>
        <h2 class="text-xl text-center text-gray-700 mb-8 font-medium">Администратор кіру</h2>
        
        <div v-if="error" class="backdrop-blur-[20px] bg-red-500/20 rounded-2xl p-4 mb-6 border border-red-400/30">
          <p class="text-red-900 font-medium">{{ error }}</p>
        </div>
        
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Электрондық пошта</label>
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
            <label class="block text-sm font-semibold text-gray-800 mb-2">Құпия сөз</label>
            <input
              type="password"
              v-model="password"
              required
              autocomplete="current-password"
              placeholder="Құпия сөзіңізді енгізіңіз"
              class="glass-input w-full"
            />
          </div>
          
          <button type="submit" class="glass-btn glass-btn-primary w-full" :disabled="loading">
            {{ loading ? 'Күте тұрыңыз...' : 'Кіру' }}
          </button>
        </form>
        
        <div class="mt-8 text-center space-y-3">
          <p class="text-gray-700 text-sm">
            Тіркелмегенсіз бе? 
            <router-link to="/admin/register" class="text-blue-600 hover:text-blue-700 font-semibold">
              Администратор тіркелу
            </router-link>
          </p>
          <p class="text-gray-700 text-sm">
            Студентсіз бе? 
            <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-semibold">
              Студент кіру
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
  name: 'AdminLogin',
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
        
        // Check user role after login
        if (authStore.user?.role !== 'admin') {
          error.value = 'Бұл аккаунт администратор емес. Студент кіру бетін пайдаланыңыз.'
          authStore.logout()
          return
        }
        
        router.push('/admin')
      } catch (err) {
        error.value = err.response?.data?.detail || err.message || 'Кіру кезінде қате пайда болды'
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

