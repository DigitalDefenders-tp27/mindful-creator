import { createApp } from 'vue'
import App from './MindfulCreatorApp/src/App.vue'
import router from './MindfulCreatorApp/src/router'

const app = createApp(App)
app.use(router)
app.mount('#app') 