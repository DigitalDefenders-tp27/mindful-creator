<template>
  <div class="memory-game-container">
    <!-- Game header -->
    <div class="game-header">
      <h1>Meme Memory Match</h1>
      <p class="subtitle">Remember and match trending memes through gameplay</p>
    </div>
    
    <!-- Game status bar -->
    <div class="game-status-bar">
      <div class="timer-display">
        {{ formatTime(timeRemaining) }}
      </div>
      <div class="match-counter">
        Match: {{ matchedPairs }} / {{ totalPairs }}
      </div>
    </div>
    
    <!-- Game board -->
    <div class="game-board" :class="`level-${currentLevel}`">
      <div 
        v-for="card in cards" 
        :key="card.id" 
        class="card" 
        :class="{ 'flipped': card.isFlipped, 'matched': card.isMatched }"
        @click="flipCard(card)"
      >
        <div class="card-inner">
          <div class="card-front"></div>
          <div class="card-back">
            <img 
              :src="card.imagePath || '/images/placeholder.png'" 
              :alt="card.text" 
              @error="handleImageError($event, card)"
            >
          </div>
        </div>
      </div>
    </div>
    
    <!-- Victory modal -->
    <div v-if="showVictoryModal" class="victory-modal">
      <div class="modal-content">
        <h2>Victory!</h2>
        
        <!-- Meme info section -->
        <div class="meme-info">
          <div class="slider-controls">
            <button class="arrow-btn left" @click="prevMeme">&lt;</button>
            <div class="meme-display">
              <img 
                :src="currentMeme.imagePath || '/images/placeholder.png'" 
                :alt="currentMeme.text"
                @error="handleMemeImageError"
              >
              <div class="meme-details">
                <p>{{ currentMeme.text }}</p>
                
                <!-- Sentiment tags -->
                <div class="sentiment-tags">
                  <div class="tag">
                    <span class="label">Humour:</span>
                    <span class="value" :class="currentMeme.sentiment.humour">{{ currentMeme.sentiment.humour }}</span>
                  </div>
                  <div class="tag">
                    <span class="label">Motivational:</span>
                    <span class="value" :class="currentMeme.sentiment.motivational">{{ currentMeme.sentiment.motivational }}</span>
                  </div>
                  <div class="tag">
                    <span class="label">Sarcasm:</span>
                    <span class="value" :class="currentMeme.sentiment.sarcasm">{{ currentMeme.sentiment.sarcasm }}</span>
                  </div>
                  <div class="tag">
                    <span class="label">Overall sentiment:</span>
                    <span class="value" :class="currentMeme.sentiment.overall">{{ currentMeme.sentiment.overall }}</span>
                  </div>
                  <div class="tag">
                    <span class="label">Offensive:</span>
                    <span class="value" :class="currentMeme.sentiment.offensive">{{ currentMeme.sentiment.offensive }}</span>
                  </div>
                </div>
              </div>
            </div>
            <button class="arrow-btn right" @click="nextMeme">&gt;</button>
          </div>
        </div>
        
        <!-- Action buttons -->
        <div class="action-buttons">
          <button 
            class="action-btn" 
            @click="advanceLevel" 
            v-if="currentLevel === 1"
          >
            CHALLENGE ADVANCE
          </button>
          <button class="action-btn" @click="restartGame">TRY AGAIN</button>
          <button class="action-btn" @click="exitGame">EXIT</button>
        </div>
      </div>
    </div>
    
    <!-- Loading overlay -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading memes...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

// API configuration
const MEME_API_URL = import.meta.env.VITE_MEME_API_URL || 'http://localhost:8001';

// Game settings
const currentLevel = ref(1);
const timeRemaining = ref(60); // 60 seconds for the game
const isGameActive = ref(false);
const isLoading = ref(true);
const showVictoryModal = ref(false);
const timerInterval = ref(null);

// Cards state
const cards = ref([]);
const flippedCards = ref([]);
const memes = ref([]);
const totalPairs = computed(() => currentLevel.value === 1 ? 5 : 25);
const matchedPairs = ref(0);

