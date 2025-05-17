<template>
  <div class="dropdown-container">
    <!-- Hamburger Toggle Button -->
    <div class="hamburger" @click="toggleMenu" :class="{ 'active': isOpen }">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </div>
    
    <!-- Dropdown Menu -->
    <div class="dropdown-menu" :class="{ 'active': isOpen }">
      <slot></slot>
    </div>
    
    <!-- Overlay - Click to close menu -->
    <div class="overlay" v-if="isOpen" @click="closeMenu"></div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

// Props and emits
const emit = defineEmits(['update:open', 'close'])

// Menu State Control
const isOpen = ref(false)

// Toggle Menu Display State
const toggleMenu = () => {
  isOpen.value = !isOpen.value
  emit('update:open', isOpen.value)
}

// Close Menu
const closeMenu = () => {
  isOpen.value = false
  emit('update:open', false)
  emit('close')
}
</script>

<style scoped>
/* Hamburger Menu Button Styles */
.hamburger {
  display: block;
  cursor: pointer;
  z-index: 100;
  width: 35px;
  height: 30px;
  padding: 5px;
  position: absolute;
  right: 2rem;
  top: 50%;
  transform: translateY(-50%);
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

/* Dropdown Menu Styles */
.dropdown-menu {
  position: absolute;
  top: 80px;
  right: 3rem;
  left: auto;
  flex-direction: column;
  background-color: rgba(255, 255, 255, 0.98);
  width: fit-content;
  min-width: 200px;
  max-width: max-content;
  max-height: 0;
  overflow: hidden;
  text-align: right;
  transition: max-height 0.3s ease-in-out, opacity 0.2s ease-in-out, visibility 0.2s ease-in-out;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 90;
  padding: 0;
  margin: 0;
  opacity: 0;
  visibility: hidden;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  border-radius: 0 0 8px 8px;
  display: flex;
}

.dropdown-menu.active {
  max-height: 500px;
  padding: 0.5rem 0;
  opacity: 1;
  visibility: visible;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
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

/* Overlay styles */
.overlay {
  position: fixed;
  top: 60px;
  left: 0;
  width: 100%;
  height: calc(100vh - 60px);
  background: transparent;
  z-index: 85;
}

/* Small Screen Responsive Adjustments */
@media (max-width: 640px) {
  .dropdown-menu {
    top: 60px;
    min-width: 180px;
    max-width: max-content;
    right: 1.25rem;
  }
  
  .hamburger {
    right: 0.75rem;
    width: 30px;
    height: 25px;
  }
  
  .bar {
    width: 22px;
    height: 2px;
    margin: 4px auto;
  }
}

/* Extra small screen adjustments */
@media (max-width: 360px) {
  .dropdown-menu {
    min-width: 250px;
    max-width: 300px;
  }
  
  .hamburger {
    right: 0.5rem;
  }
}
</style> 