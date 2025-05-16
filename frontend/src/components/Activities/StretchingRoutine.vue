<template>
  <div class="activity-plain">
    <h2>Stretching Routine</h2>
    <p>Follow along with this 12-minute daily stretching video to ease tension and improve flexibility.</p>
    <div class="video-section">
      <video controls preload="auto" class="stretching-video">
        <source src="/media/12 MIN DAILY STRETCH .mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div class="video-caption">Enjoy this guided stretching session for your wellbeing!</div>
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
.stretching-video {
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
</style>
  