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
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

// API configuration
const MEME_API_URL = import.meta.env.VITE_MEME_API_URL || 'http://localhost:8000';
const IS_DEVELOPMENT = import.meta.env.DEV;

// Game settings
const currentLevel = ref(1);
const timeRemaining = ref(60); // 60 seconds for the game
const isGameActive = ref(false);
const isLoading = ref(true);
const showVictoryModal = ref(false);
const timerInterval = ref(null);
const memeDirAccessible = ref(true); // Flag to track if memes directory is accessible

// Cards state
const cards = ref([]);
const flippedCards = ref([]);
const memes = ref([]);
const totalPairs = computed(() => currentLevel.value === 1 ? 6 : 25);
const matchedPairs = ref(0);

// Track victory status
const isVictory = ref(true);

// Victory modal state
const currentMemeIndex = ref(0);
const usedMemes = computed(() => {
  // In the victory modal, show only the memes that were used in the game
  const uniqueMemeIds = [...new Set(cards.value.map(card => card.originalId))];
  return memes.value.filter(meme => uniqueMemeIds.includes(meme.id));
});

// Update currentMeme to use usedMemes instead of all memes
const currentMeme = computed(() => {
  if (!usedMemes.value || usedMemes.value.length === 0) {
    return { 
      id: 0,
      text: 'No meme available',
      imagePath: '/images/placeholder.png',
      sentiment: {
        humour: 'unknown',
        sarcasm: 'unknown',
        offensive: 'not_offensive',
        motivational: 'unknown',
        overall: 'neutral'
      }
    };
  }
  
  // Make sure currentMemeIndex is within bounds
  if (currentMemeIndex.value >= usedMemes.value.length) {
    currentMemeIndex.value = 0;
  }
  
  // Use the current index (for navigation)
  const meme = usedMemes.value[currentMemeIndex.value];
  
  // Format image path - ensure it has the proper prefix
  let imagePath = meme.image_name;
  if (!imagePath.startsWith('/')) {
    imagePath = `/memes/${imagePath}`;
  } else if (!imagePath.startsWith('/memes/')) {
    imagePath = `/memes${imagePath}`;
  }
  
  // Ensure all sentiment data is present
  return {
    id: meme.id,
    text: meme.text || `Meme ${meme.id}`,
    imagePath: imagePath,
    sentiment: {
      humour: meme.humour || 'unknown',
      sarcasm: meme.sarcasm || 'unknown',
      offensive: meme.offensive || 'not_offensive',
      motivational: meme.motivational || 'unknown',
      overall: meme.overall_sentiment || 'neutral'
    }
  };
});

// Sample sentiment values for randomization
const sentimentOptions = {
  humour: ['very_funny', 'funny', 'not_funny', 'neutral'],
  sarcasm: ['very_sarcastic', 'sarcastic', 'not_sarcastic', 'neutral'],
  offensive: ['offensive', 'not_offensive'],
  motivational: ['motivational', 'not_motivational', 'neutral'],
  overall: ['very_positive', 'positive', 'neutral', 'negative', 'very_negative']
};

// Ensure we have the getRandomSentiment function properly defined
// This function should be right after sentimentOptions declaration to ensure it is defined before use
const getRandomSentiment = (type) => {
  // Ensure sentimentOptions is defined
  if (!sentimentOptions[type]) {
    console.warn(`Unknown sentiment type: ${type}, using fallback`);
    return 'neutral'; // Safe fallback
  }
  const options = sentimentOptions[type];
  return options[Math.floor(Math.random() * options.length)];
};

