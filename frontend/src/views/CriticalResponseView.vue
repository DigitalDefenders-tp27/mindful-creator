<template>
    <div class="critical-response-view">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="slogan">
            <div class="title-group">
              <h1>Critical Response</h1>
              <h2>Turning Feedback into Growth</h2>
            </div>
            <p class="subtitle">Learn to handle criticism constructively and protect yourself from cyberbullying</p>
          </div>
          <div class="decorative-elements">
            <!-- 右上角第一排 / Top Row Right -->
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
            <!-- 右下角第一排 / Bottom Row 1 Right -->
            <div class="bottom-row-1">
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Z_Red.svg" alt="Z" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
              </div>
            </div>
          </div>
        </div>
      </section>
  
      <!-- Feeling Box -->
      <div class="feeling-box">
        <div class="bell-container">
          <img :src="bell" alt="Bell" class="bell-icon" />
        </div>
        <h2>HOW ARE YOU FEELING NOW?</h2>
        <div class="emotions">
          <div class="emoji-option" v-for="(emoji, index) in emojis" :key="index">
            <img
              :src="emoji.src"
              :alt="emoji.alt"
              class="emoji-img"
              :class="{ selected: selectedEmotion === emoji.alt }"
              @click="handleDotClick(emoji.alt)"
            />
          </div>
        </div>
      </div>
  
      <!-- Emotional Check-in Pop-up -->
      <div v-if="showCheckIn" class="overlay">
        <div class="popup">
          <h2>Would you like to take a moment to relax before continuing?</h2>
          <div class="buttons">
            <button @click="goToRelaxation">Yes, let me try</button>
            <button @click="closePopup">No, thanks. I'm ok to continue</button>
          </div>
        </div>
      </div>
  
      <!-- Comparison Section -->
      <div class="comparison">
        <div class="comparison-header">
          <div class="col">Constructive Criticism<br /><span>(Helpful Feedback 👍)</span></div>
          <div class="col label">What's the goal?</div>
          <div class="col">Cyberbullying<br /><span>(Harmful Attacks 🚨)</span></div>
        </div>
  
        <div class="comparison-row" v-for="(label, i) in labels" :key="i">
          <div class="cell left">{{ leftCol[i] }}</div>
          <div class="cell label">{{ label }}</div>
          <div class="cell right">{{ rightCol[i] }}</div>
        </div>
      </div>
  
      <!-- Seek Help Link -->
      <div class="seek-help">
        <RippleButton 
          class="help-button" 
          rippleColor="rgba(255, 255, 255, 0.6)"
          @click="handleSeekHelp"
        >
          SEEK HELP
        </RippleButton>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import InteractiveHoverButton from '@/components/ui/interactive-hover-button.vue'
  import RippleButton from '@/components/ui/ripple-button.vue'
  
  import bell from '../assets/emojis/bell.png'
  import happy from '../assets/emojis/Happy.png'
  import peace from '../assets/emojis/Peace.png'
  import angry from '../assets/emojis/Angry.png'
  import sad from '../assets/emojis/Sad.png'
  import mda from '../assets/emojis/Mad.png'
  
  const router = useRouter()
  const showCheckIn = ref(false)
  const selectedEmotion = ref(null)
  
  const goToRelaxation = () => router.push('/relaxation')
  const closePopup = () => (showCheckIn.value = false)
  const handleDotClick = (emotion) => {
    selectedEmotion.value = emotion
    showCheckIn.value = true
  }
  
  const handleSeekHelp = () => {
    window.open('https://www.esafety.gov.au/young-people/tough-situations/cyberbullying', '_blank')
  }
  
  const emojis = [
    { src: happy, alt: 'Happy' },
    { src: peace, alt: 'Sad' },
    { src: angry, alt: 'Angry' },
    { src: sad, alt: 'Confused' },
    { src: mda, alt: 'Frustrated' },
  ]
  
  const labels = [
    "What's the goal? 🎯",
    'How does it sound? 🗣️',
    'What do they say? 💬',
    'Where does it happen? 📍',
    'How does it make you feel? 😊',
  ]
  
  const leftCol = [
    'To help you improve. The person wants to share advice or opinions to make your content better. ✨',
    'Respectful, clear, and focused on your content. 🤝',
    '"Your video is great, but the sound could be clearer. Maybe try using a different mic?" 🎤',
    'Often in a thoughtful comment, private message, or a discussion space. 📱',
    'Encouraged to improve and learn. 🌱',
  ]
  
  const rightCol = [
    'To hurt, embarrass, or bring you down. The person is trying to make you feel bad. 👎',
    'Mean, rude, and often personal. 😠',
    '"Your voice is so annoying, just stop making videos!" ❌',
    'Usually in public comments, DMs, or even shared posts to mock you. 📢',
    'Upset, anxious, or even scared to post again. 😔',
  ]
  </script>
  
  <style scoped>
  .critical-response-view {
    background: #fffdf4;
    font-family: Avenir, Helvetica, sans-serif;
    text-align: center;
  }
  
  .hero-section {
    min-height: 75vh;
    background-color: rgb(255, 252, 244);
    display: flex;
    align-items: center;
    overflow: hidden;
    position: relative;
    z-index: 1;
    padding: 1rem 0;
  }
  
  .hero-content {
    position: relative;
    width: 100%;
    min-height: 75vh;
    display: flex;
    align-items: center;
    padding-left: 2rem;
    margin: 0 auto;
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
    background: linear-gradient(135deg, #8E2DE2 0%, #FF6B9B 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    display: block;
    margin-bottom: 1rem;
    white-space: normal;
    text-align: left;
  }
  
  .title-group h2 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
    line-height: 1.2;
    display: block;
    white-space: normal;
    text-align: left;
  }
  
  .subtitle {
    font-size: 1.25rem;
    color: #666;
    line-height: 1.4;
    margin-top: 1.5rem;
    white-space: normal;
    text-align: left;
  }
  
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
    }
  }
  
  .decorative-elements {
    position: absolute;
    top: 0;
    right: 0;
    width: 960px;
    height: 100%;
    display: grid;
    grid-template-columns: repeat(6, 160px);
    grid-template-rows: repeat(4, auto);
    row-gap: 1rem;
    padding: 2rem 0;
    z-index: 1;
    pointer-events: none;
    transform: translateX(-2rem);
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
  
  .bottom-row-1 {
    display: grid;
    grid-template-columns: repeat(3, 160px);
    gap: 0.5rem;
    align-items: start;
    margin: 0;
    padding: 0;
    grid-column: 4 / 7;
    grid-row: 2;
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
  
  /* Hover效果增强 */
  .top-row .element:hover {
    transform: rotate(-15deg) scale(1.1);
  }
  
  .bottom-row-1 .element:hover {
    transform: rotate(15deg) scale(1.1);
  }
  
  /* 响应式调整 */
  @media (max-width: 1800px) {
    .decorative-elements {
      width: 840px;
      grid-template-columns: repeat(6, 140px);
      opacity: 0.9;
      transform: translateX(-1.5rem);
    }
  }
  
  @media (max-width: 1536px) {
    .decorative-elements {
      width: 720px;
      grid-template-columns: repeat(6, 120px);
      opacity: 0.8;
      transform: translateX(-1rem);
    }
  }
  
  @media (max-width: 1280px) {
    .decorative-elements {
      width: 600px;
      grid-template-columns: repeat(6, 100px);
      opacity: 0.7;
      transform: translateX(-0.5rem);
      row-gap: 0.75rem;
    }
  }
  
  @media (max-width: 1024px) {
    .hero-section {
      min-height: 65vh;
    }
    
    .hero-content {
      min-height: 65vh;
    }
    
    .slogan {
      margin-left: 1.5rem;
    }
    
    .decorative-elements {
      transform: translateX(0) scale(0.9);
      opacity: 0.5;
      row-gap: 0.5rem;
    }

    .title-group h1 {
      @apply text-5xl;
    }
    
    .title-group h2 {
      @apply text-4xl;
      white-space: normal;
    }
    
    .subtitle {
      @apply text-xl;
      white-space: normal;
    }
  }
  
  @media (max-width: 768px) {
    .hero-section {
      min-height: 55vh;
    }
    
    .hero-content {
      min-height: 55vh;
    }
    
    .slogan {
      margin-left: 1rem;
    }
    
    .decorative-elements {
      opacity: 0;
      transform: translateX(0) scale(0.8);
      transition: opacity 0.3s ease;
    }

    .title-group h1 {
      @apply text-4xl;
    }
    
    .title-group h2 {
      @apply text-3xl;
    }
    
    .subtitle {
      @apply text-lg;
    }
  }
  
  @media (max-width: 640px) {
    .hero-section {
      padding: 1.5rem 0;
    }

    .hero-content {
      padding: 0 1rem;
    }

    .slogan {
      padding-top: 1rem;
    }

    .title-group h1 {
      @apply text-3xl;
    }
    
    .title-group h2 {
      @apply text-2xl;
    }
    
    .subtitle {
      @apply text-base;
    }
  }
  
  .feeling-box {
    border: 2px solid #333;
    padding: 2rem 1rem 1rem;
    border-radius: 24px;
    width: 90%;
    max-width: 1200px;
    margin: -30px auto 4rem;
    position: relative;
    background: white;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    z-index: 5;
  }
  
  .bell-container {
    position: absolute;
    top: -48px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border: 2px solid #333;
    border-radius: 50%;
    width: 96px;
    height: 96px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 6;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease;
  }
  
  .bell-container:hover {
    animation: bell-shake 0.5s ease-in-out infinite;
  }
  
  .bell-icon {
    width: 96px;
    transition: transform 0.2s ease;
  }
  
  @keyframes bell-shake {
    0% {
      transform: translateX(-50%) rotate(0deg);
    }
    25% {
      transform: translateX(-50%) rotate(5deg);
    }
    50% {
      transform: translateX(-50%) rotate(0deg);
    }
    75% {
      transform: translateX(-50%) rotate(-5deg);
    }
    100% {
      transform: translateX(-50%) rotate(0deg);
    }
  }
  
  .feeling-box h2 {
    font-size: 36px;
    font-weight: 700;
    margin-top: 60px;
    margin-bottom: 30px;
    letter-spacing: 1px;
  }
  
  .emotions {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 2rem 0 1.5rem;
  }
  
  .emoji-option {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .emoji-img {
    width: 150px;
    height: 150px;
    object-fit: contain;
    transition: 0.25s ease;
    cursor: pointer;
    border-radius: 50%;
    padding: 8px;
    border: 5px solid transparent;
  }
  
  .emoji-img:hover {
    transform: scale(1.15);
    box-shadow: 0 0 20px rgba(212, 238, 90, 0.6);
  }
  
  .emoji-img.selected {
    border-radius: 50%;
    border: 5px solid rgb(212, 238, 90);
    box-shadow: 0 0 0 8px rgba(212, 238, 90, 0.4);
  }
  
  .emoji-option:last-child .emoji-img {
    width: 160px;
    height: 160px;
    margin-top: -12px;
  }
  
  /* 删除圆点相关样式并不显示圆点 */
  .dot {
    display: none;
  }
  
  .comparison {
    margin-top: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 3rem;
  }
  
  .comparison-header,
  .comparison-row {
    display: grid;
    grid-template-columns: 3fr 2fr 3fr;
    width: 90%;
    max-width: 1200px;
  }
  
  .comparison-header .col {
    font-weight: bold;
    padding: 1.5rem;
    background: #fffbf3;
    border: 2px solid #000;
    font-size: 18px;
    text-align: center;
  }
  
  .comparison-header .col:first-child {
    border-top-left-radius: 16px;
  }
  
  .comparison-header .col:last-child {
    border-top-right-radius: 16px;
  }
  
  .comparison-header .label {
    background: #fffbf3;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: none;
    border-right: none;
  }
  
  .comparison-row .cell {
    padding: 1.5rem;
    font-size: 16px;
    line-height: 1.6;
    text-align: left;
    border-left: 2px solid #000;
    border-right: 2px solid #000;
    border-bottom: 2px solid #000;
  }
  
  .comparison-row:last-child .cell:first-child {
    border-bottom-left-radius: 16px;
  }
  
  .comparison-row:last-child .cell:last-child {
    border-bottom-right-radius: 16px;
  }
  
  .comparison-row .left {
    background: #e1f37e;
  }
  
  .comparison-row .right {
    background: #ff914d;
  }
  
  .comparison-row .label {
    font-weight: bold;
    color: #2c3e50;
    background: #fffbf3;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: none;
    border-right: none;
  }
  
  .seek-help {
    margin-top: 2rem;
    margin-bottom: 3rem;
    font-weight: bold;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }
  
  .popup {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 400px;
    text-align: center;
  }
  
  .popup h2 {
    margin-bottom: 1.5rem;
  }
  
  .popup .buttons {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 20px;
  }
  
  .popup .buttons button {
    margin: 0;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    background-color: #6c63ff;
    color: white;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
  }
  
  .popup .buttons button:hover {
    background-color: #5a52d5;
    transform: translateY(-2px);
  }
  
  .popup .buttons button:first-child {
    background-color: #7963ff;
  }
  
  .popup .buttons button:last-child {
    background-color: #9290a6;
  }
  
  /* 为 InteractiveHoverButton 组件添加样式 */
  .read-more-button {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 2;
    margin-right: 3.5rem;
    --tw-border-opacity: 0.3;
    background-color: transparent !important;
    color: #1E6A42;
  }
  
  .read-more-button :deep(.bg-primary) {
    background-color: #1E6A42 !important;
  }
  
  .read-more-button :deep(.text-primary-foreground) {
    color: white !important;
  }
  
  .read-more-button:hover {
    transform: translateY(-50%) translateX(5px);
  }
  
  /* Responsive button position adjustment */
  @media (max-width: 1280px) {
    .read-more-button {
      margin-right: 2.5rem;
    }
  }
  
  @media (max-width: 1024px) {
    .read-more-button {
      margin-right: 2rem;
    }
  }
  
  @media (max-width: 768px) {
    .read-more-button {
      margin-right: 1.5rem;
    }
  }
  
  @media (max-width: 640px) {
    .read-more-button {
      margin-right: 1rem;
    }
  }
  
  .help-button {
    font-size: 26px;
    font-weight: 700;
    padding: 1.25rem 4rem;
    background-color: #FF6B6B;
    color: white;
    border: 2px solid black;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
    transition: all 0.3s ease;
    min-width: 300px;
    text-align: center;
  }
  
  .help-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
    background-color: #FF5252;
  }
  </style>