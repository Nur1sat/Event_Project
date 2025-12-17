<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-8">
    <div class="w-full max-w-md">
      <div class="glass-card p-10">
        <h1 class="text-4xl font-semibold text-center text-gray-900 mb-2 tracking-tight">JIHC Клубтар</h1>
        <h2 class="text-xl text-center text-gray-700 mb-8 font-medium">Администратор тіркелу</h2>
        
        <div v-if="error" class="backdrop-blur-[20px] bg-red-500/20 rounded-2xl p-4 mb-6 border border-red-400/30">
          <p class="text-red-900 font-medium">{{ error }}</p>
        </div>
        <div v-if="success" class="backdrop-blur-[20px] bg-green-500/20 rounded-2xl p-4 mb-6 border border-green-400/30">
          <p class="text-green-900 font-medium">{{ success }}</p>
        </div>
        
        <form @submit.prevent="handleRegister" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Аты-жөні</label>
            <input
              type="text"
              v-model="fullName"
              required
              autocomplete="name"
              placeholder="Аты-жөніңізді енгізіңіз"
              class="glass-input w-full"
            />
          </div>
          
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
            <label class="block text-sm font-semibold text-gray-800 mb-2">Топ</label>
            <input
              type="text"
              v-model="group"
              autocomplete="organization"
              placeholder="Мысалы: 1F1"
              class="glass-input w-full"
            />
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Құпия код</label>
            <input
              type="text"
              v-model="secretCode"
              required
              autocomplete="off"
              placeholder="6-цифрлық құпия код"
              class="glass-input w-full"
            />
            <p class="text-xs text-gray-600 mt-1">Құпия код: 111111</p>
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Құпия сөз</label>
            <input
              type="password"
              v-model="password"
              required
              autocomplete="new-password"
              placeholder="Құпия сөзді енгізіңіз"
              minlength="6"
              class="glass-input w-full"
            />
          </div>
          
          <button type="submit" class="glass-btn glass-btn-primary w-full" :disabled="loading">
            {{ loading ? 'Күте тұрыңыз...' : 'Тіркелу' }}
          </button>
        </form>
        
        <p class="mt-8 text-center text-gray-700 text-sm">
          Тіркелгенсіз бе? 
          <router-link to="/admin/login" class="text-blue-600 hover:text-blue-700 font-semibold">
            Кіру
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
import api from '../services/api'

export default {
  name: 'AdminRegister',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const fullName = ref('')
    const email = ref('')
    const group = ref('')
    const secretCode = ref('')
    const password = ref('')
    const error = ref('')
    const success = ref('')
    const loading = ref(false)
    
    const handleRegister = async () => {
      error.value = ''
      success.value = ''
      loading.value = true
      
      try {
        await api.post('/register', {
          full_name: fullName.value,
          email: email.value,
          group: group.value,
          role: 'admin',
          secret_code: secretCode.value,
          password: password.value
        })
        
        success.value = 'Тіркелу сәтті аяқталды! Кіру бетіне бағытталуда...'
        setTimeout(() => {
          router.push('/admin/login')
        }, 1500)
      } catch (err) {
        error.value = err.response?.data?.detail || 'Тіркелу кезінде қате пайда болды'
      } finally {
        loading.value = false
      }
    }
    
    return {
      fullName,
      email,
      group,
      secretCode,
      password,
      error,
      success,
      loading,
      handleRegister
    }
  }
}
</script>

