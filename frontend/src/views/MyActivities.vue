<template>
  <div class="container">
    <h1 style="margin-bottom:24px">My Activities</h1>

    <div class="stats-row">
      <div class="stat-item">
        <span class="stat-num">{{ registrations.length }}</span>
        <span class="stat-text">Total Registrations</span>
      </div>
      <div class="stat-item">
        <span class="stat-num">{{ upcomingCount }}</span>
        <span class="stat-text">Upcoming Events</span>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="registrations.length === 0" class="card">
      <p>You haven't registered for any events yet.</p>
      <router-link to="/" class="btn btn-primary" style="margin-top:12px;display:inline-block">Browse Events</router-link>
    </div>
    
    <div v-else>
      <div v-for="reg in registrations" :key="reg.id" class="card registration-card">
        <div class="reg-info">
          <h3>{{ reg.event.title }}</h3>
          <div class="reg-meta">
            <span>📅 {{ formatDate(reg.event.date) }}</span>
            <span>📍 {{ reg.event.location }}</span>
          </div>
          <div class="reg-date">
            Registered: {{ formatDate(reg.registered_at) }}
          </div>
        </div>
        <button class="btn btn-danger" @click="cancel(reg.event_id)" :disabled="cancelling === reg.event_id">
          {{ cancelling === reg.event_id ? 'Cancelling...' : 'Cancel' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const registrations = ref([])
const loading = ref(true)
const cancelling = ref(null)

const upcomingCount = computed(() => {
  return registrations.value.filter(r => new Date(r.event.date) > new Date()).length
})

const formatDate = (date) => {
  return new Date(date).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const fetchRegistrations = async () => {
  try {
    const { data } = await api.get('/registrations/my')
    registrations.value = data
  } finally {
    loading.value = false
  }
}

const cancel = async (eventId) => {
  cancelling.value = eventId
  try {
    await api.delete(`/registrations/${eventId}`)
    fetchRegistrations()
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to cancel')
  } finally {
    cancelling.value = null
  }
}

onMounted(fetchRegistrations)
</script>

<style scoped>
.stats-row {
  display: flex;
  gap: 24px;
  margin-bottom: 24px;
}
.stat-item {
  background: white;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.stat-num {
  font-size: 24px;
  font-weight: bold;
  color: #2563eb;
  margin-right: 8px;
}
.stat-text {
  color: #6b7280;
}
.registration-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.reg-info h3 {
  margin-bottom: 8px;
}
.reg-meta {
  color: #6b7280;
  font-size: 14px;
  display: flex;
  gap: 16px;
}
.reg-date {
  font-size: 12px;
  color: #9ca3af;
  margin-top: 4px;
}
</style>
