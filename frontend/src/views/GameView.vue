<template>
  <div class="game-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Meme-ory Palace</h1>
            <h2>Where Brain Cells Go to Party</h2>
          </div>
          <p class="subtitle">Proving your memory is better than a goldfish, one meme at a time</p>
        </div>
        <div class="decorative-elements">
          <!-- Decorative elements, similar to home page -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Wide_Red.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Game Portal -->
    <div class="game-portal-container">
      <div class="game-portal" @click="startGame('memory')">
        <div class="portal-image-container">
          <img src="/memes/MemoryMatch.jpg" alt="Memory Match Game" class="portal-image">
        </div>
        <div class="portal-info">
          <h2>Meme Memory Match</h2>
          <p>Test your memory with a classic card matching game using trending memes.</p>
        </div>
      </div>
    </div>

    <!-- Game Modal -->
    <div v-if="showGameModal" class="modal">
      <div class="modal-content game-modal" :class="{ 'fullscreen': isFullscreenGame }">
        <span v-if="!isFullscreenGame" class="close" @click="closeModal">&times;</span>
        
        <!-- Game Content -->
        <div class="game-content">
          <MemoryMatch v-if="currentGame === 'memory'" @game-completed="onGameCompleted" @exit-game="closeModal" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MemoryMatch from '@/components/Games/MemoryMatch.vue'

// Game state
const showGameModal = ref(false)
const currentGame = ref(null)
const gameCompleted = ref(false)

// Check if current game should be displayed fullscreen
const isFullscreenGame = computed(() => {
  return true; // Always fullscreen
});

// Start a game
const startGame = (gameType) => {
  currentGame.value = gameType
  gameCompleted.value = false
  showGameModal.value = true
}

// Close the modal
const closeModal = () => {
  showGameModal.value = false
  currentGame.value = null
}

// Handle game completion
const onGameCompleted = () => {
  gameCompleted.value = true
}
</script>

<style scoped>
/* Hero Section Styles */
.hero-section {
  width: 100%;
  background-color: #f5f7fa;
  padding: 100px 20px 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.hero-content {
  width: 100%;
  max-width: 1200px;
  display: flex;
  justify-content: center;
  position: relative;
  z-index: 2;
}

.slogan {
  max-width: 800px;
  text-align: center;
  position: relative;
  z-index: 3;
}

.title-group {
  margin-bottom: 20px;
}

.title-group h1 {
  font-size: clamp(2.5rem, 8vw, 4rem);
  font-weight: bold;
  margin-bottom: 10px;
  background: linear-gradient(
    to right,
    #e75a97 20%,
    #4d8cd5 40%,
    #4d8cd5 60%,
    #e75a97 80%
  );
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  animation: liquidFlow 3s linear infinite;
}

.title-group h2 {
  font-size: clamp(1.2rem, 4vw, 2rem);
  color: #333;
  font-weight: 500;
}

.subtitle {
  font-size: clamp(1rem, 3vw, 1.2rem);
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.decorative-elements {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.top-row {
  position: absolute;
  top: -30px;
  right: 0;
  display: flex;
  gap: 20px;
}

.element-wrapper {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  opacity: 0.8;
}

.hoverable {
  transition: transform 0.5s ease, opacity 0.5s ease;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

@keyframes liquidFlow {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

/* Existing game container styles */
.game-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  background-color: #f5f7fa;
}

.game-portal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  padding: 2rem;
}

.game-portal {
  width: 100%;
  max-width: 600px;
  height: 400px;
  background-color: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.game-portal:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
}

.portal-image-container {
  width: 100%;
  height: 300px;
  overflow: hidden;
}

.portal-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.game-portal:hover .portal-image {
  transform: scale(1.05);
}

.portal-info {
  padding: 1.5rem;
  background: linear-gradient(135deg, #FF3D8C 0%, #FF8B3D 100%);
  color: white;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.portal-info h2 {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.portal-info p {
  font-size: 1rem;
  margin: 0;
}

.modal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1000;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}

.modal-content {
  position: relative;
  background-color: white;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.game-content {
  width: 100%;
  height: 100%;
}

.close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  color: white;
  cursor: pointer;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.5);
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.close:hover {
  background-color: rgba(255, 61, 140, 0.8);
}

@media (max-width: 768px) {
  .game-portal {
    max-width: 100%;
    height: 350px;
  }
  
  .portal-image-container {
    height: 250px;
  }
  
  .portal-info h2 {
    font-size: 1.5rem;
  }
}
</style> 