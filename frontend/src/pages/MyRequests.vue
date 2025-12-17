<template>
  <div class="min-h-screen py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-4xl font-semibold text-gray-900 tracking-tight">My Requests</h1>
        <router-link 
          v-if="user?.role !== 'admin'"
          to="/event-request" 
          class="glass-btn glass-btn-primary"
        >
          + New Request
        </router-link>
      </div>
      <div v-if="loading" class="text-center py-16">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-3 border-blue-500/30 border-t-blue-500"></div>
        <p class="mt-4 text-gray-700 font-medium">Loading...</p>
      </div>
      <div v-else-if="requests.length === 0" class="text-center py-16">
        <div class="glass-card p-12 max-w-md mx-auto">
          <h3 class="text-2xl font-semibold text-gray-900 mb-3">No requests</h3>
          <p class="text-gray-700 mb-6">You haven't submitted any event requests yet</p>
          <router-link 
            v-if="user?.role !== 'admin'"
            to="/event-request" 
            class="glass-btn glass-btn-primary inline-block mb-3"
          >
            Create New Request
          </router-link>
          <br>
          <router-link to="/calendar" class="glass-btn inline-block">Go to Calendar</router-link>
        </div>
      </div>
      <div v-else class="space-y-6">
        <div
          v-for="request in requests"
          :key="request.id"
          class="glass-card p-6"
        >
          <div class="flex justify-between items-start mb-4">
            <div class="flex-1">
              <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ request.title }}</h3>
              <p class="text-gray-700 mb-4">{{ request.description }}</p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-600">
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span><span class="font-semibold">Date:</span> {{ formatDate(request.date) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span><span class="font-semibold">Time:</span> {{ formatTime(request.start_time) }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  <span><span class="font-semibold">Location:</span> {{ request.location }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <svg class="w-4 h-4 text-gray-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <span><span class="font-semibold">Participants:</span> {{ request.max_participants }} people</span>
                </div>
              </div>
            </div>
            <span
              :class="[
                'px-4 py-2 rounded-full text-sm font-semibold whitespace-nowrap ml-4',
                request.status === 'approved' ? 'bg-green-100 text-green-800' :
                request.status === 'rejected' ? 'bg-red-100 text-red-800' :
                'bg-yellow-100 text-yellow-800'
              ]"
            >
              {{ request.status === 'approved' ? '✓ Approved' :
                 request.status === 'rejected' ? '✗ Rejected' :
                 '⏳ Pending' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

export default {
  name: 'MyRequests',
  setup() {
    const authStore = useAuthStore()
    const user = computed(() => authStore.user)
    const requests = ref([])
    const loading = ref(true)
    
    const fetchRequests = async () => {
      try {
        const response = await api.get('/my-event-requests')
        requests.value = response.data
      } catch (error) {
        console.error('Failed to fetch requests:', error)
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
    
    onMounted(() => {
      fetchRequests()
    })
    
    return {
      user,
      requests,
      loading,
      formatDate,
      formatTime
    }
  }
}
</script>

