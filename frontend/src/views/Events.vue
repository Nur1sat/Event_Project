<template>
  <div class="container">
    <div class="page-header">
      <h1>Club Activities</h1>
      <div class="filters">
        <input type="text" v-model="search" placeholder="Search events..." class="search-input" />
        <select v-model="statusFilter" class="filter-select">
          <option value="">All Status</option>
          <option value="upcoming">Upcoming</option>
          <option value="full">Full</option>
          <option value="finished">Finished</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading events...</div>
    <div v-else-if="filteredEvents.length === 0" class="card">No events found</div>
    
    <div v-else class="events-grid">
      <div v-for="event in filteredEvents" :key="event.id" class="card event-card">
        <div style="display:flex;justify-content:space-between;align-items:start">
          <h3>{{ event.title }}</h3>
          <span :class="'badge badge-' + event.status">{{ event.status }}</span>
        </div>
        <div class="meta">
          <div>📅 {{ formatDate(event.date) }}</div>
          <div>📍 {{ event.location }}</div>
        </div>
        <p v-if="event.description" style="margin-bottom:12px;color:#6b7280;font-size:14px">
          {{ event.description }}
        </p>
        <div class="spots" :style="{ color: event.available_spots === 0 ? '#dc2626' : '#16a34a' }">
          {{ event.available_spots }} / {{ event.max_participants }} spots available
        </div>
        <button 
          v-if="event.is_registered"
          class="btn btn-danger"
          @click="cancelRegistration(event.id)"
          :disabled="actionLoading === event.id"
        >
          Cancel Registration
        </button>
        <button 
          v-else
          class="btn btn-primary"
          @click="registerForEvent(event.id)"
          :disabled="event.status !== 'upcoming' || actionLoading === event.id"
        >
          {{ event.status === 'full' ? 'No spots available' : event.status === 'finished' ? 'Event finished' : 'Register' }}
        </button>
      </div>
    </div>

    <div v-if="message" :class="'alert ' + (messageType === 'error' ? 'alert-error' : 'alert-success')" style="position:fixed;bottom:20px;right:20px;z-index:100">
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const events = ref([])
const loading = ref(true)
const actionLoading = ref(null)
const search = ref('')
const statusFilter = ref('')
const message = ref('')
const messageType = ref('success')

const filteredEvents = computed(() => {
  let result = events.value
  if (search.value) {
    result = result.filter(e => 
      e.title.toLowerCase().includes(search.value.toLowerCase()) ||
      e.location.toLowerCase().includes(search.value.toLowerCase())
    )
  }
  if (statusFilter.value) {
    result = result.filter(e => e.status === statusFilter.value)
  }
  return result
})

const formatDate = (date) => {
  return new Date(date).toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const showMessage = (msg, type = 'success') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => { message.value = '' }, 3000)
}

const fetchEvents = async () => {
  try {
    const { data } = await api.get('/events/')
    events.value = data.events
  } catch (e) {
    showMessage('Failed to load events', 'error')
  } finally {
    loading.value = false
  }
}

const registerForEvent = async (eventId) => {
  actionLoading.value = eventId
  try {
    await api.post(`/registrations/${eventId}`)
    showMessage('Successfully registered!')
    fetchEvents()
  } catch (e) {
    showMessage(e.response?.data?.detail || 'Registration failed', 'error')
  } finally {
    actionLoading.value = null
  }
}

const cancelRegistration = async (eventId) => {
  actionLoading.value = eventId
  try {
    await api.delete(`/registrations/${eventId}`)
    showMessage('Registration cancelled')
    fetchEvents()
  } catch (e) {
    showMessage(e.response?.data?.detail || 'Failed to cancel', 'error')
  } finally {
    actionLoading.value = null
  }
}

onMounted(fetchEvents)
</script>

<style scoped>
.filters {
  display: flex;
  gap: 12px;
}
.search-input {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  width: 200px;
}
.filter-select {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
}
</style>
