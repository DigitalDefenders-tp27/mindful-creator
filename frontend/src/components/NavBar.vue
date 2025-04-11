<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-left">
        <router-link to="/" class="logo">
          <img src="../assets/icons/elements/logo.svg" alt="Inflowence Logo" class="logo-img">
          <span class="logo-text">INFLOWENCE</span>
        </router-link>
      </div>

      <!-- 导航链接 / Navigation Links -->
      <div class="navbar-center" :class="{ 'active': isMenuOpen }">
        <router-link to="/" class="nav-link" @click="closeMenu">HOME</router-link>
        <router-link to="/ethic-influencer" class="nav-link" @click="closeMenu">ETHIC INFLUENCER</router-link>
        <router-link to="/critical-response" class="nav-link" @click="closeMenu">CRITICAL RESPONSE</router-link>
        <router-link to="/relaxation" class="nav-link" @click="closeMenu">RELAXATION</router-link>
        <router-link to="/comment-response-scripts" class="nav-link" @click="closeMenu">COMMENT RESPONSE</router-link>
      </div>

      <!-- 汉堡菜单按钮 / Hamburger Menu Button -->
      <div class="hamburger" @click="toggleMenu" :class="{ 'active': isMenuOpen }">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>

      <!-- 为了保持平衡的空占位区域 / Empty space to maintain layout balance -->
      <div class="navbar-right"></div>
    </div>

    <!-- 遮罩层 - 点击关闭菜单 / Overlay - Click to close menu -->
    <div class="overlay" v-if="isMenuOpen" @click="closeMenu"></div>
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
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background-color: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  height: 80px; /* 增加导航栏高度 / Increase navbar height */
  display: flex;
  align-items: center;
}

.navbar-container {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto 1fr; /* 三等分布局：左边、中间、右边 / Three-part layout: left, center, right */
  align-items: center;
  position: relative;
}

/* 左侧Logo区域 / Left Logo Area */
.navbar-left {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 左对齐 / Left align */
  padding-left: 2rem; /* 恢复内边距 / Restore padding */
}

/* 中间导航链接区域 / Center Navigation Links Area */
.navbar-center {
  display: flex;
  align-items: center;
  gap: 2.5rem; /* 增加链接之间的间距 / Increase spacing between links */
  justify-content: center; /* 居中对齐 / Center align */
  position: relative; /* 改为相对定位 / Change to relative positioning */
  transform: none; /* 移除transform / Remove transform */
}

/* 右侧空占位区域，保持布局平衡 / Right empty space area to maintain layout balance */
.navbar-right {
  display: flex;
  justify-content: flex-end; /* 右对齐 / Right align */
  padding-right: 2rem; /* 保持内边距 / Maintain padding */
}

/* Logo样式 / Logo Styles */
.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-img {
  height: 45px; /* 进一步增大 logo 尺寸 / Further increase logo size */
  width: auto;
}

.logo-text {
  font-size: 1.5rem; /* 放大logo文字 / Enlarge logo text */
  font-weight: bold;
  letter-spacing: 1px;
}

/* 导航链接样式 / Navigation Link Styles */
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

.nav-link:hover {
  color: #6c63ff;
}

