<template>
  <div class="memory-game-container" tabindex="0" @keydown.esc="exitGame" ref="gameContainer">
    <!-- Game status bar -->
    <div v-if="gameStarted && !gameOver" class="game-status-bar new-status-bar">
      <div class="status-item timer-display">
        Time: <span>{{ formatTime(timer) }}</span>
      </div>
      <div class="status-item match-counter">
        Matches: <span>{{ matchedPairs }} / {{ totalPairs }}</span>
      </div>
    </div>
    
    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Loading memes...</p>
    </div>

    <div v-if="errorMessage && !isLoading" class="error-message-container">
        <p>Error: {{ errorMessage }}</p>
        <button @click="startGame">Try Again</button>
        <button @click="goHome">Go Home</button>
    </div>

    <!-- Game board -->
    <div v-if="gameStarted && !isLoading && !errorMessage && !gameOver" class="game-board-container">
      <div class="game-board" :class="`level-${currentLevel}`">
        <div 
          v-for="card_iter in cards"  
          :key="card_iter.id" 
          class="card" 
          :class="{ 'flipped': card_iter.isFlipped, 'matched': card_iter.isMatched }"
          @click="flipCard(card_iter)" 
        >
          <div class="card-inner">
            <div class="card-front"></div>
            <div class="card-back">
              <!-- Always use img, remove offline logic -->
              <img 
                :src="card_iter.memeData.image_url || '/images/placeholder.png'" 
                :alt="card_iter.memeData.text" 
                @error="event => (event.target as HTMLImageElement).src = 'https://via.placeholder.com/100?text=Error'"
              >
            </div>
          </div>
        </div>
      </div>
      <div v-if="currentLevel === 2" class="level-2-help">Scroll to see more cards</div>
    </div>
    
    <!-- Victory modal - Simplified -->
    <div v-if="showVictoryModal" class="victory-modal new-victory-modal">
      <div class="modal-content new-modal-content">
        <h2 class="new-modal-h2">{{ gameWon ? 'Victory!' : 'Time\'s Up!' }}</h2>
        
        <div class="new-modal-subtitle">
          Your Meme Collection <span class="level-badge new-level-badge">Level {{ currentLevel }}</span>
        </div>
        
        <div v-if="gameMemesForModal.length > 0 && currentModalMeme" class="meme-gallery-modal victory-style new-meme-gallery">
          <div class="meme-carousel new-meme-carousel">
            <button @click="prevModalMeme" class="arrow-btn left-arrow new-arrow-btn">&#x276E;</button>
            <div class="modal-meme-item-container new-meme-item-container">
              <img 
                :src="currentModalMeme.image_url || '/images/placeholder.png'" 
                :alt="currentModalMeme.text"
                @error="event => (event.target as HTMLImageElement).src = 'https://via.placeholder.com/100?text=Error'"
                class="modal-meme-image-single new-modal-meme-image"
              >
              <p class="meme-identifier new-meme-identifier">Meme {{ currentModalMemeIndex + 1 }}</p>
              <div class="modal-meme-sentiments new-modal-sentiments">
                <!-- Overall sentiment with progress bar at the top -->
                <div class="sentiment-progress-section">
                  <div class="sentiment-progress-container">
                    <div class="sentiment-progress-bar" :style="{width: getSentimentPercentage(currentModalMeme.overall_sentiment) + '%'}"></div>
                    <span class="sentiment-value">{{ formatSentiment(currentModalMeme.overall_sentiment) || 'N/A' }}</span>
                  </div>
                </div>
                
                <div class="sentiment-grid new-sentiment-grid">
                  <div v-if="currentModalMeme.humour" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Humour:</span> <span class="sentiment-tag new-sentiment-tag humour">{{ formatSentiment(currentModalMeme.humour) }}</span>
                  </div>
                  <div v-if="currentModalMeme.sarcasm" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Sarcasm:</span> <span class="sentiment-tag new-sentiment-tag sarcasm">{{ formatSentiment(currentModalMeme.sarcasm) }}</span>
                  </div>
                  <div v-if="currentModalMeme.motivational" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Motivational:</span> <span class="sentiment-tag new-sentiment-tag motivational">{{ formatSentiment(currentModalMeme.motivational) }}</span>
                  </div>
                  <div v-if="currentModalMeme.offensive" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Offensive:</span> <span class="sentiment-tag new-sentiment-tag offensive">{{ formatSentiment(currentModalMeme.offensive) }}</span>
                  </div>
                </div>
              </div>
            </div>
            <button @click="nextModalMeme" class="arrow-btn right-arrow new-arrow-btn">&#x276F;</button>
          </div>
        </div>
        
        <div class="modal-controls new-modal-controls">
          <button v-if="gameWon && canAdvanceLevel" class="control-btn new-control-btn next-level-btn" @click="challengeAdvance">NEXT LEVEL</button>
          <div class="second-row-buttons">
            <button class="control-btn new-control-btn play-again-btn" @click="restartGame">PLAY AGAIN</button>
            <button class="control-btn new-control-btn exit-btn" @click="exitGame">EXIT</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
