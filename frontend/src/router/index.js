import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import EthicInfluencerView from '../views/EthicInfluencerView.vue'
import CriticalResponseView from '../views/CriticalResponseView.vue'
import RelaxationView from '../views/RelaxationView.vue'
import PasswordPage from '../components/PasswordPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }  // Protected route
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
      meta: { requiresAuth: true }
    },
    {
      path: '/password',
      name: 'password',
      component: PasswordPage  // Password page route
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = sessionStorage.getItem('authenticated');
  console.log(isAuthenticated);  

  // If route requires authentication, and user is not authenticated, redirect to the password page
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'password' })  // Redirect to password page if not authenticated
  } else {
    next()  // Allow access if authenticated
  }
})

export default router