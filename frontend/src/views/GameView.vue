<template>
  <div class="game-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Creator Games</h1>
            <h2>Fun Activities for Mental Breaks</h2>
          </div>
          <p class="subtitle">Enjoy these quick games designed to give your mind a refreshing break from content creation</p>
        </div>
        <div class="decorative-elements">
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

    <!-- Games -->
    <div class="games-container">
      <h2 class="games-title">Featured Games</h2>
      <p class="games-subtitle">Choose any game to give yourself a moment of fun</p>
      <BentoGrid class="games-bento">
        <BentoGridCard
          v-for="(game, index) in gamesWithLayout"
          :key="index"
          :name="game.title"
          :description="game.description"
          :class="game.class"
          @click="startGame(game.type)"
        >
          <template v-if="game.image" #background>
            <div
              class="absolute inset-0 bg-cover bg-center transition-transform duration-700 ease-out group-hover:scale-110 will-change-transform"
              :style="`background-image: url('/bentoImages/${game.image}')`"
            ></div>
          </template>
        </BentoGridCard>
      </BentoGrid>
    </div>

    <!-- Game Modal -->
    <div v-if="showGameModal" class="modal">
      <div class="modal-content game-modal" :class="{ 'fullscreen': isFullscreenGame }">
        <span v-if="!isFullscreenGame" class="close" @click="closeModal">&times;</span>
        
        <!-- Game Content -->
        <div class="game-content">
          <MemoryMatch v-if="currentGame === 'memory'" @game-completed="onGameCompleted" />
          <div v-else class="coming-soon">
            <h2>Coming Soon!</h2>
            <p>This game is under development. Please try again later.</p>
            <button class="cta-button" @click="closeModal">Return to Games</button>
          </div>
        </div>
        
        <!-- Rating Section -->
        <div class="feedback">
          <h2>How did you enjoy this game?</h2>
          <p class="total-ratings">{{ totalRatings }} people have rated this game</p>
          <div class="stars">
            <span v-for="n in 5" :key="n" @click="rating = n" class="star-wrapper">
              <img :src="n <= rating ? starFilledIcon : starEmptyIcon" 
                   alt="star" 
                   class="star"
                   @mouseover="hoverRating = n"
                   @mouseleave="hoverRating = 0" />
            </span>
          </div>
          <button @click="submitFeedback" 
                  :disabled="rating === 0" 
                  class="submit-button"
                  :class="{ 'button-disabled': rating === 0 }">
            Submit Feedback
          </button>
        </div>

        <!-- Thank You Message -->
        <div v-if="submitted" class="thank-you">
          <h3>Thank you for your feedback!</h3>
        </div>
      </div>
    </div>

    <!-- Continue Buttons -->
    <div class="continue-section">
      <router-link to="/relaxation">
        <button class="continue-btn">Jump to Relaxation</button>
      </router-link>
      <router-link to="/creator-wellbeing">
        <button class="continue-btn wellbeing-btn">Jump to Creator Wellbeing</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import BentoGrid from '@/components/Activities/Bento/BentoGrid.vue'
import BentoGridCard from '@/components/Activities/Bento/BentoGridCard.vue'
import MemoryMatch from '@/components/Games/MemoryMatch.vue'

// Star Icons
import starFilledIcon from '../assets/star-filled.svg'
import starEmptyIcon from '../assets/star-empty.svg'

// Games
const games = [
  {
    title: 'Memory Match',
    description: 'Test your memory with a classic card matching game using trending memes.',
    type: 'memory',
    image: 'BreathingExercise.png',  // Placeholder image
    fullscreen: true
  },
  {
    title: 'Word Scramble',
    description: 'Unscramble words related to digital wellbeing.',
    type: 'word-scramble',
    image: 'Meditation.png',  // Placeholder image
    fullscreen: false
  },
  {
    title: 'Quick Quiz',
    description: 'Test your knowledge with a short quiz on digital wellness.',
    type: 'quiz',
    image: 'SensoryGrounding.png',  // Placeholder image
    fullscreen: false
  },
  {
    title: 'Bubble Pop',
    description: 'Pop bubbles to release stress and have fun.',
    type: 'bubble-pop',
    image: 'NatureSounds.jpg',  // Placeholder image
    fullscreen: false
  }
]

// Adding layout classes to create different card sizes
const gamesWithLayout = computed(() => [
  { 
    ...games[0], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-2 md:col-span-1 xl:h-[28rem]' // Memory Match - tall card
  }, 
  { 
    ...games[1], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-2 md:col-span-2 xl:h-[28rem]' // Word Scramble
  },
  { 
    ...games[2], 
    class: 'lg:col-span-1 row-span-1 md:col-span-1 lg:h-[14rem]' // Quick Quiz - small card
  },
  { 
    ...games[3], 
    class: 'lg:col-span-2 row-span-1 md:col-span-2 lg:h-[16rem]' // Bubble Pop - wide card
  }
]);

// States
const showGameModal = ref(false)
const rating = ref(0)
const hoverRating = ref(0)
const submitted = ref(false)
const currentGame = ref(null)
const gameCompleted = ref(false)
const totalRatings = ref(0)