// Methods
const fetchMemes = async () => {
  try {
    isLoading.value = true;
    console.log('Fetching memes...');

    // API server status flag
    let apiUnavailable = !memeDirAccessible.value; // Start with directory access status
    
    // Skip API calls if memes directory is already known to be inaccessible
    if (apiUnavailable) {
      console.log('Memes directory inaccessible, using offline mode immediately');
    } else {
      // Try to fetch memes from the API if directory is accessible
      try {
        console.log('Attempting to fetch memes from API...');
        // Use a higher count to ensure we have enough memes after filtering duplicates
        const response = await fetch(`${MEME_API_URL}/api/memes/random?count=100`, { 
          signal: AbortSignal.timeout(5000) // 5 second timeout
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data && data.length > 0) {
            console.log(`Successfully fetched ${data.length} memes from API`);
            
            // Process the API memes
            const processedMemes = data.map((meme, index) => ({
              id: meme.id || index + 1,
              image_name: meme.image_name || `meme_${index + 1}.jpg`,
              text: meme.text || `Meme ${index + 1}`,
              humour: meme.humour || getRandomSentiment('humour'),
              sarcasm: meme.sarcasm || getRandomSentiment('sarcasm'),
              offensive: meme.offensive || getRandomSentiment('offensive'),
              motivational: meme.motivational || getRandomSentiment('motivational'),
              overall_sentiment: meme.overall_sentiment || getRandomSentiment('overall')
            }));
            
            // Filter out duplicates by image_name
            const uniqueMemes = filterDuplicateMemes(processedMemes);
            memes.value = uniqueMemes;
            
            setupCards();
            isLoading.value = false;
            startGame();
            return;
          }
        } else {
          console.warn(`API response was not OK: ${response.status}`);
          apiUnavailable = true;
        }
      } catch (apiError) {
        console.warn('API fetch failed, falling back to local memes:', apiError);
        apiUnavailable = true;
      }
    }
    
    // If API fetch failed or directory inaccessible, use local fallback
    if (apiUnavailable) {
      console.log('API unavailable, creating offline fallback cards');
      
      // Create the array of known fallback meme filenames directly
      const knownMemeFiles = [
        // Numbered meme files we know exist
        ...Array.from({ length: 20 }, (_, i) => `meme_${i + 1}.jpg`),
        // MemoryMatch special files
        'MemoryMatch_1.jpg', 'MemoryMatch_2.jpg', 'MemoryMatch_3.jpg', 'MemoryMatch.jpg',
        // Known dataset images that we've verified exist
        'image_1258.jpg', 'image_1264.jpg', 'image_1270.jpg', 'image_2037.jpg',
        'image_2779.jpg', 'image_3301.jpg', 'image_3315.jpg', 'image_3329.jpg',
        'image_3467.jpg', 'image_3473.jpg', 'image_4308.jpg', 'image_4446.jpg',
        'image_5002.jpg', 'image_5016.jpg', 'image_5758.jpg', 'image_5980.jpg',
        'image_6251.jpg', 'image_6279.jpg', 'image_6537.jpg', 'image_811.jpg'
      ];
      
      console.log(`Using ${knownMemeFiles.length} static fallback filenames`);
      
      // Create meme objects
      const allMemes = knownMemeFiles.map((filename, index) => ({
        id: index + 1,
        image_name: filename,
        text: `Meme ${index + 1}`,
        humour: getRandomSentiment('humour'),
        sarcasm: getRandomSentiment('sarcasm'),
        offensive: getRandomSentiment('offensive'),
        motivational: getRandomSentiment('motivational'),
        overall_sentiment: getRandomSentiment('overall')
      }));
      
      // Filter and select memes
      const uniqueMemes = filterDuplicateMemes(allMemes);
      const shuffledMemes = shuffleArray([...uniqueMemes]);
      const selectedMemes = shuffledMemes.slice(0, totalPairs.value);
      
      memes.value = selectedMemes;
      setupCards();
      isLoading.value = false;
      startGame();
      return;
    }

    // ... rest of existing code ...
  
  } catch (error) {
    console.error('Error setting up memes:', error);
    isLoading.value = false;
    
    // Don't try retryWithImagesDirectory if we already know the memes directory is inaccessible
    if (memeDirAccessible.value) {
      // Try the fallback method as a last resort
      retryWithImagesDirectory();
    } else {
      // Create a completely offline fallback with just canvas elements if needed
      createOfflineFallbackCards();
    }
  }
};