// Victory modal state
const currentMemeIndex = ref(0);
const currentMeme = computed(() => {
  if (memes.value.length === 0) {
    return { 
      imagePath: '', 
      text: '', 
      sentiment: { 
        humour: 'unknown', 
        motivational: 'unknown', 
        sarcasm: 'unknown', 
        overall: 'neutral',
        offensive: 'unknown'
      } 
    };
  }
  
  const meme = memes.value[currentMemeIndex.value];
  return {
    ...meme,
    imagePath: `${MEME_API_URL}/memes/${meme.image_name}`,
    sentiment: {
      humour: meme.humour || 'unknown',
      motivational: meme.motivational || 'unknown',
      sarcasm: meme.sarcasm || 'unknown',
      overall: meme.overall_sentiment || 'neutral',
      offensive: meme.offensive || 'unknown'
    }
  };
});

// Methods
const fetchMemes = async () => {
  try {
    isLoading.value = true;
    
    const response = await axios.get(`${MEME_API_URL}/memes`);
    memes.value = response.data || [];
    
    // Create pairs of cards
    setupCards();
    
    isLoading.value = false;
    startGame();
  } catch (error) {
    console.error('Error fetching memes:', error);
    isLoading.value = false;
    
    // Create placeholder cards if API fails
    createPlaceholderCards();
  }
};

const createPlaceholderCards = () => {
  // Create placeholder memes
  memes.value = Array.from({ length: totalPairs.value }, (_, index) => ({
    id: index,
    imagePath: '/images/placeholder.png',
    text: `Placeholder Meme ${index + 1}`,
    sentiment: {
      humour: 'unknown',
      motivational: 'unknown',
      sarcasm: 'unknown',
      overall: 'neutral',
      offensive: 'unknown'
    }
  }));
  
  // Setup cards with placeholder memes
  setupCards();
  startGame();
};

const setupCards = () => {
  // Create two cards for each meme
  const cardPairs = memes.value.map(meme => [
    {
      id: `${meme.id}-1`,
      originalId: meme.id,
      imagePath: `${MEME_API_URL}/memes/${meme.image_name}`,
      text: meme.text || '',
      isFlipped: false,
      isMatched: false
    },
    {
      id: `${meme.id}-2`,
      originalId: meme.id,
      imagePath: `${MEME_API_URL}/memes/${meme.image_name}`,
      text: meme.text || '',
      isFlipped: false,
      isMatched: false
    }
  ]).flat();
  
  // Shuffle the cards
  cards.value = shuffleArray(cardPairs);
};

const shuffleArray = (array) => {
  const newArray = [...array];
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
  }
  return newArray;
};

const startGame = () => {
  resetGameState();
  isGameActive.value = true;
  
  // Start the timer
  timerInterval.value = setInterval(() => {
    if (timeRemaining.value > 0) {
      timeRemaining.value--;
    } else {
      endGame(false); // End game with loss
    }
  }, 1000);
};

const resetGameState = () => {
  timeRemaining.value = 60;
  matchedPairs.value = 0;
  flippedCards.value = [];
  showVictoryModal.value = false;
  
  // Reset all cards
  cards.value.forEach(card => {
    card.isFlipped = false;
    card.isMatched = false;
  });
  
  // Clear any existing timer
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
};

const flipCard = (card) => {
  // Don't allow flipping if game not active, card already matched or already flipped
  if (!isGameActive.value || card.isMatched || card.isFlipped || flippedCards.value.length >= 2) {
    return;
  }
  
  // Flip the card
  card.isFlipped = true;
  flippedCards.value.push(card);
  
  // Check for match if we have two cards flipped
  if (flippedCards.value.length === 2) {
    checkForMatch();
  }
};

const checkForMatch = () => {
  const [card1, card2] = flippedCards.value;
  
  // Check if the cards have the same original ID (same meme)
  if (card1.originalId === card2.originalId) {
    // It's a match
    card1.isMatched = true;
    card2.isMatched = true;
    matchedPairs.value++;
    
    // Check if all pairs are matched
    if (matchedPairs.value === totalPairs.value) {
      endGame(true); // End game with victory
    }
  } else {
    // Not a match, flip cards back after delay
    setTimeout(() => {
      card1.isFlipped = false;
      card2.isFlipped = false;
    }, 1000);
  }
  
  // Reset flipped cards
  flippedCards.value = [];
};

const endGame = (isVictory) => {
  isGameActive.value = false;
  
  // Clear the timer
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
  
  if (isVictory) {
    // Show victory modal
    currentMemeIndex.value = 0;
    showVictoryModal.value = true;
  } else {
    // Show all cards briefly, then restart
    cards.value.forEach(card => {
      card.isFlipped = true;
    });
    
    setTimeout(() => {
      resetGameState();
      startGame();
    }, 3000);
  }
};

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const nextMeme = () => {
  if (memes.value.length > 0) {
    currentMemeIndex.value = (currentMemeIndex.value + 1) % memes.value.length;
  }
};

