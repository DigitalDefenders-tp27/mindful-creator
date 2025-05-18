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
      <div class="game-layout">
        <!-- Left side - Game card -->
        <div class="game-portal" @click="startGame('memory')">
          <div class="portal-image-container">
            <img src="/memes/MemoryMatch.jpg" alt="Memory Match Game" class="portal-image">
          </div>
          <div class="portal-info">
            <h2>Meme Memory Match</h2>
            <p>Test your memory with a classic card matching game using trending memes.</p>
          </div>
        </div>
        
        <!-- Right side - Instructions and start button -->
        <div class="game-instructions">
          <h3>How to Play</h3>
          
          <div class="warning-box">
            <p><strong>⚠️ Warning:</strong> This game contains memes that may include potentially insulting, sarcastic, or offensive content. Please play responsibly.</p>
          </div>
          
          <ul>
            <li>Flip cards to find matching meme pairs</li>
            <li>Clear all pairs before time runs out</li>
            <li>Challenge yourself with different difficulty levels</li>
          </ul>
          
          <button class="start-game-btn" @click="startGame('memory')">
            Start Game
          </button>
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

    <div v-if="showPasswordInput" class="password-protect">
      <h2>Enter Password</h2>
      <input v-model="password" type="password" placeholder="Password" @keyup.enter="checkPassword" />
      <button @click="checkPassword">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MemoryMatch from '@/components/Games/MemoryMatch.vue'

const router = useRouter()
const password = ref('')
const correctPassword = 'your_password_here' // TODO: Replace with your real password
const showPasswordInput = ref(false)

// Game state
const showGameModal = ref(false)
const currentGame = ref(null)
const gameCompleted = ref(false)

// Check if current game should be displayed fullscreen
const isFullscreenGame = computed(() => {
  return true; // Always fullscreen
})

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

const showAlert = ref(false)
const alertMessage = ref('')
const alertType = ref('error')

function showErrorAlert(message) {
  alertMessage.value = message
  alertType.value = 'error'
  showAlert.value = true
}

function dismissAlert() {
  showAlert.value = false
}

// Function to create random hover effects for the title
onMounted(() => {
  const titleElement = document.querySelector('.title-group h1')
  if (titleElement) {
    titleElement.addEventListener('mouseenter', () => {
      // Generate random values for the animation and transform
      const randomSpeed = 0.5 + (Math.random() * 2) // Between 0.5s and 2.5s
      const randomScale = 1 + (Math.random() * 0.05) // Between 1 and 1.05
      const randomRotate = (Math.random() * 3) - 1.5 // Between -1.5 and 1.5 degrees
      
      // Apply random styles
      titleElement.style.animationDuration = `${randomSpeed}s`
      titleElement.style.transform = `scale(${randomScale}) rotate(${randomRotate}deg) translateY(-0.05em)`
    })
    
    // Reset on mouse leave
    titleElement.addEventListener('mouseleave', () => {
      titleElement.style.animationDuration = '3s'
      titleElement.style.transform = 'translateY(-0.05em)'
    })
  }

  if (sessionStorage.getItem('authenticated') !== 'true') {
    router.push({ name: 'password' })
  }
})

function checkPassword() {
  if (password.value === correctPassword) {
    localStorage.setItem('authenticated', 'true')
    router.push('/')
  } else {
    alert('Incorrect password!')
  }
}
</script>

<style scoped>
/* Game container styles */
.game-container {
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  width: 100%;
  position: relative;
  padding-bottom: 5rem;
}

/* Hero Section Styles - Matched exactly with HomeView */
.hero-section {
  min-height: 40vh;
  background-color: rgb(255, 252, 244);
  display: flex;
  align-items: center;
  overflow: visible;
  position: relative;
  z-index: 1;
  padding: 6rem 0 1rem;
  margin-bottom: 2rem;
}

.hero-content {
  position: relative;
  width: 100%;
  min-height: 40vh;
  display: flex;
  align-items: center;
  padding-left: 2rem;
  margin: 0 auto;
  overflow: visible;
}

