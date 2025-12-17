<template>
  <div class="min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-semibold text-gray-900 mb-8 tracking-tight">Admin Panel</h1>
      
      <!-- Tabs -->
      <div class="mb-6 flex gap-2 border-b border-white/30">
        <button
          @click="activeTab = 'events'"
          :class="[
            'px-6 py-3 font-semibold text-sm transition-glass',
            activeTab === 'events'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          ]"
        >
          Events
        </button>
        <button
          @click="activeTab = 'requests'"
          :class="[
            'px-6 py-3 font-semibold text-sm transition-glass relative',
            activeTab === 'requests'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          ]"
        >
          Requests
          <span
            v-if="pendingRequestsCount > 0"
            class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full min-w-[20px] h-5 px-1.5 flex items-center justify-center shadow-lg"
          >
            {{ pendingRequestsCount > 99 ? '99+' : pendingRequestsCount }}
          </span>
        </button>
      </div>

      <!-- Events Tab -->
      <div v-if="activeTab === 'events'">
        <div class="mb-6 flex justify-between items-center">
          <h2 class="text-2xl font-semibold text-gray-900">Manage Events</h2>
          <button @click="openEventModal(null)" class="glass-btn glass-btn-primary">
            + New Event
          </button>
        </div>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-600">Loading...</p>
        </div>

        <div v-else-if="events.length === 0" class="glass-card p-12 text-center">
          <p class="text-gray-700">No events</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="event in events"
            :key="event.id"
            class="glass-card p-6 cursor-pointer transition-glass"
            @click="openEventModal(event)"
          >
            <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ event.title }}</h3>
            <p class="text-gray-700 mb-4 line-clamp-2">{{ event.description }}</p>
            <div class="text-sm text-gray-600 space-y-1">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>{{ formatDate(event.date) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ formatTime(event.start_time) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>{{ event.location }}</span>
              </div>
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span>{{ event.max_participants }} spots</span>
              </div>
            </div>
            <div class="mt-4 flex gap-2">
              <button
                @click.stop="openEventModal(event)"
                class="flex-1 glass-btn text-sm"
              >
                Edit
              </button>
              <button
                @click.stop="deleteEvent(event.id)"
                class="flex-1 glass-btn text-sm bg-red-500/80 text-white border-red-400/40"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Event Requests Tab -->
      <div v-if="activeTab === 'requests'">
        <div class="mb-6">
          <h2 class="text-2xl font-semibold text-gray-900">Event Requests</h2>
        </div>

        <div v-if="loadingRequests" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          <p class="mt-4 text-gray-600">Loading...</p>
        </div>

        <div v-else-if="eventRequests.length === 0" class="glass-card p-12 text-center">
          <p class="text-gray-700">No requests</p>
        </div>

        <div v-else class="space-y-4">
          <div
            v-for="request in eventRequests"
            :key="request.id"
            class="glass-card p-6"
          >
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ request.title }}</h3>
                <p class="text-gray-700 mb-2">{{ request.description }}</p>
                <div class="text-sm text-gray-600 space-y-1">
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    <span>{{ formatDate(request.date) }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span>{{ formatTime(request.start_time) }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                    <span>{{ request.location }}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                    </svg>
                    <span>{{ request.max_participants }} spots</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    <span>{{ request.user?.full_name || 'User' }}</span>
                  </div>
                </div>
              </div>
              <span
                :class="[
                  'px-3 py-1 rounded-full text-sm font-semibold',
                  request.status === 'approved' ? 'bg-green-100 text-green-800' :
                  request.status === 'rejected' ? 'bg-red-100 text-red-800' :
                  'bg-yellow-100 text-yellow-800'
                ]"
              >
                {{ request.status === 'approved' ? 'Approved' :
                   request.status === 'rejected' ? 'Rejected' :
                   'Pending' }}
              </span>
            </div>
            <div v-if="request.status === 'pending'" class="flex gap-2">
              <button
                @click="updateRequestStatus(request.id, 'approved')"
                class="flex-1 glass-btn glass-btn-primary"
              >
                Approve
              </button>
              <button
                @click="updateRequestStatus(request.id, 'rejected')"
                class="flex-1 glass-btn bg-red-500/80 text-white border-red-400/40"
              >
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Event Modal -->
      <div v-if="showEventModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 glass-overlay" @click.self="closeEventModal">
        <div class="glass-modal max-w-2xl w-full p-8 max-h-[90vh] overflow-y-auto scrollbar-glass">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-semibold text-gray-900">
              {{ editingEvent ? 'Edit Event' : 'New Event' }}
            </h2>
            <button @click="closeEventModal" class="text-gray-500 hover:text-gray-700 text-2xl">×</button>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-5">
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Title</label>
              <input
                v-model="eventForm.title"
                type="text"
                required
                class="glass-input w-full"
                placeholder="Event title"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Description</label>
              
              <!-- AI Description Generator -->
              <div class="mb-3 p-4 glass-card bg-blue-50/30 border border-blue-200/40 rounded-xl">
                <div class="flex items-start gap-3 mb-3">
                  <div class="flex-1">
                    <label class="block text-xs font-semibold text-gray-700 mb-1.5">Keywords</label>
                    <input
                      v-model="keywords"
                      type="text"
                      class="glass-input w-full text-sm"
                      placeholder="Example: AI, workshop, beginner"
                    />
                  </div>
                  <button
                    type="button"
                    @click="generateDescription"
                    :disabled="generatingDescription || !keywords.trim()"
                    class="glass-btn glass-btn-primary px-4 py-2.5 whitespace-nowrap mt-6"
                    :class="{ 'opacity-50 cursor-not-allowed': generatingDescription || !keywords.trim() }"
                  >
                    <span v-if="generatingDescription" class="flex items-center gap-2">
                      <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Generating...
                    </span>
                    <span v-else class="flex items-center gap-2">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Generate Description
                    </span>
                  </button>
                </div>
                <p class="text-xs text-gray-600">Enter keywords and AI will automatically generate a description</p>
              </div>
              
              <textarea
                v-model="eventForm.description"
                required
                rows="6"
                class="glass-input w-full"
                placeholder="Event description (or use keywords above to generate automatically)"
              ></textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-semibold text-gray-800 mb-2">Date</label>
                <input
                  v-model="eventForm.date"
                  type="date"
                  required
                  class="glass-input w-full"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-gray-800 mb-2">Time</label>
                <input
                  v-model="eventForm.start_time"
                  type="time"
                  required
                  class="glass-input w-full"
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Location</label>
              <input
                v-model="eventForm.location"
                type="text"
                required
                class="glass-input w-full"
                placeholder="Event location"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Max Participants</label>
              <input
                v-model.number="eventForm.max_participants"
                type="number"
                required
                min="1"
                class="glass-input w-full"
                placeholder="Қатысушылар саны"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Іс-шара суреті</label>
              <div class="mb-3">
                <input
                  type="file"
                  accept="image/*"
                  @change="handleImageUpload"
                  class="hidden"
                  ref="imageInput"
                  id="event-image-upload"
                />
                <label
                  for="event-image-upload"
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
              <button type="submit" class="flex-1 glass-btn glass-btn-primary" :disabled="submitting">
                {{ submitting ? 'Saving...' : (editingEvent ? 'Save' : 'Add') }}
              </button>
              <button type="button" @click="closeEventModal" class="flex-1 glass-btn">
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

export default {
  name: 'AdminPanel',
  setup() {
    const activeTab = ref('events')
    const events = ref([])
    const eventRequests = ref([])
    const loading = ref(true)
    const loadingRequests = ref(true)
    const showEventModal = ref(false)
    const editingEvent = ref(null)
    const submitting = ref(false)
    const generatingDescription = ref(false)
    const keywords = ref('')

    const pendingRequestsCount = computed(() => {
      return eventRequests.value.filter(req => req.status === 'pending').length
    })

    const eventForm = ref({
      title: '',
      description: '',
      date: '',
      start_time: '',
      location: '',
      max_participants: 1,
      image_url: ''
    })
    const imageInput = ref(null)

    const fetchEvents = async () => {
      try {
        loading.value = true
        const response = await api.get('/events')
        events.value = response.data
      } catch (error) {
        console.error('Failed to fetch events:', error)
      } finally {
        loading.value = false
      }
    }

    const fetchEventRequests = async () => {
      try {
        loadingRequests.value = true
        const response = await api.get('/event-requests')
        eventRequests.value = response.data
      } catch (error) {
        console.error('Failed to fetch event requests:', error)
      } finally {
        loadingRequests.value = false
      }
    }

    const openEventModal = (event) => {
      if (event) {
        editingEvent.value = event
        eventForm.value = {
          title: event.title,
          description: event.description,
          date: event.date,
          start_time: event.start_time.substring(0, 5),
          location: event.location,
          max_participants: event.max_participants,
          image_url: event.image_url || ''
        }
        keywords.value = ''
      } else {
        editingEvent.value = null
        eventForm.value = {
          title: '',
          description: '',
          date: '',
          start_time: '',
          location: '',
          max_participants: 1,
          image_url: ''
        }
        keywords.value = ''
      }
      showEventModal.value = true
    }

    const closeEventModal = () => {
      showEventModal.value = false
      editingEvent.value = null
    }

    const handleSubmit = async () => {
      try {
        submitting.value = true
        
        // Prepare form data, handle empty image_url
        const formData = {
          ...eventForm.value,
          max_participants: parseInt(eventForm.value.max_participants),
          image_url: eventForm.value.image_url || null
        }

        console.log('Submitting event data:', {
          ...formData,
          image_url: formData.image_url ? `[base64 string, length: ${formData.image_url.length}]` : null
        })

        if (editingEvent.value) {
          await api.put(`/events/${editingEvent.value.id}`, formData)
        } else {
          await api.post('/events', formData)
        }

        await fetchEvents()
        closeEventModal()
      } catch (error) {
        console.error('Failed to save event:', error)
        console.error('Error response:', error.response?.data)
        const errorMessage = error.response?.data?.detail || error.message || 'An error occurred while saving the event'
        alert(errorMessage)
      } finally {
        submitting.value = false
      }
    }

    const deleteEvent = async (eventId) => {
      if (!confirm('Are you sure you want to delete this event?')) return

      try {
        await api.delete(`/events/${eventId}`)
        await fetchEvents()
      } catch (error) {
        console.error('Failed to delete event:', error)
        alert(error.response?.data?.detail || 'An error occurred while deleting the event')
      }
    }

    const updateRequestStatus = async (requestId, status) => {
      try {
        await api.put(`/event-requests/${requestId}/status?status=${status}`)
        await fetchEventRequests()
        await fetchEvents() // Refresh events list in case a new event was created
      } catch (error) {
        console.error('Failed to update request status:', error)
        alert(error.response?.data?.detail || 'An error occurred while updating request status')
      }
    }

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-US')
    }

    const formatTime = (timeString) => {
      return timeString.substring(0, 5)
    }

    const generateDescription = async () => {
      if (!keywords.value.trim()) {
        alert('Please enter keywords')
        return
      }

      try {
        generatingDescription.value = true
        
        // Check if token exists
        const token = sessionStorage.getItem('token')
        if (!token) {
          alert('You must be logged in')
          generatingDescription.value = false
          return
        }
        
        const requestData = {
          keywords: keywords.value.trim(),
          title: eventForm.value.title || '',
          type: detectEventType(keywords.value),
          audience: detectAudience(keywords.value),
          date: eventForm.value.date || null,
          location: eventForm.value.location || null
        }
        
        console.log('🚀 Generating description with data:', requestData)
        console.log('📍 API endpoint: /api/generate-event-description')
        console.log('🔑 Token exists:', !!token)
        
        const response = await api.post('/generate-event-description', requestData)
        
        console.log('✅ Description generated successfully:', response.data)
        
        if (response.data && response.data.description) {
          eventForm.value.description = response.data.description
          // Clear keywords after successful generation
          keywords.value = ''
        } else {
          console.error('❌ No description in response:', response.data)
          alert('Description could not be retrieved. Please try again.')
        }
      } catch (error) {
        console.error('❌ Failed to generate description:', error)
        console.error('Error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          statusText: error.response?.statusText,
          config: error.config
        })
        
        let errorMessage = 'An error occurred while generating description'
        if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.message) {
          errorMessage = error.message
        }
        
        alert(errorMessage)
      } finally {
        generatingDescription.value = false
      }
    }

    const detectEventType = (keywords) => {
      const lower = keywords.toLowerCase()
      // Концерты и развлекательные мероприятия
      if (lower.includes('концерт') || lower.includes('concert') || lower.includes('концерт')) return 'concert'
      if (lower.includes('концерт') || lower.includes('концерт')) return 'concert'
      // Семинары и лекции
      if (lower.includes('seminar') || lower.includes('семинар') || lower.includes('лекция')) return 'seminar'
      // Соревнования
      if (lower.includes('competition') || lower.includes('жарыс') || lower.includes('турнир') || lower.includes('соревнование')) return 'competition'
      // Встречи
      if (lower.includes('meetup') || lower.includes('кездесу') || lower.includes('встреча')) return 'meetup'
      // Воркшопы
      if (lower.includes('workshop') || lower.includes('воркшоп')) return 'workshop'
      // По умолчанию - определить по контексту
      return 'event'
    }

    const detectAudience = (keywords) => {
      const lower = keywords.toLowerCase()
      if (lower.includes('beginner') || lower.includes('бастапқы') || lower.includes('жаңадан')) return 'beginner'
      if (lower.includes('advanced') || lower.includes('кәсіби') || lower.includes('тәжірибелі')) return 'advanced'
      return 'students'
    }

    const handleImageUpload = (event) => {
      const file = event.target.files[0]
      if (!file) return

      // Validate file type
      if (!file.type.startsWith('image/')) {
        alert('Only image files can be uploaded')
        return
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        alert('Image size must not exceed 10MB')
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

    onMounted(() => {
      fetchEvents()
      fetchEventRequests()
    })

      return {
      activeTab,
      events,
      eventRequests,
      loading,
      loadingRequests,
      showEventModal,
      editingEvent,
      submitting,
      eventForm,
      pendingRequestsCount,
      keywords,
      generatingDescription,
      imageInput,
      openEventModal,
      closeEventModal,
      handleSubmit,
      deleteEvent,
      updateRequestStatus,
      formatDate,
      formatTime,
      generateDescription,
      handleImageUpload,
      removeImage
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
