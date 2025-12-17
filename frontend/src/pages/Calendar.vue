<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/20 py-4 sm:py-8">
    <div class="max-w-[1600px] mx-auto px-2 sm:px-4 lg:px-8">
      <!-- Calendar Header -->
      <div class="glass-card mb-4 sm:mb-6 p-3 sm:p-4">
        <div class="flex items-center justify-center gap-2 sm:gap-4">
          <button @click="previousMonth" class="nav-arrow" aria-label="Previous month">‹</button>
          <h2 class="month-year">{{ monthName }} {{ year }}</h2>
          <button @click="nextMonth" class="nav-arrow" aria-label="Next month">›</button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        <p class="mt-4 text-gray-600">Loading...</p>
      </div>

      <!-- Calendar Layout -->
      <div v-else class="calendar-layout">
        <!-- Left: Calendar -->
        <div class="calendar-wrapper">
          <div class="glass-card p-3 sm:p-4">
            <!-- Week Days Header -->
            <div class="weekdays-header">
              <div v-for="dayName in weekDayNames" :key="dayName" class="weekday-cell">
                {{ dayName }}
              </div>
            </div>

            <!-- Calendar Grid -->
            <div class="calendar-grid scrollbar-glass">
              <div
                v-for="day in calendarDays"
                :key="day.date"
                :class="[
                  'calendar-day',
                  {
                    'other-month': !day.isCurrentMonth,
                    'today': day.is_today,
                    'has-events': day.events && day.events.length > 0,
                    'selected': selectedEvent && day.events.some(e => e.id === selectedEvent.id)
                  }
                ]"
                @click="selectDay(day)"
              >
                <div class="day-number">{{ day.day }}</div>
                
                <!-- Events in day cell -->
                <div v-if="day.events && day.events.length > 0" class="events-in-cell">
                  <div
                    v-for="event in day.events.slice(0, 3)"
                    :key="event.id"
                    :class="['event-block', getEventColorClass(event.id)]"
                    @click.stop="selectEvent(event)"
                  >
                    <span class="event-text">{{ event.title }} {{ formatTime(event.start_time) }}</span>
                  </div>
                  <div v-if="day.events.length > 3" class="more-events">
                    +{{ day.events.length - 3 }} more
                  </div>
                </div>
                <!-- Debug: Show if events exist but not displaying -->
                <!-- <div v-if="day.events && day.events.length > 0" style="font-size: 10px; color: red;">
                  DEBUG: {{ day.events.length }} events
                </div> -->
              </div>
            </div>
          </div>
        </div>

        <!-- Right: Event Details Card -->
        <div v-if="selectedEvent" class="event-details-wrapper">
          <div class="event-details-card glass-card">
            <!-- Confirmation Banner -->
            <div v-if="isRegistered" class="confirmation-banner">
              <svg class="check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <span>Registered!</span>
            </div>

            <!-- User Info -->
            <div class="user-info">
              <div class="user-avatar">
                <img 
                  v-if="currentUser?.photo_url" 
                  :src="currentUser.photo_url" 
                  :alt="currentUser?.full_name"
                  class="avatar-img"
                />
                <div v-else class="avatar-placeholder">
                  {{ currentUser?.full_name?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
              </div>
              <div class="user-name">{{ currentUser?.full_name || 'User' }}</div>
            </div>

            <!-- Date and Time Pill -->
            <div class="date-time-pill">
              <div class="pill-item">
                <svg class="pill-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{{ formatEventDate(selectedEvent.date) }}</span>
              </div>
              <div class="pill-divider"></div>
              <div class="pill-item">
                <svg class="pill-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ formatTime(selectedEvent.start_time) }}</span>
              </div>
            </div>

            <!-- Event Details -->
            <div class="event-details-content">
              <h3 class="event-detail-title">{{ selectedEvent.title }}</h3>
              <p v-if="selectedEvent.description" class="event-detail-description">{{ selectedEvent.description }}</p>
              
              <div class="event-detail-meta">
                <div class="meta-item">
                  <svg class="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span>{{ selectedEvent.location }}</span>
                </div>
                <div class="meta-item">
                  <svg class="meta-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <span>{{ eventStats.current_registrations || 0 }} / {{ selectedEvent.max_participants }} people</span>
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <button
              v-if="!isRegistered && !eventStats.is_full"
              @click="handleRegister"
              :disabled="registering"
              class="register-btn glass-btn glass-btn-primary"
            >
              {{ registering ? 'Please wait...' : 'Register' }}
            </button>
            <button
              v-else-if="isRegistered"
              disabled
              class="register-btn glass-btn glass-btn-disabled"
            >
              Registered
            </button>
            <button
              v-else
              disabled
              class="register-btn glass-btn glass-btn-disabled"
            >
              Full
            </button>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="event-details-wrapper">
          <div class="event-details-card glass-card empty-state">
            <div class="empty-icon">
              <img src="/calendar-week.svg" alt="Calendar" class="calendar-icon-img" />
            </div>
            <p class="empty-text">Select an event</p>
            <p class="empty-subtext mb-6">Click on an event in the calendar to view details</p>
            <router-link 
              v-if="currentUser?.role !== 'admin'"
              to="/event-request" 
              class="glass-btn glass-btn-primary inline-block"
            >
              + New Event Request
            </router-link>
            <button 
              v-else
              @click="openEventModal"
              class="glass-btn glass-btn-primary inline-block"
            >
              + Add New Event
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Event Creation Modal for Admin -->
    <div v-if="showEventModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 glass-overlay" @click.self="closeEventModal">
      <div class="glass-modal max-w-2xl w-full p-8 max-h-[90vh] overflow-y-auto scrollbar-glass">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-semibold text-gray-900">Add New Event</h2>
          <button @click="closeEventModal" class="text-gray-500 hover:text-gray-700 text-2xl">×</button>
        </div>

        <form @submit.prevent="handleEventSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Title *</label>
            <input
              v-model="eventForm.title"
              type="text"
              required
              class="glass-input w-full"
              placeholder="Event title"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Description *</label>
            <textarea
              v-model="eventForm.description"
              required
              rows="5"
              class="glass-input w-full"
              placeholder="Enter full event description..."
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Date *</label>
              <input
                v-model="eventForm.date"
                type="date"
                required
                :min="minDate"
                class="glass-input w-full"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Start Time *</label>
              <input
                v-model="eventForm.start_time"
                type="time"
                required
                class="glass-input w-full"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Location *</label>
            <input
              v-model="eventForm.location"
              type="text"
              required
              class="glass-input w-full"
              placeholder="Event location"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Max Participants *</label>
            <input
              v-model.number="eventForm.max_participants"
              type="number"
              required
              min="1"
              class="glass-input w-full"
              placeholder="Number of participants"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Event Image</label>
            <div class="mb-3">
              <input
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="hidden"
                ref="imageInput"
                id="calendar-event-image-upload"
              />
              <label
                for="calendar-event-image-upload"
                class="glass-btn cursor-pointer inline-block text-center w-full py-3"
              >
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {{ eventForm.image_url ? 'Change Image' : 'Upload Image' }}
                </span>
              </label>
            </div>
            <div v-if="eventForm.image_url" class="mt-3">
              <img
                :src="eventForm.image_url"
                alt="Event preview"
                class="w-full h-48 object-cover rounded-xl border border-white/40"
              />
              <button
                type="button"
                @click="removeImage"
                class="mt-2 text-sm text-red-600 hover:text-red-700"
              >
                Remove Image
              </button>
            </div>
          </div>

          <div class="flex gap-3 pt-4">
            <button type="submit" class="flex-1 glass-btn glass-btn-primary" :disabled="submittingEvent">
              {{ submittingEvent ? 'Saving...' : 'Add' }}
            </button>
            <button type="button" @click="closeEventModal" class="flex-1 glass-btn">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

export default {
  name: 'Calendar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const calendarData = ref(null)
    const selectedEvent = ref(null)
    const loading = ref(true)
    const registering = ref(false)
    const eventStats = ref({})
    const isRegistered = ref(false)
    const showEventModal = ref(false)
    const submittingEvent = ref(false)
    const imageInput = ref(null)
    
    const eventForm = ref({
      title: '',
      description: '',
      date: '',
      start_time: '',
      location: '',
      max_participants: 1,
      image_url: ''
    })
    
    const minDate = computed(() => {
      const today = new Date()
      return today.toISOString().split('T')[0]
    })
    
    const now = new Date()
    const year = ref(now.getFullYear())
    const month = ref(now.getMonth() + 1)
    
    const weekDayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    const currentUser = computed(() => authStore.user)
    
    const monthName = computed(() => {
      if (calendarData.value) {
        // If backend returns Kazakh name, convert to English
        const monthMap = {
          'Қаңтар': 'January', 'Ақпан': 'February', 'Наурыз': 'March', 'Сәуір': 'April',
          'Мамыр': 'May', 'Маусым': 'June', 'Шілде': 'July', 'Тамыз': 'August',
          'Қыркүйек': 'September', 'Қазан': 'October', 'Қараша': 'November', 'Желтоқсан': 'December'
        }
        return monthMap[calendarData.value.month_name] || calendarData.value.month_name
      }
      const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ]
      return months[month.value - 1]
    })
    
    const calendarDays = computed(() => {
      if (!calendarData.value) return []
      
      const days = []
      const firstDay = new Date(year.value, month.value - 1, 1)
      const lastDay = new Date(year.value, month.value, 0)
      const firstDayOfWeek = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1 // Monday = 0
      
      // Helper function to format date as YYYY-MM-DD in local timezone
      const formatDateLocal = (year, month, day) => {
        const d = new Date(year, month - 1, day)
        const y = d.getFullYear()
        const m = String(d.getMonth() + 1).padStart(2, '0')
        const dayNum = String(d.getDate()).padStart(2, '0')
        return `${y}-${m}-${dayNum}`
      }
      
      // Add days from previous month
      const prevMonthLastDay = new Date(year.value, month.value - 1, 0).getDate()
      const prevMonth = month.value === 1 ? 12 : month.value - 1
      const prevYear = month.value === 1 ? year.value - 1 : year.value
      for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        const day = prevMonthLastDay - i
        const dateStr = formatDateLocal(prevYear, prevMonth, day)
        days.push({
          day: day,
          date: dateStr,
          isCurrentMonth: false,
          is_today: false,
          events: []
        })
      }
      
      // Get today's date in local timezone
      const today = new Date()
      const todayStr = formatDateLocal(today.getFullYear(), today.getMonth() + 1, today.getDate())
      
      // Add days from current month
      for (let day = 1; day <= lastDay.getDate(); day++) {
        const dateStr = formatDateLocal(year.value, month.value, day)
        const dayData = calendarData.value.days.find(d => d.date === dateStr)
        
        days.push({
          day: day,
          date: dateStr,
          isCurrentMonth: true,
          is_today: dateStr === todayStr,
          events: dayData ? dayData.events : []
        })
      }
      
      // Add days from next month to fill the grid
      const remainingDays = 42 - days.length // 6 weeks * 7 days
      const nextMonth = month.value === 12 ? 1 : month.value + 1
      const nextYear = month.value === 12 ? year.value + 1 : year.value
      for (let day = 1; day <= remainingDays; day++) {
        const dateStr = formatDateLocal(nextYear, nextMonth, day)
        days.push({
          day: day,
          date: dateStr,
          isCurrentMonth: false,
          is_today: false,
          events: []
        })
      }
      
      return days
    })
    
    const fetchCalendar = async () => {
      try {
        loading.value = true
        const response = await api.get(`/calendar?year=${year.value}&month=${month.value}`)
        calendarData.value = response.data
        
        // If we had a selected event, try to find it again
        if (selectedEvent.value) {
          const eventId = selectedEvent.value.id
          for (const day of calendarData.value.days) {
            const event = day.events.find(e => e.id === eventId)
            if (event) {
              selectedEvent.value = event
              await fetchEventDetails(event.id)
              break
            }
          }
        }
      } catch (error) {
        console.error('Failed to fetch calendar:', error)
      } finally {
        loading.value = false
      }
    }
    
    const fetchEventDetails = async (eventId) => {
      try {
        // Fetch event stats
        const statsResponse = await api.get(`/events/${eventId}/stats`)
        eventStats.value = statsResponse.data
        
        // Check if user is registered
        try {
          const regResponse = await api.get(`/events/${eventId}/is-registered`)
          isRegistered.value = regResponse.data.is_registered
        } catch (error) {
          isRegistered.value = false
        }
      } catch (error) {
        console.error('Failed to fetch event details:', error)
      }
    }
    
    const selectDay = (day) => {
      if (day.isCurrentMonth) {
        if (day.events && day.events.length > 0) {
          // Select first event if day has events
          selectEvent(day.events[0])
        } else {
          // Show empty state for days without events
          selectedEvent.value = null
        }
      }
    }
    
    const selectEvent = async (event) => {
      selectedEvent.value = event
      await fetchEventDetails(event.id)
    }
    
    const handleRegister = async () => {
      if (!selectedEvent.value) return
      
      try {
        registering.value = true
        await api.post(`/events/${selectedEvent.value.id}/register`)
        isRegistered.value = true
        await fetchEventDetails(selectedEvent.value.id)
      } catch (error) {
        console.error('Failed to register:', error)
        alert(error.response?.data?.detail || 'An error occurred while registering')
      } finally {
        registering.value = false
      }
    }
    
    const previousMonth = () => {
      if (month.value === 1) {
        month.value = 12
        year.value--
      } else {
        month.value--
      }
      selectedEvent.value = null
      fetchCalendar()
    }
    
    const nextMonth = () => {
      if (month.value === 12) {
        month.value = 1
        year.value++
      } else {
        month.value++
      }
      selectedEvent.value = null
      fetchCalendar()
    }
    
    const formatTime = (timeString) => {
      return timeString.substring(0, 5)
    }
    
    const formatEventDate = (dateStr) => {
      if (!dateStr) return ''
      // Parse date string (YYYY-MM-DD) directly to avoid timezone issues
      const [year, month, day] = dateStr.split('-').map(Number)
      const date = new Date(year, month - 1, day)
      const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
      const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
      ]
      return `${days[date.getDay()]}, ${date.getDate()} ${months[date.getMonth()]}`
    }
    
    const getEventColorClass = (eventId) => {
      const colors = ['color-blue', 'color-green', 'color-orange', 'color-purple', 'color-pink']
      return colors[eventId % colors.length]
    }
    
    const openEventModal = () => {
      eventForm.value = {
        title: '',
        description: '',
        date: '',
        start_time: '',
        location: '',
        max_participants: 1,
        image_url: ''
      }
      showEventModal.value = true
    }
    
    const closeEventModal = () => {
      showEventModal.value = false
      eventForm.value = {
        title: '',
        description: '',
        date: '',
        start_time: '',
        location: '',
        max_participants: 1,
        image_url: ''
      }
      if (imageInput.value) {
        imageInput.value.value = ''
      }
    }
    
    const handleEventSubmit = async () => {
      try {
        submittingEvent.value = true
        
        const formData = {
          ...eventForm.value,
          max_participants: parseInt(eventForm.value.max_participants),
          image_url: eventForm.value.image_url || null
        }
        
        await api.post('/events', formData)
        
        // Refresh calendar after creating event
        await fetchCalendar()
        closeEventModal()
        
        // Show success message
        alert('Іс-шара сәтті қосылды!')
      } catch (error) {
        console.error('Failed to create event:', error)
        const errorMessage = error.response?.data?.detail || error.message || 'An error occurred while adding the event'
        alert(errorMessage)
      } finally {
        submittingEvent.value = false
      }
    }
    
    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (!file) return
      
      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Тек сурет файлдарын жүктеуге болады')
        return
      }
      
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Суреттің өлшемі 10MB-тан аспауы керек')
        return
      }
      
      // Convert to base64
      const reader = new FileReader()
      reader.onload = (e) => {
        eventForm.value.image_url = e.target.result
      }
      reader.onerror = () => {
        alert('An error occurred while uploading the image')
      }
      reader.readAsDataURL(file)
    }
    
    const removeImage = () => {
      eventForm.value.image_url = ''
      if (imageInput.value) {
        imageInput.value.value = ''
      }
    }
    
    onMounted(async () => {
      await authStore.fetchUser()
      await fetchCalendar()
    })
    
    return {
      calendarData,
      selectedEvent,
      loading,
      registering,
      eventStats,
      isRegistered,
      currentUser,
      year,
      month,
      monthName,
      weekDayNames,
      calendarDays,
      selectDay,
      selectEvent,
      previousMonth,
      nextMonth,
      formatTime,
      formatEventDate,
      getEventColorClass,
      handleRegister,
      showEventModal,
      eventForm,
      submittingEvent,
      imageInput,
      minDate,
      openEventModal,
      closeEventModal,
      handleEventSubmit,
      handleImageUpload,
      removeImage
    }
  }
}
</script>