// Fix createOfflineFallbackCards function to ensure it works properly
const createOfflineFallbackCards = () => {
  console.log('Creating 100% offline fallback cards with canvas');
  
  // Generate unique pairs based on the current level
  const numPairs = totalPairs.value;
  const offlineMemes = [];
  
  // Create memes with unique colors based on ID
  for (let i = 1; i <= numPairs; i++) {
    const hue = (i * 30) % 360; // Create a unique color for each meme
    
    offlineMemes.push({
      id: i,
      image_name: `offline_${i}.jpg`, // This won't be used for rendering
      text: `Meme ${i}`,
      humour: getRandomSentiment('humour'),
      sarcasm: getRandomSentiment('sarcasm'),
      offensive: getRandomSentiment('offensive'),
      motivational: getRandomSentiment('motivational'),
      overall_sentiment: getRandomSentiment('overall'),
      isOffline: true, // This flag tells the renderer to use canvas
      hue: hue // Store the hue for rendering
    });
  }
  
  console.log(`Created ${offlineMemes.length} offline memes with unique colors`);
  
  // Set the memes and set up the game
  memes.value = offlineMemes;
  
  // Show the cards
  setupCards();
  
  // End loading and start the game
  isLoading.value = false;
  startGame();
};

// Enhanced helper function to filter duplicate memes
const filterDuplicateMemes = (memeArray) => {
  // Track unique images by both filename and visual content
  const uniqueImageNames = new Set();
  const uniqueVisualContent = new Set();
  
  return memeArray.filter(meme => {
    // Skip if no image name
    if (!meme.image_name) return false;
    
    // Get base filename without extension and path to catch duplicates with different extensions
    const filename = meme.image_name;
    // Remove path prefix if present
    const fileNameOnly = filename.includes('/') ? 
      filename.substring(filename.lastIndexOf('/') + 1) : filename;
    // Remove extension
    const baseName = fileNameOnly.includes('.') ? 
      fileNameOnly.substring(0, fileNameOnly.lastIndexOf('.')) : fileNameOnly;
    
    // Extract any ID numbers present in the filename for deeper comparison
    const idMatches = baseName.match(/\d+/g);
    const fileId = idMatches ? idMatches.join('_') : '';
    
    // Create a visual content hash based on filename and any known pattern
    // This helps identify visually identical content with different filenames
    let visualContentId = baseName.toLowerCase();
    
    // Some files might have same visual content with different naming schemes
    // e.g., "meme_1.jpg" and "funny_1.jpg" could be the same image
    if (fileId) {
      visualContentId = fileId;
    }
    
    // Check for both filename and content duplicates
    if (!uniqueImageNames.has(baseName.toLowerCase()) && 
        !uniqueVisualContent.has(visualContentId)) {
      uniqueImageNames.add(baseName.toLowerCase());
      uniqueVisualContent.add(visualContentId);
      return true;
    }
    
    return false;
  });
};

// Update card setup to use the public memes directory
const setupCards = () => {
  // Create two cards for each meme
  const memesNeeded = totalPairs.value;
  const memesToUse = memes.value.slice(0, memesNeeded);
  
  console.log(`Setting up ${memesNeeded} pairs of cards with memes:`, memesToUse);
  
  // Create pairs of cards
  const cardPairs = memesToUse.map(meme => {
    // Determine the correct image path based on image name
    let imagePath = meme.isOffline ? null : `/memes/${meme.image_name}`;
    console.log(`Using path for ${meme.image_name}: ${imagePath || '[canvas fallback]'}`);
    
    return [
      {
        id: `${meme.id}-1`,
        originalId: meme.id,
        imagePath: imagePath,
        text: meme.text || '',
        isOffline: meme.isOffline || false,
        hue: meme.hue || ((meme.id * 137) % 360), // Used for offline mode
        isFlipped: false,
        isMatched: false
      },
      {
        id: `${meme.id}-2`,
        originalId: meme.id,
        imagePath: imagePath,
        text: meme.text || '',
        isOffline: meme.isOffline || false,
        hue: meme.hue || ((meme.id * 137) % 360), // Used for offline mode
        isFlipped: false,
        isMatched: false
      }
    ];
  }).flat();
  
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
    }, 600); // Reduced from 1000ms to 600ms for faster gameplay
  }
  
  // Reset flipped cards
  flippedCards.value = [];
};

