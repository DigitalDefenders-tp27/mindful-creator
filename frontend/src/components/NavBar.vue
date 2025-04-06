<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link to="/" class="logo">
        <img src="../components/icons/elements/Logo.svg" alt="Inflowence Logo" class="logo-img">
        <span class="logo-text">INFLOWENCE</span>
      </router-link>
    </div>
    
    <!-- 汉堡菜单按钮 -->
    <div class="hamburger" @click="toggleMenu" :class="{ 'active': isMenuOpen }">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </div>
    
    <!-- 导航链接 -->
    <div class="navbar-right" :class="{ 'active': isMenuOpen }">
      <router-link to="/" class="nav-link" @click="closeMenu">HOME</router-link>
      <router-link to="/about" class="nav-link" @click="closeMenu">ABOUT</router-link>
      <router-link to="/ethic-influencer" class="nav-link" @click="closeMenu">ETHIC INFLUENCER</router-link>
      <router-link to="/creator-wellbeing" class="nav-link" @click="closeMenu">CREATOR WELLBEING</router-link>
      <router-link to="/critical-response" class="nav-link" @click="closeMenu">CRITICAL RESPONSE</router-link>
      <router-link to="/privacy" class="nav-link" @click="closeMenu">PRIVACY</router-link>
      <router-link to="/copyright" class="nav-link" @click="closeMenu">COPYRIGHT</router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'

const isMenuOpen = ref(false)

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
  padding: 1rem 2rem;
  margin-bottom: 0;
  border-bottom: 1px solid #ddd;
  position: relative;
}

.navbar-left {
  display: flex;
  align-items: center;
  z-index: 10;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  text-decoration: none;
}

.logo-img {
  height: 36px;
  width: auto;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: black;
  letter-spacing: 0.02em;
}

.navbar-right {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: black;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

.nav-link.router-link-active {
  background-color: #FF69B4;
  color: white;
}

.nav-link:hover:not(.active) {
  background-color: rgba(255, 105, 180, 0.1);
}

/* 汉堡菜单按钮样式 */
.hamburger {
  display: none;
  cursor: pointer;
  z-index: 10;
}

.bar {
  display: block;
  width: 25px;
  height: 3px;
  margin: 5px auto;
  transition: all 0.3s ease-in-out;
  background-color: black;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  .hamburger {
    display: block;
  }
  
  .navbar-right {
    position: fixed;
    left: -100%;
    top: 0;
    flex-direction: column;
    background-color: white;
    width: 100%;
    height: 100vh;
    text-align: center;
    transition: 0.3s;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding-top: 80px;
    z-index: 5;
  }
  
  .navbar-right.active {
    left: 0;
  }
  
  .navbar-right .nav-link {
    margin: 1rem 0;
    font-size: 1.1rem;
  }
  
  /* 汉堡菜单动画 */
  .hamburger.active .bar:nth-child(2) {
    opacity: 0;
  }
  
  .hamburger.active .bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
  }
  
  .hamburger.active .bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
  }
}

@media (max-width: 640px) {
  .logo-text {
    font-size: 1.2rem;
  }
  
  .logo-img {
    height: 30px;
  }
}
</style> 