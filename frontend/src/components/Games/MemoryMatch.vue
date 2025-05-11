<template>
  <div class="memory-game-container">
    <!-- Game header -->
    <div class="game-header">
      <h1>Meme Memory Match</h1>
      <!-- Level selection (simplified, can be expanded) -->
      <div v-if="!gameStarted && !gameOver" class="level-selector">
        <!-- Level selection removed from initial screen, game defaults to Level 1 -->
        <!-- Buttons were: <button @click="selectLevel(1)"...>, <button @click="selectLevel(2)"...> -->
        <p class="game-instructions">
          Welcome to Meme Memory Match! <br />
          Click the cards to find matching pairs of memes. Clear the board before time runs out!
        </p>
        <button @click="startGame" class="start-button">Start Game</button>
      </div>
    </div>
    
    <!-- Game status bar -->
    <div v-if="gameStarted && !gameOver" class="game-status-bar new-status-bar">
      <div class="status-item timer-display">
        Time: <span>{{ formatTime(timer) }}</span>
      </div>
      <div class="status-item score-display">
        Score: <span>{{ score }}</span>
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
        <h2 class="new-modal-h2">Victory!</h2>
        
        <div class="new-modal-subtitle">
          Your Meme Collection <span class="level-badge new-level-badge">Level {{ currentLevel }}</span>
        </div>
        
        <div v-if="gameWon && gameMemesForModal.length > 0 && currentModalMeme" class="meme-gallery-modal victory-style new-meme-gallery">
          <div class="meme-carousel new-meme-carousel">
            <button @click="prevModalMeme" class="arrow-btn left-arrow new-arrow-btn" :disabled="currentModalMemeIndex === 0">&#x276E;</button>
            <div class="modal-meme-item-container new-meme-item-container">
              <img 
                :src="currentModalMeme.image_url || '/images/placeholder.png'" 
                :alt="currentModalMeme.text"
                @error="event => (event.target as HTMLImageElement).src = 'https://via.placeholder.com/100?text=Error'"
                class="modal-meme-image-single new-modal-meme-image"
              >
              <p class="meme-identifier new-meme-identifier">Meme {{ currentModalMemeIndex + 1 }}</p>
              <div class="modal-meme-sentiments new-modal-sentiments">
                <div class="sentiment-row new-sentiment-row">
                  <span class="sentiment-label">Overall Sentiment:</span>
                  <span class="sentiment-tag overall new-sentiment-tag">{{ currentModalMeme.overall_sentiment || 'N/A' }}</span>
                </div>
                <div class="sentiment-grid new-sentiment-grid">
                  <div v-if="currentModalMeme.humour" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Humour:</span> <span class="sentiment-tag new-sentiment-tag humour">{{ currentModalMeme.humour }}</span>
                  </div>
                  <div v-if="currentModalMeme.sarcasm" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Sarcasm:</span> <span class="sentiment-tag new-sentiment-tag sarcasm">{{ currentModalMeme.sarcasm }}</span>
                  </div>
                  <div v-if="currentModalMeme.motivational" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Motivational:</span> <span class="sentiment-tag new-sentiment-tag motivational">{{ currentModalMeme.motivational }}</span>
                  </div>
                  <div v-if="currentModalMeme.offensive" class="sentiment-item new-sentiment-item">
                    <span class="sentiment-label">Offensive:</span> <span class="sentiment-tag new-sentiment-tag offensive">{{ currentModalMeme.offensive }}</span>
                  </div>
                </div>
              </div>
            </div>
            <button @click="nextModalMeme" class="arrow-btn right-arrow new-arrow-btn" :disabled="currentModalMemeIndex === gameMemesForModal.length - 1">&#x276F;</button>
          </div>
        </div>
        <div v-else-if="!gameWon" class="meme-gallery-simplified">
          <p>Better luck next time!</p>
        </div>
        
        <div class="modal-controls new-modal-controls">
          <button v-if="gameWon && canAdvanceLevel" class="control-btn new-control-btn next-level-btn" @click="challengeAdvance">NEXT LEVEL</button>
          <button class="control-btn new-control-btn play-again-btn" @click="restartGame">PLAY AGAIN</button>
          <button class="control-btn new-control-btn exit-btn" @click="exitGame">EXIT</button>
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
  1: { pairs: 6, columns: 4, name: 'Easy (6 pairs)', cardWidth: 'w-24', cardHeight: 'h-24', textSize: 'text-xs', gameTime: 120 }, // 6 pairs, 4x3 grid, 120s
  2: { pairs: 25, columns: 5, name: 'Medium (25 pairs)', cardWidth: 'w-20', cardHeight: 'h-20', textSize: 'text-xxs', gameTime: 300 },
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

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://api.tiezhu.org';

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
  if (processingFlip.value || clickedCard.isFlipped || clickedCard.isMatched || gameOver.value) {
    return;
  }

  if (flippedCards.value.length < 2) {
    clickedCard.isFlipped = true;
    flippedCards.value.push(clickedCard);

    if (flippedCards.value.length === 2) {
      processingFlip.value = true;
      checkForMatch();
    }
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
      card1.isFlipped = false;
      card2.isFlipped = false;
      flippedCards.value = [];
      processingFlip.value = false;
    }, 1000);
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
}

