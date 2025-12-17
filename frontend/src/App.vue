<template>
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
