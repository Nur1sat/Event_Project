<template>
  <div class="min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-3 border-blue-500/30 border-t-blue-500"></div>
        <p class="mt-4 text-gray-700 font-medium">Жүктелуде...</p>
      </div>
      <div v-else-if="event" class="glass-card overflow-hidden">
        <!-- Event Image -->
        <div v-if="event.image_url" class="w-full h-64 md:h-96 overflow-hidden">
          <img
            :src="event.image_url"
            :alt="event.title"
            class="w-full h-full object-cover"
          />
        </div>
        <div v-else class="w-full h-64 md:h-96 bg-gradient-to-br from-blue-100/50 to-purple-100/50 flex items-center justify-center">
          <svg class="w-24 h-24 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        
        <!-- Event Content -->
        <div class="p-8 lg:p-10">
          <!-- Status Badges at the top -->
          <div class="flex flex-wrap gap-2 mb-6">
            <span
              v-if="getEventStatus(event) === 'upcoming'"
              class="px-4 py-2 text-sm font-semibold rounded-full bg-blue-500/20 text-blue-700 border border-blue-400/40"
            >
              Алдағы
            </span>
            <span
              v-else-if="getEventStatus(event) === 'finished'"
              class="px-4 py-2 text-sm font-semibold rounded-full bg-gray-500/20 text-gray-700 border border-gray-400/40"
            >
              Аяқталған
            </span>
            <span
              v-if="isRegistered"
              class="px-4 py-2 text-sm font-semibold rounded-full bg-green-500/20 text-green-700 border border-green-400/40"
            >
              Тіркелген
            </span>
          </div>
          
          <h1 class="text-4xl font-semibold text-gray-900 mb-6 tracking-tight">{{ event.title }}</h1>
          <p class="text-lg text-gray-800 mb-6 whitespace-pre-line">{{ event.description }}</p>
          <div class="space-y-4">
            <p><strong>Күні:</strong> {{ formatDate(event.date) }}</p>
            <p><strong>Уақыты:</strong> {{ formatTime(event.start_time) }}</p>
            <p><strong>Орын:</strong> {{ event.location }}</p>
          </div>
          <button
            v-if="!isRegistered && getEventStatus(event) === 'upcoming'"
            @click="handleRegister"
            class="glass-btn glass-btn-primary mt-6"
            :disabled="registering"
          >
            {{ registering ? 'Күте тұрыңыз...' : 'Тіркелу' }}
          </button>
          <p v-else-if="isRegistered" class="mt-6 text-green-600 font-semibold">Сіз бұл іс-шараға тіркелгенсіз</p>
          <p v-else-if="getEventStatus(event) === 'finished'" class="mt-6 text-gray-600 font-semibold">Бұл іс-шара аяқталған</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../services/api'

export default {
  name: 'EventDetails',
  setup() {
    const route = useRoute()
    const event = ref(null)
    const isRegistered = ref(false)
    const loading = ref(true)
    const registering = ref(false)
    
    const fetchEvent = async () => {
      try {
        const response = await api.get(`/events/${route.params.id}`)
        event.value = response.data
        
        // Check if user is registered
        try {
          const regResponse = await api.get(`/events/${route.params.id}/is-registered`)
          isRegistered.value = regResponse.data.is_registered
        } catch (error) {
          // User might not be authenticated
          isRegistered.value = false
        }
      } catch (error) {
        console.error('Failed to fetch event:', error)
      } finally {
        loading.value = false
      }
    }
    
    const getEventStatus = (event) => {
      if (!event) return 'upcoming'
      const eventDate = new Date(event.date)
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      eventDate.setHours(0, 0, 0, 0)
      
      if (eventDate < today) {
        return 'finished'
      } else {
        return 'upcoming'
      }
    }
    
    const handleRegister = async () => {
      try {
        registering.value = true
        await api.post(`/events/${route.params.id}/register`)
        isRegistered.value = true
      } catch (error) {
        alert(error.response?.data?.detail || 'Тіркелу кезінде қате пайда болды')
      } finally {
        registering.value = false
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US')
    }
    
    const formatTime = (timeString) => {
      return timeString.substring(0, 5)
    }
    
    onMounted(() => {
      fetchEvent()
    })
    
    return {
      event,
      isRegistered,
      loading,
      registering,
      handleRegister,
      formatDate,
      formatTime,
      getEventStatus
    }
  }
}
</script>

