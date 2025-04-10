<template>
    <div class="breathing-video">
      <h2>Breathing Exercise - 4-7-8 Breathing</h2>
      <p>Follow along with the video to perform a 4-7-8 breathing exercise to calm your mind.</p>
    <!-- 嵌入 YouTube 视频 -->
    <div class="video-wrapper">
      <iframe
        src="https://www.youtube.com/embed/YRPh_GaiL8s"
        title="4-7-8 Breathing Exercise"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
      ></iframe>
    </div>
  </div>
</template>
  
  <script setup>
  </script>
  
  <style scoped>
  .breathing-video {
    text-align: center;
    max-width: 1000px;
    margin: 0 auto;
    padding: 24px;
  }
  
  .breathing-video h2 {
    font-size: 28px;
    margin-bottom: 12px;
  }
  
  .breathing-video p {
    margin-bottom: 20px;
  }
  
  video {
    width: 100%;
    max-width: 600px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .video-wrapper {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 ratio */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  max-width: 900px;
  margin: 0 auto;
  }

  .video-wrapper iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
    border-radius: 12px;
  }
  </style>
  