// Removed: import { useGameStore, GameResult } from '@/stores/gameStore';
// Removed: import FullScreenButton from '@/components/Tools/FullScreenButton.vue';
// Removed: import router from '@/router';
// Removed: import { showConfetti } from '@/utils/confetti';

// const gameStore = useGameStore(); // Removed

// Game levels and their configurations
const levels = {
  1: { pairs: 6, columns: 4, name: 'Easy (6 pairs)', cardWidth: 'w-24', cardHeight: 'h-24', textSize: 'text-xs', gameTime: 60 }, // 6 pairs, 4x3 grid, 60s
  2: { pairs: 25, columns: 10, name: 'Medium (25 pairs)', cardWidth: 'w-20', cardHeight: 'h-20', textSize: 'text-xxs', gameTime: 120 }, // 25 pairs, 5x10 grid, 120s
};
type LevelKey = keyof typeof levels;

const currentLevel = ref<LevelKey>(1);
const gameStarted = ref(false);
const gameOver = ref(false);
const gameWon = ref(false);
const cards = ref<Card[]>([]);
const flippedCards = ref<Card[]>([]);
const matchedPairs = ref(0);
const timer = ref(levels[currentLevel.value].gameTime);
const timerId = ref<number | null>(null);
const score = ref(0);
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);
const showVictoryModal = ref(false);
const processingFlip = ref(false);
const gameMemesForModal = ref<MemeData[]>([]);
const currentModalMemeIndex = ref(0);

// Hard-coded backend API address
const API_BASE_URL = 'https://api.tiezhu.org';

// Define emits
const emit = defineEmits(['game-completed', 'exit-game']);

interface MemeData {
  id: any;
  image_name: string;
  image_url: string;
  text: string;
  humour?: string;
  sarcasm?: string;
  offensive?: string;
  motivational?: string;
  overall_sentiment?: string;
}

interface Card {
  id: number;
  memeData: MemeData;
  isFlipped: boolean;
  isMatched: boolean;
}

const totalPairs = computed(() => levels[currentLevel.value].pairs);

function formatTime(seconds: number): string {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}

const gridClass = computed(() => `grid-cols-${levels[currentLevel.value].columns}`);

const cardSizeClass = computed(() => {
  const config = levels[currentLevel.value];
  return `${config.cardWidth} ${config.cardHeight}`;
});

const cardTextSizeClass = computed(() => levels[currentLevel.value].textSize);

const modalMeme = ref<MemeData | null>(null);

const currentModalMeme = computed(() => {
  if (gameMemesForModal.value.length > 0 && currentModalMemeIndex.value < gameMemesForModal.value.length) {
    return gameMemesForModal.value[currentModalMemeIndex.value];
  }
  return null;
});

