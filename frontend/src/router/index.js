import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EthicInfluencerView from '../views/EthicInfluencerView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/ethic-influencer',
      name: 'ethic-influencer',
      component: EthicInfluencerView
    }
  ]
})

export default router 