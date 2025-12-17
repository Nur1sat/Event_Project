<template>
  <div :class="isEmbedded ? '' : 'min-h-screen py-8'">
    <div :class="isEmbedded ? '' : 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'">
      <h1 v-if="!isEmbedded" class="text-4xl font-semibold text-gray-900 mb-8 tracking-tight">My Events</h1>
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-3 border-blue-500/30 border-t-blue-500"></div>
        <p class="mt-4 text-gray-700 font-medium">Loading...</p>
      </div>
      <div v-else-if="events.length === 0" class="text-center py-16">
        <div class="glass-card p-12 max-w-md mx-auto">
          <h3 class="text-2xl font-semibold text-gray-900 mb-3">You are not registered for any events</h3>
          <router-link to="/events" class="glass-btn glass-btn-primary inline-block mt-4">View Events</router-link>
        </div>
      </div>
      <div v-else class="grid grid-cols-1 gap-4">
        <div
          v-for="event in events"
          :key="event.id"
          class="glass-card overflow-hidden cursor-pointer transition-glass relative flex flex-row items-center"
          @click="goToEvent(event.id)"
        >
          <!-- Event Image - Very Small Square -->
          <div class="w-24 h-24 flex-shrink-0 overflow-hidden rounded-lg flex items-center justify-center bg-gray-50">
            <div v-if="event.image_url" class="w-full h-full flex items-center justify-center">
              <img
                :src="event.image_url"
                :alt="event.title"
                class="max-w-full max-h-full object-contain"
              />
            </div>
            <div v-else class="w-full h-full bg-gradient-to-br from-blue-100/50 to-purple-100/50 flex items-center justify-center">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          
          <!-- Event Content -->
          <div class="flex-1 p-3 flex flex-col min-w-0">
            <!-- Title -->
            <h2 class="text-base font-semibold text-gray-900 truncate flex-1 mb-1.5">{{ event.title }}</h2>
            
            <!-- Description (if available) -->
            <p v-if="event.description" class="text-sm text-gray-700 mb-2 line-clamp-2">{{ event.description }}</p>
            
            <!-- Event Details (Compact) -->
            <div class="text-xs text-gray-600 space-y-1">
              <div class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="truncate">Date: {{ formatDate(event.date) }}</span>
              </div>
              <div class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>Time: {{ formatTime(event.start_time) }}</span>
              </div>
              <div v-if="event.location" class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="truncate">{{ event.location }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

export default {
  name: 'MyEvents',
  props: {
    isEmbedded: {
      type: Boolean,
      default: false
    }
  },
  setup() {
    const router = useRouter()
    const events = ref([])
    const loading = ref(true)
    
    const fetchMyEvents = async () => {
      try {
        const response = await api.get('/my-events')
        events.value = response.data
      } catch (error) {
        console.error('Failed to fetch my events:', error)
      } finally {
        loading.value = false
      }
    }
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US')
    }
    
    const formatTime = (timeString) => {
      return timeString.substring(0, 5)
    }
    
    const goToEvent = (eventId) => {
      router.push(`/events/${eventId}`)
    }
    
    onMounted(() => {
      fetchMyEvents()
    })
    
    return {
      events,
      loading,
      formatDate,
      formatTime,
      goToEvent
    }
  }
}
</script>