const canAdvanceLevel = computed(() => {
  const levelKeys = Object.keys(levels).map(Number) as LevelKey[];
  const maxLevel = Math.max(...levelKeys);
  return currentLevel.value < maxLevel;
});

const gameContainer = ref<HTMLElement | null>(null);

function formatSentiment(sentiment: string | undefined): string {
  if (!sentiment) return 'N/A';
  return sentiment.replace(/_/g, ' ');
}

function getSentimentPercentage(sentiment: string | undefined): number {
  if (!sentiment) return 0;
  
  const sentimentMap = {
    'very_positive': 100,
    'positive': 75,
    'neutral': 50,
    'negative': 25,
    'very_negative': 0
  };
  
  return sentimentMap[sentiment as keyof typeof sentimentMap] || 50;
}

async function initializeGameFromBackend() {
  if (!gameStarted.value) return;
  isLoading.value = true;
  errorMessage.value = null;
  cards.value = [];
  matchedPairs.value = 0;
  gameMemesForModal.value = [];
  currentModalMemeIndex.value = 0;

  try {
    console.log(`Requesting ${levels[currentLevel.value].pairs} pairs for level ${currentLevel.value} from backend.`);
    const response = await fetch(`${API_BASE_URL}/api/games/memory_match/initialize_game`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ level: currentLevel.value }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: "Failed to parse error response." }));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const memesFromApi: MemeData[] = await response.json();
    console.log('Memes received from API:', memesFromApi);

    if (memesFromApi.length < levels[currentLevel.value].pairs) {
      throw new Error(`Not enough memes. Expected ${levels[currentLevel.value].pairs}, got ${memesFromApi.length}.`);
    }

    const gameCards: Card[] = [];
    const memesForLevel = memesFromApi.slice(0, levels[currentLevel.value].pairs);

    gameMemesForModal.value = [...memesForLevel];

    memesForLevel.forEach((meme, index) => {
      gameCards.push({ id: index * 2, memeData: meme, isFlipped: false, isMatched: false });
      gameCards.push({ id: index * 2 + 1, memeData: meme, isFlipped: false, isMatched: false });
    });

    cards.value = shuffleArray(gameCards);
    console.log('Shuffled cards ready:', cards.value);

  } catch (error: any) {
    console.error('Error initializing game:', error);
    errorMessage.value = error.message || "An unknown error occurred.";
    stopGame();
  } finally {
    isLoading.value = false;
  }
}

function selectLevel(level: LevelKey) {
  currentLevel.value = level;
  if (!gameStarted.value) {
    resetGameState();
    timer.value = levels[currentLevel.value].gameTime;
  }
}

function startGame() {
  gameStarted.value = true;
  gameOver.value = false;
  gameWon.value = false;
  showVictoryModal.value = false;
  processingFlip.value = false;
  gameMemesForModal.value = [];
  currentModalMemeIndex.value = 0;
  resetGameState();
  timer.value = levels[currentLevel.value].gameTime;
  initializeGameFromBackend();
  startTimer();
}

function resetGameState() {
  flippedCards.value = [];
  matchedPairs.value = 0;
  score.value = 0;
  cards.value.forEach(card => {
    card.isFlipped = false;
    card.isMatched = false;
  });
  if (timerId.value) {
    clearInterval(timerId.value);
    timerId.value = null;
  }
}

function stopGame() {
  gameStarted.value = false;
  if (timerId.value) {
    clearInterval(timerId.value);
    timerId.value = null;
  }
}

function shuffleArray<T>(array: T[]): T[] {
  const newArray = [...array];
  for (let i = newArray.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [newArray[i], newArray[j]] = [newArray[j], newArray[i]];
  }
  return newArray;
}

