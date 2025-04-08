<template>
    <div class="password-page">
      <h2>Enter Password to Access the Site</h2>
      <input v-model="password" type="password" placeholder="Enter password" />
      <button @click="checkPassword">Submit</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const password = ref('')
  const errorMessage = ref('')
  const router = useRouter()
  
  const correctPassword = '1234'  // Set your password here
  
  const checkPassword = () => {
    if (password.value === correctPassword) {
      sessionStorage.setItem('authenticated', 'true')
      console.log('Redirecting to /home')
      router.push('/home') // Redirect to the main app page
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
  }
  
  input {
    padding: 8px;
    margin-top: 10px;
    width: 200px;
  }
  
  button {
    margin-top: 10px;
    padding: 10px;
    background-color: #4f83ff;
    color: white;
    border: none;
    cursor: pointer;
    font-weight: bold;
    transition: 0.3s;
  }
  
  button:hover {
    background-color: #375ecf;
  }
  
  .error {
    color: red;
    margin-top: 10px;
  }
  </style>
  
  