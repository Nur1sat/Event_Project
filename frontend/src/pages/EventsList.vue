<template>
  <div class="min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-semibold text-gray-900 mb-8 tracking-tight">All Events</h1>
      
      <!-- Search Input -->
      <div class="mb-8">
        <div class="relative max-w-md">
          <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <input
            v-model="searchQuery"
            type="text"
            class="glass-input w-full pl-12 pr-4 py-3"
            placeholder="Search by event name..."
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-3 border-blue-500/30 border-t-blue-500"></div>
        <p class="mt-4 text-gray-700 font-medium">Loading...</p>
      </div>
      <div v-else-if="allEvents.length === 0" class="text-center py-16">
        <div class="glass-card p-12 max-w-md mx-auto">
          <h3 class="text-2xl font-semibold text-gray-900 mb-3">No events found</h3>
          <p class="text-gray-700">There are no upcoming events at the moment</p>
        </div>
      </div>
      <div v-else-if="filteredEvents.length === 0" class="text-center py-16">
        <div class="glass-card p-12 max-w-md mx-auto">
          <h3 class="text-2xl font-semibold text-gray-900 mb-3">No events found</h3>
          <p class="text-gray-700">No events found for "{{ searchQuery }}"</p>
          <button
            @click="searchQuery = ''"
            class="glass-btn glass-btn-primary mt-4"
          >
            Show all events
          </button>
        </div>
      </div>
      <div v-else class="grid grid-cols-1 gap-4">
        <div
          v-for="event in filteredEvents"
          :key="event.id"
          class="glass-card overflow-hidden cursor-pointer transition-glass relative flex flex-row items-center"
          @click="openEventModal(event)"
        >
          <!-- Event Image - Very Small Square -->
          <div class="w-24 h-24 flex-shrink-0 overflow-hidden rounded-lg">
            <div v-if="event.image_url" class="w-full h-full">
              <img
                :src="event.image_url"
                :alt="event.title"
                class="w-full h-full object-contain bg-gray-50"
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
            <!-- Status Badges and Title Row -->
            <div class="flex items-start justify-between gap-2 mb-1.5">
              <h2 class="text-base font-semibold text-gray-900 truncate flex-1">{{ event.title }}</h2>
              <div class="flex gap-1.5 flex-shrink-0">
                <span
                  v-if="getEventStatus(event) === 'upcoming'"
                  class="px-1.5 py-0.5 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-700 border border-blue-400/40"
                >
                  Upcoming
                </span>
                <span
                  v-else-if="getEventStatus(event) === 'finished'"
                  class="px-1.5 py-0.5 text-xs font-semibold rounded-full bg-gray-500/20 text-gray-700 border border-gray-400/40"
                >
                  Finished
                </span>
                <span
                  v-if="eventRegistrations[event.id]"
                  class="px-1.5 py-0.5 text-xs font-semibold rounded-full bg-green-500/20 text-green-700 border border-green-400/40"
                >
                  Registered
                </span>
              </div>
            </div>
            
            <!-- Event Details (Compact) -->
            <div class="text-xs text-gray-600 space-y-1">
              <div class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span class="truncate">{{ formatDate(event.date) }}</span>
              </div>
              <div class="flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ formatTime(event.start_time) }}</span>
              </div>
              <div class="flex items-center gap-1.5">
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

    <!-- Event Modal -->
    <div v-if="selectedEvent" class="fixed inset-0 z-50 flex items-center justify-center p-4 glass-overlay" @click.self="closeEventModal">
      <div class="glass-modal max-w-md w-full p-5 max-h-[85vh] overflow-y-auto scrollbar-glass">
        <!-- Close Button -->
        <button @click="closeEventModal" class="absolute top-4 right-4 text-gray-500 hover:text-gray-700 text-2xl">
          ×
        </button>

        <!-- Event Image -->
        <div v-if="selectedEvent.image_url" class="w-full h-40 mb-3 rounded-lg overflow-hidden">
          <img
            :src="selectedEvent.image_url"
            :alt="selectedEvent.title"
            class="w-full h-full object-cover"
          />
        </div>
        <div v-else class="w-full h-40 mb-3 bg-gradient-to-br from-blue-100/50 to-purple-100/50 rounded-lg flex items-center justify-center">
          <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>

        <!-- Status Badge -->
        <div class="mb-3">
          <span
            v-if="getEventStatus(selectedEvent) === 'upcoming'"
            class="px-3 py-1 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-700 border border-blue-400/40"
          >
            Алдағы
          </span>
          <span
            v-else-if="getEventStatus(selectedEvent) === 'finished'"
            class="px-3 py-1 text-xs font-semibold rounded-full bg-gray-500/20 text-gray-700 border border-gray-400/40"
          >
            Аяқталған
          </span>
          <span
            v-if="eventRegistrations[selectedEvent.id]"
            class="px-3 py-1 text-xs font-semibold rounded-full bg-green-500/20 text-green-700 border border-green-400/40 ml-2"
          >
            Тіркелген
          </span>
        </div>

        <!-- Title -->
        <h2 class="text-xl font-semibold text-gray-900 mb-2">{{ selectedEvent.title }}</h2>

        <!-- Description -->
        <p v-if="selectedEvent.description" class="text-gray-700 mb-3 whitespace-pre-line text-sm line-clamp-4">
          {{ selectedEvent.description }}
        </p>

        <!-- Event Details -->
        <div class="text-sm text-gray-600 space-y-2 mb-4">
          <div class="flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>{{ formatDate(selectedEvent.date) }}</span>
          </div>
          <div class="flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ formatTime(selectedEvent.start_time) }}</span>
          </div>
          <div class="flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span>{{ selectedEvent.location }}</span>
          </div>
          <div v-if="selectedEvent.max_participants" class="flex items-center gap-2">
            <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>Max participants: {{ selectedEvent.max_participants }}</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div v-if="authStore.isAuthenticated && authStore.user?.role !== 'admin'" class="flex gap-3 mt-4">
          <button
            v-if="!eventRegistrations[selectedEvent.id] && getEventStatus(selectedEvent) === 'upcoming'"
            @click="handleRegister"
            class="flex-1 glass-btn glass-btn-primary"
            :disabled="registering"
          >
            {{ registering ? 'Please wait...' : 'Register' }}
          </button>
          <p v-else-if="eventRegistrations[selectedEvent.id]" class="text-green-600 font-semibold text-sm">
            You are registered for this event
          </p>
          <p v-else-if="getEventStatus(selectedEvent) === 'finished'" class="text-gray-600 font-semibold text-sm">
            This event has finished
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