function flipCard(clickedCard: Card) {
  if (clickedCard.isFlipped || clickedCard.isMatched || gameOver.value) {
    return;
  }

  if (processingFlip.value && flippedCards.value.length === 2) {
    if (!flippedCards.value[0].isMatched) {
      flippedCards.value[0].isFlipped = false;
      flippedCards.value[1].isFlipped = false;
      flippedCards.value = [];
      processingFlip.value = false;
    }
  }

  clickedCard.isFlipped = true;
  flippedCards.value.push(clickedCard);

  if (flippedCards.value.length === 2) {
    processingFlip.value = true;
    checkForMatch();
  }
}

function checkForMatch() {
  const [card1, card2] = flippedCards.value;

  if (card1.memeData.image_name === card2.memeData.image_name) {
    card1.isMatched = true;
    card2.isMatched = true;
    matchedPairs.value++;
    score.value += 100;
    modalMeme.value = card1.memeData;

    flippedCards.value = [];
    processingFlip.value = false;

    if (matchedPairs.value === totalPairs.value) {
      endGame(true);
    }
  } else {
    score.value = Math.max(0, score.value - 10);
    setTimeout(() => {
      if (flippedCards.value.includes(card1) && flippedCards.value.includes(card2)) {
        card1.isFlipped = false;
        card2.isFlipped = false;
        flippedCards.value = [];
        processingFlip.value = false;
      }
    }, 500);
  }
}

function startTimer() {
  if (timerId.value) clearInterval(timerId.value);
  timerId.value = setInterval(() => {
    timer.value--;
    if (timer.value <= 0) {
      endGame(false);
    }
  }, 1000);
}

function stopTimer() {
  if (timerId.value) {
    clearInterval(timerId.value);
    timerId.value = null;
  }
}

function endGame(won: boolean) {
  stopTimer();
  gameOver.value = true;
  gameWon.value = won;
  currentModalMemeIndex.value = 0;
  showVictoryModal.value = true;

  if (won) {
    score.value += timer.value * 10;
  }
}

function goHome() {
  window.location.href = '/';
}

function restartGame() {
  showVictoryModal.value = false;
  gameOver.value = false;
  gameWon.value = false;
  resetGameState();
  timer.value = levels[currentLevel.value].gameTime;
  startGame();
}

function exitGame() {
  showVictoryModal.value = false;
  gameStarted.value = false;
  gameOver.value = false;
  gameWon.value = false;
  currentLevel.value = 1;
  resetGameState();
  timer.value = levels[currentLevel.value].gameTime;
  emit('exit-game');
}

function nextModalMeme() {
  if (currentModalMemeIndex.value < gameMemesForModal.value.length - 1) {
    currentModalMemeIndex.value++;
  } else {
    // Loop back to the first meme
    currentModalMemeIndex.value = 0;
  }
}

function prevModalMeme() {
  if (currentModalMemeIndex.value > 0) {
    currentModalMemeIndex.value--;
  } else {
    // Loop back to the last meme
    currentModalMemeIndex.value = gameMemesForModal.value.length - 1;
  }
}

function challengeAdvance() {
  if (canAdvanceLevel.value) {
    const levelKeys = Object.keys(levels).map(Number).sort((a,b) => a-b) as LevelKey[];
    const currentLevelIndex = levelKeys.indexOf(currentLevel.value);
    if (currentLevelIndex < levelKeys.length - 1) {
      currentLevel.value = levelKeys[currentLevelIndex + 1];
      restartGame();
    }
  }
}

// Focus the game container to enable keyboard events
function focusGameContainer() {
  if (gameContainer.value) {
    gameContainer.value.focus();
  }
}

onMounted(() => {
  // Start the game automatically when component is mounted
  startGame();
  focusGameContainer();
  
  // Focus on component when modal opens
  setTimeout(focusGameContainer, 100);
});

onUnmounted(() => {
  if (timerId.value) {
    clearInterval(timerId.value);
  }
});