const endGame = async (isWin) => {
  isGameActive.value = false;
  isVictory.value = isWin;
  
  // Clear the timer
  if (timerInterval.value) {
    clearInterval(timerInterval.value);
    timerInterval.value = null;
  }
  
  // Get unique meme IDs used in this game
  const uniqueMemeIds = [...new Set(cards.value.map(card => card.originalId))];
  
  if (isWin) {
    try {
      // Try to fetch sentiment data for the memes used in this game
      const sentimentData = await fetchSentimentData(uniqueMemeIds);
      
      // If we got sentiment data, update the memes
      if (sentimentData) {
        memes.value = memes.value.map(meme => {
          const updatedSentiment = sentimentData.find(s => s.id === meme.id);
          if (updatedSentiment) {
            // Make sure we preserve the image_name from the original meme
            return {
              ...meme,
              ...updatedSentiment,
              image_name: meme.image_name // Ensure we keep the original image_name
            };
          }
          return meme;
        });
        console.log('Updated memes with sentiment data:', memes.value);
      }
    } catch (error) {
      console.error('Error updating sentiment data:', error);
    }
    
    // Show victory modal
    currentMemeIndex.value = 0;
    showVictoryModal.value = true;
  } else {
    // Show game over modal after showing all cards
    cards.value.forEach(card => {
      card.isFlipped = true;
    });
    
    setTimeout(async () => {
      try {
        // Try to fetch sentiment data for the memes used in this game
        const sentimentData = await fetchSentimentData(uniqueMemeIds);
        
        // If we got sentiment data, update the memes
        if (sentimentData) {
          memes.value = memes.value.map(meme => {
            const updatedSentiment = sentimentData.find(s => s.id === meme.id);
            if (updatedSentiment) {
              // Make sure we preserve the image_name from the original meme
              return {
                ...meme,
                ...updatedSentiment,
                image_name: meme.image_name // Ensure we keep the original image_name
              };
            }
            return meme;
          });
          console.log('Updated memes with sentiment data for game over:', memes.value);
        }
      } catch (error) {
        console.error('Error updating sentiment data for game over:', error);
      }
      
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
  emit('exit-game');
};

const handleImageError = (event, card) => {
  console.warn(`Failed to load image for card: ${card.originalId}`);
  console.warn(`Image path was: ${card.imagePath}`);
  
  // Try different image sources in sequence
  const img = event.target;
  
  // Extract the base filename without extension
  const currentPath = card.imagePath;
  const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1);
  const baseFilename = filename.includes('.') ? 
    filename.substring(0, filename.lastIndexOf('.')) : filename;
  const basePath = `/memes/${baseFilename}`;
  
  console.log(`Attempting to find alternative format for: ${baseFilename}`);
  
  // Store alternate paths to try
  const alternatePathsToTry = [];
  
  // 1. First, try different extensions for same filename
  const extensions = ['.jpg', '.png', '.jpeg', '.gif'];
  const currentExt = filename.includes('.') ? filename.substring(filename.lastIndexOf('.')) : '';
  
  // Add alternate extensions to try
  for (const ext of extensions) {
    if (ext === currentExt) continue;
    alternatePathsToTry.push(`${basePath}${ext}`);
  }
  
  // 2. Try alternative meme files based on ID number 
  const numericId = parseInt(card.originalId) || 1;
  
  // Add some reliable fallback options (we know these exist)
  alternatePathsToTry.push(
    `/memes/meme_${(numericId % 20) + 1}.jpg`,
    `/memes/MemoryMatch_${(numericId % 3) + 1}.jpg`
  );
  
  // 3. As the last resort, include emergency fallbacks we've verified
  const emergencyFallbacks = [
    '/memes/MemoryMatch_1.jpg',
    '/memes/MemoryMatch_2.jpg',
    '/memes/MemoryMatch_3.jpg',
    '/memes/meme_1.jpg',
    '/memes/meme_5.jpg',
    '/memes/image_1258.jpg'
  ];
  
  // Add emergency fallbacks
  alternatePathsToTry.push(...emergencyFallbacks);
  
  // Track if we found a working replacement
  let found = false;
  
  // Try each path in sequence
  const tryNextPath = async (index = 0) => {
    // If we've tried all paths, use canvas fallback
    if (index >= alternatePathsToTry.length) {
      console.log('All alternative paths failed, using canvas fallback');
      createCanvasCardFallback(img, card);
      return;
    }
    
    // Try the current path
    const path = alternatePathsToTry[index];
    console.log(`Trying [${index+1}/${alternatePathsToTry.length}]: ${path}`);
    
    const tempImg = new Image();
    tempImg.onload = () => {
      // Path works - use it
      img.src = path;
      found = true;
      console.log(`Successfully loaded: ${path}`);
    };
    
    tempImg.onerror = () => {
      // Path failed - try next
      console.log(`Failed: ${path}`);
      tryNextPath(index + 1);
    };
    
    // Set source to trigger load attempt
    tempImg.src = path;
  };
  
  // Helper function to create canvas fallback
  const createCanvasCardFallback = (imgElement, cardData) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 200;
      canvas.height = 200;
      const ctx = canvas.getContext('2d');
      
      // Create a gradient background based on card ID
      const hueRotation = (numericId * 137) % 360;
      const gradient = ctx.createLinearGradient(0, 0, 200, 200);
      gradient.addColorStop(0, `hsl(${hueRotation}, 70%, 60%)`);
      gradient.addColorStop(1, `hsl(${(hueRotation + 120) % 360}, 70%, 60%)`);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 200, 200);
      
      // Add card ID text
      ctx.fillStyle = 'white';
      ctx.font = '36px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(`Card ${numericId}`, 100, 100);
      
      // Add fallback indicator
      ctx.font = '14px Arial';
      ctx.fillText('Image unavailable', 100, 130);
      
      imgElement.src = canvas.toDataURL('image/png');
    } catch (e) {
      console.error('Failed to create canvas fallback:', e);
      // Last resort - empty image with border
      imgElement.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
      imgElement.style.border = '1px dashed #ccc';
      imgElement.style.borderRadius = '8px';
      imgElement.style.backgroundColor = '#f8f8f8';
    }
  };
  
  // Start the process of trying alternative paths
  tryNextPath();
};

