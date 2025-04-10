<template>
  <div class="meditation-audio">
    <h2>Guided Meditation</h2>
    <p>Listen to a short meditation audio to relax and refocus.</p>
    <audio controls>
      <source src="@/assets/resources/meditation.mp3" type="audio/mp3" />
      Your browser does not support the audio element.
    </audio>
  </div>
</template>

<script setup>
// No setup required
</script>

<style scoped>
.meditation-audio {
  padding: 2rem;
  text-align: center;
}

audio {
  width: 100%;
  max-width: 500px;
  margin-top: 1rem;
}
</style>
