import './assets/main.css'
import './styles/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
// import { createPinia } from 'pinia'
import VueApexCharts from 'vue3-apexcharts'
// 使用测试文件中的pinia实例
import pinia from './piniaTest.js'

import VueGoogleMaps from '@fawmi/vue-google-maps'

// 创建应用实例
const app = createApp(App)

// 使用插件
app.use(router)
app.use(pinia)
app.use(VueApexCharts)
app.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyCicNe0f0AyhwGXWlA5ASPtEqc8GXsR3-U',
    libraries: "places"
  },
})

// 添加全局配置
app.config.globalProperties.$api = {
  baseURL: 'http://localhost:8000',
  async getInfluencerGuide() {
    const response = await fetch(`${this.baseURL}/api/influencer-guide`)
    return response.json()
  },
  async getBestPractices() {
    const response = await fetch(`${this.baseURL}/api/best-practices`)
    return response.json()
  }
}

// 挂载应用
app.mount('#app')
