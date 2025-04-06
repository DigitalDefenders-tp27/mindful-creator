<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link to="/" class="logo">
        <img src="../components/icons/elements/Logo.svg" alt="Inflowence Logo" class="logo-img">
        <span class="logo-text">INFLOWENCE</span>
      </router-link>
    </div>
    
    <!-- 汉堡菜单按钮 / Hamburger Menu Button -->
    <div class="hamburger" @click="toggleMenu" :class="{ 'active': isMenuOpen }">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </div>
    
    <!-- 导航链接 / Navigation Links -->
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

// 菜单状态控制 / Menu State Control
const isMenuOpen = ref(false)

// 切换菜单显示状态 / Toggle Menu Display State
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 关闭菜单 / Close Menu
const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<style scoped>
/* 导航栏容器 / Navbar Container */
.navbar {
  @apply fixed top-0 left-0 right-0 z-50;
  @apply bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md;
  @apply border-b border-neutral-200 dark:border-neutral-800;
  @apply px-4 py-3;
}

/* 导航栏内容布局 / Navbar Content Layout */
.navbar-content {
  @apply max-w-7xl mx-auto;
  @apply flex items-center justify-between;
}

/* 左侧Logo区域 / Left Logo Area */
.navbar-left {
  @apply flex items-center;
}

/* Logo样式 / Logo Styles */
.logo {
  @apply text-xl font-bold text-neutral-900 dark:text-white;
  @apply hover:text-blue-600 dark:hover:text-blue-400;
  @apply transition-colors duration-200;
}

/* 右侧导航链接区域 / Right Navigation Links Area */
.navbar-right {
  @apply flex items-center space-x-6;
}

/* 导航链接样式 / Navigation Link Styles */
.nav-link {
  @apply text-neutral-600 dark:text-neutral-400;
  @apply hover:text-blue-600 dark:hover:text-blue-400;
  @apply transition-colors duration-200;
  @apply relative;
}

/* 活动链接样式 / Active Link Styles */
.nav-link.active {
  @apply text-blue-600 dark:text-blue-400;
  @apply font-medium;
}

/* 活动链接下划线 / Active Link Underline */
.nav-link.active::after {
  content: '';
  @apply absolute bottom-0 left-0 right-0;
  @apply h-0.5 bg-blue-600 dark:bg-blue-400;
  @apply transform scale-x-100;
  @apply transition-transform duration-200;
}

/* 非活动链接下划线 / Inactive Link Underline */
.nav-link::after {
  content: '';
  @apply absolute bottom-0 left-0 right-0;
  @apply h-0.5 bg-blue-600 dark:bg-blue-400;
  @apply transform scale-x-0;
  @apply transition-transform duration-200;
}

/* 链接悬停效果 / Link Hover Effect */
.nav-link:hover::after {
  @apply transform scale-x-100;
}

/* 响应式调整 / Responsive Adjustments */
@media (max-width: 768px) {
  .navbar {
    @apply px-3 py-2;
  }

  .navbar-right {
    @apply space-x-4;
  }

  .nav-link {
    @apply text-sm;
  }
}

/* 汉堡菜单按钮样式 / Hamburger Menu Button Styles */
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

/* 响应式设计 / Responsive Design */
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
  
  /* 汉堡菜单动画 / Hamburger Menu Animation */
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

/* 小屏幕响应式调整 / Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .logo-text {
    font-size: 1.2rem;
  }
  
  .logo-img {
    height: 30px;
  }
}
</style> 