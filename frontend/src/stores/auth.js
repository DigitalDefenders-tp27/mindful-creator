import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false)
  const user = ref(null)
  
  // Check if user is authenticated from session storage on store initialization
  if (sessionStorage.getItem('authenticated') === 'true') {
    isAuthenticated.value = true
  }
  
  function login() {
    isAuthenticated.value = true
    sessionStorage.setItem('authenticated', 'true')
  }
  
  function logout() {
    isAuthenticated.value = false
    user.value = null
    sessionStorage.removeItem('authenticated')
  }
  
  function checkAuth() {
    return isAuthenticated.value || sessionStorage.getItem('authenticated') === 'true'
  }
  
  return {
    isAuthenticated,
    user,
    login,
    logout,
    checkAuth
  }
}) 