.slogan {
  max-width: 800px;
  position: relative;
  z-index: 2;
  margin-left: 2rem;
  text-align: left;
}

.title-group {
  margin-bottom: 0.5rem;
  text-align: left;
}

.title-group h1 {
  font-size: 4rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #FF3D8C 0%,
    #FF8B3D 25%,
    #6FCF97 50%,
    #4D8CD5 75%,
    #FF3D8C 100%
  );
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  animation: rainbowFlow 3s linear infinite;
  filter: drop-shadow(0 0 3px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
  line-height: 1.3;
  display: inline-block;
  margin-bottom: 1rem;
  white-space: nowrap;
  text-align: left;
  padding: 0 0 0.2em;
  transform: translateY(-0.05em);
  overflow: visible;
}

.title-group h1:hover {
  filter: drop-shadow(0 0 5px rgba(255, 61, 140, 0.7));
  animation: rainbowFlow 1.5s linear infinite;
  transform: scale(1.02) rotate(-1deg);
}

@keyframes rainbowFlow {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
}

.title-group h2 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
  display: block;
  white-space: nowrap;
  text-align: left;
  overflow: visible;
}

.subtitle {
  font-size: 1.25rem;
  color: #666;
  line-height: 1.4;
  margin-top: 1.5rem;
  white-space: normal;
  text-align: left;
  max-width: 100%;
}

.decorative-elements {
  position: absolute;
  top: 0;
  right: 0;
  width: 960px;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(6, 160px);
  grid-template-rows: auto;
  row-gap: 1rem;
  padding: 2rem 0;
  z-index: 1;
  pointer-events: none;
  transform: translateX(0);
  justify-content: end;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(3, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 4 / 7;
  grid-row: 1;
  justify-self: end;
}

.element-wrapper {
  width: 160px;
  height: 120px;
  position: relative;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: auto;
  transition: transform 0.5s ease;
}

.element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  margin: 0;
  padding: 0;
  transition: all 0.5s ease;
}

/* Hover effect enhancement */
.top-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
}

/* Responsive Media Queries - Matching HomeView */
@media (min-width: 640px) {
  .title-group h1 {
    font-size: 3rem;
  }
  .title-group h2 {
    font-size: 1.875rem;
  }
  .subtitle {
    font-size: 1.125rem;
  }
}

@media (min-width: 768px) {
  .title-group h1 {
    font-size: 3.75rem;
  }
  .title-group h2 {
    font-size: 2.25rem;
  }
  .subtitle {
    font-size: 1.25rem;
  }
}

@media (min-width: 1024px) {
  .title-group h1 {
    font-size: 4.5rem;
  }
  .title-group h2 {
    font-size: 3rem;
  }
  .subtitle {
    font-size: 1.5rem;
    white-space: nowrap;
  }
}

@media (min-width: 1280px) {
  .title-group h1 {
    font-size: 6rem;
  }
  .title-group h2 {
    font-size: 3.75rem;
  }
  .subtitle {
    font-size: 1.875rem;
    white-space: nowrap;
  }
}

@media (max-width: 1800px) {
  .decorative-elements {
    width: 840px;
    grid-template-columns: repeat(6, 140px);
    opacity: 0.9;
    transform: translateX(0);
    justify-content: end;
  }
}

@media (max-width: 1536px) {
  .decorative-elements {
    width: 720px;
    grid-template-columns: repeat(6, 120px);
    opacity: 0.8;
    transform: translateX(0);
    justify-content: end;
  }
}

@media (max-width: 1280px) {
  .decorative-elements {
    width: 600px;
    grid-template-columns: repeat(6, 100px);
    opacity: 0.7;
    transform: translateX(0);
    row-gap: 0.75rem;
    justify-content: end;
  }
}

