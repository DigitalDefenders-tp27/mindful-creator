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

      <!-- Navigation Links -->
      <div class="navbar-center" :class="{ 'active': isMenuOpen }">
        <router-link to="/" class="nav-link" exact-active-class="active" @click="closeMenu"><span>HOME</span></router-link>
        <router-link to="/ethic-influencer" class="nav-link two-words" active-class="active" @click="closeMenu">
          <span>ETHIC</span>
          <span>INFLUENCER</span>
        </router-link>
        <router-link to="/critical-response" class="nav-link two-words" active-class="active" @click="closeMenu">
          <span>CRITICAL</span>
          <span>RESPONSE</span>
        </router-link>
        <router-link to="/relaxation" class="nav-link" active-class="active" @click="closeMenu"><span>RELAXATION</span></router-link>
        <router-link to="/comment-response-scripts" class="nav-link two-words" active-class="active" @click="closeMenu">
          <span>COMMENT</span>
          <span>RESPONSE</span>
        </router-link>
        <router-link to="/creator-wellbeing" class="nav-link two-words" active-class="active" @click="closeMenu">
          <span>CREATOR</span>
          <span>WELLBEING</span>
        </router-link>
        <router-link to="/privacy" class="nav-link" active-class="active" @click="closeMenu"><span>PRIVACY</span></router-link>
        <router-link to="/test" class="nav-link" active-class="active" @click="closeMenu"><span>TEST</span></router-link>
      </div>

      <!-- Hamburger Menu Button -->
      <div class="hamburger" @click="toggleMenu" :class="{ 'active': isMenuOpen }">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>

      <!-- Empty space to maintain layout balance -->
      <div class="navbar-right"></div>
    </div>

    <!-- Overlay - Click to close menu -->
    <div class="overlay" v-if="isMenuOpen" @click="closeMenu"></div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
// LiquidLogo component commented out until issues are resolved
// import LiquidLogo from './Activities/LiquidLogo/LiquidLogo.vue'

// Menu State Control
const isMenuOpen = ref(false)

// Toggle Menu Display State
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// Close Menu
const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<style scoped>
/* Navbar Container */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000; /* Increase z-index to ensure navbar is on top */
  background-color: rgba(255, 255, 255, 0.95); /* Increase opacity */
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  height: 80px; /* Increase navbar height */
  display: flex;
  align-items: center;
}

.navbar-container {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr; /* Three-part layout: left, centre, right */
  align-items: center;
  position: relative;
}

/* Left Logo Area */
.navbar-left {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* Left align */
  padding-left: 2rem; /* Restore padding */
}

/* Centre Navigation Links Area */
.navbar-center {
  display: flex;
  align-items: center;
  gap: 2.5rem; /* Increase spacing between links */
  justify-content: center; /* Centre align */
  position: relative; /* Change to relative positioning */
  transform: none; /* Remove transform */
}

/* Right empty space area to maintain layout balance */
.navbar-right {
  display: flex;
  justify-content: flex-end; /* Right align */
  padding-right: 2rem; /* Maintain padding */
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
  font-size: 1.5rem; /* Enlarge logo text */
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
  animation: liquidFlow 1.5s linear infinite; /* Speed up animation on hover */
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
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s;
  position: relative;
  text-decoration: none;
  letter-spacing: 0.5px;
  white-space: nowrap;
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
  flex-direction: column;
  align-items: center;
  line-height: 1.2;
  gap: 2px;
  text-align: center;
  width: max-content;
}

.nav-link.two-words span {
  display: block;
  white-space: nowrap;
  font-size: 0.9rem;
}

.nav-link:hover {
  color: #e75a97;
}

/* Hamburger Menu Button Styles */
.hamburger {
  display: none;
  cursor: pointer;
  z-index: 100; /* Increase z-index to ensure hamburger menu is on top */
  width: 35px;
  height: 30px;
  padding: 5px;
  position: absolute; /* Add absolute positioning */
  right: 2rem; /* Set right position */
  top: 50%; /* Vertical centre */
  transform: translateY(-50%); /* Precise vertical centring */
}