/* 汉堡菜单按钮样式 / Hamburger Menu Button Styles */
.hamburger {
  display: none;
  cursor: pointer;
  z-index: 100; /* 增加z-index确保汉堡菜单在最上层 / Increase z-index to ensure hamburger menu is on top */
  width: 35px;
  height: 30px;
  padding: 5px;
  position: absolute; /* 添加绝对定位 / Add absolute positioning */
  right: 2rem; /* 设置右侧位置 / Set right position */
  top: 50%; /* 垂直居中 / Vertical center */
  transform: translateY(-50%); /* 精确垂直居中 / Precise vertical centering */
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

/* 响应式设计 / Responsive Design */
@media (max-width: 1024px) {
  .navbar-container {
    grid-template-columns: 1fr 1fr; /* 两列布局：左边(logo)和右边(汉堡菜单) / Two-column layout: left (logo) and right (hamburger menu) */
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
    padding-top: 100px; /* 调整顶部填充以适应更高的导航栏 / Adjust top padding to accommodate taller navbar */
    z-index: 90; /* 提高z-index确保在最上层 / Increase z-index to ensure it's on top */
    gap: 2rem;
    justify-content: flex-start;
    backdrop-filter: blur(10px);
  }

  .navbar-center.active {
    left: 0;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  }

  .navbar-right {
    display: none; /* 在小屏幕上隐藏右侧空占位区域 / Hide right placeholder area on small screens */
  }

  .hamburger {
    display: block; /* 显示汉堡菜单 / Display hamburger menu */
    /* 其他属性已在基本设置中定义，不需要重复 / Other properties already defined in base settings, no need to repeat */
  }

  /* 防止菜单开启时页面滚动 / Prevent page scrolling when menu is open */
  body:has(.navbar-center.active) {
    overflow: hidden;
  }

  /* 汉堡菜单动画 / Hamburger Menu Animation */
  .hamburger.active .bar:nth-child(2) {
    opacity: 0;
  }

  .hamburger.active .bar:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
    background-color: #6c63ff;
  }

  .hamburger.active .bar:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
    background-color: #6c63ff;
  }

  /* 菜单打开时改变链接样式 / Change link styles when menu is open */
  .navbar-center.active .nav-link {
    opacity: 0;
    animation: fadeIn 0.3s ease forwards;
    animation-delay: calc(0.1s * var(--i, 1));
    position: relative; /* 确保定位上下文 / Ensure positioning context */
  }

  .navbar-center .nav-link {
    font-size: 1.2rem;
    transition: transform 0.2s ease, color 0.2s ease;
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
}

/* 小屏幕响应式调整 / Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .navbar {
    height: 60px; /* 在小屏幕上减小高度 / Reduce height on small screens */
  }

  .navbar-container {
    padding: 0 0.5rem;
  }

  .navbar-left {
    padding-left: 0.5rem;
    max-width: 75%; /* 限制Logo区域最大宽度，防止与汉堡菜单重叠 / Limit logo area max width to prevent overlap with hamburger menu */
  }

  .logo {
    gap: 6px; /* 减小Logo与文字间距 / Reduce spacing between logo and text */
  }

  .logo-text {
    font-size: 1rem; /* 更小的屏幕上减小字体大小 / Reduce font size on smaller screens */
    max-width: calc(100% - 40px); /* 确保文本不会太长而溢出容器 / Ensure text doesn't overflow container */
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .logo-img {
    height: 28px; /* 更小的屏幕上减小logo尺寸 / Reduce logo size on smaller screens */
    min-width: 28px; /* 确保logo不会因为flex缩放而过小 / Ensure logo doesn't become too small due to flex scaling */
  }

  .navbar-center {
    padding-top: 80px; /* 为小屏幕调整顶部填充 / Adjust top padding for small screens */
  }

  .hamburger {
    right: 0.75rem; /* 减小右侧距离，防止与Logo重叠 / Reduce right distance to prevent overlap with logo */
    width: 30px; /* 缩小汉堡菜单尺寸 / Reduce hamburger menu size */
    height: 25px;
  }

  .bar {
    width: 22px; /* 缩小汉堡菜单线条宽度 / Reduce hamburger menu bar width */
    height: 2px; /* 缩小汉堡菜单线条高度 / Reduce hamburger menu bar height */
    margin: 4px auto; /* 减小间距 / Reduce spacing */
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
}

/* 超小屏幕调整（如iPhone SE等） / Extra small screen adjustments (e.g. iPhone SE) */
@media (max-width: 360px) {
  .navbar-left {
    max-width: 70%; /* 进一步限制Logo区域宽度 / Further limit logo area width */
  }

  .logo-text {
    font-size: 0.9rem; /* 更小的字体 / Smaller font */
  }

  .logo-img {
    height: 24px; /* 更小的logo / Smaller logo */
    min-width: 24px;
  }

  .hamburger {
    right: 0.5rem; /* 进一步减小右侧距离 / Further reduce right distance */
  }
}

/* 活动链接样式 / Active Link Styles */
.nav-link.active {
  color: #6c63ff;
  font-weight: 600;
}

/* 活动链接下划线 / Active Link Underline */
.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #6c63ff;
  transform: scaleX(1);
  transition: transform 0.2s;
}

/* 非活动链接下划线 / Inactive Link Underline */
.nav-link::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  right: 0;
  height: 3px;
  background-color: #6c63ff;
  transform: scaleX(0);
  transition: transform 0.2s;
}

/* 链接悬停效果 / Link Hover Effect */
.nav-link:hover::after {
  transform: scaleX(1);
}

/* 遮罩层样式 / Overlay styles */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  z-index: 80; /* 低于菜单但高于其他内容 / Below menu but above other content */
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