const prevMeme = () => {
  if (memes.value.length > 0) {
    currentMemeIndex.value = (currentMemeIndex.value - 1 + memes.value.length) % memes.value.length;
  }
};

const advanceLevel = () => {
  currentLevel.value = 2;
  showVictoryModal.value = false;
  fetchMemes();
};

const restartGame = () => {
  showVictoryModal.value = false;
  resetGameState();
  startGame();
};

const exitGame = () => {
  // Emit event to parent component
  showVictoryModal.value = false;
  resetGameState();
  // You can emit an event to the parent component to close the game
};

const handleImageError = (event, card) => {
  // Replace broken image with placeholder
  event.target.src = '/images/placeholder.png';
};

const handleMemeImageError = (event) => {
  // Replace broken image with placeholder
  event.target.src = '/images/placeholder.png';
};

// Cleanup when component is unmounted
const cleanup = () => {
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
};

// Load game on mount
onMounted(() => {
  fetchMemes();
  
  // Cleanup when component is unmounted
  return cleanup;
});
</script>

<style scoped>
.memory-game-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

.game-header {
  text-align: center;
  margin-bottom: 20px;
}

.game-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
}

.game-status-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
  padding: 15px 20px;
  background-color: #D8FF89;
  border-radius: 10px;
  font-size: 1.5rem;
  font-weight: bold;
}

.timer-display {
  margin-right: 30px;
  font-family: 'Courier New', monospace;
}

.match-counter {
  font-weight: bold;
}

.game-board {
  display: grid;
  gap: 15px;
  margin: 0 auto;
  max-width: 1000px;
}

.game-board.level-1 {
  grid-template-columns: repeat(5, 1fr);
}

.game-board.level-2 {
  grid-template-columns: repeat(10, 1fr);
  gap: 8px;
}

.card {
  perspective: 1000px;
  height: 120px;
  cursor: pointer;
  position: relative;
  transform-style: preserve-3d;
}

.level-2 .card {
  height: 80px;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.card-front {
  background-color: #FF3D8C;
}

.card-back {
  background-color: white;
  transform: rotateY(180deg);
  border: 1px solid #ddd;
}

.card-back img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.victory-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 20px;
  padding: 30px;
  width: 80%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 30px rgba(0, 0, 0, 0.3);
}

.modal-content h2 {
  text-align: center;
  font-size: 2.5rem;
  color: #FF3D8C;
  margin-bottom: 20px;
}

.meme-info {
  margin-bottom: 30px;
}

.slider-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.arrow-btn {
  background-color: #333;
  color: white;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.meme-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 20px;
  width: 100%;
}

.meme-display img {
  max-width: 300px;
  max-height: 300px;
  border-radius: 10px;
  margin-bottom: 15px;
  object-fit: contain;
}

.meme-details {
  width: 100%;
  text-align: center;
}

.meme-details p {
  margin-bottom: 15px;
  font-size: 1.1rem;
}

.sentiment-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  margin-top: 15px;
}

.tag {
  background-color: #f0f0f0;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
}

.tag .label {
  font-weight: bold;
  margin-right: 5px;
}

.tag .value {
  padding: 2px 8px;
  border-radius: 10px;
  background-color: #eee;
}

.tag .value.positive {
  background-color: #D8FF89;
}

.tag .value.negative {
  background-color: #FFD6E0;
}

.tag .value.neutral {
  background-color: #E4EAF1;
}

.tag .value.very {
  background-color: #FFF9C2;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.action-btn {
  background-color: #2D2D52;
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.action-btn:hover {
  background-color: #1f1f38;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-left-color: #FF3D8C;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .game-board.level-1 {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(5, 1fr);
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 10px;
  }
  
  .modal-content {
    width: 95%;
    padding: 20px;
  }
  
  .meme-display {
    flex-direction: column;
  }
}

@media (max-width: 480px) {
  .game-board.level-1 {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(4, 1fr);
  }
  
  .card {
    height: 100px;
  }
  
  .level-2 .card {
    height: 60px;
  }
  
  .game-status-bar {
    flex-direction: column;
    gap: 10px;
  }
  
  .timer-display {
    margin-right: 0;
  }
}
</style> 