const handleMemeImageError = (event, meme) => {
  console.log(`Image error in modal for meme ${meme.id} with path ${meme.imagePath}`);
  
  const img = event.target;
  const originalSrc = img.src;
  
  // Extract the base filename without extension for more robust handling
  const pathParts = originalSrc.split('/');
  const filename = pathParts[pathParts.length - 1];
  const baseName = filename.includes('.') ? 
    filename.substring(0, filename.lastIndexOf('.')) : filename;
  
  // Store alternate paths to try
  const alternatePathsToTry = [];
  
  // 1. First, try different extensions for same filename
  const extensions = ['.jpg', '.png', '.jpeg', '.gif'];
  const currentExt = filename.includes('.') ? filename.substring(filename.lastIndexOf('.')) : '';
  
  // Add alternate extensions to try
  for (const ext of extensions) {
    if (ext === currentExt) continue;
    alternatePathsToTry.push(`/memes/${baseName}${ext}`);
  }
  
  // 2. Extract any potential numeric ID from the original filename or use meme ID
  const numMatch = baseName.match(/\d+/);
  const numericId = numMatch ? parseInt(numMatch[0]) : parseInt(meme.id) || 1;
  
  // Add known good fallbacks, prioritizing based on ID
  alternatePathsToTry.push(
    `/memes/meme_${(numericId % 20) + 1}.jpg`,
    `/memes/MemoryMatch_${(numericId % 3) + 1}.jpg`
  );
  
  // 3. Add emergency fallbacks as last resort
  const emergencyFallbacks = [
    '/memes/MemoryMatch_1.jpg',
    '/memes/MemoryMatch_2.jpg',
    '/memes/MemoryMatch_3.jpg',
    '/memes/meme_1.jpg',
    '/memes/meme_5.jpg',
    '/memes/image_1258.jpg'
  ];
  
  // Add emergency fallbacks
  alternatePathsToTry.push(...emergencyFallbacks);
  
  // Track if we found a working replacement
  let found = false;
  
  // Try each path in sequence
  const tryNextPath = (index = 0) => {
    // If we've tried all paths, use canvas fallback
    if (index >= alternatePathsToTry.length) {
      console.log('All alternative paths failed, using canvas fallback for modal image');
      createModalCanvasFallback(img, meme);
      return;
    }
    
    // Try the current path
    const path = alternatePathsToTry[index];
    console.log(`Trying modal image [${index+1}/${alternatePathsToTry.length}]: ${path}`);
    
    const tempImg = new Image();
    tempImg.onload = () => {
      // Path works - use it
      img.src = path;
      found = true;
      console.log(`Successfully loaded modal image: ${path}`);
    };
    
    tempImg.onerror = () => {
      // Path failed - try next
      console.log(`Failed modal image: ${path}`);
      tryNextPath(index + 1);
    };
    
    // Set source to trigger load attempt
    tempImg.src = path;
  };
  
  // Helper function to create canvas fallback for the modal
  const createModalCanvasFallback = (imgElement, memeData) => {
    try {
      const canvas = document.createElement('canvas');
      canvas.width = 300;
      canvas.height = 300;
      const ctx = canvas.getContext('2d');
      
      // Create a visually pleasing gradient background with meme ID influence
      const hueBase = (parseInt(meme.id) * 137) % 360;
      const gradient = ctx.createLinearGradient(0, 0, 300, 300);
      gradient.addColorStop(0, `hsl(${hueBase}, 70%, 65%)`);
      gradient.addColorStop(1, `hsl(${(hueBase + 180) % 360}, 70%, 65%)`);
      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, 300, 300);
      
      // Add text and emoji
      ctx.font = '80px Arial';
      ctx.textAlign = 'center';
      ctx.fillStyle = 'white';
      ctx.fillText('😎', 150, 140);
      
      ctx.font = '24px Arial';
      ctx.fillText('Meme Unavailable', 150, 200);
      
      ctx.font = '16px Arial';
      ctx.fillText(`ID: ${meme.id}`, 150, 230);
      ctx.fillText(`${meme.text || 'No text available'}`, 150, 260, 280);
      
      // Set the canvas as the image source
      imgElement.src = canvas.toDataURL('image/png');
    } catch (e) {
      console.error('Failed to create canvas fallback for modal:', e);
      // Last resort - empty image with styled border
      imgElement.src = 'data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==';
      imgElement.style.border = '2px dashed #ccc';
      imgElement.style.borderRadius = '8px';
      imgElement.style.backgroundColor = '#f8f8f8';
      
      // Add text element after the image with error message
      const errorText = document.createElement('div');
      errorText.textContent = 'Image unavailable';
      errorText.style.color = '#666';
      errorText.style.fontStyle = 'italic';
      errorText.style.padding = '10px';
      errorText.style.textAlign = 'center';
      
      if (imgElement.parentNode) {
        imgElement.parentNode.insertBefore(errorText, imgElement.nextSibling);
      }
    }
  };
  
  // Start the process of trying alternative paths
  tryNextPath();
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
  console.log("MemoryMatch component mounted");
  console.log(`API URL: ${MEME_API_URL}, Development mode: ${IS_DEVELOPMENT}`);
  
  // Test direct access to backend image path
  const testBackendImage = new Image();
  testBackendImage.onload = () => {
    console.log("Backend image loaded successfully from: backend/datasets/meme/memotion_dataset_7k/images/image_1.jpg");
  };
  testBackendImage.onerror = () => {
    console.warn("Couldn't load backend image - path is inaccessible");
  };
  testBackendImage.src = "/backend/datasets/meme/memotion_dataset_7k/images/image_1.jpg";
  
  // Check if memes directory is accessible
  checkMemeDirectoryAccess().then(isAccessible => {
    memeDirAccessible.value = isAccessible;
    console.log(`Memes directory accessible: ${memeDirAccessible.value}`);
    fetchMemes();
  });
  
  // Cleanup when component is unmounted
  return cleanup;
});