export default {
  name: 'EventsList',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const allEvents = ref([])
    const loading = ref(true)
    const eventRegistrations = ref({})
    const searchQuery = ref('')
    const selectedEvent = ref(null)
    const registering = ref(false)
    
    const fetchEvents = async () => {
      try {
        const response = await api.get('/events')
        allEvents.value = response.data
        
        // Check registrations for each event if user is authenticated
        if (authStore.isAuthenticated) {
          await checkRegistrations()
        }
      } catch (error) {
        console.error('Failed to fetch events:', error)
      } finally {
        loading.value = false
      }
    }
    
    const checkRegistrations = async () => {
      for (const event of allEvents.value) {
        try {
          const response = await api.get(`/events/${event.id}/is-registered`)
          if (response.data.is_registered) {
            eventRegistrations.value[event.id] = true
          }
        } catch (error) {
          // User might not be authenticated or event doesn't exist
          console.error(`Failed to check registration for event ${event.id}:`, error)
        }
      }
    }
    
    // Filter events by search query
    const filteredEvents = computed(() => {
      if (!searchQuery.value.trim()) {
        return allEvents.value
      }
      
      const query = searchQuery.value.toLowerCase().trim()
      return allEvents.value.filter(event => 
        event.title.toLowerCase().includes(query)
      )
    })
    
    const getEventStatus = (event) => {
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
    
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US')
    }
    
    const formatTime = (timeString) => {
      return timeString.substring(0, 5)
    }
    
    const openEventModal = (event) => {
      selectedEvent.value = event
    }

    const closeEventModal = () => {
      selectedEvent.value = null
    }

    const handleRegister = async () => {
      if (!selectedEvent.value) return
      
      try {
        registering.value = true
        await api.post(`/events/${selectedEvent.value.id}/register`)
        eventRegistrations.value[selectedEvent.value.id] = true
      } catch (error) {
        alert(error.response?.data?.detail || 'An error occurred while registering')
      } finally {
        registering.value = false
      }
    }
    
    onMounted(() => {
      fetchEvents()
    })
    
    return {
      allEvents,
      loading,
      eventRegistrations,
      searchQuery,
      filteredEvents,
      formatDate,
      formatTime,
      openEventModal,
      closeEventModal,
      selectedEvent,
      handleRegister,
      registering,
      getEventStatus,
      authStore
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>

