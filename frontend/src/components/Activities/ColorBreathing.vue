<template>
  <div class="activity-plain">
    <h2>Color Breathing</h2>
    <p>Visualize breathing in calming colors and breathing out stress.</p>
    <div class="video-section">
      <video controls preload="auto" class="color-breathing-video">
        <source src="/media/color_breathing_VIDEO.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div class="video-caption">Follow along with this calming color breathing video</div>
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
  background-image: url('/docs/media/Color-breathing.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 24px;
  position: relative;
  min-height: 340px;
}
.activity-plain::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255,255,255,0.60);
  z-index: 0;
  border-radius: 24px;
  pointer-events: none;
}
.activity-plain > * {
  position: relative;
  z-index: 1;
}
.activity-plain h2 {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  color: #1a232b;
}
.activity-plain p {
  font-size: 1.15rem;
  margin: 1rem 0 1.2rem 0;
  color: #444;
}
.video-section {
  margin: 1.5rem 0 2.2rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}
.color-breathing-video {
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
  margin-top: 1.2rem;
  color: #6CBDB5;
  font-size: 1.15rem;
  font-weight: 600;
  font-style: italic;
  text-align: center;
  letter-spacing: 0.01em;
  opacity: 1;
  text-shadow: 0 2px 8px #fff, 0 1px 2px #6cbdb533;
  background: rgba(255,255,255,0.7);
  border-radius: 10px;
  padding: 0.5em 0.8em;
  display: inline-block;
}
</style>

  