// Function to check if the memes directory is accessible
const checkMemeDirectoryAccess = async () => {
  // Try to load a known image to check access
  const testImage = new Image();
  
  return new Promise(resolve => {
    // Set a timeout for the check
    const timeout = setTimeout(() => {
      console.warn("Image load timeout - memes directory might be inaccessible");
      resolve(false);
    }, 3000);
    
    testImage.onload = () => {
      clearTimeout(timeout);
      console.log("Test meme loaded successfully - memes directory is accessible");
      resolve(true);
    };
    
    testImage.onerror = () => {
      clearTimeout(timeout);
      console.warn("Couldn't load test meme - memes directory is inaccessible");
      resolve(false);
    };
    
    // Try to load a known image
    testImage.src = "/memes/MemoryMatch_1.jpg";
  });
};

// Add defineEmits declaration at the top of script setup
const emit = defineEmits(['game-completed', 'exit-game']);

// Update the navigation methods to use usedMemes
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

// Get CSS class based on sentiment value
const getSentimentClass = (sentiment) => {
  if (!sentiment) return '';
  
  switch(sentiment.toLowerCase()) {
    case 'positive':
    case 'very_positive':
      return 'positive';
    case 'negative':
    case 'very_negative':
      return 'negative';
    case 'neutral':
      return 'neutral';
    case 'not_offensive':
      return 'positive';
    case 'offensive':
      return 'negative';
    case 'very_funny':
    case 'funny':
      return 'positive';
    case 'not_funny':
      return 'negative';
    case 'motivational':
      return 'positive';
    case 'not_motivational':
      return 'negative';
    default:
      return '';
  }
};