function nextModalMeme() {
  if (currentModalMemeIndex.value < gameMemesForModal.value.length - 1) {
    currentModalMemeIndex.value++;
  }
}

function prevModalMeme() {
  if (currentModalMemeIndex.value > 0) {
    currentModalMemeIndex.value--;
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

onMounted(() => {
  // Game starts on button click via startGame()
  // No automatic start here
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
  overflow: hidden;
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

.level-selector {
  margin-bottom: 10px;
  font-size: clamp(0.8rem, 2.5vw, 1rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}
.game-instructions {
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  color: #5f6368;
  margin-bottom: 10px;
  max-width: 500px;
  line-height: 1.4;
}

.start-button {
  padding: clamp(10px, 3vw, 12px) clamp(20px, 5vw, 25px);
  font-size: clamp(1rem, 3.5vw, 1.2rem);
  background-color: #34a853 !important;
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
  align-items: center;
  width: 100%;
  padding: 0;
  overflow: hidden;
  min-height: 0;
  box-sizing: border-box;
}

.game-board {
  display: grid;
  width: auto;
  height: auto;
  max-width: 90vw;
  max-height: 80vh;
  gap: clamp(5px, 1.5vmin, 10px);
  padding: clamp(5px, 1.5vmin, 10px);
  background: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
  position: relative;
  box-sizing: border-box;
}

.game-board.level-1 {
  grid-template-columns: repeat(4, 1fr); /* 4 columns for 6 pairs */
  grid-template-rows: repeat(3, 1fr);    /* 3 rows for 6 pairs */
  aspect-ratio: 4 / 3;
}

.game-board.level-2 {
  grid-template-columns: repeat(5, 1fr); /* Default 5 columns for 25 pairs */
  grid-template-rows: repeat(10, 1fr);   /* 10 rows for 25 pairs */
  aspect-ratio: 5 / 10; /* Default aspect ratio (simplifies to 1/2) */
  /* overflow-y: auto; will be applied by media queries when needed */
}

.card {
  aspect-ratio: 1 / 1;
  perspective: 1000px;
  cursor: pointer;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
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
  max-height: 200px;
  object-fit: contain;
  border-radius: 8px;
  margin-bottom: 10px;
  border: 1px solid #e0e0e0;
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
  display: none;
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 6px 12px;
  border-radius: 15px;
  font-size: clamp(0.7rem, 2vw, 0.8rem);
  white-space: nowrap;
  z-index: 50;
  pointer-events: none;
}

@media (max-width: 768px) {
  .game-board {
    max-height: calc(100vh - 140px);
    gap: clamp(4px, 1.2vmin, 8px);
    padding: clamp(4px, 1.2vmin, 8px);
  }
  .game-board.level-2 {
    overflow-y: auto; /* Enable scrolling for Level 2 on smaller screens */
    aspect-ratio: unset; /* Allow height to be determined by content for scrolling */
    width: 98%; /* Take most of the container width */
    height: auto; /* Height will be determined by content and max-height of .game-board */
    /* grid-template-columns will be inherited (5) or overridden by narrower media queries */
  }
  .level-2-help {
    display: block !important;
  }
  .modal-content {
    width: 95%;
  }
}

@media (max-width: 480px) {
  .game-board {
    max-height: calc(100vh - 120px);
    gap: 3px;
    padding: 3px;
  }
  .game-board.level-1 {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, 1fr);
    aspect-ratio: 2 / 3;
  }
  .game-board.level-2 {
    grid-template-columns: repeat(4, 1fr);
    width: 100%;
  }
  .modal-content {
    padding: 15px;
  }
   .modal-content h2 { font-size: clamp(1.5rem, 6vw, 2rem); }
   .control-btn { padding: 8px 15px; font-size: clamp(0.8rem, 2.5vw, 1rem); }
}

@media (max-height: 480px) and (orientation: landscape) {
    .memory-game-container {
        padding: 5px;
        gap: 5px;
    }
    .game-header { margin-bottom: 5px; }
    .game-header h1 {
        font-size: clamp(1.1rem, 4vh, 1.3rem);
        margin-bottom: 2px;
    }
    .level-selector {
        font-size: clamp(0.7rem, 3vh, 0.9rem);
        margin-bottom: 5px;
    }
    .level-selector button { padding: 3px 6px; }
    .game-status-bar {
        padding: 4px 6px;
        margin-bottom: 5px;
        font-size: clamp(0.75rem, 3vh, 0.9rem);
    }
    .game-board-container {
        margin: 0 auto;
    }
    .game-board {
        gap: clamp(3px, 1vmin, 5px);
        padding: clamp(3px, 1vmin, 5px);
    }
     .game-board.level-1 {
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(2, 1fr);
        aspect-ratio: 3 / 2;
    }
    .game-board.level-2 {
        grid-template-columns: repeat(7, 1fr); /* 7 columns for landscape Level 2 */
        aspect-ratio: unset; /* Correct: allow scrolling to determine height */
        overflow-y: auto; /* Correct: enable scrolling */
        width: 98vw; /* Take almost full viewport width */
    }
    .modal-content {
        width: 90%;
        max-height: 90vh;
        padding: 10px;
    }
    .modal-content h2 { font-size: clamp(1.2rem, 5vh, 1.8rem); }
    .modal-meme-image { max-height: 150px; }
    .modal-meme-sentiment { font-size: clamp(0.7rem, 2vh, 0.8rem); padding: 8px;}
    .control-btn { padding: 6px 12px; font-size: clamp(0.7rem, 2.5vh, 0.9rem); }
    .level-2-help {
        font-size: 0.65rem;
        padding: 3px 8px;
        bottom: 2px;
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
  color: #ffffff; /* White text for values */
}

.victory-modal.new-victory-modal {
  background-color: rgba(20, 20, 20, 0.85); /* Darker overlay, less transparency */
  backdrop-filter: blur(10px); /* Increased blur */
}

.modal-content.new-modal-content {
  background-color: #ffffff;
  border-radius: 16px; /* More rounded */
  padding: 20px;
  width: min(90%, 550px); /* Slightly adjusted width */
  max-height: 95vh;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25);
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
  max-height: 220px; /* Slightly more height for image */
  object-fit: contain;
  border-radius: 8px;
  margin-bottom: 10px;
  /* border: 1px solid #e0e0e0; */ /* Border removed as per design */
}

.meme-identifier.new-meme-identifier { /* "Meme X" */
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  color: #4F4F4F; /* Dark Grey */
  text-align: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.modal-meme-sentiments.new-modal-sentiments {
  background-color: #ffffff; /* White background for sentiment area to match modal */
  border-radius: 8px;
  padding: 15px;
  width: 100%;
  box-sizing: border-box;
}

.sentiment-row.new-sentiment-row { /* For "Overall Sentiment: value" */
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}
.sentiment-row.new-sentiment-row .sentiment-label {
  font-weight: bold;
  color: #333333; /* Black/Dark Grey for "Overall Sentiment:" */
  font-size: clamp(0.85rem, 2.2vw, 1rem);
}
.sentiment-row.new-sentiment-row .sentiment-tag.new-sentiment-tag {
  padding: 4px 10px;
  font-size: clamp(0.8rem, 2vw, 0.9rem);
  background-color: #E0E0E0; /* Light grey pill for overall sentiment value */
  color: #333333; /* Dark text */
}


.sentiment-grid.new-sentiment-grid {
  display: grid;
  grid-template-columns: 1fr; /* Each item takes full width for label: value display */
  gap: 8px; /* Reduced gap between sentiment rows */
}

.sentiment-item.new-sentiment-item {
  display: flex; /* Changed to flex for inline label and tag */
  justify-content: space-between; /* Pushes label and tag to ends */
  align-items: center; 
  width: 100%;
}

.sentiment-item.new-sentiment-item .sentiment-label {
  font-size: clamp(0.75rem, 1.8vw, 0.9rem); /* Slightly increased size */
  color: #828282; /* Lighter grey for individual sentiment labels */
  margin-bottom: 0; /* Remove bottom margin */
  margin-right: 8px; /* Add right margin for spacing */
}

.sentiment-tag.new-sentiment-tag {
  padding: 5px 12px; /* Adjusted padding for pill look */
  border-radius: 15px;
  font-size: clamp(0.75rem, 2vw, 0.9rem);
  font-weight: 500;
  border: none; /* Remove border from previous style */
  width: fit-content; /* Tag only as wide as its content */
}
/* New Sentiment Tag Colors (approximating from screenshot) */
.sentiment-tag.new-sentiment-tag.overall { background-color: #e0e0e0; color: #333; } /* Re-defined above, kept for clarity */
.sentiment-tag.new-sentiment-tag.humour { background-color: #6FCF97; color: #212529; } /* Brighter Green pill, dark text */
.sentiment-tag.new-sentiment-tag.sarcasm { background-color: #F2C94C; color: #212529; } /* Yellow/Orange pill, dark text */
.sentiment-tag.new-sentiment-tag.motivational { background-color: #6FCF97; color: #212529; } /* Brighter Green pill, dark text (same as humour) */
.sentiment-tag.new-sentiment-tag.offensive { background-color: #F2C94C; color: #212529; } /* Yellow/Orange pill, dark text (same as sarcasm) */


.modal-controls.new-modal-controls {
  gap: 10px; /* Reduced gap */
}

.control-btn.new-control-btn {
  border-radius: 25px; /* Pill shape */
  padding: clamp(10px, 2.5vw, 12px) clamp(20px, 4vw, 30px); /* Adjusted padding */
  font-size: clamp(0.85rem, 2.5vw, 1rem); /* Slightly smaller font */
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.control-btn.new-control-btn:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.next-level-btn { background: #56CCF2; color: #212529; } /* Light Blue/Cyan, dark text */
.play-again-btn { background: #F2994A; color: #212529; } /* Orange, dark text */
.exit-btn { background: #F2F2F2; color: #4F4F4F; border: 1px solid #BDBDBD; } /* Light grey, dark text, grey border */

</style> 