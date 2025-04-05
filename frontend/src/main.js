import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/index.css'

const app = createApp(App)
app.use(router)

// Add global configuration
app.config.globalProperties.$api = {
  baseURL: 'http://localhost:5000',
  async getInfluencerGuide() {
    const response = await fetch(`${this.baseURL}/api/influencer-guide`)
    return response.json()
  },
  async getBestPractices() {
    const response = await fetch(`${this.baseURL}/api/best-practices`)
    return response.json()
  }
}

app.mount('#app')
