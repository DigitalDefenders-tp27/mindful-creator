<template>
  <div class="activity-plain">
    <h2>Nature Sounds</h2>
    <p class="nature-desc">Listen to calming sounds like rain or forest.</p>
    <div class="audio-section">
      <div class="audio-block">
        <img src="/media/Forest.svg" alt="Forest Icon" class="nature-icon-full" />
        <div class="nature-label">Forest</div>
        <audio controls class="nature-audio">
          <source src="/media/forest.mp3" type="audio/mp3" />
          Your browser does not support the audio element.
        </audio>
      </div>
      <div class="audio-block">
        <img src="/media/Rain.svg" alt="Rain Icon" class="nature-icon-full" />
        <div class="nature-label">Rain</div>
        <audio controls class="nature-audio">
          <source src="/media/rain.mp3" type="audio/mp3" />
          Your browser does not support the audio element.
        </audio>
      </div>
    </div>
    <p class="activity-guide">
      Click to play, close your eyes,<br>and quietly enjoy this moment that belongs to you.
    </p>
  </div>
</template>

<script setup>
// No JS needed
</script>

<style scoped>
.activity-plain {
  padding: 0;
  margin: 0 auto;
  color: #222;
  text-align: center;
  max-width: 600px;
}
.activity-plain h2 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: #1a232b;
}
.nature-desc {
  font-size: 1.15rem;
  margin: 1rem 0 2.2rem 0;
  color: #444;
}
.audio-section {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 2.7rem;
  align-items: center;
}
.audio-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.nature-icon-full {
  width: 100%;
  max-width: 420px;
  height: 90px;
  object-fit: cover;
  margin-bottom: 0.5rem;
  border-radius: 14px;
  box-shadow: none !important;
  background: none !important;
  border: none !important;
  display: block;
}
.nature-label {
  font-size: 1.08rem;
  color: #6CBDB5;
  font-weight: 600;
  margin-bottom: 0.7rem;
  letter-spacing: 0.03em;
}
.nature-audio {
  width: 100%;
  max-width: 420px;
  background: none !important;
  border-radius: 12px;
  margin-bottom: 0.2rem;
  box-shadow: none !important;
  border: none !important;
  outline: none !important;
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

  