@media (max-width: 1024px) {
  .hero-section {
    min-height: 40vh;
    padding: 6rem 0 1rem;
  }
  
  .hero-content {
    min-height: 40vh;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    width: 100%;
    box-sizing: border-box;
  }
  
  .slogan {
    margin-left: 0;
    max-width: 100%;
  }
  
  .decorative-elements {
    transform: translateX(0) scale(0.8);
    opacity: 0.4;
    row-gap: 0.5rem;
    justify-content: end;
  }
  .title-group h1 {
    font-size: 3.5rem;
  }
  .title-group h2 {
    font-size: 2rem;
  }
  .subtitle {
    font-size: 1.15rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: auto;
    padding: 7rem 0 1rem;
  }
  
  .hero-content {
    min-height: auto;
    flex-direction: column;
    align-items: flex-start;
    padding: 0.75rem 1rem 0;
    width: 100%;
    box-sizing: border-box;
  }
  
  .slogan {
    margin-left: 0;
    max-width: 100%;
    text-align: left;
  }

  .title-group h1, .title-group h2, .subtitle {
    text-align: left;
    white-space: normal;
  }
  
  .decorative-elements {
    display: none;
  }
  .title-group h1 {
    font-size: 2.8rem;
  }
  .title-group h2 {
    font-size: 1.75rem;
  }
  .subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 640px) {
  .hero-section {
    min-height: auto;
    padding: 7rem 0 1rem;
    margin-bottom: 1rem;
  }

  .hero-content {
    padding: 0.25rem 1rem 0;
    min-height: auto;
    width: 100%;
    box-sizing: border-box;
  }

  .slogan {
    padding-top: 0;
    margin-left: 0;
    max-width: 100%;
  }

  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.7);
  }
  .title-group h1 {
    font-size: 2.2rem;
  }
  .title-group h2 {
    font-size: 1.5rem;
  }
  .subtitle {
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    min-height: 16vh;
    padding: 8rem 0.5rem 0.5rem;
  }
  
  .hero-content {
    min-height: 16vh;
    padding-left: 0;
    padding-right: 0;
  }

  .slogan {
    margin-left: 0;
    max-width: 100%;
  }
  
  .decorative-elements {
    opacity: 0;
    display: none;
  }
  .title-group h1 {
    font-size: 1.8rem;
  }
  .title-group h2 {
    font-size: 1.25rem;
  }
  .subtitle {
    font-size: 0.8rem;
  }
}

/* Game Portal Styles */
.game-portal-container {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  padding: 2rem;
  margin: 0 auto;
  margin-bottom: 4rem;
}

.game-layout {
  display: flex;
  width: 100%;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.game-portal {
  width: 100%;
  max-width: 500px;
  height: 400px;
  background-color: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.game-instructions {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2rem;
  background-color: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  min-width: 300px;
  height: 400px;
  max-width: 500px;
  width: 100%;
}

.game-instructions h3 {
  font-size: 1.8rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 700;
}

.game-instructions ul {
  margin-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.game-instructions li {
  margin-bottom: 0.8rem;
  font-size: 1.1rem;
  color: #555;
}

.warning-box {
  background-color: #fff8e6;
  border: 1px solid #ffd166;
  border-radius: 8px;
  padding: 1rem;
  margin: 1rem 0 1.5rem 0;
}

.warning-box p {
  color: #856404;
  font-size: 1rem;
  line-height: 1.5;
  margin: 0;
}

.start-game-btn {
  background: linear-gradient(135deg, #FF3D8C 0%, #FF8B3D 100%);
  border: none;
  color: white;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  align-self: center;
  box-shadow: 0 4px 15px rgba(255, 61, 140, 0.3);
  margin-bottom: 0.5rem;
}

.start-game-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 7px 20px rgba(255, 61, 140, 0.4);
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
  .game-layout {
    flex-direction: column;
    align-items: center;
  }
  
  .game-portal, .game-instructions {
    max-width: 100%;
    height: 350px;
    width: 100%;
  }
  
  .game-instructions {
    padding: 1.5rem;
  }
  
  .portal-image-container {
    height: 250px;
  }
  
  .portal-info h2 {
    font-size: 1.5rem;
  }
}

.password-protect {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 4rem;
}
.password-protect input {
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  font-size: 1.1rem;
}
.password-protect button {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
  background: #e573a6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style> 