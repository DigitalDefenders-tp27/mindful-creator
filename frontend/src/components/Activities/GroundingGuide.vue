<template>
  <div class="grounding-guide">
    <h2>Sensory Grounding - 5-4-3-2-1 Exercise</h2>
    <p>Try a 5-4-3-2-1 activity to bring yourself into the present.</p>
    <ul>
      <li>5 things you can see</li>
      <li>4 things you can touch</li>
      <li>3 things you can hear</li>
      <li>2 things you can smell</li>
      <li>1 thing you can taste</li>
    </ul>
    <p>Take a few deep breaths and engage your senses.</p>
    <div class="video-container">
      <iframe
        src="https://www.youtube.com/embed/30VMIEmA114"
        title="5-4-3-2-1 Grounding Exercise Video"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<script setup>
// No special setup needed for the grounding exercise.
</script>

<style scoped>
.grounding-guide {
  padding: 2rem;
  text-align: center;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 0.5rem 0;
}

.video-container {
  margin-top: 20px;
  position: relative;
  overflow: hidden;
  width: 100%;
  padding-top: 56.25%; /* 16:9 Aspect Ratio */
}

.video-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
</style>
