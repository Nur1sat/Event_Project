<template>
  <div class="container">
    <div class="page-header">
      <h1>Admin Panel</h1>
      <button class="btn btn-primary" @click="openModal()">+ New Event</button>
    </div>

    <!-- Stats -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-value">{{ events.length }}</div>
        <div class="stat-label">Total Events</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ upcomingCount }}</div>
        <div class="stat-label">Upcoming</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ totalParticipants }}</div>
        <div class="stat-label">Total Registrations</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{{ users.length }}</div>
        <div class="stat-label">Total Users</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="tabs">
      <button :class="{ active: tab === 'events' }" @click="tab = 'events'">Events</button>
      <button :class="{ active: tab === 'users' }" @click="tab = 'users'">Users</button>
    </div>

    <!-- Events Tab -->
    <div v-if="tab === 'events'">
      <div v-if="loading" class="loading">Loading...</div>
      <table v-else class="table card">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Date</th>
            <th>Location</th>
            <th>Participants</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="event in events" :key="event.id">
            <td>{{ event.id }}</td>
            <td>{{ event.title }}</td>
            <td>{{ formatDate(event.date) }}</td>
            <td>{{ event.location }}</td>
            <td>{{ event.current_participants }} / {{ event.max_participants }}</td>
            <td><span :class="'badge badge-' + event.status">{{ event.status }}</span></td>
            <td>
              <button class="btn btn-secondary" style="margin-right:8px;padding:6px 12px" @click="viewParticipants(event)">👥</button>
              <button class="btn btn-primary" style="margin-right:8px;padding:6px 12px" @click="openModal(event)">✏️</button>
              <button class="btn btn-danger" style="padding:6px 12px" @click="deleteEvent(event.id)">🗑️</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Users Tab -->
    <div v-if="tab === 'users'">
      <table class="table card">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Group</th>
            <th>Role</th>
            <th>Registered</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.full_name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.group || '-' }}</td>
            <td><span :class="'badge badge-' + (user.role === 'admin' ? 'full' : 'upcoming')">{{ user.role }}</span></td>
            <td>{{ formatDate(user.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Event Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal">
        <h2>{{ editingEvent ? 'Edit Event' : 'Create Event' }}</h2>
        <form @submit.prevent="saveEvent">
          <div class="form-group">
            <label>Title *</label>
            <input v-model="form.title" required />
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div class="form-group">
            <label>Date & Time *</label>
            <input type="datetime-local" v-model="form.date" required />
          </div>
          <div class="form-group">
            <label>Location *</label>
            <input v-model="form.location" required />
          </div>
          <div class="form-group">
            <label>Max Participants *</label>
            <input type="number" v-model="form.max_participants" min="1" required />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="showModal = false">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              {{ saving ? 'Saving...' : 'Save' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Participants Modal -->
    <div v-if="showParticipants" class="modal-overlay" @click.self="showParticipants = false">
      <div class="modal">
        <h2>Participants - {{ selectedEvent?.title }}</h2>
        <div v-if="participants.length === 0" style="color:#6b7280;padding:20px 0">
          No participants yet
        </div>
        <table v-else class="table" style="margin-top:16px">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Group</th>
              <th>Registered At</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in participants" :key="p.id">
              <td>{{ p.full_name }}</td>
              <td>{{ p.email }}</td>
              <td>{{ p.group || '-' }}</td>
              <td>{{ formatDate(p.registered_at) }}</td>
            </tr>
          </tbody>
        </table>
        <div class="modal-actions">
          <button class="btn btn-secondary" @click="showParticipants = false">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const events = ref([])
const users = ref([])
const loading = ref(true)
const showModal = ref(false)
const showParticipants = ref(false)
const editingEvent = ref(null)
const selectedEvent = ref(null)
const participants = ref([])
const saving = ref(false)
const tab = ref('events')

const form = ref({
  title: '',
  description: '',
  date: '',
  location: '',
  max_participants: 20
})

const upcomingCount = computed(() => events.value.filter(e => e.status === 'upcoming').length)
const totalParticipants = computed(() => events.value.reduce((sum, e) => sum + e.current_participants, 0))

const formatDate = (date) => {
  return new Date(date).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchEvents = async () => {
  try {
    const { data } = await api.get('/events/')
    events.value = data.events
  } finally {
    loading.value = false
  }
}

const fetchUsers = async () => {
  try {
    const { data } = await api.get('/users/')
    users.value = data
  } catch (e) {
    console.error('Failed to fetch users')
  }
}

const openModal = (event = null) => {
  editingEvent.value = event
  if (event) {
    form.value = {
      title: event.title,
      description: event.description || '',
      date: new Date(event.date).toISOString().slice(0, 16),
      location: event.location,
      max_participants: event.max_participants
    }
  } else {
    form.value = { title: '', description: '', date: '', location: '', max_participants: 20 }
  }
  showModal.value = true
}

const saveEvent = async () => {
  saving.value = true
  try {
    const payload = {
      ...form.value,
      date: new Date(form.value.date).toISOString()
    }
    if (editingEvent.value) {
      await api.put(`/events/${editingEvent.value.id}`, payload)
    } else {
      await api.post('/events/', payload)
    }
    showModal.value = false
    fetchEvents()
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to save event')
  } finally {
    saving.value = false
  }
}

const deleteEvent = async (id) => {
  if (!confirm('Delete this event?')) return
  try {
    await api.delete(`/events/${id}`)
    fetchEvents()
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete')
  }
}

const viewParticipants = async (event) => {
  selectedEvent.value = event
  try {
    const { data } = await api.get(`/events/${event.id}/participants`)
    participants.value = data
    showParticipants.value = true
  } catch (e) {
    alert('Failed to load participants')
  }
}

onMounted(() => {
  fetchEvents()
  fetchUsers()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #2563eb;
}
.stat-label {
  color: #6b7280;
  margin-top: 4px;
}
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.tabs button {
  padding: 10px 20px;
  border: none;
  background: #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
}
.tabs button.active {
  background: #2563eb;
  color: white;
}
</style>
