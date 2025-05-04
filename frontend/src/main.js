import './assets/main.css'
import './styles/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import VueApexCharts from 'vue3-apexcharts'
import pinia from './piniaTest.js'

import VueGoogleMaps from '@fawmi/vue-google-maps'


const app = createApp(App)


app.use(router)
app.use(pinia)
app.use(VueApexCharts)
app.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCicNe0f0AyhwGXWlA5ASPtEqc8GXsR3-U',
    libraries: "places"
  },
})

app.config.globalProperties.$api = {
  baseURL: 'https://api.tiezhu.org',
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
