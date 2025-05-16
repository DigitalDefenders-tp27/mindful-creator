<template>
  <div class="activity-plain">
    <h2 class="activity-title">Sensory Grounding</h2>
    <p class="activity-desc">Try this 5-4-3-2-1 mindfulness video to bring yourself into the present moment.</p>
    <div class="video-section">
      <video controls preload="auto" class="grounding-video">
        <source src="/media/Senses .mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div class="video-caption">Follow along and use your senses to feel grounded.</div>
    </div>
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
.video-section {
  margin: 1.5rem 0 2.2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.grounding-video {
  width: 100%;
  max-width: 480px;
  border-radius: 16px;
  margin-bottom: 0.5rem;
  border: none !important;
  outline: none !important;
  background: none !important;
  box-shadow: none !important;
}
.video-caption {
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
  