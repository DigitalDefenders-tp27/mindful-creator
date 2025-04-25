import './assets/main.css'
import './styles/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import VueApexCharts from 'vue3-apexcharts'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.use(VueApexCharts)

// Add global configuration
app.config.globalProperties.$api = {
  baseURL: 'http://localhost:5001',
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
