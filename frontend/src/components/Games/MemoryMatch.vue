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
    <div v-if="gameStarted && !gameOver" class="game-status-bar">
      <div class="timer-display">
        Time: {{ formatTime(timer) }}
      </div>
      <div class="score-display">
        Score: {{ score }}
      </div>
      <div class="match-counter">
        Matches: {{ matchedPairs }} / {{ totalPairs }}
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
      <div v-if="currentLevel === 2 && cards.length > levels[1].pairs * 2" class="level-2-help">Scroll to see more cards</div>
    </div>
    
    <!-- Victory modal - Simplified -->
    <div v-if="showVictoryModal" class="victory-modal">
      <div class="modal-content">
        <h2>{{ gameWon ? 'Victory!' : 'Game Over' }}</h2>
        
        <div class="modal-subtitle" v-if="gameWon">
          You matched all {{ totalPairs }} pairs in {{ formatTime(levels[currentLevel].gameTime - timer) }}!
          <span class="level-badge">Level {{ currentLevel }}</span>
        </div>
         <div class="modal-subtitle" v-else>
          {{ timer <= 0 ? "Time's up!" : "Keep trying!" }}
          <span class="level-badge">Level {{ currentLevel }}</span>
        </div>
        <p>Score: {{ score }}</p>
        
        <!-- Meme gallery in modal - updated for single display with navigation -->
        <div v-if="gameWon && gameMemesForModal.length > 0 && currentModalMeme" class="meme-gallery-modal victory-style">
          <h3>Know more about it</h3>
          <div class="meme-carousel">
            <button @click="prevModalMeme" class="arrow-btn left-arrow" :disabled="currentModalMemeIndex === 0">&#x276E;</button>
            <div class="modal-meme-item-container">
              <img 
                :src="currentModalMeme.image_url || '/images/placeholder.png'" 
                :alt="currentModalMeme.text"
                @error="event => (event.target as HTMLImageElement).src = 'https://via.placeholder.com/100?text=Error'"
                class="modal-meme-image-single"
              >
              <p class="modal-meme-text-under-image">{{ currentModalMeme.text || 'N/A' }}</p>
              <div class="modal-meme-sentiments">
                <span v-if="currentModalMeme.humour" class="sentiment-tag humour">Humour: {{ currentModalMeme.humour }}</span>
                <span v-if="currentModalMeme.sarcasm" class="sentiment-tag sarcasm">Sarcasm: {{ currentModalMeme.sarcasm }}</span>
                <span v-if="currentModalMeme.offensive" class="sentiment-tag offensive">Offensive: {{ currentModalMeme.offensive }}</span>
                <span v-if="currentModalMeme.motivational" class="sentiment-tag motivational">Motivational: {{ currentModalMeme.motivational }}</span>
                <span v-if="currentModalMeme.overall_sentiment" class="sentiment-tag overall">Overall Sentiment: {{ currentModalMeme.overall_sentiment }}</span>
              </div>
            </div>
            <button @click="nextModalMeme" class="arrow-btn right-arrow" :disabled="currentModalMemeIndex === gameMemesForModal.length - 1">&#x276F;</button>
          </div>
        </div>
        <div v-else-if="!gameWon" class="meme-gallery-simplified">
          <p>Better luck next time!</p>
        </div>
        
        <div class="modal-controls">
          <button v-if="gameWon && canAdvanceLevel" class="control-btn advance-btn" @click="challengeAdvance">CHALLENGE ADVANCE</button>
          <button class="control-btn try-again-btn" @click="restartGame">TRY AGAIN</button>
          <button class="control-btn exit-btn" @click="exitGame">EXIT</button>
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
  1: { pairs: 3, columns: 3, name: 'Easy (3 pairs)', cardWidth: 'w-24', cardHeight: 'h-24', textSize: 'text-xs', gameTime: 60 },
  2: { pairs: 10, columns: 5, name: 'Medium (10 pairs)', cardWidth: 'w-20', cardHeight: 'h-20', textSize: 'text-xxs', gameTime: 180 },
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
  stopGame();
  gameOver.value = false;
  gameWon.value = false;
  currentLevel.value = 1;
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
  background-color: #f8f9fa;
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
  color: #1a73e8;
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
  flex-shrink: 0;
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
  margin: 0 auto;
}

.game-board {
  display: grid;
  width: clamp(280px, min(90vh - 150px, 95vw), 1200px);
  margin: 0 auto;
  gap: clamp(5px, 1.5vmin, 15px);
  padding: clamp(5px, 1.5vmin, 15px);
  background: rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  position: relative;
  box-sizing: border-box;
}

.game-board.level-1 {
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  aspect-ratio: 3 / 2;
  max-width: clamp(280px, 60vh, 600px);
}

.game-board.level-2 {
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(4, 1fr);
  aspect-ratio: 5 / 4;
  max-width: clamp(400px, 80vh, 1000px);
}

.card {
  aspect-ratio: 1 / 1;
  perspective: 1000px;
  cursor: pointer;
  position: relative;
  transform-style: preserve-3d;
  width: 100%;
  height: 100%;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
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
  background: linear-gradient(145deg, #4e73df, #224abe);
}
.card-front::before {
    content: '?';
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
  opacity: 0.7;
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
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
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
  color: #1a73e8;
  margin-bottom: 15px;
}

.modal-subtitle {
  text-align: center;
  font-size: clamp(0.9rem, 2.5vw, 1.1rem);
  color: #5f6368;
  margin-bottom: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-weight: bold;
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
  background-color: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
  padding: 15px;
  margin-top: 15px;
  margin-bottom: 20px;
}

.meme-gallery-modal.victory-style h3 {
  text-align: center;
  font-size: clamp(1.1rem, 3vw, 1.3rem);
  color: #d6336c;
  margin-bottom: 15px;
  font-weight: bold;
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
  color: #1a73e8;
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
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.75rem;
  white-space: nowrap;
  z-index: 50;
  pointer-events: none;
}

@media (max-width: 768px) {
  .game-board.level-2 {
    overflow-y: auto;
    aspect-ratio: unset;
    grid-template-rows: repeat(auto-fill, minmax(min(18vw, 100px), 1fr));
  }
  .level-2-help {
    display: block;
  }
  .modal-content {
    width: 95%;
  }
}

@media (max-width: 480px) {
  .game-header h1 { font-size: clamp(1.3rem, 6vw, 1.8rem); }
  .level-selector button { padding: 4px 8px; margin: 0 3px; }
  .game-status-bar { padding: 6px 8px; }
  .game-board.level-1 {
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(3, 1fr);
    aspect-ratio: 2 / 3;
  }
  .game-board.level-2 {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(5, 1fr);
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
    }
    .game-header h1 {
        font-size: clamp(1rem, 4vh, 1.3rem);
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
        font-size: clamp(0.7rem, 3vh, 0.9rem);
    }
    .game-board-container {
    }
    .game-board {
        gap: clamp(3px, 1vmin, 5px);
        padding: clamp(3px, 1vmin, 5px);
        width: clamp(200px, min(85vh - 80px, 90vw), 800px);
    }
     .game-board.level-1 {
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(2, 1fr);
        aspect-ratio: 3 / 2;
    }
    .game-board.level-2 {
        grid-template-columns: repeat(5, 1fr);
        grid-template-rows: repeat(4, 1fr);
        aspect-ratio: 5 / 4;
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

</style> 