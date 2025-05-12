import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EthicInfluencerView from '../views/EthicInfluencerView.vue'
import CriticalResponseView from '../views/CriticalResponseView.vue'
import RelaxationView from '../views/RelaxationView.vue'
import PasswordPage from '../components/PasswordPage.vue'
import CreatorWellbeingView from '../views/CreatorWellbeingView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import CopyrightView from '../views/CopyrightView.vue'
import TestWebSocketView from '../views/TestWebSocketView.vue'
import GameView from '../views/GameView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/ethic-influencer',
      name: 'ethic-influencer',
      component: EthicInfluencerView,
      meta: { requiresAuth: true }
    },
    {
      path: '/critical-response',
      name: 'critical-response',
      component: CriticalResponseView,
      meta: { requiresAuth: true }
    },
    {
      path: '/relaxation',
      name: 'relaxation',
      component: RelaxationView,
      meta: { requiresAuth: false }
    },
    {
      path: '/games',
      name: 'games',
      component: GameView,
      meta: { requiresAuth: false }
    },
    {
      path: '/creator-wellbeing',
      name: 'creator-wellbeing',
      component: CreatorWellbeingView,
      meta: { requiresAuth: true }
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyView,
      meta: { requiresAuth: true } 
    },
    {
      path: '/copyright',
      name: 'copyright',
      component: CopyrightView,
      meta: { requiresAuth: true } 
    },
    {
      path: '/password',
      name: 'password',
      component: PasswordPage
    },
    {
      path: '/websocket-test',
      name: 'websocket-test',
      component: TestWebSocketView,
      meta: { requiresAuth: true }
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('authenticated');
  console.log('Authentication status:', isAuthenticated);

  // If route requires authentication, and user is not authenticated, redirect to the password page
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'password' });  // Redirect to password page if not authenticated
  } else {
    next();  // Allow access if authenticated or route doesn't require auth
  }
})

export default router