watch(currentLevel, (newLevel) => {
  if (!gameStarted.value) {
    timer.value = levels[newLevel].gameTime;
    score.value = 0;
    matchedPairs.value = 0;
  }
});

</script>

<style scoped>
.memory-game-container {
  width: 100%;
  height: 100vh;
  max-width: none;
  margin: 0;
  padding: 10px;
  font-family: Arial, sans-serif;
  color: #333;
  display: flex;
  flex-direction: column;
  background-color: #FDFDFF; /* Very light off-white, almost pure white */
  box-sizing: border-box;
  overflow: auto; /* Changed from hidden to auto to allow scrolling */
  position: relative;
}

.game-header {
  text-align: center;
  margin-bottom: 10px;
  flex-shrink: 0;
}

.game-header h1 {
  font-size: clamp(1.8rem, 5vw, 2.2rem);
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #333333; /* Dark grey/black for game title */
}

.game-status-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 10px;
  padding: 8px 10px;
  background-color: #ffffff;
  border-radius: 8px;
  font-size: clamp(0.9rem, 3vw, 1.2rem);
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  width: 95%;
  align-self: center;
  color: #3c4043;
}

.timer-display, .match-counter, .score-display {
  font-family: 'Consolas', 'Courier New', monospace;
}
.score-display {
    color: #1a73e8;
}

.error-message-container {
    text-align: center;
    padding: 20px;
    margin: 20px auto;
    background-color: #fdecea;
    border: 1px solid #f5c6cb;
    color: #721c24;
    border-radius: 8px;
    max-width: 500px;
}
.error-message-container button {
    margin: 10px 5px 0;
    padding: 8px 15px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    background-color: #007bff;
    color: white;
}
.error-message-container button:hover {
    background-color: #0056b3;
}

.game-board-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Changed from center to allow content to start from top */
  width: 100%;
  padding: 10px 0; /* Added vertical padding */
  overflow-y: auto; /* Allow vertical scrolling */
  min-height: 0;
  box-sizing: border-box;
  margin: 0 auto;
  max-height: none; /* Removed max-height restriction */
}

.game-board {
  display: grid;
  width: 100%;
  height: auto;
  max-width: 95vw;
  max-height: none; /* Removed max-height restriction */
  gap: 10px; /* Fixed gap size */
  padding: 15px;
  background: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  position: relative;
  box-sizing: border-box;
}

.game-board.level-1 {
  grid-template-columns: repeat(4, minmax(70px, 1fr));
  grid-template-rows: repeat(3, minmax(70px, 1fr));
  aspect-ratio: auto; /* Remove fixed aspect ratio */
}

.game-board.level-2 {
  grid-template-columns: repeat(10, minmax(55px, 1fr));
  grid-template-rows: repeat(5, minmax(55px, 1fr));
  aspect-ratio: auto; /* Remove fixed aspect ratio */
}

.card {
  aspect-ratio: 1 / 1;
  perspective: 1000px;
  cursor: pointer;
  min-width: 0; /* Allow cards to shrink below min-content */
  min-height: 0; /* Allow cards to shrink below min-content */
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}

