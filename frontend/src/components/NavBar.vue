<template>
  <nav class="navbar">
    <div class="navbar-left">
      <router-link to="/" class="logo">
        <img src="../components/icons/elements/Logo.svg" alt="Inflowence Logo" class="logo-img">
        <span class="logo-text">INFLOWENCE</span>
      </router-link>
    </div>
    <div class="navbar-right">
      <router-link to="/" class="nav-link">HOME</router-link>
      <router-link to="/about" class="nav-link">ABOUT</router-link>
      <router-link to="/ethic-influencer" class="nav-link">ETHIC INFLUENCER</router-link>
      <router-link to="/creator-wellbeing" class="nav-link">CREATOR WELLBEING</router-link>
      <router-link to="/critical-response" class="nav-link">CRITICAL RESPONSE</router-link>
      <router-link to="/privacy" class="nav-link">PRIVACY</router-link>
      <router-link to="/copyright" class="nav-link">COPYRIGHT</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar'
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
}

.navbar-left {
  display: flex;
  align-items: center;
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
</style> 