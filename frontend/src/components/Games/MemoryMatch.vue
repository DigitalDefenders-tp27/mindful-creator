<template>
  <div class="memory-game-container">
    <!-- Game header -->
    <div class="game-header">
      <h1>Meme Memory Match</h1>
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
    <div class="game-board-container">
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
              <!-- If offline mode, create a canvas card -->
              <div v-if="card.isOffline" class="offline-card" :style="getOfflineCardStyle(card)">
                <span class="card-id">{{ card.originalId }}</span>
                <span class="card-text">{{ card.text }}</span>
              </div>
              <!-- Otherwise use the image -->
              <img 
                v-else
                :src="card.imagePath || '/images/placeholder.png'" 
                :alt="card.text" 
                @error="handleImageError($event, card)"
              >
            </div>
          </div>
        </div>
      </div>
      <div v-if="currentLevel === 2" class="level-2-help">Scroll to see more cards</div>
    </div>
    
    <!-- Victory modal -->
    <div v-if="showVictoryModal" class="victory-modal">
      <div class="modal-content">
        <h2>{{ isVictory ? 'Victory!' : 'Game Over' }}</h2>
        
        <div class="modal-subtitle">
          Your Meme Collection
          <span class="level-badge">Level {{ currentLevel }}</span>
        </div>
        
        <!-- Meme gallery display -->
        <div class="meme-gallery">
          <button class="arrow-btn left" @click="prevMeme">&lt;</button>
          
          <div class="meme-display">
            <!-- If offline mode, show a canvas-based meme -->
            <div v-if="currentMeme.isOffline" class="offline-meme" :style="getOfflineMemeStyle(currentMeme)">
              <div class="offline-emoji">😎</div>
              <div class="offline-meme-text">{{ currentMeme.text }}</div>
            </div>
            <!-- Otherwise use the image -->
            <img 
              v-else
              :src="currentMeme.imagePath || '/images/placeholder.png'" 
              :alt="currentMeme.text"
              @error="(e) => handleMemeImageError(e, currentMeme)"
            >
            
            <!-- Sentiment information -->
            <div class="meme-sentiment">
              <h3>{{ currentMeme.text }}</h3>
              
              <div class="sentiment-summary">
                <div class="sentiment-meter">
                  <div class="meter-label">Overall Sentiment</div>
                  <div class="meter-bar">
                    <div class="meter-fill" 
                      :style="getSentimentBarStyle(currentMeme.sentiment.overall)"
                      :class="getSentimentClass(currentMeme.sentiment.overall)">
                    </div>
                  </div>
                  <div class="meter-value">{{ currentMeme.sentiment.overall }}</div>
                </div>
              </div>
              
              <div class="sentiment-tags">
                <div class="tag" v-if="currentMeme.sentiment.humour">
                  <span class="label">Humour:</span>
                  <span class="value" :class="getSentimentClass(currentMeme.sentiment.humour)">
                    {{ currentMeme.sentiment.humour }}
                  </span>
                </div>
                
                <div class="tag" v-if="currentMeme.sentiment.sarcasm">
                  <span class="label">Sarcasm:</span>
                  <span class="value" :class="getSentimentClass(currentMeme.sentiment.sarcasm)">
                    {{ currentMeme.sentiment.sarcasm }}
                  </span>
                </div>
                
                <div class="tag" v-if="currentMeme.sentiment.motivational">
                  <span class="label">Motivational:</span>
                  <span class="value" :class="getSentimentClass(currentMeme.sentiment.motivational)">
                    {{ currentMeme.sentiment.motivational }}
                  </span>
                </div>
                
                <div class="tag" v-if="currentMeme.sentiment.offensive">
                  <span class="label">Offensive:</span>
                  <span class="value" :class="getSentimentClass(currentMeme.sentiment.offensive)">
                    {{ currentMeme.sentiment.offensive }}
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <button class="arrow-btn right" @click="nextMeme">&gt;</button>
        </div>
        
        <!-- Replace the modal controls -->
        <div class="modal-controls">
          <button 
            v-if="currentLevel === 1 && isVictory"
            class="control-btn next-btn" 
            @click="advanceLevel"
          >
            NEXT LEVEL
          </button>
          
          <button 
            class="control-btn play-btn" 
            @click="restartGame"
          >
            PLAY AGAIN
          </button>
          
          <button 
            class="control-btn exit-btn" 
            @click="exitGame"
          >
            EXIT
          </button>
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
import { ref, computed, onMounted, watch, onUnmounted } from 'vue';
import axios from 'axios';

