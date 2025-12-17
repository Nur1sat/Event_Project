<template>
    <div class="min-h-screen py-8">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Profile Header with Photo -->
        <div class="glass-card p-10 mb-6">
          <div class="flex flex-col items-center">
            <!-- Photo Section -->
            <div class="relative mb-6">
              <div class="w-32 h-32 rounded-full overflow-hidden border-4 border-white/60 shadow-2xl backdrop-blur-[30px] bg-white/40">
                <img 
                  v-if="user?.photo_url" 
                  :src="user.photo_url" 
                  :alt="user?.full_name"
                  class="w-full h-full object-cover"
                />
                <div 
                  v-else
                  class="w-full h-full bg-gradient-to-br from-blue-500/80 to-purple-500/80 flex items-center justify-center text-white text-4xl font-bold"
                >
                  {{ user?.full_name?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
              </div>
              <!-- Change Photo Button -->
              <button
                @click="triggerFileInput"
                class="absolute bottom-0 right-0 w-12 h-12 backdrop-blur-[30px] bg-white/80 rounded-full flex items-center justify-center shadow-xl border-2 border-white/60 hover:bg-white hover:scale-110 transition-glass"
              >
                <svg class="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
              <input
                ref="fileInput"
                type="file"
                accept="image/*"
                @change="handleFileSelect"
                class="hidden"
              />
            </div>
            
            <!-- User Name and Role -->
            <h1 class="text-4xl font-semibold text-gray-900 mb-3 tracking-tight">{{ user?.full_name }}</h1>
            <div class="flex items-center space-x-2 mb-4">
              <span class="px-5 py-2 backdrop-blur-[20px] bg-white/50 text-gray-900 text-sm font-semibold rounded-full border border-white/60">
                {{ user?.role === 'admin' ? 'Administrator' : 'Student' }}
              </span>
            </div>
          </div>
        </div>
  
        <!-- Tabs -->
        <div class="glass-card mb-6 overflow-hidden">
          <div class="flex border-b border-white/40">
            <button
              @click="activeTab = 'about'"
              :class="[
                'flex-1 px-6 py-4 text-sm font-semibold transition-glass',
                activeTab === 'about'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-white/30'
                  : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
              ]"
            >
              About
            </button>
            <button
              @click="activeTab = 'events'"
              :class="[
                'flex-1 px-6 py-4 text-sm font-semibold transition-glass',
                activeTab === 'events'
                  ? 'text-blue-600 border-b-2 border-blue-600 bg-white/30'
                  : 'text-gray-700 hover:text-gray-900 hover:bg-white/20'
              ]"
            >
              My Events
            </button>
          </div>
  
          <!-- Tab Content -->
          <div class="p-6">
            <!-- About Tab -->
            <div v-if="activeTab === 'about'" class="space-y-6">
              <div class="backdrop-blur-[20px] bg-white/40 rounded-2xl p-8 border border-white/50">
                <h2 class="text-2xl font-semibold text-gray-900 mb-6 tracking-tight">User Information</h2>
                <div class="space-y-5">
                  <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2">Full Name</label>
                    <input
                      v-model="editForm.full_name"
                      type="text"
                      class="glass-input w-full"
                      placeholder="Enter your full name"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2">Group</label>
                    <input
                      v-model="editForm.group"
                      type="text"
                      class="glass-input w-full"
                      placeholder="Example: 1F1"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2">Email</label>
                    <input
                      :value="user?.email"
                      type="email"
                      disabled
                      class="w-full px-4 py-3 backdrop-blur-[20px] bg-gray-200/40 border border-gray-300/40 rounded-xl text-gray-600 cursor-not-allowed"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-semibold text-gray-800 mb-2">Role</label>
                    <input
                      :value="user?.role === 'admin' ? 'Administrator' : 'Student'"
                      type="text"
                      disabled
                      class="w-full px-4 py-3 backdrop-blur-[20px] bg-gray-200/40 border border-gray-300/40 rounded-xl text-gray-600 cursor-not-allowed"
                    />
                  </div>
                  <button
                    @click="saveProfile"
                    :disabled="saving"
                    class="glass-btn glass-btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ saving ? 'Saving...' : 'Save Changes' }}
                  </button>
                </div>
              </div>
            </div>
  
            <!-- My Events Tab -->
            <div v-if="activeTab === 'events'" class="min-h-[400px]">
              <MyEvents :is-embedded="true" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'
  import { useAuthStore } from '../stores/auth'
  import api from '../services/api'
  import MyEvents from './MyEvents.vue'
  
  export default {
    name: 'Profile',
    components: {
      MyEvents
    },
    setup() {
      const authStore = useAuthStore()
      const activeTab = ref('about')
      const fileInput = ref(null)
      const saving = ref(false)
      const editForm = ref({
        full_name: '',
        group: ''
      })
  
      const user = computed(() => authStore.user)
  
      onMounted(() => {
        if (user.value) {
          editForm.value.full_name = user.value.full_name || ''
          editForm.value.group = user.value.group || ''
        }
      })
  
      const triggerFileInput = () => {
        fileInput.value?.click()
      }
  
      const handleFileSelect = async (event) => {
        const file = event.target.files[0]
        if (!file) return
  
        // Validate file type
        if (!file.type.startsWith('image/')) {
          alert('Please select an image')
          return
        }
  
        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
          alert('File size must not exceed 5MB')
          return
        }
  
        // Convert to base64
        const reader = new FileReader()
        reader.onload = async (e) => {
          const base64String = e.target.result
          try {
            saving.value = true
            const response = await api.put('/users/me', {
              photo_url: base64String
            })
            await authStore.fetchUser() // Refresh user data
            alert('Photo updated successfully!')
          } catch (error) {
            console.error('Error updating photo:', error)
            console.error('Error response:', error.response)
            const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Unknown error'
            console.error('Full error data:', error.response?.data)
            alert(`Error updating photo: ${errorMessage}`)
          } finally {
            saving.value = false
          }
        }
        reader.onerror = () => {
          alert('Error reading file. Please select another file.')
          saving.value = false
        }
        reader.readAsDataURL(file)
      }
  
      const saveProfile = async () => {
        try {
          saving.value = true
          const response = await api.put('/users/me', {
            full_name: editForm.value.full_name,
            group: editForm.value.group
          })
          await authStore.fetchUser() // Refresh user data
          alert('Profile updated successfully!')
        } catch (error) {
          console.error('Error updating profile:', error)
          alert('Error updating profile. Please try again.')
        } finally {
          saving.value = false
        }
      }
  
      return {
        user,
        activeTab,
        fileInput,
        editForm,
        saving,
        triggerFileInput,
        handleFileSelect,
        saveProfile
      }
    }
  }
  </script>
  

