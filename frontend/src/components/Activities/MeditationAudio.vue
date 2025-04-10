<template>
    <div class="meditation-audio">
      <h2>Guided Meditation</h2>
      <p>Listen to a short meditation audio to relax and refocus.</p>
      <audio controls>
        <source src="/media/meditation.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>
  </template>
  
  <script setup>
  // No special setup needed for audio, it's just for playback
  </script>
  
  <style scoped>
  .meditation-audio {
    padding: 2rem;
    text-align: center;
    margin-top: -1rem; 
  }
  
  .meditation-audio h2 {
  font-size: 26px;
  margin-bottom: 0.4rem;
  }

  .meditation-audio p {
    font-size: 16px;
    margin-bottom: 1.5rem;
    color: #555;
  }

  audio {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    display: block;
    border-radius: 8px;
  }
  </style>
  