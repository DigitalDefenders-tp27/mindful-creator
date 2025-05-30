import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  
  // Authentication removed - all users have direct access
  
  return {
    user
  }
}) 