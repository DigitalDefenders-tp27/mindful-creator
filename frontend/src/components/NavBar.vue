<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <router-link to="/" class="logo">
          <div class="logo-img-container">
            <img src="/src/assets/icons/elements/logo.svg" alt="Inflowence Logo" class="logo-img">
          </div>
          <span class="logo-text liquid-text">INFLOWENCE</span>
        </router-link>
      </div>

      <!-- Desktop Navigation Links -->
      <div class="navbar-center" :class="{ 'desktop-only': isMobile }">
        <router-link to="/" class="nav-link" exact-active-class="active"><span>HOME</span></router-link>
        <router-link to="/ethic-influencer" class="nav-link two-words" active-class="active">
          <span>ETHIC</span>
          <span>INFLUENCER</span>
        </router-link>
        <router-link to="/creator-wellbeing" class="nav-link two-words" active-class="active">
          <span>CREATOR </span>
          <span>WELLBEING</span>
        </router-link>
        <router-link to="/critical-response" class="nav-link two-words" active-class="active">
          <span>CRITICAL </span>
          <span>RESPONSE</span>
        </router-link>
        <router-link to="/privacy" class="nav-link" active-class="active"><span>PRIVACY</span></router-link>
        <router-link to="/copyright" class="nav-link" active-class="active"><span>COPYRIGHT</span></router-link>
        <router-link to="/relaxation" class="nav-link" active-class="active">
          <span>RELAXATION</span>
        </router-link>
        <router-link to="/games" class="nav-link two-words" active-class="active">
          <span>MEME </span>
          <span>GAME</span>
        </router-link>
      </div>

      <!-- Mobile Dropdown Menu -->
      <div v-if="isMobile" class="dropdown-wrapper">
        <DropDownMenu v-model:open="isMenuOpen" @close="closeMenu">
          <router-link to="/" class="dropdown-nav-item" exact-active-class="active" @click="closeMenu"><span>HOME</span></router-link>
          <router-link to="/ethic-influencer" class="dropdown-nav-item two-words" active-class="active" @click="closeMenu">
            <span>ETHIC</span>
            <span>INFLUENCER</span>
          </router-link>
          <router-link to="/creator-wellbeing" class="dropdown-nav-item two-words" active-class="active" @click="closeMenu">
            <span>CREATOR </span>
            <span>WELLBEING</span>
          </router-link>
          <router-link to="/critical-response" class="dropdown-nav-item two-words" active-class="active" @click="closeMenu">
            <span>CRITICAL </span>
            <span>RESPONSE</span>
          </router-link>
          <router-link to="/privacy" class="dropdown-nav-item" active-class="active" @click="closeMenu"><span>PRIVACY</span></router-link>
          <router-link to="/copyright" class="dropdown-nav-item" active-class="active" @click="closeMenu"><span>COPYRIGHT</span></router-link>
          <router-link to="/relaxation" class="dropdown-nav-item" active-class="active" @click="closeMenu">
            <span>RELAXATION</span>
          </router-link>
          <router-link to="/games" class="dropdown-nav-item two-words" active-class="active" @click="closeMenu">
            <span>MEME </span>
            <span>GAME</span>
          </router-link>
        </DropDownMenu>
      </div>

      <!-- Empty space to maintain layout balance -->
      <div class="navbar-right"></div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import DropDownMenu from './DropDownMenu.vue'
import './NavItemStyles.vue'

// Screen width tracking
const windowWidth = ref(window.innerWidth)
const isMobile = computed(() => windowWidth.value <= 1280)

// Menu State Control
const isMenuOpen = ref(false)

// Close Menu
const closeMenu = () => {
  isMenuOpen.value = false
}

// Window resize handling
const updateWindowWidth = () => {
  windowWidth.value = window.innerWidth
}

onMounted(() => {
  window.addEventListener('resize', updateWindowWidth)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateWindowWidth)
})
</script>

<style scoped>
/* Navbar Container */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  height: 80px;
  display: flex;
  align-items: center;
}

.navbar-container {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  position: relative;
}

/* Left Logo Area */
.navbar-left {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding-left: 3rem;
}

