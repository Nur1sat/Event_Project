<template>
    <div class="home-page">
      <!-- Hero Section with Liquid Ether Background -->
      <div class="relative min-h-screen overflow-hidden bg-white">
        <!-- Liquid Ether Background with fallback -->
        <div class="absolute inset-0 w-full h-full" style="z-index: 1; pointer-events: auto;">
          <component
            v-if="showAnimation && LiquidEtherComponent"
            :is="LiquidEtherComponent"
            :colors="['#0066FF', '#00D4FF', '#80B8FF']"
            :mouseForce="35"
            :cursorSize="150"
            :isViscous="false"
            :viscous="30"
            :iterationsViscous="32"
            :iterationsPoisson="32"
            :resolution="0.5"
            :isBounce="false"
            :autoDemo="false"
            :autoSpeed="0.5"
            :autoIntensity="2.2"
            :takeoverDuration="0.25"
            :autoResumeDelay="3000"
            :autoRampDuration="0.6"
            :style="{ width: '100%', height: '100%', position: 'absolute', top: 0, left: 0, pointerEvents: 'auto' }"
            className="w-full h-full"
          />
          <div v-else class="absolute inset-0 w-full h-full bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 animate-pulse"></div>
        </div>
        
        <!-- Hero Content - Text Overlay -->
        <div class="relative min-h-screen flex items-center justify-center pt-24" style="z-index: 10; position: relative; pointer-events: none;">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full" style="position: relative; z-index: 11; pointer-events: none;">
            <div class="max-w-3xl mx-auto text-center">
              <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold text-black mb-6 leading-tight drop-shadow-lg" style="position: relative; z-index: 12; pointer-events: none;">
                Welcome to JIHC Clubs
              </h1>
              <p class="text-lg md:text-xl text-black mb-8 leading-relaxed drop-shadow-md" style="position: relative; z-index: 12; pointer-events: none;">
                Easily manage your campus life. Browse upcoming events, check the academic calendar, or make a room booking request.
              </p>
              <div class="flex flex-wrap gap-4 justify-center" style="position: relative; z-index: 12; pointer-events: auto;">
                <router-link to="/events" class="glass-btn glass-btn-primary text-lg px-8 py-4">
                  View Events
                </router-link>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Smooth Transition Overlay - Subtle fade -->
        <div class="absolute bottom-0 left-0 right-0 h-40 bg-gradient-to-b from-transparent via-white/30 to-white" style="z-index: 20; pointer-events: none;"></div>
      </div>
  
      <!-- Campus Events CTA Section -->
      <div class="relative bg-white py-20 md:py-32 overflow-hidden">
        <!-- Left Metallic Shape -->
        <div class="absolute left-0 top-0 bottom-0 w-1/3 md:w-1/4 opacity-40 pointer-events-none">
          <svg viewBox="0 0 500 1000" class="w-full h-full" preserveAspectRatio="xMinYMin meet">
            <defs>
              <linearGradient id="homeMetallicGradientLeft" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.9" />
                <stop offset="30%" style="stop-color:#d1d5db;stop-opacity:0.7" />
                <stop offset="60%" style="stop-color:#9ca3af;stop-opacity:0.6" />
                <stop offset="100%" style="stop-color:#6b7280;stop-opacity:0.4" />
              </linearGradient>
              <filter id="homeBlurLeft">
                <feGaussianBlur in="SourceGraphic" stdDeviation="3"/>
              </filter>
            </defs>
            <!-- Main fluid shape -->
            <path d="M0,80 C50,120 80,200 100,300 C120,400 90,500 120,600 C150,700 100,800 150,900 C180,950 200,1000 250,1000" 
                  fill="url(#homeMetallicGradientLeft)" 
                  filter="url(#homeBlurLeft)"
                  opacity="0.5"/>
            <!-- Secondary shape -->
            <path d="M30,0 C100,50 120,150 140,280 C160,400 130,520 160,650 C190,750 150,850 200,950" 
                  fill="url(#homeMetallicGradientLeft)" 
                  opacity="0.3"/>
          </svg>
        </div>
        
        <!-- Right Metallic Shape -->
        <div class="absolute right-0 top-0 bottom-0 w-1/3 md:w-1/4 opacity-40 pointer-events-none">
          <svg viewBox="0 0 500 1000" class="w-full h-full" preserveAspectRatio="xMaxYMin meet">
            <defs>
              <linearGradient id="homeMetallicGradientRight" x1="100%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.9" />
                <stop offset="30%" style="stop-color:#d1d5db;stop-opacity:0.7" />
                <stop offset="60%" style="stop-color:#9ca3af;stop-opacity:0.6" />
                <stop offset="100%" style="stop-color:#6b7280;stop-opacity:0.4" />
              </linearGradient>
              <filter id="homeBlurRight">
                <feGaussianBlur in="SourceGraphic" stdDeviation="3"/>
              </filter>
            </defs>
            <!-- Main fluid shape with hook -->
            <path d="M500,100 C450,150 420,250 400,350 C380,450 410,550 380,650 C350,750 400,850 350,950 C320,1000 300,1000 250,1000" 
                  fill="url(#homeMetallicGradientRight)" 
                  filter="url(#homeBlurRight)"
                  opacity="0.5"/>
            <!-- Secondary hook shape -->
            <path d="M470,0 C400,80 380,200 360,320 C340,450 370,570 340,700 C310,800 350,900 300,1000" 
                  fill="url(#homeMetallicGradientRight)" 
                  opacity="0.3"/>
          </svg>
        </div>
        
        <!-- Content -->
        <div class="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 class="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            Don't Miss What's Happening on Campus
          </h2>
          <p class="text-lg md:text-xl text-gray-700 mb-4 leading-relaxed max-w-2xl mx-auto">
            Stay updated on upcoming events, meetups, and student activities.
          </p>
          <p class="text-lg md:text-xl text-gray-700 mb-10 leading-relaxed max-w-2xl mx-auto">
            Choose an event, join in, and make memories.
          </p>
          <router-link to="/calendar" class="inline-flex items-center gap-2 glass-btn glass-btn-primary text-lg px-8 py-4">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            Calendar
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </router-link>
        </div>
      </div>
  
      <!-- Upcoming Events Preview -->
      <div v-if="upcomingEvents.length > 0" class="bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/20 py-16 relative z-10">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-12 text-center">Upcoming Events</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="event in upcomingEvents.slice(0, 6)"
              :key="event.id"
              class="glass-card overflow-hidden cursor-pointer transition-glass hover:scale-105 hover:shadow-lg"
              @click="openEventModal(event)"
            >
              <!-- Event Image -->
              <div class="w-full h-48 overflow-hidden bg-gray-50">
                <div v-if="event.image_url" class="w-full h-full">
                  <img
                    :src="event.image_url"
                    :alt="event.title"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div v-else class="w-full h-full bg-gradient-to-br from-blue-100/50 to-purple-100/50 flex items-center justify-center">
                  <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              </div>
              
              <!-- Event Content -->
              <div class="p-4">
                <!-- Status Badge -->
                <div class="mb-2">
                  <span class="px-2 py-1 text-xs font-semibold rounded-full bg-blue-500/20 text-blue-700 border border-blue-400/40">
                    Upcoming
                  </span>
                </div>
                
                <!-- Title -->
                <h3 class="text-lg font-semibold text-gray-900 mb-3 line-clamp-2">{{ event.title }}</h3>
                
                <!-- Description -->
                <p v-if="event.description" class="text-sm text-gray-600 mb-4 line-clamp-2">
                  {{ event.description }}
                </p>
                
                <!-- Event Details -->
                <div class="space-y-2">
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{{ formatDate(event.date) }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{{ formatTime(event.start_time) }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span class="truncate">{{ event.location }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="text-center mt-8">
            <router-link to="/events" class="glass-btn glass-btn-primary text-lg px-8 py-4">
              View All Events
            </router-link>
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
              Upcoming
            </span>
            <span
              v-else-if="getEventStatus(selectedEvent) === 'finished'"
              class="px-3 py-1 text-xs font-semibold rounded-full bg-gray-500/20 text-gray-700 border border-gray-400/40"
            >
              Finished
            </span>
            <span
              v-if="eventRegistrations[selectedEvent.id]"
              class="px-3 py-1 text-xs font-semibold rounded-full bg-green-500/20 text-green-700 border border-green-400/40 ml-2"
            >
              Registered
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
          <div v-if="isAuthenticated && authStore.user?.role !== 'admin'" class="flex gap-3 mt-4">
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
  import { ref, computed, onMounted, onErrorCaptured, shallowRef } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '../stores/auth'
  import api from '../services/api'
  
  export default {
    name: 'Home',
    components: {},
    setup() {
      const router = useRouter()
      const authStore = useAuthStore()
      const events = ref([])
      const loading = ref(true)
      const selectedEvent = ref(null)
      const registering = ref(false)
      const eventRegistrations = ref({})
      const showAnimation = ref(true)
      const LiquidEtherComponent = shallowRef(null)
      
      // Catch any errors from child components (like LiquidEther)
      onErrorCaptured((err, instance, info) => {
        console.error('Component error caught:', err, info)
        showAnimation.value = false
        return false // Prevent error from propagating - page must always work
      })
      
      // Load LiquidEther component
      onMounted(async () => {
        fetchEvents()
        
        // Try to load LiquidEther with multiple strategies
        try {
          // Strategy 1: Direct import
          const module = await import('../components/LiquidEther.vue')
          LiquidEtherComponent.value = module.default || module
          console.log('✅ LiquidEther loaded successfully')
        } catch (error1) {
          console.warn('Direct import failed, trying alternative:', error1)
          try {
            // Strategy 2: Import with explicit .vue extension
            const module = await import('../components/LiquidEther.vue?raw')
            // This won't work for components, but let's try
            showAnimation.value = false
          } catch (error2) {
            console.warn('All import strategies failed, using fallback:', error2)
            showAnimation.value = false
          }
        }
      })
      
      const isAuthenticated = computed(() => authStore.isAuthenticated)
      
      const stats = computed(() => {
        const totalEvents = events.value.length
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        
        const upcoming = events.value.filter(event => {
          const eventDate = new Date(event.date)
          eventDate.setHours(0, 0, 0, 0)
          return eventDate >= today
        }).length
        
        // Calculate total participants (simplified - count registrations)
        const totalParticipants = events.value.reduce((sum, event) => {
          return sum + (event.max_participants || 0)
        }, 0)
        
        return {
          totalEvents,
          upcomingEvents: upcoming,
          totalParticipants
        }
      })
      
      const upcomingEvents = computed(() => {
        const today = new Date()
        today.setHours(0, 0, 0, 0)
        
        return events.value
          .filter(event => {
            const eventDate = new Date(event.date)
            eventDate.setHours(0, 0, 0, 0)
            return eventDate >= today
          })
          .sort((a, b) => new Date(a.date) - new Date(b.date))
      })
      
      const fetchEvents = async () => {
        try {
          const response = await api.get('/events')
          events.value = response.data || []
          
          // Check registrations for each event if user is authenticated
          if (authStore.isAuthenticated) {
            await checkRegistrations()
          }
        } catch (error) {
          console.error('Failed to fetch events:', error)
          events.value = [] // Ensure events is always an array
        } finally {
          loading.value = false
        }
      }
      
      const checkRegistrations = async () => {
        for (const event of events.value) {
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
      
      const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US')
      }
      
      const formatTime = (timeString) => {
        return timeString.substring(0, 5)
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
      
      
      return {
        events,
        loading,
        stats,
        upcomingEvents,
        isAuthenticated,
        formatDate,
        formatTime,
        getEventStatus,
        openEventModal,
        closeEventModal,
        selectedEvent,
        handleRegister,
        registering,
        eventRegistrations,
        authStore,
        showAnimation,
        LiquidEtherComponent
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