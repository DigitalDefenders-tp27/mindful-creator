<template>
    <div class="nature-sounds">
      <h2>Nature Sounds</h2>
      <p>Listen to calming sounds like rain, ocean waves, or forest.</p>
      <audio controls>
        <source src="@/assets/resources/forest.mp3" type="audio/mp3" />
        <source src="@/assets/resources/rain.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>
  </template>
  
  <script setup>
  // The component just plays a nature sound.
  </script>
  
  <style scoped>
  .nature-sounds {
    padding: 2rem;
    text-align: center;
  }
  
  audio {
    width: 100%;
    max-width: 500px;
    margin-top: 1rem;
  }
  </style>
  