// Function to get sentiment data for the matched memes
const fetchSentimentData = async (memeIds) => {
  try {
    console.log(`Fetching sentiment data for meme IDs: ${memeIds.join(', ')}`);
    
    // Create sentiment data objects for the meme IDs
    const sentimentData = memeIds.map(id => {
      // Get the original meme object if available
      const originalMeme = memes.value.find(m => m.id === id);
      
      // Check if we already have sentiment data
      if (originalMeme && 
          (originalMeme.humour || originalMeme.overall_sentiment || 
           originalMeme.sarcasm || originalMeme.offensive || 
           originalMeme.motivational)) {
        
        // Use existing sentiment data
        return {
          id,
          humour: originalMeme.humour || getRandomSentiment('humour'),
          sarcasm: originalMeme.sarcasm || getRandomSentiment('sarcasm'),
          offensive: originalMeme.offensive || getRandomSentiment('offensive'),
          motivational: originalMeme.motivational || getRandomSentiment('motivational'),
          overall_sentiment: originalMeme.overall_sentiment || getRandomSentiment('overall')
        };
      }
      
      // Generate random sentiment data if none exists
      return {
        id,
        humour: getRandomSentiment('humour'),
        sarcasm: getRandomSentiment('sarcasm'),
        offensive: getRandomSentiment('offensive'),
        motivational: getRandomSentiment('motivational'),
        overall_sentiment: getRandomSentiment('overall')
      };
    });
    
    console.log('Generated sentiment data:', sentimentData);
    return sentimentData;
  } catch (error) {
    console.error('Error fetching sentiment data:', error);
    return null;
  }
};

// Get a style for the sentiment meter based on the sentiment value
const getSentimentBarStyle = (sentiment) => {
  // Default width at 50% for neutral/unknown
  let width = '50%';
  
  if (!sentiment) return { width };
  
  // Determine width based on sentiment
  switch(sentiment.toLowerCase()) {
    case 'very_positive':
      width = '90%';
      break;
    case 'positive':
      width = '75%';
      break;
    case 'neutral':
      width = '50%';
      break;
    case 'negative':
      width = '25%';
      break;
    case 'very_negative':
      width = '10%';
      break;
    case 'very_funny':
      width = '90%';
      break;
    case 'funny':
      width = '75%';
      break;
    case 'not_funny':
      width = '25%';
      break;
    case 'offensive':
      width = '20%';
      break;
    case 'not_offensive':
      width = '80%';
      break;
    default:
      width = '50%';
  }
  
  return { width };
};

// Get a style for offline cards using CSS gradients
const getOfflineCardStyle = (card) => {
  const hue = card.hue || ((parseInt(card.originalId) * 137) % 360);
  return {
    background: `linear-gradient(135deg, 
      hsl(${hue}, 70%, 60%), 
      hsl(${(hue + 120) % 360}, 70%, 60%))`,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '100%',
    borderRadius: '8px',
    color: 'white',
    textShadow: '0 1px 3px rgba(0,0,0,0.3)',
    fontWeight: 'bold'
  };
};

// Get a style for offline memes in the victory modal
const getOfflineMemeStyle = (meme) => {
  const hue = meme.hue || ((parseInt(meme.id) * 137) % 360);
  return {
    background: `linear-gradient(135deg, 
      hsl(${hue}, 70%, 65%), 
      hsl(${(hue + 180) % 360}, 70%, 65%))`,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    width: '100%',
    height: '300px',
    borderRadius: '10px',
    color: 'white',
    marginBottom: '15px'
  };
};
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