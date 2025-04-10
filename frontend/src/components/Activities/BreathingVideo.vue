<template>
    <div class="breathing-video">
      <h2>Breathing Exercise - 4-7-8 Breathing</h2>
      <p>Follow along with the video to perform a 4-7-8 breathing exercise to calm your mind.</p>
      <video controls>
        <source src="@/assets/resources/breathing.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  .breathing-video {
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
  }
  
  .breathing-video h2 {
    font-size: 24px;
    margin-bottom: 10px;
  }
  
  .breathing-video p {
    margin-bottom: 20px;
  }
  
  video {
    width: 100%;
    max-width: 600px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }
  </style>
  