<style scoped>
.calendar-layout {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 1.5rem;
}

.calendar-wrapper {
  min-width: 0;
}

.month-year {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111;
  min-width: 200px;
  text-align: center;
}

.nav-arrow {
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.4);
  width: 44px;
  height: 44px;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-arrow:hover {
  background: rgba(255, 255, 255, 0.8);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.weekdays-header {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.4);
}

.weekday-cell {
  text-align: center;
  font-weight: 600;
  color: #666;
  font-size: 0.875rem;
  padding: 0.75rem;
  letter-spacing: 0.01em;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.calendar-day {
  min-height: 120px;
  backdrop-filter: blur(20px);
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  padding: 0.75rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.calendar-day:hover {
  background: rgba(255, 255, 255, 0.7);
  border-color: rgba(59, 130, 246, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.calendar-day.other-month {
  opacity: 0.35;
  background: rgba(255, 255, 255, 0.3);
}

.calendar-day.today {
  background: rgba(255, 251, 230, 0.7);
  border-color: rgba(251, 191, 36, 0.6);
  border-width: 2px;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.2);
}

.calendar-day.has-events {
  border-color: rgba(59, 130, 246, 0.5);
}

.calendar-day.selected {
  background: rgba(239, 246, 255, 0.8);
  border-color: rgba(59, 130, 246, 0.7);
  border-width: 2px;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
}

.day-number {
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.events-in-cell {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-top: 0.25rem;
}

.event-block {
  padding: 0.375rem 0.625rem;
  border-radius: 10px;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
}

.event-block:hover {
  transform: scale(1.03) translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.event-text {
  font-weight: 500;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
  line-height: 1.3;
}

.event-title {
  font-weight: 600;
  margin-bottom: 0.125rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-time {
  font-size: 0.7rem;
  opacity: 0.85;
  font-weight: 500;
}

  .event-block.color-blue {
  background: rgba(147, 197, 253, 0.6);
  color: #1e3a8a;
  border-color: rgba(59, 130, 246, 0.4);
  font-weight: 500;
}

.event-block.color-green {
  background: rgba(134, 239, 172, 0.6);
  color: #064e3b;
  border-color: rgba(16, 185, 129, 0.4);
  font-weight: 500;
}

.event-block.color-orange {
  background: rgba(254, 215, 170, 0.6);
  color: #7c2d12;
  border-color: rgba(249, 115, 22, 0.4);
  font-weight: 500;
}

.event-block.color-purple {
  background: rgba(196, 181, 253, 0.6);
  color: #5b21b6;
  border-color: rgba(168, 85, 247, 0.4);
  font-weight: 500;
}

.event-block.color-pink {
  background: rgba(251, 207, 232, 0.6);
  color: #831843;
  border-color: rgba(236, 72, 153, 0.4);
  font-weight: 500;
}

/* Mobile optimizations for event blocks */
@media (max-width: 768px) {
  .event-block.color-blue {
    background: rgba(147, 197, 253, 0.7);
    border-width: 1.5px;
  }
  
  .event-block.color-green {
    background: rgba(134, 239, 172, 0.7);
    border-width: 1.5px;
  }
  
  .event-block.color-orange {
    background: rgba(254, 215, 170, 0.7);
    border-width: 1.5px;
  }
  
  .event-block.color-purple {
    background: rgba(196, 181, 253, 0.7);
    border-width: 1.5px;
  }
  
  .event-block.color-pink {
    background: rgba(251, 207, 232, 0.7);
    border-width: 1.5px;
  }
}

.more-events {
  font-size: 0.7rem;
  color: #666;
  text-align: center;
  padding: 0.25rem;
  font-weight: 600;
}

.event-details-wrapper {
  position: sticky;
  top: 6rem;
  height: fit-content;
  max-height: calc(100vh - 8rem);
  overflow-y: auto;
}

.event-details-card {
  padding: 0;
  overflow: hidden;
}

.confirmation-banner {
  background: rgba(16, 185, 129, 0.2);
  border-bottom: 1px solid rgba(16, 185, 129, 0.3);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #065f46;
  font-weight: 600;
  font-size: 0.95rem;
}

.check-icon {
  width: 20px;
  height: 20px;
  color: #10b981;
}

.user-info {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

.user-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  background: rgba(59, 130, 246, 0.2);
}

.user-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #111;
}

.date-time-pill {
  margin: 1.5rem;
  padding: 0.875rem 1.25rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.pill-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #333;
  font-weight: 500;
  font-size: 0.9rem;
}

.pill-icon {
  width: 18px;
  height: 18px;
  color: #666;
}

.pill-divider {
  width: 1px;
  height: 20px;
  background: rgba(0, 0, 0, 0.1);
}

.event-details-content {
  padding: 0 1.5rem 1.5rem;
}

.event-detail-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111;
  margin-bottom: 0.75rem;
}

.event-detail-description {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.25rem;
}

.event-detail-meta {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
  font-size: 0.9rem;
}

.meta-icon {
  width: 18px;
  height: 18px;
  color: #999;
}

.register-btn {
  margin: 0 1.5rem 1.5rem;
  width: calc(100% - 3rem);
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.register-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.empty-state {
  padding: 3rem 2rem;
  text-align: center;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}
.calendar-icon-img {
  width: 100%;
  height: 100%;
  max-width: 150px;
  max-height: 150px;
  object-fit: contain;
}

.empty-text {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111;
  margin-bottom: 0.5rem;
}

.empty-subtext {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
}

@media (max-width: 1024px) {
  .calendar-layout {
    grid-template-columns: 1fr;
  }
  
  .event-details-wrapper {
    position: relative;
    top: 0;
    margin-top: 1.5rem;
  }
}

@media (max-width: 768px) {
  .calendar-layout {
    gap: 1rem;
  }

  .calendar-wrapper {
    width: 100%;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: thin;
  }

  .calendar-wrapper .glass-card {
    min-width: 600px;
    width: 100%;
  }

  .weekdays-header {
    gap: 0.25rem;
    padding-bottom: 0.5rem;
    margin-bottom: 0.5rem;
  }

  .weekday-cell {
    font-size: 0.75rem;
    padding: 0.5rem 0.25rem;
  }

  .calendar-grid {
    gap: 0.375rem;
    min-width: 600px; /* Ensure calendar doesn't get too cramped */
  }

  .calendar-day {
    min-height: 100px;
    padding: 0.5rem;
    border-radius: 12px;
  }

  .day-number {
    font-size: 0.85rem;
    margin-bottom: 0.375rem;
  }

  .events-in-cell {
    gap: 0.375rem;
    margin-top: 0.375rem;
  }

  .event-block {
    font-size: 0.7rem;
    padding: 0.5rem 0.625rem;
    border-radius: 8px;
    min-height: 28px;
    display: flex;
    align-items: center;
  }

  .event-text {
    font-size: 0.7rem;
    line-height: 1.4;
  }

  .more-events {
    font-size: 0.65rem;
    padding: 0.375rem;
    margin-top: 0.25rem;
  }

  .month-year {
    font-size: 1.25rem;
    min-width: 150px;
  }

  .nav-arrow {
    width: 38px;
    height: 38px;
    font-size: 1.25rem;
  }

  .event-details-wrapper {
    margin-top: 1rem;
  }

  .event-details-card {
    border-radius: 20px;
  }

  .confirmation-banner {
    padding: 0.875rem 1.25rem;
    font-size: 0.875rem;
  }

  .user-info {
    padding: 1.25rem;
  }

  .user-avatar {
    width: 56px;
    height: 56px;
  }

  .user-name {
    font-size: 1rem;
  }

  .date-time-pill {
    margin: 1.25rem;
    padding: 0.75rem 1rem;
    flex-wrap: wrap;
    gap: 0.75rem;
  }

  .pill-item {
    font-size: 0.85rem;
  }

  .pill-divider {
    display: none; /* Hide divider on mobile for better wrapping */
  }

  .event-details-content {
    padding: 0 1.25rem 1.25rem;
  }

  .event-detail-title {
    font-size: 1.25rem;
    margin-bottom: 0.625rem;
  }

  .event-detail-description {
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }

  .meta-item {
    font-size: 0.85rem;
    gap: 0.625rem;
  }

  .register-btn {
    margin: 0 1.25rem 1.25rem;
    padding: 0.75rem;
    font-size: 0.95rem;
  }

  .empty-state {
    padding: 2rem 1.5rem;
  }

  .empty-icon {
    font-size: 2.5rem;
  }
  .calendar-icon-img {
    max-width: 120px;
    max-height: 120px;
  }

  .empty-text {
    font-size: 1.1rem;
  }

  .empty-subtext {
    font-size: 0.85rem;
  }
}

@media (max-width: 480px) {
  .calendar-wrapper .glass-card {
    min-width: 100%;
    padding: 0.75rem;
  }

  .calendar-grid {
    min-width: 100%;
    gap: 0.375rem;
  }

  .calendar-day {
    min-height: 95px;
    padding: 0.5rem 0.375rem;
    border-radius: 12px;
  }

  .day-number {
    font-size: 0.85rem;
    margin-bottom: 0.375rem;
    font-weight: 700;
  }

  .event-block {
    font-size: 0.7rem;
    padding: 0.5rem 0.625rem;
    min-height: 28px;
    border-radius: 8px;
  }

  .event-text {
    font-size: 0.7rem;
    font-weight: 500;
  }

  .weekday-cell {
    font-size: 0.75rem;
    padding: 0.5rem 0.25rem;
    font-weight: 700;
  }

  .weekdays-header {
    gap: 0.375rem;
  }

  .month-year {
    font-size: 1.15rem;
    min-width: 140px;
  }

  .nav-arrow {
    width: 36px;
    height: 36px;
    font-size: 1.2rem;
  }

  .event-detail-title {
    font-size: 1.15rem;
  }

  .date-time-pill {
    margin: 1rem;
    padding: 0.75rem 1rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .pill-divider {
    display: none;
  }

  .pill-item {
    font-size: 0.85rem;
  }

  .user-info {
    padding: 1rem;
  }

  .user-avatar {
    width: 52px;
    height: 52px;
  }

  .event-details-content {
    padding: 0 1rem 1rem;
  }

  .register-btn {
    margin: 0 1rem 1rem;
    padding: 0.875rem;
  }
}
</style>
