<template>
    <div class="critical-response-view">
      <!-- Title -->
      <h1 class="title">
        Constructive Criticism vs. Cyberbullying<br />
        – Know the Difference!
      </h1>
  
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
            />
            <div
              class="dot"
              :class="{ active: selectedEmotion === emoji.alt }"
              @click="handleDotClick(emoji.alt)"
            ></div>
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
        <a href="https://www.esafety.gov.au/young-people/tough-situations/cyberbullying" target="_blank">
          [SEEK HELP]
        </a>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
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
  
  const emojis = [
    { src: happy, alt: 'Happy' },
    { src: peace, alt: 'Sad' },
    { src: angry, alt: 'Angry' },
    { src: sad, alt: 'Confused' },
    { src: mda, alt: 'Frustrated' },
  ]
  
  const labels = [
    "What's the goal?",
    'How does it sound?',
    'What do they say?',
    'Where does it happen?',
    'How does it make you feel?',
  ]
  
  const leftCol = [
    'To help you improve. The person wants to share advice or opinions to make your content better.',
    'Respectful, clear, and focused on your content.',
    '"Your video is great, but the sound could be clearer. Maybe try using a different mic?" 🎤',
    'Often in a thoughtful comment, private message, or a discussion space.',
    'Encouraged to improve and learn.',
  ]
  
  const rightCol = [
    'To hurt, embarrass, or bring you down. The person is trying to make you feel bad.',
    'Mean, rude, and often personal.',
    '"Your voice is so annoying, just stop making videos!" ❌',
    'Usually in public comments, DMs, or even shared posts to mock you.',
    'Upset, anxious, or even scared to post again.',
  ]
  </script>
  
  <style scoped>
  .critical-response-view {
    background: #fffdf4;
    padding: 2rem;
    font-family: Avenir, Helvetica, sans-serif;
    text-align: center;
  }
  
  .title {
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 2rem;
  }
  
  .feeling-box {
    border: 2px solid #333;
    padding: 2rem 1rem 1rem;
    border-radius: 16px;
    width: fit-content;
    margin: 0 auto 2rem;
    position: relative;
    background: white;
  }
  
  .bell-container {
    position: absolute;
    top: -38px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border: 2px solid #333;
    border-radius: 50%;
    width: 76px;
    height: 76px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1;
  }
  
  .bell-icon {
    width: 78px;
  }
  
  .feeling-box h2 {
    font-size: 28px;
    font-weight: 680;
    margin-top: 50px;
  }
  
  .emotions {
    display: flex;
    justify-content: center;
    gap: 28px;
    margin-top: 1rem;
  }
  
  .emoji-option {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .emoji-img {
    width: 68px;
    height: 68px;
    object-fit: contain;
    transition: 0.2s ease;
    cursor: pointer;
  }
  
  .emoji-img.selected {
    border-radius: 50%;
    border: 4px solid #7f73ff;
    box-shadow: 0 0 0 6px rgba(127, 115, 255, 0.3);
  }
  
  .dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #999;
    margin-top: 10px;
    cursor: pointer;
  }
  
  .dot.active {
    background: #6c63ff;
  }
  
  .comparison {
    margin-top: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .comparison-header,
  .comparison-row {
    display: grid;
    grid-template-columns: 3fr 2fr 3fr;
    width: 100%;
    max-width: 1000px;
  }
  
  .comparison-header .col {
    font-weight: bold;
    padding: 1rem;
    background: #fffbf3;
    border-bottom: 2px solid #ccc;
    font-size: 16px;
    text-align: center;
  }
  
  .comparison-header .label {
    background: #fffbf3;
  }
  
  .comparison-row .cell {
    padding: 1rem;
    font-size: 14px;
    line-height: 1.6;
    text-align: left;
    border-bottom: 1px dashed #ccc;
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
  }
  
  .seek-help {
    margin-top: 2rem;
    font-weight: bold;
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
  
  .popup .buttons button {
    margin: 0 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    background-color: #6c63ff;
    color: white;
    cursor: pointer;
    font-weight: bold;
  }
  
  .emoji-option:last-child .emoji-img {
    width: 78px;
    height: 78px;
    margin-top: -9px;
  }
  </style>