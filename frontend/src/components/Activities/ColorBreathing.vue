<template>
  <div class="color-breathing">
    <h2>Color Breathing</h2>
    <p>Visualise breathing in calming colours and breathing out stress.</p>
    <p>Inhale while imagining the colour blue, and exhale while imagining the colour red. Continue for a few minutes.</p>

    <!-- Embedded YouTube video -->
    <div class="video-wrapper">
      <iframe
        width="560"
        height="315"
        src="https://www.youtube.com/embed/HVXLFiwMB14"
        title="Color Breathing Guided Meditation"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<script setup>
// No additional setup needed
</script>

<style scoped>
.color-breathing {
  padding: 2rem;
  text-align: center;
}

.video-wrapper {
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
}

iframe {
  border-radius: 8px;
  max-width: 100%;
}
</style>