// Check if current game should be displayed fullscreen
const isFullscreenGame = computed(() => {
  const game = games.find(g => g.type === currentGame.value);
  return game ? game.fullscreen : false;
});

// Start a game
const startGame = (gameType) => {
  currentGame.value = gameType
  
  // Reset states
  rating.value = 0
  submitted.value = false
  gameCompleted.value = false
  
  // Show modal
  showGameModal.value = true
  
  // For demonstration, set a random number of ratings
  totalRatings.value = Math.floor(Math.random() * 100) + 50
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

// Submit feedback
const submitFeedback = async () => {
  if (rating.value === 0) return
  
  try {
    // API call would go here in production
    // await axios.post('/api/games/feedback', {
    //   gameType: currentGame.value,
    //   rating: rating.value
    // })
    
    submitted.value = true
    // Increment total ratings
    totalRatings.value++
    
    // Reset after 2 seconds
    setTimeout(() => {
      submitted.value = false
    }, 2000)
  } catch (error) {
    console.error('Error submitting feedback:', error)
  }
}

onMounted(() => {
  // Any initialization code here
})
</script>

<style scoped>
.game-container {
  padding-top: 80px;
  overflow-x: hidden;
}

.hero-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4eaf1 100%);
  padding: 4rem 1rem;
  position: relative;
  overflow: hidden;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  position: relative;
}

.slogan {
  max-width: 600px;
  z-index: 2;
}

.title-group {
  margin-bottom: 1rem;
}

.slogan h1 {
  font-size: 3rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 0.5rem;
  line-height: 1.2;
  background: linear-gradient(90deg, #e75a97 0%, #4d8cd5 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.slogan h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #555;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #666;
  max-width: 90%;
  line-height: 1.6;
}

.decorative-elements {
  position: absolute;
  right: 0;
  top: 0;
  z-index: 1;
}

.top-row {
  display: flex;
  gap: 0.5rem;
}

.element-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.element {
  height: 80px;
  width: auto;
  object-fit: contain;
  opacity: 0.85;
  transform-origin: center;
  transition: all 0.4s ease;
}

.element.hoverable:hover {
  transform: scale(1.1) rotate(5deg);
  opacity: 1;
}

.games-container {
  padding: 3rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.games-title {
  font-size: 2rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.5rem;
  text-align: center;
}

.games-subtitle {
  font-size: 1.1rem;
  color: #666;
  text-align: center;
  margin-bottom: 2.5rem;
}

.games-bento {
  margin-bottom: 3rem;
}

.modal {
  display: flex;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6);
  z-index: 1000;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(3px);
}

.modal-content {
  position: relative;
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.modal-content.fullscreen {
  width: 100%;
  height: 100%;
  max-width: none;
  max-height: none;
  border-radius: 0;
  padding: 0;
  overflow: hidden;
}

.game-modal {
  min-height: 500px;
  display: flex;
  flex-direction: column;
}

.close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 28px;
  font-weight: bold;
  color: #666;
  cursor: pointer;
  z-index: 10;
}

.close:hover {
  color: #e75a97;
}

.game-content {
  flex: 1;
  margin-bottom: 2rem;
  height: 100%;
}

.feedback {
  margin-top: 1rem;
  text-align: center;
  padding: 1.5rem;
  border-top: 1px solid #eee;
}

.feedback h2 {
  font-size: 1.3rem;
  margin-bottom: 0.5rem;
  color: #333;
}

.stars {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
  gap: 0.5rem;
}

.star-wrapper {
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star-wrapper:hover {
  transform: scale(1.1);
}

.star {
  width: 35px;
  height: 35px;
}

.submit-button {
  background: linear-gradient(to right, #e75a97, #4d8cd5);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.button-disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.button-disabled:hover {
  transform: none;
  box-shadow: none;
}

.thank-you {
  margin-top: 1rem;
  text-align: center;
  animation: fadeIn 0.5s ease-in-out;
}

.thank-you h3 {
  color: #4d8cd5;
  font-size: 1.2rem;
}

.total-ratings {
  color: #888;
  font-size: 0.9rem;
  margin-top: 0.3rem;
}

.continue-section {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  padding: 2rem 1rem 4rem;
  flex-wrap: wrap;
}

.continue-btn {
  background-color: white;
  color: #333;
  border: 2px solid #e75a97;
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.continue-btn:hover {
  background-color: #e75a97;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.wellbeing-btn {
  border-color: #4d8cd5;
}

.wellbeing-btn:hover {
  background-color: #4d8cd5;
}

.coming-soon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 2rem;
  text-align: center;
}

.coming-soon h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #e75a97;
}

.coming-soon p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}

.cta-button {
  background: linear-gradient(to right, #e75a97, #4d8cd5);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .slogan h1 {
    font-size: 2.2rem;
  }
  
  .slogan h2 {
    font-size: 1.3rem;
  }
  
  .hero-content {
    flex-direction: column;
  }
  
  .decorative-elements {
    position: relative;
    margin-top: 2rem;
    align-self: flex-end;
  }
  
  .continue-section {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .continue-btn {
    width: 100%;
    max-width: 300px;
  }
}
</style> 