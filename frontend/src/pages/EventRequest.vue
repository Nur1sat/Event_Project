<template>
  <div class="min-h-screen py-8">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
      <h1 class="text-4xl font-semibold text-gray-900 mb-8 tracking-tight">Event Request</h1>
      
      <div class="glass-card p-8">
        <p class="text-gray-700 mb-6">
          Submit a request to the administrator to add an event. After your request is reviewed, 
          if approved, the event will be added to the calendar.
        </p>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Event Title *</label>
            <input
              v-model="requestForm.title"
              type="text"
              required
              class="glass-input w-full"
              placeholder="Example: Football Tournament"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Description *</label>
            <textarea
              v-model="requestForm.description"
              required
              rows="5"
              class="glass-input w-full"
              placeholder="Enter full event description..."
            ></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Date *</label>
              <input
                v-model="requestForm.date"
                type="date"
                required
                :min="minDate"
                class="glass-input w-full"
              />
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-800 mb-2">Start Time *</label>
              <input
                v-model="requestForm.start_time"
                type="time"
                required
                class="glass-input w-full"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Location *</label>
            <input
              v-model="requestForm.location"
              type="text"
              required
              class="glass-input w-full"
              placeholder="Example: Sports Hall, Room 101"
            />
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-800 mb-2">Max Participants *</label>
            <input
              v-model.number="requestForm.max_participants"
              type="number"
              required
              min="1"
              class="glass-input w-full"
              placeholder="Example: 20"
            />
            <p class="text-sm text-gray-600 mt-1">Maximum number of people who can participate in the event</p>
          </div>

          <div v-if="error" class="backdrop-blur-[20px] bg-red-500/20 rounded-2xl p-4 border border-red-400/30">
            <p class="text-red-900 font-medium">{{ error }}</p>
          </div>

          <div v-if="success" class="backdrop-blur-[20px] bg-green-500/20 rounded-2xl p-4 border border-green-400/30">
            <p class="text-green-900 font-medium">{{ success }}</p>
          </div>

          <div class="flex gap-4 pt-4">
            <button
              type="submit"
              :disabled="submitting"
              class="flex-1 glass-btn glass-btn-primary"
            >
              {{ submitting ? 'Submitting...' : 'Submit Request' }}
            </button>
            <button
              type="button"
              @click="$router.back()"
              class="flex-1 glass-btn"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'

export default {
  name: 'EventRequest',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const submitting = ref(false)
    const error = ref(null)
    const success = ref(null)
    
    // Redirect admins to admin panel
    onMounted(() => {
      if (authStore.user?.role === 'admin') {
        router.push('/admin')
      }
    })

    const requestForm = ref({
      title: '',
      description: '',
      date: '',
      start_time: '',
      location: '',
      max_participants: 1
    })

    const minDate = computed(() => {
      const today = new Date()
      return today.toISOString().split('T')[0]
    })

    const handleSubmit = async () => {
      try {
        submitting.value = true
        error.value = null
        success.value = null

        const formData = {
          ...requestForm.value,
          max_participants: parseInt(requestForm.value.max_participants)
        }

        await api.post('/event-requests', formData)
        
        success.value = 'Your request has been submitted successfully! The administrator will review it.'
        
        // Reset form
        requestForm.value = {
          title: '',
          description: '',
          date: '',
          start_time: '',
          location: '',
          max_participants: 1
        }

        // Redirect after 2 seconds
        setTimeout(() => {
          router.push('/my-requests')
        }, 2000)
      } catch (err) {
        console.error('Failed to submit request:', err)
        error.value = err.response?.data?.detail || 'An error occurred while submitting the request'
      } finally {
        submitting.value = false
      }
    }

    return {
      requestForm,
      submitting,
      error,
      success,
      minDate,
      handleSubmit
    }
  }
}
</script>

