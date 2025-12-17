<template>
<<<<<<< HEAD
  <div id="app">
    <nav v-if="authStore.isAuthenticated">
      <div class="nav-content">
        <router-link to="/" class="logo">JIHC Clubs</router-link>
        <div class="nav-links">
          <router-link to="/">Events</router-link>
          <router-link to="/my-activities">My Activities</router-link>
          <router-link v-if="authStore.isAdmin" to="/admin">Admin Panel</router-link>
        </div>
        <div class="user-info">
          <span>{{ authStore.user?.full_name }} <span v-if="authStore.isAdmin" class="badge">(Admin)</span></span>
          <button class="btn btn-secondary" @click="logout">Logout</button>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.badge {
  background: #dc2626;
  color: white;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 11px;
}
</style>
=======
  <div id="app" class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50/30 to-purple-50/20 relative">
    <nav v-if="isAuthenticated" :class="[
      'glass-nav px-6 py-3 flex justify-between items-center z-30 transition-glass',
      route.path === '/' 
        ? 'absolute top-6 left-1/2 transform -translate-x-1/2 w-[calc(100%-2rem)] max-w-7xl backdrop-blur-[20px] bg-white/50 border border-white/40' 
        : 'mt-6 mx-auto max-w-7xl w-[calc(100%-2rem)] backdrop-blur-[20px] bg-white/50 border border-white/40 sticky top-6'
    ]">
      <!-- Logo Section - Left -->
      <router-link to="/" class="flex items-center hover:opacity-80 transition-opacity">
        <JIHCLogo :is-home="route.path === '/'" />
      </router-link>
      
      <!-- Navigation Links - Centered -->
      <div class="hidden md:flex items-center space-x-1 absolute left-1/2 transform -translate-x-1/2">
        <router-link 
          to="/events" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-xl transition-glass relative flex items-center',
            route.path === '/' 
              ? 'text-gray-900 hover:bg-gray-100/50' 
              : 'text-gray-900 hover:bg-white/50'
          ]"
        >
          <span>All Events</span>
          <svg v-if="route.path === '/events'" class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </router-link>
        <router-link 
          to="/calendar" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-xl transition-glass relative flex items-center',
            route.path === '/' 
              ? 'text-gray-900 hover:bg-gray-100/50' 
              : 'text-gray-900 hover:bg-white/50'
          ]"
        >
          <span>Calendar</span>
          <svg v-if="route.path === '/calendar'" class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </router-link>
        <router-link 
          v-if="user?.role !== 'admin'"
          to="/my-requests" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-xl transition-glass relative flex items-center',
            route.path === '/' 
              ? 'text-gray-900 hover:bg-gray-100/50' 
              : 'text-gray-900 hover:bg-white/50'
          ]"
        >
          <span>My Requests</span>
          <svg v-if="route.path === '/my-requests'" class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </router-link>
        <router-link 
          v-if="user?.role === 'admin'"
          to="/admin" 
          :class="[
            'px-4 py-2 text-sm font-medium rounded-xl transition-glass relative flex items-center',
            route.path === '/' 
              ? 'text-gray-900 hover:bg-gray-100/50' 
              : 'text-gray-900 hover:bg-white/50'
          ]"
        >
          <span>Admin Panel</span>
          <svg v-if="route.path === '/admin'" class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </router-link>
      </div>
      
      <!-- Right Side: User Section -->
      <div class="flex items-center space-x-3">
        <router-link 
          to="/profile" 
          class="flex items-center space-x-2 hover:opacity-80 transition-opacity cursor-pointer"
        >
          <div :class="[
            'w-8 h-8 backdrop-blur-[20px] rounded-full flex items-center justify-center text-sm font-semibold border overflow-hidden transition-glass',
            route.path === '/' 
              ? 'bg-white/80 text-gray-900 border-gray-300/40' 
              : 'bg-white/60 text-gray-900 border-white/50'
          ]">
            <img 
              v-if="user?.photo_url" 
              :src="user.photo_url" 
              :alt="user?.full_name"
              class="w-full h-full object-cover"
            />
            <span v-else>
              {{ user?.full_name?.charAt(0)?.toUpperCase() || 'U' }}
            </span>
          </div>
          <span :class="[
            'text-sm font-medium hidden lg:inline',
            route.path === '/' ? 'text-gray-900' : 'text-gray-900'
          ]">
            {{ user?.full_name }}
          </span>
        </router-link>
        <button 
          @click="logout" 
          :class="[
            'px-4 py-2 text-sm font-medium backdrop-blur-[20px] rounded-xl transition-glass',
            route.path === '/' 
              ? 'text-gray-900 bg-white/80 border border-gray-300/40 hover:bg-white/90' 
              : 'text-gray-900 bg-white/50 border border-white/40 hover:bg-white/70'
          ]"
        >
          Logout
        </button>
      </div>
    </nav>
    <div class="flex flex-col min-h-screen">
      <div class="flex-grow">
        <router-view />
      </div>
      <Footer />
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
import JIHCLogo from './components/JIHCLogo.vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    JIHCLogo,
    Footer
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)

    const logout = () => {
      const wasAdmin = user.value?.role === 'admin'
      authStore.logout()
      router.push(wasAdmin ? '/admin/login' : '/login')
    }

    return {
      isAuthenticated,
      user,
      logout,
      route
    }
  }
}
</script>

>>>>>>> 694dc7c (the_last_update)
