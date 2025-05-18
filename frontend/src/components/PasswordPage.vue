<template>
    <div class="password-page">
      <div class="password-form">
        <h2>Enter Password to Access the Site</h2>
        <div class="input-group">
          <input v-model="password" type="password" placeholder="Enter password" @keyup.enter="checkPassword" />
          <button @click="checkPassword">Submit</button>
        </div>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
      
      <!-- Huge background elements -->
      <div class="huge-elements">
        <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Huge Flower" class="huge-element huge-flower-1">
        <img src="/src/assets/icons/elements/Flower_Orange.svg" alt="Huge Flower" class="huge-element huge-flower-2">
        <img src="/src/assets/icons/elements/Z_Pink.svg" alt="Huge Z Shape" class="huge-element huge-z-1">
        <img src="/src/assets/icons/elements/Flower_red.svg" alt="Huge Flower" class="huge-element huge-flower-3">
        <img src="/src/assets/icons/elements/Z_Red.svg" alt="Huge Z Shape" class="huge-element huge-z-2">
      </div>
      
      <!-- Decorative elements -->
      <div class="decorative-elements">
        <!-- Original elements -->
        <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element flower-pink">
        <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element flower-green">
        <img src="/src/assets/icons/elements/Flower_Orange.svg" alt="Flower" class="element flower-orange">
        <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element flower-pink-round">
        <img src="/src/assets/icons/elements/Flower_red.svg" alt="Flower" class="element flower-red">
        <img src="/src/assets/icons/elements/Z_Pink.svg" alt="Z Shape" class="element z-pink">
        <img src="/src/assets/icons/elements/Z_Red.svg" alt="Z Shape" class="element z-red">
        
        <!-- Additional elements (keeping only 3) -->
        <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element flower-pink-2">
        <img src="/src/assets/icons/elements/Flower_Orange.svg" alt="Flower" class="element flower-orange-2">
        <img src="/src/assets/icons/elements/Z_Pink.svg" alt="Z Shape" class="element z-pink-2">
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const password = ref('')
  const errorMessage = ref('')
  const router = useRouter()
  
  const correctPassword = '1234'  
  
  const checkPassword = () => {
    if (password.value === correctPassword) {
      sessionStorage.setItem('authenticated', 'true')
      router.push({ name: 'home' }) 
    } else {
      errorMessage.value = 'Incorrect password. Please try again.'
    }
  }

  </script>
  
  <style scoped>
  .password-page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #fefbf4;
    position: relative;
    overflow: hidden;
  }
  
  .password-form {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    max-width: 400px;
    z-index: 5;
  }
  
  .input-group {
    display: flex;
    width: 100%;
    margin-top: 12px;
    align-items: center;
  }
  
  input {
    padding: 8px;
    width: 100%;
    border-radius: 4px 0 0 4px;
    border: 1px solid #ddd;
    border-right: none;
    z-index: 5;
    height: 36px;
    box-sizing: border-box;
  }
  
  button {
    padding: 0 15px;
    height: 36px;
    background-color: #4f83ff;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    transition: 0.3s;
    border-radius: 0 4px 4px 0;
    z-index: 5;
    white-space: nowrap;
  }
  
  button:hover {
    background-color: #375ecf;
  }
  
  .error {
    color: red;
    margin-top: 10px;
    z-index: 5;
  }

  /* Huge background elements */
  .huge-elements {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    pointer-events: none;
  }
  
  .huge-element {
    position: absolute;
    transition: transform 8s ease;
    opacity: 0.2;
  }
  
  .huge-element:hover {
    transform: rotate(5deg) scale(1.05);
  }
  
  .huge-flower-1 {
    top: 5%;
    left: 5%;
    width: 15vw;
    height: 15vw;
    transform: rotate(-15deg);
  }
  
  .huge-flower-2 {
    bottom: 10%;
    right: 8%;
    width: 18vw;
    height: 18vw;
    transform: rotate(15deg);
  }
  
  .huge-z-1 {
    top: 40%;
    left: 8%;
    width: 20vw;
    height: 15vw;
    transform: rotate(-5deg);
  }
  
  .huge-flower-3 {
    top: 12%;
    right: 10%;
    width: 16vw;
    height: 16vw;
    transform: rotate(25deg);
  }
  
  .huge-z-2 {
    bottom: 15%;
    left: 30%;
    width: 18vw;
    height: 14vw;
    transform: rotate(-20deg);
  }

  /* Decorative elements */
  .decorative-elements {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 2;
    pointer-events: none;
  }
  
  .element {
    position: absolute;
    transition: transform 0.5s ease;
  }
  
  .element:hover {
    transform: rotate(15deg) scale(1.1);
  }
  
  /* Original 7 elements */
  .flower-pink {
    top: 15%;
    left: 10%;
    width: 80px;
  }
  
  .flower-green {
    top: 70%;
    right: 15%;
    width: 60px;
  }
  
  .flower-orange {
    bottom: 20%;
    left: 20%;
    width: 100px;
  }
  
  .flower-pink-round {
    top: 20%;
    right: 10%;
    width: 70px;
  }
  
  .flower-red {
    top: 40%;
    left: 5%;
    width: 60px;
  }
  
  .z-pink {
    bottom: 15%;
    right: 20%;
    width: 120px;
    opacity: 0.7;
  }
  
  .z-red {
    top: 80%;
    left: 15%;
    width: 100px;
    opacity: 0.6;
  }

  /* Additional elements - set 2 */
  .flower-pink-2 {
    top: 25%;
    right: 30%;
    width: 65px;
    transform: rotate(45deg);
    opacity: 0.8;
  }
  
  .flower-orange-2 {
    top: 10%;
    left: 40%;
    width: 85px;
    transform: rotate(20deg);
    opacity: 0.7;
  }
  
  .z-pink-2 {
    top: 5%;
    left: 60%;
    width: 90px;
    opacity: 0.5;
    transform: rotate(-10deg);
  }

  h2 {
    z-index: 5;
    margin-bottom: 10px;
    color: #333;
    text-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
    text-align: left;
    align-self: flex-start;
  }
  </style>
  
  