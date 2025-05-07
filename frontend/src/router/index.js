import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EthicInfluencerView from '../views/EthicInfluencerView.vue'
import CriticalResponseView from '../views/CriticalResponseView.vue'
import RelaxationView from '../views/RelaxationView.vue'
// import PasswordPage from '../components/PasswordPage.vue'
import CreatorWellbeingView from '../views/CreatorWellbeingView.vue'
import PrivacyView from '../views/PrivacyView.vue'
import TestWebSocketView from '../views/TestWebSocketView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }  // Temporarily disabled auth
    },
    {
      path: '/ethic-influencer',
      name: 'ethic-influencer',
      component: EthicInfluencerView,
      meta: { requiresAuth: false }  // Temporarily disabled auth
    },
    {
      path: '/critical-response',
      name: 'critical-response',
      component: CriticalResponseView,
      meta: { requiresAuth: false }  // Temporarily disabled auth
    },
    {
      path: '/relaxation',
      name: 'relaxation',
      component: RelaxationView,
      meta: { requiresAuth: false }  // Temporarily disabled auth
    },
    {
      path: '/creator-wellbeing',
      name: 'creator-wellbeing',
      component: CreatorWellbeingView,
      meta: { requiresAuth: false }  // Temporarily disabled auth
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyView,
      meta: { requiresAuth: false } 
    },
    // {
    //   path: '/password',
    //   name: 'password',
    //   component: PasswordPage  // Password page route
    // },
    {
      path: '/websocket-test',
      name: 'websocket-test',
      component: TestWebSocketView,
      meta: { requiresAuth: false }
    }
  ],
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  // Temporarily disabled authentication
  next()
  
  // Original authentication logic (commented out)
  /*
  const isAuthenticated = sessionStorage.getItem('authenticated');
  console.log(isAuthenticated);

  // If route requires authentication, and user is not authenticated, redirect to the password page
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'password' })  // Redirect to password page if not authenticated
  } else {
    next()  // Allow access if authenticated
  }
  */
})

export default router
