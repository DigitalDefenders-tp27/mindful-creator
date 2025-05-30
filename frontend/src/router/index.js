import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EthicInfluencerView from '../views/EthicInfluencerView.vue'
import CriticalResponseView from '../views/CriticalResponseView.vue'
import RelaxationView from '../views/RelaxationView.vue'
import CreatorWellbeingView from '../views/CreatorWellbeingView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import CopyrightView from '../views/CopyrightView.vue'
import TestWebSocketView from '../views/TestWebSocketView.vue'
import GameView from '../views/GameView.vue'
import VisualisationView from '../views/Visualisation.vue'

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
    },
    {
      path: '/critical-response',
      name: 'critical-response',
      component: CriticalResponseView
    },
    {
      path: '/relaxation',
      name: 'relaxation',
      component: RelaxationView
    },
    {
      path: '/games',
      name: 'games',
      component: GameView
    },
    {
      path: '/creator-wellbeing',
      name: 'creator-wellbeing',
      component: CreatorWellbeingView
    },
    {
      path: '/visualisation',
      name: 'visualisation',
      component: VisualisationView
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyView
    },
    {
      path: '/copyright',
      name: 'copyright',
      component: CopyrightView
    },
    {
      path: '/websocket-test',
      name: 'websocket-test',
      component: TestWebSocketView
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

export default router
