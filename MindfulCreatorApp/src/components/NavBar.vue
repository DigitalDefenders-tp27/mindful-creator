<template>
  <nav class="navbar">
    <div class="navbar-left">
      <div class="logo">
        <img src="../components/icons/elements/Logo.svg" alt="Inflowence Logo" class="logo-img">
        <span class="logo-text">Inflowence</span>
      </div>
    </div>
    <div class="navbar-right">
      <router-link to="/">Home</router-link>
      <router-link to="/ethic-influencer">Mindful Creator</router-link>
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
  gap: 0.5rem;
}

.logo-img {
  height: 32px;
  width: auto;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: bold;
  color: black;
}

.navbar-right {
  display: flex;
  gap: 1rem;
}

.navbar-right a {
  color: black;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.navbar-right a:hover {
  background-color: rgb(232, 107, 164);
  color: white;
}

.navbar-right a.router-link-active {
  background-color: rgb(232, 107, 164);
  color: white;
}
</style> 