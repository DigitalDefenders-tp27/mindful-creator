<template>
  <div class="affirmation-reflection-plain">
    <h2>Affirmation Reflection</h2>
    <p>Read and reflect on positive affirmations for a mental reset.</p>
    <div class="audio-section">
      <audio controls preload="auto" class="affirmation-audio">
        <source src="/media/Affirmation Reflection Practice.MP3" type="audio/mpeg" />
        Your browser does not support the audio element.
      </audio>
      <div class="audio-caption">Listen to a calming affirmation practice</div>
    </div>
    <p class="activity-guide">
      Click to play, close your eyes,<br>and quietly enjoy this moment that belongs to you.
    </p>
    <!-- <ul>
      <li>"I am capable and strong."</li>
      <li>"I choose happiness over fear."</li>
      <li>"Every challenge is an opportunity for growth."</li>
      <li>"I trust myself and my abilities."</li>
      <li>"I am worthy of success and love."</li>
    </ul>
    <p>Take a moment to reflect on each one.</p> -->
  </div>
</template>

<script setup>
// No JS needed
</script>

<style scoped>
.affirmation-reflection-plain {
  padding: 0;
  margin: 0 auto;
  color: #222;
  text-align: center;
  max-width: 600px;
}
.affirmation-reflection-plain h2 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: #1a232b;
}
.affirmation-reflection-plain p {
  font-size: 1.15rem;
  margin: 1rem 0 1.2rem 0;
  color: #444;
}
.audio-section {
  margin: 1.5rem 0 2.2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.affirmation-audio {
  width: 100%;
  max-width: 420px;
  border-radius: 16px;
  margin-bottom: 0.5rem;
  border: none !important;
  outline: none !important;
  background: none !important;
  box-shadow: none !important;
}
.audio-caption {
  font-size: 1rem;
  color: #6CBDB5;
  margin-top: 0.2rem;
  font-weight: 500;
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
  