.bar {
  display: block;
  width: 25px;
  height: 3px;
  margin: 5px auto;
  transition: all 0.3s ease-in-out;
  background-color: #333;
  border-radius: 3px;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .navbar-container {
    grid-template-columns: 1fr 1fr; /* Two-column layout: left (logo) and right (hamburger menu) */
    padding: 0 1rem;
  }

  .navbar-center {
    position: fixed;
    left: -100%;
    top: 0;
    flex-direction: column;
    background-color: rgba(255, 255, 255, 0.95);
    width: 100%;
    height: 100vh;
    text-align: center;
    transition: 0.3s ease-in-out;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding-top: 100px; /* Adjust top padding to accommodate taller navbar */
    z-index: 90; /* Increase z-index to ensure it's on top */
    gap: 2rem;
    justify-content: flex-start;
    backdrop-filter: blur(10px);
  }

  .navbar-center.active {
    left: 0;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }

  .navbar-right {
    display: none; /* Hide right placeholder area on small screens */
  }

  .hamburger {
    display: block; /* Display hamburger menu */
    /* Other properties already defined in base settings, no need to repeat */
  }

  /* Prevent page scrolling when menu is open */
  body:has(.navbar-center.active) {
    overflow: hidden;
  }

  /* Hamburger Menu Animation */
  .hamburger.active .bar:nth-child(2) {
    opacity: 0;
  }

  .hamburger.active .bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
    background-color: #e75a97;
  }

  .hamburger.active .bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
    background-color: #e75a97;
  }

  /* Change link styles when menu is open */
  .navbar-center.active .nav-link {
    opacity: 0;
    animation: fadeIn 0.3s ease forwards;
    animation-delay: calc(0.1s * var(--i, 1));
    position: relative; /* Ensure positioning context */
  }

  .navbar-center .nav-link {
    font-size: 1.2rem;
    transition: transform 0.2s ease, color 0.2s ease;
  }
  
  /* Mobile navigation link styles */
  .navbar-center.active .nav-link span {
    font-size: 1.2rem;
  }
  
  /* Mobile Two-word Navigation Link Styles */
  .navbar-center.active .nav-link.two-words {
    flex-direction: row;
    gap: 8px;
    justify-content: center;
    padding: 0.5rem 0;
  }
  
  .navbar-center.active .nav-link.two-words span {
    font-size: 1.2rem;
  }

  .navbar-center .nav-link:active {
    transform: scale(0.95);
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Ensure the last navigation item has no bottom border */
  .nav-link:last-child {
    border-bottom: none !important;
  }
}

/* Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .navbar {
    height: 60px; /* Reduce height on small screens */
  }

  .navbar-container {
    padding: 0 0.5rem;
  }

  .navbar-left {
    padding-left: 0.5rem;
    max-width: 80%; /* Increase logo area width to allow text to display fully */
  }

  .logo {
    gap: 6px; /* Reduce spacing between logo and text */
  }

  .logo-text {
    font-size: 1rem; /* Reduce font size on smaller screens */
    white-space: nowrap; /* Prevent text wrapping */
    min-width: fit-content; /* Ensure text has its natural width */
  }

  .logo-img-container {
    height: 24px; /* Reduce logo size further on smaller screens */
    width: 24px;
    min-width: 24px; /* Ensure logo doesn't become too small due to flex scaling */
  }

  .navbar-center {
    padding-top: 80px; /* Adjust top padding for small screens */
  }

  .hamburger {
    right: 0.75rem; /* Reduce right distance to prevent overlap with logo */
    width: 30px; /* Reduce hamburger menu size */
    height: 25px;
  }

  .bar {
    width: 22px; /* Reduce hamburger menu bar width */
    height: 2px; /* Reduce hamburger menu bar height */
    margin: 4px auto; /* Reduce spacing */
  }

  .nav-link {
    font-size: 1.1rem;
    padding: 1rem 0;
    width: 80%;
    margin: 0 auto;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .nav-link:last-child {
    border-bottom: none;
  }

  .logo-text.liquid-text {
    font-size: 1rem;
    background-size: 150% auto; /* Reduce background size to fit smaller text */
  }
}

/* Extra small screen adjustments (e.g. iPhone SE) */
@media (max-width: 360px) {
  .navbar-left {
    max-width: 75%; /* Keep enough width for logo area */
  }

  .logo-text {
    font-size: 0.9rem; /* Slightly smaller font but still visible */
    white-space: nowrap; /* Ensure text stays on one line */
  }

  .logo-img-container {
    height: 22px; /* Even smaller logo */
    width: 22px;
    min-width: 22px;
    margin-right: -2px; /* Reduce space between logo and text */
  }

  .hamburger {
    right: 0.5rem; /* Further reduce right distance */
    transform: scale(0.9) translateY(-50%); /* Slightly reduce hamburger size */
  }

  .logo-text.liquid-text {
    font-size: 0.9rem;
    background-size: 120% auto; /* Further reduce background size */
  }
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

/* Overlay styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  z-index: 80; /* Below menu but above other content */
  backdrop-filter: blur(2px);
  opacity: 0;
  animation: fadeInOverlay 0.3s forwards;
}

@keyframes fadeInOverlay {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
