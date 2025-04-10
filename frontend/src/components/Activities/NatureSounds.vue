<template>
  <div class="nature-sounds">
    <h2>Nature Sounds</h2>
    <p>Listen to calming sounds like rain, ocean waves, or forest.</p>

    <!-- 第一段：Forest -->
    <div class="sound-item">
      <h3>Forest Ambience 🌲</h3>
      <audio controls>
        <source src="/media/forest.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>

    <!-- 第二段：Rain -->
    <div class="sound-item">
      <h3>Rain Sounds 🌧️</h3>
      <audio controls>
        <source src="/media/rain.mp3" type="audio/mp3" />
        Your browser does not support the audio element.
      </audio>
    </div>
  </div>
</template>

<script setup>
// No logic needed here yet
</script>

<style scoped>
.nature-sounds {
  padding: 2rem;
  text-align: center;
}

.sound-item {
  margin-bottom: 2rem;
}

.sound-item h3 {
  margin-bottom: 0.5rem;
  font-weight: 600;
}

audio {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  display: block;
}
</style>

  