/* Centre Navigation Links Area */
.navbar-center {
  display: flex;
  align-items: center;
  gap: 3rem;
  justify-content: center;
  position: relative;
  transform: none;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.navbar-center.desktop-only {
  display: none;
}

/* Right empty space area */
.navbar-right {
  display: flex;
  justify-content: flex-end;
  padding-right: 3rem;
}

/* Logo Styles */
.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-img-container {
  height: 45px;
  width: 45px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-img {
  height: 100%;
  width: 100%;
  object-fit: contain;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 1px;
}

/* Liquid text effect */
.liquid-text {
  position: relative;
  background: linear-gradient(
    to right,
    #e75a97 20%,
    #4d8cd5 40%,
    #4d8cd5 60%,
    #e75a97 80%
  );
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  animation: liquidFlow 3s linear infinite;
  filter: drop-shadow(0 0 1px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
}

.liquid-text:hover {
  filter: drop-shadow(0 0 2px rgba(231, 90, 151, 0.5));
  transform: scale(1.02);
  animation: liquidFlow 1.5s linear infinite;
}

@keyframes liquidFlow {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

/* Navigation Link Styles */
.nav-link {
  color: #555;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
  text-decoration: none;
  letter-spacing: 0.5px;
  white-space: nowrap;
  padding: 0.5rem 0;
}

/* Single word navigation link styles */
.nav-link span {
  display: block;
  white-space: nowrap;
  font-size: 0.9rem;
  font-weight: 500;
}

/* Two-word Navigation Link Styles */
.nav-link.two-words {
  display: flex;
  flex-direction: row;
  align-items: center;
  line-height: 1.3;
  gap: 6px;
  text-align: center;
  width: max-content;
}

.nav-link.two-words span {
  display: inline;
  white-space: nowrap;
  font-size: 0.9rem;
}

.nav-link:hover {
  color: #e75a97;
}

/* Mobile dropdown wrapper */
.dropdown-wrapper {
  position: absolute;
  right: 0;
  top: 0;
  height: 100%;
}

/* Active Link Styles */
.nav-link.active {
  color: #e75a97;
  font-weight: 600;
}

/* Active Link Underline */
.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #e75a97;
  transform: scaleX(1);
  transition: transform 0.2s;
}

/* Two-word Active Link Underline */
.nav-link.two-words.active::after {
  bottom: -8px;
}

/* Inactive Link Underline */
.nav-link::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #e75a97;
  transform: scaleX(0);
  transition: transform 0.2s;
}

/* Link Hover Effect */
.nav-link:hover::after {
  transform: scaleX(1);
}

/* Desktop vs mobile navigation display */
@media (min-width: 1281px) {
  .navbar-center {
    display: flex;
  }
}

/* Two-word nav items display in column when under 1500px */
@media (max-width: 1500px) {
  .nav-link.two-words {
    flex-direction: column;
    gap: 2px;
    text-align: center;
    line-height: 1.1;
  }
  
  .nav-link.two-words span {
    text-align: center;
  }
  
  /* Adjust active link underline position for two-word links */
  .nav-link.two-words.active::after {
    bottom: -12px;
  }
}

/* Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .navbar {
    height: 60px;
  }

  .navbar-container {
    padding: 0 0.5rem;
  }

  .navbar-left {
    padding-left: 0.5rem;
    max-width: 80%;
  }

  .logo {
    gap: 6px;
  }

  .logo-text {
    font-size: 1rem;
    white-space: nowrap;
    min-width: fit-content;
  }

  .logo-img-container {
    height: 24px;
    width: 24px;
    min-width: 24px;
  }

  .logo-text.liquid-text {
    font-size: 1rem;
    background-size: 150% auto;
  }
}

/* Extra small screen adjustments (e.g. iPhone SE) */
@media (max-width: 360px) {
  .navbar-left {
    max-width: 75%;
  }

  .logo-text {
    font-size: 0.9rem;
    white-space: nowrap;
  }

  .logo-img-container {
    height: 22px;
    width: 22px;
    min-width: 22px;
    margin-right: -2px;
  }

  .logo-text.liquid-text {
    font-size: 0.9rem;
    background-size: 120% auto;
  }
}
</style>
