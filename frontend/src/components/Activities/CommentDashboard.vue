<template>
    <div class="comment-analyzer">
      <h2>Try Comment Classifier</h2>
      <input v-model="comment" placeholder="Paste a comment..." class="comment-input" />
      <button @click="submitComment" class="analyze-btn">Analyze</button>
  
      <div v-if="result" class="result-box">
        <p><strong>Type:</strong> {{ result.type }}</p>
        <ul>
          <li><strong>Step 1:</strong> {{ result.strategy.step1 }}</li>
          <li><strong>Step 2:</strong> {{ result.strategy.step2 }}</li>
          <li><strong>Step 3:</strong> {{ result.strategy.step3 }}</li>
        </ul>
        <p><strong>Suggested Reply:</strong> {{ result.reply }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  
  const comment = ref('')
  const result = ref(null)
  
  const submitComment = async () => {
    try {
      const res = await fetch('/api/classify-comment', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: comment.value })
      })
      result.value = await res.json()
    } catch (err) {
      console.error('Error fetching analysis:', err)
    }
  }
  </script>
  
  <style scoped>
  .comment-analyzer {
    padding: 2rem;
    text-align: center;
  }
  
  .comment-input {
    width: 80%;
    padding: 0.8rem;
    margin: 1rem 0;
    font-size: 1rem;
  }
  
  .analyze-btn {
    padding: 0.5rem 1rem;
    font-weight: bold;
    background: #4caf50;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
  }
  
  .result-box {
    margin-top: 1.5rem;
    text-align: left;
    background: #f4f4f4;
    padding: 1rem;
    border-radius: 8px;
  }
  </style>
  