.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.card-front {
  /* background: linear-gradient(145deg, #4e73df, #224abe); */ /* Old blue gradient */
  background: linear-gradient(145deg, #FF7E5F, #FEB47B); /* New orange/reddish gradient */
  /* Other styles like display flex, align, justify for content if any */
}
.card-front::before {
    /* content: '?'; */ /* Question mark removed */
    content: ''; /* Ensure no content */
    font-size: clamp(20px, 10vmin, 50px);
    color: rgba(255,255,255,0.7);
    font-weight: bold;
}

.card-back {
  background-color: #ffffff;
  transform: rotateY(180deg);
}

.card-back img {
  max-width: 90%;
  max-height: 90%;
  object-fit: contain;
  border-radius: 4px;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}
.card.matched .card-inner {
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.card.matched {
    pointer-events: none;
}

.victory-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(20, 20, 20, 0.85); /* Darker overlay, less transparency */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(10px); /* Increased blur */
  padding: 15px;
  box-sizing: border-box;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  padding: clamp(15px, 4vw, 25px);
  width: min(95%, 600px);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
}

.modal-content h2 {
  text-align: center;
  font-size: clamp(1.8rem, 5vw, 2.5rem);
  color: #FE6B8B; /* Pinkish color from a similar design */
  margin-bottom: 15px;
}

.modal-subtitle {
  text-align: center;
  font-size: clamp(1rem, 3vw, 1.2rem);
  color: #4F4F4F; /* Darker Grey for subtitle text */
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.level-badge {
  background-color: #1a73e8;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: clamp(0.7rem, 2vw, 0.9rem);
  font-weight: bold;
}
.modal-content > p {
    text-align: center;
    font-size: clamp(1rem, 3vw, 1.3rem);
    margin-bottom: 15px;
    font-weight: bold;
}

.meme-gallery-modal.victory-style {
  background-color: transparent; /* No separate background for the gallery box itself */
  border: none;
  padding: 0;
  margin-top: 0;
  margin-bottom: 20px;
}

.meme-carousel {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-meme-item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-grow: 1;
  padding: 0 10px;
}

.arrow-btn {
  background: none;
  border: none;
  font-size: 2.5rem;
  color: #5f6368;
  cursor: pointer;
  padding: 0 10px;
  transition: color 0.2s;
}
.arrow-btn:hover:not(:disabled) {
  color: #FE6B8B;
}
.arrow-btn:disabled {
  color: #cccccc;
  cursor: not-allowed;
}

.modal-meme-image-single {
  max-width: 100%;
  max-height: 280px; /* Increased from 220px */
  object-fit: contain;
  border-radius: 8px;
  margin-bottom: 15px; /* Increased from 10px */
}

.modal-meme-text-under-image {
  font-size: clamp(0.8rem, 2.2vw, 1rem);
  color: #333;
  text-align: center;
  margin-bottom: 15px;
  font-style: italic;
}

.modal-meme-sentiments {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  width: 100%;
}

.sentiment-tag {
  padding: 5px 10px;
  border-radius: 15px;
  font-size: clamp(0.7rem, 2vw, 0.85rem);
  font-weight: 500;
  color: #333;
  background-color: #e9ecef;
  border: 1px solid #ced4da;
}
.sentiment-tag.humour { background-color: #c3e6cb; border-color: #b1dfbb; color: #155724; }
.sentiment-tag.sarcasm { background-color: #f5c6cb; border-color: #f1b0b7; color: #721c24; }
.sentiment-tag.offensive { background-color: #ffeeba; border-color: #ffdf7e; color: #856404; }
.sentiment-tag.motivational { background-color: #bee5eb; border-color: #abdde5; color: #0c5460; }
.sentiment-tag.overall { background-color: #d6d8db; border-color: #c6c8ca; color: #383d41; }

.modal-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: auto;
  padding-top: 15px;
  gap: 15px;
  flex-wrap: wrap;
}

.control-btn {
  color: white;
  border: none;
  border-radius: 8px;
  padding: clamp(10px, 2.5vw, 12px) clamp(15px, 4vw, 25px);
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  flex-grow: 1;
  min-width: 120px;
  text-align: center;
}
.control-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.play-btn { background: linear-gradient(135deg, #34a853, #2c8a42); }
.try-again-btn { background: linear-gradient(135deg, #ffc107, #e0a800); color: #212529; }
.exit-btn { background: linear-gradient(135deg, #ea4335, #c5221f); }
.advance-btn { background: linear-gradient(135deg, #6f42c1, #5a32a3); }

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.85);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.spinner {
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-left-color: #1a73e8;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 0.8s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-overlay p {
    font-size: clamp(1rem, 3vw, 1.2rem);
    color: #3c4043;
}

.level-2-help {
  display: block;
  position: static;
  text-align: center;
  margin-top: 10px;
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  white-space: nowrap;
  transform: none;
  left: auto;
}

@media (max-width: 768px) {
  .game-board.level-2 {
    grid-template-columns: repeat(5, minmax(55px, 1fr));
    grid-template-rows: repeat(10, minmax(55px, 1fr));
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .game-board-container {
    padding: 5px;
  }
  
  .game-board {
    gap: 5px;
    padding: 5px;
    max-width: 98vw;
  }
  
  .game-board.level-1 {
    grid-template-columns: repeat(4, minmax(50px, 1fr));
    grid-template-rows: repeat(3, minmax(50px, 1fr));
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(5, minmax(45px, 1fr));
    grid-template-rows: repeat(10, minmax(45px, 1fr));
    gap: 5px;
  }
}

.game-status-bar.new-status-bar {
  display: flex;
  justify-content: center; /* Center items */
  align-items: center;
  margin: 10px auto 15px auto; /* Center block and add some margin */
  padding: 8px 15px;
  background-color: #FE6B8B; /* Changed to dark pink theme color */
  border-radius: 25px; /* Pill shape */
  font-size: clamp(0.8rem, 2.5vw, 1rem); /* Adjusted font size */
  font-weight: 500;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  max-width: 400px; /* Max width for the pill */
  width: auto; /* Auto width based on content */
  align-self: center;
  color: #ffffff; /* White text for labels */
}

.status-item {
  margin: 0 10px; /* Spacing between items */
  display: flex;
  align-items: center;
}
.status-item span { /* For the value part */
  font-weight: bold;
  margin-left: 5px;
  /* color: #ffffff; */ /* White text for values - already handled by parent or can be set if needed */
}

.victory-modal.new-victory-modal {
  background-color: rgba(20, 20, 20, 0.85); /* Darker overlay, less transparency */
  backdrop-filter: blur(10px); /* Increased blur */
}

.modal-content.new-modal-content {
  background-color: #ffffff;
  border-radius: 16px;
  padding: 20px;
  width: min(95%, 700px);
  max-height: 95vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
  min-height: 600px;
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.new-modal-h2 { /* For "Victory!" */
  font-size: clamp(2rem, 6vw, 2.8rem);
  color: #FE6B8B; /* Pinkish color from a similar design */
  font-weight: bold;
  text-align: center;
  margin-bottom: 10px;
}

.new-modal-subtitle { /* "Your Meme Collection Level X" */
  text-align: center;
  font-size: clamp(1rem, 3vw, 1.2rem);
  color: #4F4F4F; /* Darker Grey for subtitle text */
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.level-badge.new-level-badge {
  background-color: #FE6B8B; /* Match h2 color - Pink */
  color: white;
  padding: 5px 12px;
  border-radius: 15px;
  font-size: clamp(0.8rem, 2.5vw, 1rem);
  margin-left: 10px;
}

.meme-gallery-modal.new-meme-gallery {
  background-color: transparent; /* No separate background for the gallery box itself */
  border: none;
  padding: 0;
  margin-top: 0;
  margin-bottom: 20px;
}

.meme-carousel.new-meme-carousel {
  /* Using existing flex properties */
}

.modal-meme-item-container.new-meme-item-container {
  /* Using existing flex properties */
}

.arrow-btn.new-arrow-btn {
  font-size: 2rem; /* Slightly smaller */
  color: #aaa;
}
.arrow-btn.new-arrow-btn:hover:not(:disabled) {
  color: #FE6B8B; /* Match theme color */
}

.modal-meme-image-single.new-modal-meme-image {
  max-width: 100%;
  max-height: 280px; /* Increased from 220px */
  object-fit: contain;
  border-radius: 8px;
  margin-bottom: 15px; /* Increased from 10px */
}

.meme-identifier.new-meme-identifier {
  font-size: clamp(1.1rem, 3vw, 1.3rem); /* Increased from 0.9rem/2.5vw/1.1rem */
  color: #4F4F4F;
  text-align: center;
  margin-bottom: 18px; /* Increased from 15px */
  font-weight: bold;
}

.modal-meme-sentiments.new-modal-sentiments {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sentiment-progress-section {
  margin-bottom: 15px;
  width: 100%;
}

.sentiment-grid.new-sentiment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px 25px;
  width: 100%;
}

.sentiment-item.new-sentiment-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.sentiment-item.new-sentiment-item .sentiment-label {
  font-size: 1rem;
  color: #555;
  font-weight: 500;
  width: 40%;
  text-align: right;
  padding-right: 10px;
}

.sentiment-tag.new-sentiment-tag {
  padding: 5px 10px;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  background-color: #f1f1f1;
  color: #333;
  width: 60%;
  text-align: center;
}

/* Progress Bar Styles */
.sentiment-progress-container {
  width: 100%;
  height: 32px; /* Increased from 26px */
  background-color: #f3f3f3;
  border-radius: 16px; /* Increased from 13px */
  overflow: hidden;
  position: relative;
  margin-bottom: 10px; /* Added margin */
}

.sentiment-progress-bar {
  height: 100%;
  background: linear-gradient(to right, #FE6B8B, #FF8E53);
  border-radius: 16px; /* Increased from 13px */
  transition: width 0.5s ease;
}

.sentiment-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #333;
  font-weight: bold;
  font-size: 1.1rem; /* Increased from 0.9rem */
  text-shadow: 0px 0px 2px rgba(255, 255, 255, 0.7);
}

/* Updated Button Colors */
.next-level-btn { 
  background: linear-gradient(135deg, #e75a97 20%, #4d8cd5 80%); 
  color: white; 
}

.play-again-btn { 
  background: linear-gradient(135deg, #FF3D8C 0%, #FF8B3D 100%); 
  color: white; 
}

.exit-btn { 
  background: #f5f7fa; 
  color: #333; 
  border: 1px solid #ddd; 
}

/* Media Query for smaller screens */
@media (max-width: 600px) {
  .sentiment-grid.new-sentiment-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .sentiment-item.new-sentiment-item .sentiment-label {
    width: 45%;
  }
  
  .sentiment-tag.new-sentiment-tag {
    width: 55%;
  }
}

.modal-controls.new-modal-controls {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  margin-top: 30px !important;
  margin-bottom: 20px !important;
  padding: 15px !important;
  gap: 15px !important;
  flex-wrap: nowrap !important;
  width: 100% !important;
  flex-direction: column !important;
}

.control-btn.new-control-btn {
  display: inline-block !important;
  color: white !important;
  border: none !important;
  border-radius: 25px !important;
  padding: 12px 25px !important;
  font-size: 1.1rem !important;
  font-weight: bold !important;
  cursor: pointer !important;
  transition: all 0.2s ease-in-out !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
  min-width: 130px !important;
  text-align: center !important;
  margin: 5px !important;
  text-decoration: none !important;
  appearance: button !important;
  -webkit-appearance: button !important;
}

.control-btn.new-control-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2) !important;
}

/* Updated Button Colors */
.next-level-btn { 
  background: linear-gradient(135deg, #e75a97 20%, #4d8cd5 80%) !important; 
  color: white !important;
  width: 80% !important;
  max-width: 300px !important;
  margin-bottom: 15px !important;
}

.play-again-btn { 
  background: linear-gradient(135deg, #FF3D8C 0%, #FF8B3D 100%) !important; 
  color: white !important;
}

.exit-btn { 
  background: #4A4A4A !important; 
  color: white !important; 
  border: none !important;
}

/* Create a container for the second row buttons */
.second-row-buttons {
  display: flex !important;
  justify-content: center !important;
  gap: 15px !important;
  width: 100% !important;
}

</style> 