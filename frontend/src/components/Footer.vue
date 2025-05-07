<template>
  <footer class="footer">
    <div class="container">
      <div class="flags-container">
        <div class="flag-wrapper">
          <img src="@/assets/flags/aus.png" alt="Australian Flag" class="flag" />
        </div>
        <div class="flag-wrapper">
          <img src="@/assets/flags/abo.png" alt="Aboriginal Flag" class="flag" />
        </div>
        <div class="flag-wrapper">
          <img src="@/assets/flags/islander.jpg" alt="Torres Strait Islander Flag" class="flag" />
        </div>
        <div class="flag-wrapper">
          <img src="@/assets/flags/pride.jpg" alt="Pride Flag" class="flag" />
        </div>
      </div>
      
      <div class="acknowledgment">
        <p>
          Inflowence respect and honour Aboriginal and Torres Strait Islander Elders past, present, and future. We acknowledge the stories, traditions, and living cultures of Aboriginal and Torres Strait Islander peoples on this land and commit to building a brighter future together.
        </p>
      </div>
      
      <div class="logo-container">
        <div class="footer-logo">
          <div class="logo-img-container">
            <img src="/src/assets/icons/elements/logo.svg" alt="Inflowence Logo" class="logo-img">
          </div>
          <span class="logo-text liquid-text">INFLOWENCE</span>
        </div>
        <p class="copyright">© {{ currentYear }} INFLOWENCE</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';

const currentYear = ref(new Date().getFullYear());
</script>

<style scoped>
.footer {
  background: linear-gradient(to right, rgba(231, 90, 151, 0.1), rgba(77, 140, 213, 0.1));
  padding: 3rem 0 2rem;
  margin-top: 3rem;
  width: 100%;
  border-top: none;
  border-image: none;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 1rem;
  padding-bottom: 1.5rem;
  padding-left: 1.5rem;
  padding-right: 1.5rem;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  position: relative;
  overflow: hidden;
}

.container::before {
  display: none;
}

.flags-container {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 6rem;
  margin-bottom: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
}

.flag-wrapper {
  width: 60px;
  height: 40px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.flag {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.flag:hover {
  transform: scale(1.05);
}

.acknowledgment {
  text-align: center;
  margin-top: 4rem;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  padding-top: 0;
}

.acknowledgment p {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #444;
  background: transparent;
  padding: 0.5rem 1.5rem 1.5rem;
  border-radius: 0;
  box-shadow: none;
}

.logo-container {
  text-align: center;
  margin-top: 1rem;
  padding: 1rem;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
}

.footer-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 0.5rem;
}

.logo-img-container {
  height: 40px;
  width: 40px;
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
}

@keyframes liquidFlow {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

.copyright {
  font-size: 0.85rem;
  color: #555;
  margin-top: 0.5rem;
  position: relative;
}

.copyright::before {
  display: none;
}

@media (max-width: 768px) {
  .flags-container {
    flex-wrap: wrap;
    gap: 1.5rem;
    margin-top: 3rem;
  }
  
  .flag-wrapper {
    width: 50px;
    height: 33px;
  }
  
  .acknowledgment {
    margin-top: 1.5rem;
  }
  
  .acknowledgment p {
    font-size: 0.85rem;
  }
  
  .logo-text {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  .flags-container {
    gap: 1rem;
    margin-top: 2.5rem;
  }
  
  .flag-wrapper {
    width: 45px;
    height: 30px;
  }
}
</style>
