<template>
    <div class="journal-prompt">
      <h2>Mini Journal Prompt</h2>
      <p>Write one sentence about how you’re feeling right now.</p>
      <textarea v-model="entry" rows="4" placeholder="Write here..."></textarea>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const entry = ref('')
  </script>
  
  <style scoped>
  .journal-prompt {
    padding: 2rem;
    text-align: center;
  }
  
  textarea {
    width: 80%;
    max-width: 500px;
    padding: 12px;
    margin-top: 1rem;
    font-size: 14px;
    resize: none;
  }
  </style>
  