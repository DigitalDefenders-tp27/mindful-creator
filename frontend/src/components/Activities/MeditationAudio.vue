<template>
    <div class="meditation-audio">
      <h2 class="activity-title">Guided Meditation</h2>
      <p class="activity-desc">Listen to a short meditation audio to relax and refocus.</p>
      <audio controls>
        <source src="/media/meditation.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
      <p class="activity-guide">
        Click to play, close your eyes, and quietly enjoy this moment that belongs to you.
      </p>
    </div>
  </template>
  
  <script setup>
  // No special setup needed for audio, it's just for playback
  </script>
  
  <style scoped>
  .meditation-audio {
    padding: 0;
    text-align: center;
    margin: 0 auto;
    max-width: 600px;
  }
  
  .activity-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: #23292f;
    text-align: center;
    margin-top: 1.5rem;
    margin-bottom: 1.2rem;
  }

  .activity-desc {
    font-size: 1.35rem;
    color: #444;
    font-weight: 400;
    text-align: center;
    margin-bottom: 2.2rem;
    margin-top: 0;
    letter-spacing: 0.01em;
  }

  audio {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    display: block;
    border-radius: 8px;
  }

  .activity-guide {
    font-size: 1.15rem;
    color: #444;
    font-weight: 400;
    text-align: center;
    margin: 1.2rem 0 0 0;
    letter-spacing: 0.01em;
    font-style: normal;
    background: none;
    padding: 0;
    border-radius: 0;
    box-shadow: none;
    opacity: 1;
  }
  </style>
  