// API configuration
const MEME_API_URL = import.meta.env.VITE_MEME_API_URL || 'https://api.tiezhu.org';
// const IS_DEVELOPMENT = import.meta.env.DEV; // Keep if used

// Game settings
const currentLevel = ref(1);
const timeRemaining = ref(60); // 60 seconds for the game
const isGameActive = ref(false);
const isLoading = ref(true);
const showVictoryModal = ref(false);
const timerInterval = ref(null);
// const memeDirAccessible = ref(true); // This is no longer needed as backend handles access

// Cards state
const cards = ref([]);
const flippedCards = ref([]);
const memes = ref([]); 
const totalPairs = computed(() => currentLevel.value === 1 ? 6 : 25);
const matchedPairs = ref(0);
const createdObjectUrls = ref([]); // New: To store Object URLs for cleanup

// Track victory status
const isVictory = ref(true);

// Victory modal state
const currentMemeIndex = ref(0);
const usedMemes = computed(() => {
  // In the victory modal, show only the memes that were used in the game
  // The `id` from the backend is now the `originalId`
  const uniqueMemeOriginalIds = [...new Set(cards.value.map(card => card.originalId))];
  return memes.value.filter(meme => uniqueMemeOriginalIds.includes(meme.id)); // meme.id is the originalId now
});

// Update currentMeme to use usedMemes and the new data structure
const currentMeme = computed(() => {
  if (!usedMemes.value || usedMemes.value.length === 0) {
    return { 
      id: 0, 
      text: 'No meme available',
      imagePath: '/images/placeholder.png', // Default placeholder if no Object URL yet or error
      isOffline: false, 
      sentiment: {
        humour: 'unknown',
        sarcasm: 'unknown',
        offensive: 'unknown',
        motivational: 'unknown',
        overall: 'neutral'
      }
    };
  }
  
  if (currentMemeIndex.value >= usedMemes.value.length) {
    currentMemeIndex.value = 0;
  }
  
  const memeFromGame = usedMemes.value[currentMemeIndex.value];
  
  return {
    id: memeFromGame.id,
    text: memeFromGame.text || `Meme ${memeFromGame.id}`,
    imagePath: memeFromGame.displayImagePath || '/images/placeholder.png', // Use displayImagePath (Object URL)
    isOffline: false, 
    sentiment: { 
      humour: memeFromGame.humour || 'unknown',
      sarcasm: memeFromGame.sarcasm || 'unknown',
      offensive: memeFromGame.offensive || 'unknown',
      motivational: memeFromGame.motivational || 'unknown',
      overall: memeFromGame.overall_sentiment || 'neutral'
    }
  };
});

// Methods

// NEW: Function to initialize game data from the backend
const initializeGameFromBackend = async () => {
  isLoading.value = true;
  // Clear any previously created Object URLs before fetching new ones
  revokeAllObjectUrls(); 

  console.log('Initializing game from backend (frontend download strategy)...');
  try {
    const response = await fetch(`${MEME_API_URL}/api/games/memory_match/initialize_game`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ level: currentLevel.value }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to initialize game: ${response.status}`);
    }

    const rawMemesData = await response.json(); // These have image_url

    if (rawMemesData && rawMemesData.length > 0) {
      console.log(`Received ${rawMemesData.length} raw meme data objects from backend.`);
      // Now download images and create Object URLs
      const memesWithObjectUrls = await Promise.all(
        rawMemesData.map(async (meme) => {
          try {
            const imageResponse = await fetch(meme.image_url, { mode: 'cors' }); // Use original image_url
            if (!imageResponse.ok) {
              console.error(`Failed to download image: ${meme.image_url}, status: ${imageResponse.status}`);
              return { ...meme, displayImagePath: null }; // Or a default placeholder path
            }
            const blob = await imageResponse.blob();
            const objectURL = URL.createObjectURL(blob);
            createdObjectUrls.value.push(objectURL); // Store for cleanup
            return { ...meme, displayImagePath: objectURL };
          } catch (downloadError) {
            console.error(`Error downloading image ${meme.image_url}:`, downloadError);
            return { ...meme, displayImagePath: null }; // Fallback
          }
        })
      );
      
      memes.value = memesWithObjectUrls.filter(meme => meme.displayImagePath !== null);
      if (memes.value.length < rawMemesData.length) {
        console.warn(`Could only successfully download images for ${memes.value.length}/${rawMemesData.length} memes.`);
      }

      if (memes.value.length === 0 && rawMemesData.length > 0) {
        alert('Failed to download any meme images. Please check network or try again.');
        isLoading.value = false;
        return;
      }
      
      console.log(`Successfully processed ${memes.value.length} memes with Object URLs.`);
      setupCards();
      startGame();
    } else {
      console.error('No memes received from backend or empty array.');
      alert('Failed to load meme data for the game. Please try again later.');
    }
  } catch (error) {
    console.error('Error initializing game (frontend download strategy): ', error);
    alert(`Error initializing game: ${error.message}. Please check backend and try again.`);
  } finally {
    isLoading.value = false;
  }
};

// setupCards will now use memes.value populated by initializeGameFromBackend
// and memes will have a `displayImagePath` property (the Object URL)
const setupCards = () => {
  if (!memes.value || memes.value.length === 0) {
    console.error("Cannot setup cards, memes array is empty or image downloads failed.");
    return;
  }
  const memesToUse = memes.value; 
  
  console.log(`Setting up ${memesToUse.length} pairs of cards with memes (using Object URLs):`, memesToUse);
  
  const cardPairs = memesToUse.map(meme => {
    return [
      {
        id: `${meme.id}-1`, 
        originalId: meme.id, 
        imagePath: meme.displayImagePath, // Use the Object URL for display
        text: meme.text || '',
        isOffline: false, 
        hue: null, 
        isFlipped: false,
        isMatched: false,
        original_url_for_error_handling: meme.image_url // Store original URL if needed for specific error handling
      },
      {
        id: `${meme.id}-2`,
        originalId: meme.id,
        imagePath: meme.displayImagePath, // Use the Object URL for display
        text: meme.text || '',
        isOffline: false,
        hue: null,
        isFlipped: false,
        isMatched: false,
        original_url_for_error_handling: meme.image_url
      }
    ];
  }).flat();
  
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
  if (cards.value && cards.value.length > 0) {
    cards.value.forEach(card => {
      card.isFlipped = false;
      card.isMatched = false;
    });
  }
  
  // Clear any existing timer
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
  
  revokeAllObjectUrls();
};

const flipCard = (card) => {
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
    }, 600); // Reduced from 1000ms to 600ms for faster gameplay
  }
  
  // Reset flipped cards
  flippedCards.value = [];
};

const endGame = async (isWin) => {
  isGameActive.value = false;
  isVictory.value = isWin;
  
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
  
  // Sentiment data is already part of the meme objects in memes.value
  // The `usedMemes` computed property will filter these for the modal.
  
  if (isWin) {
    currentMemeIndex.value = 0;
    showVictoryModal.value = true;
  } else {
    // Show game over modal after showing all cards
    if (cards.value && cards.value.length > 0){
        cards.value.forEach(card => {
        card.isFlipped = true;
        });
    }
    
    setTimeout(() => {
      currentMemeIndex.value = 0;
      showVictoryModal.value = true;
    }, 2000);
  }
};

const formatTime = (seconds) => {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const advanceLevel = () => {
  currentLevel.value = 2;
  showVictoryModal.value = false;
  // resetGameState(); // Should be called by initializeGameFromBackend indirectly via startGame
  initializeGameFromBackend(); // Fetch new memes for level 2
};

const restartGame = () => {
  showVictoryModal.value = false;
  // resetGameState(); // startGame calls resetGameState
  // fetchMemes(); // Old way, now use initializeGameFromBackend
  initializeGameFromBackend();
};

// NEW: Function to revoke all created Object URLs
const revokeAllObjectUrls = () => {
  if (createdObjectUrls.value.length > 0) {
    console.log(`Revoking ${createdObjectUrls.value.length} Object URLs.`);
    createdObjectUrls.value.forEach(url => URL.revokeObjectURL(url));
    createdObjectUrls.value = []; // Clear the array
  }
};

const exitGame = async () => {
  showVictoryModal.value = false;
  resetGameState(); 
  // await cleanupTemporaryGameFiles(); // No longer calling backend for this
  revokeAllObjectUrls(); // Frontend cleanup
  emit('exit-game');
};

// Simplified image error handlers for Object URLs
const handleImageError = (event, card) => {
  // If an Object URL fails to load, it might have been revoked or the initial download failed.
  console.warn(`Failed to load image for card: ${card.originalId} using Object URL: ${card.imagePath}. Original DB URL was: ${card.original_url_for_error_handling}`);
  const img = event.target;
  // Fallback to canvas. The card object passed here should have originalId.
  createCanvasCardFallback(img, { originalId: card.originalId }); // Pass a minimal object for canvas fallback
};

const handleMemeImageError = (event, memeInModal) => {
  console.warn(`Image error in modal for meme ${memeInModal.id} using Object URL: ${memeInModal.imagePath}.`);
  const img = event.target;
  // The memeInModal object should have the necessary `id` for canvas fallback.
  createModalCanvasFallback(img, { id: memeInModal.id, text: memeInModal.text }); // Pass a minimal object
};

// Canvas fallback functions (keep these as they are good general fallbacks)
const createCanvasCardFallback = (imgElement, cardData) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 200; // Or use card dimensions
      canvas.height = 200;
      const ctx = canvas.getContext('2d');
      
      const numericId = parseInt(String(cardData.originalId).replace(/[^0-9]/g, '')) || 1;
      const hueRotation = (numericId * 137) % 360;
      const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
      gradient.addColorStop(0, `hsl(${hueRotation}, 70%, 60%)`);
      gradient.addColorStop(1, `hsl(${(hueRotation + 120) % 360}, 70%, 60%)`);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      ctx.fillStyle = 'white';
      ctx.font = 'bold 24px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(`Meme ${numericId}`, canvas.width/2, canvas.height/2 - 10);
      ctx.font = '14px Arial';
      ctx.fillText('Unavailable', canvas.width/2, canvas.height/2 + 15);
      
      imgElement.src = canvas.toDataURL('image/png');
    } catch (e) {
      console.error('Failed to create canvas card fallback:', e);
      imgElement.src = '/images/placeholder.png'; // Final fallback
    }
};

const createModalCanvasFallback = (imgElement, memeData) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 300;
      canvas.height = 300;
      const ctx = canvas.getContext('2d');
      
      const numericId = parseInt(String(memeData.id).replace(/[^0-9]/g, '')) || 1;
      const hueBase = (numericId * 137) % 360;
      const gradient = ctx.createLinearGradient(0, 0, 300, 300);
      gradient.addColorStop(0, `hsl(${hueBase}, 70%, 65%)`);
      gradient.addColorStop(1, `hsl(${(hueBase + 180) % 360}, 70%, 65%)`);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 300, 300);
      
      ctx.font = '80px Arial';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'white';
      ctx.fillText('🚫', 150, 140); // Emoji for unavailable
      
      ctx.font = 'bold 20px Arial';
      ctx.fillText('Meme Unavailable', 150, 200);
      
      ctx.font = '14px Arial';
      ctx.fillText(`ID: ${memeData.id}`, 150, 230);
      
      imgElement.src = canvas.toDataURL('image/png');
    } catch (e) {
      console.error('Failed to create canvas modal fallback:', e);
      imgElement.src = '/images/placeholder.png'; // Final fallback
    }
};

// Cleanup when component is unmounted
const performCleanup = () => { // Renamed to avoid conflict, this is frontend cleanup
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
  revokeAllObjectUrls();
};

// Load game on mount
onMounted(() => {
  console.log("MemoryMatch component mounted. Frontend download strategy.");
  initializeGameFromBackend();
});

onUnmounted(() => {
  performCleanup();
});

// emit is already defined
// const emit = defineEmits(['game-completed', 'exit-game']);

// Navigation methods (nextMeme, prevMeme) should work fine with usedMemes
const nextMeme = () => {
  if (usedMemes.value.length > 0) {
    currentMemeIndex.value = (currentMemeIndex.value + 1) % usedMemes.value.length;
  }
};

const prevMeme = () => {
  if (usedMemes.value.length > 0) {
    currentMemeIndex.value = (currentMemeIndex.value - 1 + usedMemes.value.length) % usedMemes.value.length;
  }
};

// Sentiment display helpers (getSentimentClass, getSentimentBarStyle)
// These should work if `currentMeme.sentiment` has the expected structure.
// The backend now provides overall_sentiment, humour, sarcasm, etc. directly.
const getSentimentClass = (sentimentValue) => {
  if (!sentimentValue) return '';
  
  const sentiment = String(sentimentValue).toLowerCase(); // Ensure it's a string and lowercase

  // Updated to match potential values from meme_fetch or general positive/negative
  if (sentiment.includes('positive') || sentiment.includes('funny') || sentiment === 'motivational' || sentiment === 'not_offensive' || sentiment === 'hilarious' || sentiment === 'very_funny') {
    return 'positive';
  }
  if (sentiment.includes('negative') || sentiment.includes('not_funny') || sentiment === 'offensive' || sentiment === 'not_motivational') {
    return 'negative';
  }
  if (sentiment.includes('neutral') || sentiment === 'general' || sentiment === 'unknown') {
    return 'neutral';
  }
  return ''; // Default if no specific class
};

const getSentimentBarStyle = (sentimentValue) => {
  let width = '50%'; // Neutral default
  if (!sentimentValue) return { width };

  const sentiment = String(sentimentValue).toLowerCase();

  // Simplified mapping based on general positive/negative/neutral
  if (sentiment.includes('very_positive') || sentiment.includes('very_funny') || sentiment === 'hilarious') width = '90%';
  else if (sentiment.includes('positive') || sentiment.includes('funny') || sentiment === 'motivational' || sentiment === 'not_offensive') width = '75%';
  else if (sentiment.includes('very_negative') || sentiment === 'offensive') width = '10%';
  else if (sentiment.includes('negative') || sentiment.includes('not_funny') || sentiment === 'not_motivational') width = '25%';
  else if (sentiment.includes('neutral') || sentiment === 'general' || sentiment === 'unknown') width = '50%';
  
  return { width };
};

// fetchSentimentData is no longer needed as data comes with initial load
// const fetchSentimentData = async (memeIds) => { ... };

// Offline styles (getOfflineCardStyle, getOfflineMemeStyle) are no longer primary,
// but canvas fallbacks might use similar styling if they create offline-like appearances.
// The `isOffline` flag is now always false for game cards/memes.
// The template sections for v-if="card.isOffline" or v-if="currentMeme.isOffline" will not be hit.
// Consider removing them or keeping them only if canvas fallbacks are styled to look "offline".
// For now, let's assume the canvas fallbacks are sufficient and these explicit offline styles are not needed
// for the primary card/meme display.

// The template needs to use `card.imagePath` directly for `<img>` src.
// The `offline-card` and `offline-meme` divs in the template might be removed if `isOffline` is always false.
// Let's check the template part:
// <div v-if="card.isOffline" class="offline-card" ...>
// <div v-if="currentMeme.isOffline" class="offline-meme" ...>
// These will indeed not render. The canvas fallbacks are injected directly into the <img> src.
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
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.game-status-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  padding: 8px 15px;
  background-color: #D8FF89;
  border-radius: 10px;
  font-size: 1.5rem;
  font-weight: bold;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  align-self: center;
  flex-shrink: 0;
}

.timer-display {
  margin-right: 30px;
  font-family: 'Courier New', monospace;
}

.match-counter {
  font-weight: bold;
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
  width: min(90vh - 120px, 98vw);
  height: auto;
  margin: 0 auto;
  gap: 15px;
  padding: 15px;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  position: relative;
  box-sizing: border-box;
}

.game-board.level-1 {
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: repeat(3, 1fr);
  aspect-ratio: 4/3;
  max-width: 1200px;
  width: 98vw;
}

.game-board.level-2 {
  grid-template-columns: repeat(10, 1fr);
  grid-template-rows: repeat(5, 1fr);
  gap: 10px;
  max-width: 1400px;
  width: 98vw;
  aspect-ratio: 2/1;
  place-items: center;
  align-content: center;
  justify-content: center;
  overflow: visible;
}

/* For wider screens, maximize horizontal space in level 2 */
@media (min-width: 1200px) {
  .game-board.level-2 {
    grid-template-columns: repeat(10, 1fr);
    grid-template-rows: repeat(5, 1fr);
    max-width: 1800px;
    width: 98vw;
    gap: 15px;
  }
}

/* For narrow screens, use scrolling layout in level 2 */
@media (max-width: 768px) {
  .game-header h1 {
    font-size: 1.8rem;
    margin-bottom: 5px;
  }

  .game-status-bar {
    font-size: 1.1rem;
    padding: 8px 12px;
    margin-bottom: 8px;
  }
  
  .game-board {
    width: 95vw;
    height: auto;
    gap: 10px;
    padding: 10px;
  }
  
  .game-board.level-1 {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(3, 1fr);
    aspect-ratio: 4/3;
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(5, 1fr);
    grid-template-rows: repeat(10, 1fr);
    gap: 8px;
    overflow-y: auto;
    max-height: 80vh;
    aspect-ratio: auto;
    overflow-x: hidden;
    scrollbar-width: thin;
  }
  
  .game-board.level-2 .card {
    min-width: 70px;
  }
  
  /* Show scrollbar and help text only on mobile */
  .game-board.level-2::-webkit-scrollbar {
    width: 5px;
  }
  
  .game-board.level-2::-webkit-scrollbar-thumb {
    background-color: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
  }
  
  /* Modal styles */
  .modal-controls {
    flex-direction: column;
    gap: 10px;
  }
  
  .control-btn {
    width: 100%;
    max-width: 200px;
  }
  
  .modal-content {
    padding: 20px;
    width: 95%;
    height: 95%;
    border-radius: 15px;
  }
  
  .modal-content h2 {
    font-size: 2.5rem;
    margin-bottom: 15px;
  }
  
  .meme-display img {
    max-width: 90%;
    max-height: 250px;
  }
  
  .victory-modal {
    padding: 10px;
  }
  
  .meme-gallery {
    flex-direction: column;
  }
  
  .arrow-btn {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 10;
  }
  
  .arrow-btn.left {
    left: 5px;
  }
  
  .arrow-btn.right {
    right: 5px;
  }
  
  .meme-display {
    margin: 0 40px;
  }
}

@media (max-width: 480px) {
  .memory-game-container {
    padding: 5px;
  }
  
  .game-header h1 {
    font-size: 1.5rem;
    margin-bottom: 5px;
  }
  
  .game-status-bar {
    font-size: 1rem;
    padding: 5px 10px;
    margin-bottom: 5px;
  }
  
  .game-board {
    width: 98vw;
    gap: 5px;
    padding: 8px;
  }
  
  .game-board.level-1 {
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(4, 1fr);
    aspect-ratio: 3/4;
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(13, 1fr);
    max-height: 80vh;
    gap: 5px;
  }
  
  .game-board.level-2 .card {
    min-width: 60px;
  }
  
  .modal-content {
    padding: 15px 10px;
    width: 98%;
    height: 98%;
    border-radius: 10px;
  }
  
  .modal-content h2 {
    font-size: 1.8rem;
    margin-bottom: 10px;
  }
  
  .modal-subtitle {
    font-size: 0.9rem;
    margin-bottom: 10px;
  }
  
  .meme-display {
    margin: 0 30px;
  }
  
  .arrow-btn {
    width: 30px;
    height: 30px;
  }
}

.card {
  aspect-ratio: 1 / 1;
  perspective: 1200px;
  cursor: pointer;
  position: relative;
  transform-style: preserve-3d;
  width: 100%;
  height: 100%;
  min-width: 90px;
}

.game-board.level-2 .card {
  width: 100%;
  min-width: 80px;
  margin: 0 auto;
}

.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.4s ease-out;
  transform-style: preserve-3d;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
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
  background: linear-gradient(135deg, #FF3D8C, #FF8B3D);
}

.card-back {
  background-color: white;
  transform: rotateY(180deg);
  border: 1px solid #ddd;
}

.card-back img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  background-color: #fff;
  transition: opacity 0.3s ease;
  border-radius: 6px;
  padding: 3px;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.level-2 .card {
  /* Smaller height not needed since cards are now sized by the grid */
}

.victory-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(8px);
  padding: 15px;
  box-sizing: border-box;
}

.modal-content {
  background-color: white;
  border-radius: 20px;
  padding: 25px;
  width: min(95%, 1000px);
  height: min(95%, 800px);
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  max-height: 90vh;
}

.modal-content h2 {
  text-align: center;
  font-size: 3.5rem;
  color: #FF3D8C;
  margin-bottom: 20px;
  text-shadow: 0 3px 10px rgba(255, 61, 140, 0.3);
}

.modal-subtitle {
  text-align: center;
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.level-badge {
  background-color: #FF3D8C;
  color: white;
  padding: 3px 10px;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: bold;
}

.sentiment-summary {
  width: 100%;
  margin-bottom: 15px;
}

.sentiment-meter {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
}

.meter-label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

.meter-bar {
  width: 100%;
  height: 12px;
  background-color: #E4EAF1;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 5px;
}

.meter-fill {
  height: 100%;
  transition: width 0.5s ease;
}

.meter-fill.positive {
  background-color: #D8FF89;
}

.meter-fill.negative {
  background-color: #FFD6E0;
}

.meter-fill.neutral {
  background-color: #E4EAF1;
}

.meter-value {
  font-size: 0.9rem;
  color: #666;
}

.meme-gallery {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  position: relative;
  overflow: hidden;
}

.arrow-btn {
  background-color: rgba(45, 45, 82, 0.7);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.3s ease;
  margin: 0 10px;
}

.arrow-btn:hover {
  background-color: rgba(45, 45, 82, 1);
  transform: scale(1.1);
}

.meme-sentiment {
  width: 100%;
  max-width: 500px;
  background-color: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 15px;
}

.meme-sentiment h3 {
  font-size: 1.3rem;
  margin-bottom: 15px;
  text-align: center;
  color: #2D2D52;
}

.sentiment-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.tag {
  background-color: white;
  border-radius: 20px;
  padding: 8px 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
}

.tag .label {
  font-weight: bold;
  margin-right: 8px;
  color: #555;
}

.tag .value {
  padding: 4px 10px;
  border-radius: 15px;
  font-weight: 500;
}

.tag .value.positive {
  background-color: #D8FF89;
  color: #2D5022;
}

.tag .value.negative {
  background-color: #FFD6E0;
  color: #8C2641;
}

.tag .value.neutral {
  background-color: #E4EAF1;
  color: #455A7F;
}

.meme-display {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100%;
  overflow-y: auto;
  padding: 10px;
  scrollbar-width: thin;
}

.meme-display::-webkit-scrollbar {
  width: 8px;
}

.meme-display::-webkit-scrollbar-track {
  background-color: #f1f1f1;
  border-radius: 10px;
}

.meme-display::-webkit-scrollbar-thumb {
  background-color: #FF3D8C;
  border-radius: 10px;
}

.meme-display img {
  max-width: min(100%, 500px);
  max-height: min(50%, 300px);
  width: auto;
  height: auto;
  border-radius: 10px;
  margin-bottom: 15px;
  object-fit: contain;
  background-color: #f5f5f5;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.1);
  padding: 10px;
  display: block;
}

.next-btn {
  background: linear-gradient(135deg, #4EC9C4, #3DA5DF);
}

.play-btn {
  background: linear-gradient(135deg, #FF8B3D, #FFC43D);
}

.exit-btn {
  background: linear-gradient(135deg, #8C8C8C, #666666);
}

.modal-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 15px;
}

.control-btn {
  color: white;
  border: none;
  border-radius: 30px;
  padding: 12px 25px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.control-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) and (orientation: portrait) {
  .game-board {
    width: 95vw;
    height: auto;
    aspect-ratio: 1/1;
  }
  
  .game-board.level-1 {
    aspect-ratio: 4/3;
  }
}

@media (max-width: 768px) and (orientation: landscape) {
  .game-header h1 {
    font-size: 1.5rem;
    margin-bottom: 2px;
  }
  
  .game-status-bar {
    padding: 5px 10px;
    margin-bottom: 5px;
    font-size: 1rem;
  }
  
  .game-board {
    width: 85vw;
    height: auto;
    aspect-ratio: 4/3;
    max-height: 75vh;
  }
  
  .game-board.level-1 {
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: repeat(3, 1fr);
    max-width: none;
    max-height: none;
  }
  
  .game-board.level-2 {
    grid-template-columns: repeat(6, 1fr);
    grid-template-rows: repeat(9, 1fr);
    gap: 8px;
    max-height: 65vh;
  }
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  transition: opacity 0.5s ease;
}

.spinner {
  border: 5px solid rgba(0, 0, 0, 0.1);
  border-left-color: #FF3D8C;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Only show help text on mobile screens */
.level-2-help {
  position: absolute;
  bottom: 15px; 
  left: 50%;
  transform: translateX(-50%);
  background-color: rgba(255, 61, 140, 0.8);
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
  opacity: 0.9;
  white-space: nowrap;
  z-index: 50;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  pointer-events: none;
  display: none; /* Hide by default */
}

/* Only show on mobile devices */
@media (max-width: 768px) {
  .level-2-help {
    display: block;
  }
}

/* Adjust for iPhone and other mobile devices in landscape */
@media screen and (max-height: 450px) and (orientation: landscape) {
  .memory-game-container {
    height: 100%;
    padding: 5px;
  }
  
  .game-header h1 {
    font-size: 1.3rem;
    margin-bottom: 2px;
  }
  
  .game-status-bar {
    padding: 3px 8px;
    margin-bottom: 3px;
    font-size: 0.9rem;
  }
  
  .game-board {
    width: min(95vh - 60px, 90vw);
    height: auto;
    aspect-ratio: 1/1;
    max-height: calc(100vh - 90px);
    gap: 4px;
    padding: 5px;
  }
}

/* Offline card styles */
.offline-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.card-id {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.card-text {
  font-size: 0.8rem;
  max-width: 80%;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* Offline meme styles in modal */
.offline-meme {
  width: 100%;
  max-width: 300px;
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
  margin-bottom: 15px;
}

.offline-emoji {
  font-size: 5rem;
  margin-bottom: 20px;
}

.offline-meme-text {
  font-size: 1.2rem;
  text-align: center;
  max-width: 80%;
  font-weight: bold;
}

@media (max-width: 768px) {
  .offline-meme {
    height: 250px;
  }
  
  .offline-emoji {
    font-size: 4rem;
  }
}

@media (max-width: 480px) {
  .offline-meme {
    height: 200px;
  }
  
  .offline-emoji {
    font-size: 3rem;
  }
  
  .card-id {
    font-size: 1.5rem;
  }
}
</style> 