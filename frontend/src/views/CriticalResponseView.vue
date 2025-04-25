<template>
    <div class="critical-response-view">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="slogan">
            <div class="title-group">
              <h1>Critical Response</h1>
              <h2>Navigating Feedback with Resilience</h2>
            </div>
            <p class="subtitle">Transform challenging interactions into growth opportunities</p>
          </div>
          <div class="decorative-elements">
            <!-- 右上角第一排 / Top Row Right -->
            <div class="top-row">
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
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

      <!-- Check Your Comment Section -->
      <div class="comment-section-checker">
        <h2 class="section-title">🔍 Check Your Comment Section</h2>
        
        <p class="section-description">
          Not sure if your comment section is a space for healthy
          discussion or if there's negativity creeping in?
        </p>
        
        <div class="cards-container">
          <div class="process-card">
            <div class="card-number">1</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/post.png" alt="Smartphone icon" class="card-icon">
              <p class="card-text">Open your social media platform and find your post.</p>
            </div>
          </div>
          
          <div class="process-card">
            <div class="card-number">2</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/copy.png" alt="Copy icon" class="card-icon">
              <p class="card-text">Copy the comment you want to analyze.</p>
            </div>
          </div>
          
          <div class="process-card">
            <div class="card-number">3</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/paste.png" alt="Link icon" class="card-icon">
              <p class="card-text">Paste it into the box below.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Comments Response Scripts Section -->
      <CommentInput />
    </div>
  </template>

  <script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import InteractiveHoverButton from '@/components/ui/interactive-hover-button.vue'
  import RippleButton from '@/components/ui/ripple-button.vue'
  import HalfDonutChart from '@/components/ui/HalfDonutChart.vue'
  import CommentInput from '@/components/CommentInput.vue'

  import { useAnalysisStore } from '@/stores/analysisStore'
  const analysisStore = useAnalysisStore()
  analysisStore.$reset()

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
    window.open('https://www.betterhealth.vic.gov.au/health/healthyliving/Cyberbullying', '_blank')
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

  // Added from CommentResponseScripts.vue
  const selectedIndex = ref(0)
  const selectedType = computed(() => gaugeData[selectedIndex.value])

  function prevType() {
    selectedIndex.value = (selectedIndex.value - 1 + gaugeData.length) % gaugeData.length
  }

  function nextType() {
    selectedIndex.value = (selectedIndex.value + 1) % gaugeData.length
  }

  const gaugeData = [
    {
      label: 'Accusatory Comments',
      value: 40,
      color: '#FF3B30',
      strategy: [
        {
          title: 'Acknowledge the criticism',
          text: 'Validate their perspective and thank them for the feedback'
        },
        {
          title: 'Provide brief context',
          text: 'Share relevant information without being defensive'
        },
        {
          title: 'Offer a positive path forward',
          text: 'Suggest a constructive next step or solution'
        }
      ],
      q: 'This is such a biased take. You only presented one perspective and completely ignored the other side of the argument. Disappointing content.',
      a: "Thanks 🙏 Fair point on balance – definitely working with time limits but that's on me. Planning a follow-up with more perspectives soon! Any recommendations for sources? Always looking to improve! 💯"
    },
    {
      label: 'Emotional Comments',
      value: 25,
      color: '#FFA726',
      strategy: [
        {
          title: 'Acknowledge their emotions',
          text: 'Recognise the intensity and validate their feelings'
        },
        {
          title: 'Stay calm and neutral',
          text: 'Respond without escalating the emotional tone'
        },
        {
          title: 'Invite further conversation',
          text: 'Show openness to hearing more constructively'
        }
      ],
      q: "Why do you always talk like you know everything? This is so annoying!",
      a: "Appreciate you chiming in! Definitely not my intention to come off that way – I'll keep it more conversational next time 🙏"
    },
    {
      label: 'Misunderstanding Comments',
      value: 15,
      color: '#FF7043',
      strategy: [
        {
          title: 'Clarify gently',
          text: 'Provide accurate info without implying fault'
        },
        {
          title: 'Use simple language',
          text: 'Keep the explanation clear and concise'
        },
        {
          title: 'Offer resources',
          text: 'Suggest links or follow-up posts for context'
        }
      ],
      q: "Wait, are you saying everyone should quit their job and do this instead?",
      a: "Not quite! I meant this approach works *for some* – not one-size-fits-all. Thanks for pointing that out, I'll make it clearer!"
    },
    {
      label: 'Attacking Comments',
      value: 10,
      color: '#66BB6A',
      strategy: [
        {
          title: 'Avoid engaging emotionally',
          text: "Don't match their tone or insults"
        },
        {
          title: 'Set boundaries',
          text: 'Politely assert your intent to keep it respectful'
        },
        {
          title: 'Redirect to the topic',
          text: 'Bring focus back to the content or idea'
        }
      ],
      q: "You're such a clown. This is garbage advice!",
      a: "Let's keep it constructive here. Open to hearing thoughtful counterpoints if you have suggestions!"
    },
    {
      label: 'Constructive Comments',
      value: 10,
      color: '#81C784',
      strategy: [
        {
          title: 'Appreciate the input',
          text: 'Thank them for thoughtful feedback'
        },
        {
          title: 'Engage with the idea',
          text: 'Build upon or reflect on their suggestion'
        },
        {
          title: 'Show willingness to act',
          text: 'Indicate any upcoming improvements or plans'
        }
      ],
      q: "I think this could be stronger if you added more sources.",
      a: "Love that suggestion! I'm adding more citations in the next update – stay tuned and feel free to share any links!"
    }
  ]
  </script>

  <style scoped>
  .critical-response-view {
    background: #fffdf4;
    font-family: Avenir, Helvetica, sans-serif;
    text-align: center;
  }

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
    font-size: 5rem;
    font-weight: bold;
    background: linear-gradient(135deg, #E67F83 0%, #A86ADD 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.4;
    display: block;
    margin-bottom: 0.5rem;
    white-space: nowrap;
    text-align: left;
    overflow: visible;
    padding-right: 1rem;
    padding-bottom: 0.5rem;
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
    white-space: nowrap;
    text-align: left;
    overflow: visible;
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

  .top-row .element:hover {
    transform: rotate(-15deg) scale(1.1);
  }

  section:not(:last-child)::after {
    display: none;
  }

  /* 添加响应式媒体查询 */
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
    
    .title-group h2,
    .subtitle {
      white-space: normal;
    }
  }

  @media (max-width: 1024px) {
    .decorative-elements {
      transform: translateX(0) scale(0.9);
      opacity: 0.5;
      row-gap: 0.5rem;
    }
    
    .title-group h1 {
      white-space: normal;
    }
  }

  @media (max-width: 768px) {
    .decorative-elements {
      opacity: 0.1;
      transform: translateX(0) scale(0.8);
    }
    
    .hero-content {
      flex-direction: column;
      align-items: flex-start;
      padding-top: 0.75rem;
      min-height: 22vh;
    }
    
    .hero-section {
      min-height: 22vh;
      padding: 7rem 0 0.5rem;
    }
    
    .slogan {
      max-width: 90%;
    }
    
    .title-group h1 {
      font-size: 3.5rem;
    }
    
    .title-group h2 {
      font-size: 2rem;
    }
    
    .subtitle {
      font-size: 1.125rem;
    }
  }

  @media (max-width: 640px) {
    .decorative-elements {
      opacity: 0;
      transform: translateX(0) scale(0.7);
    }
    
    .hero-content {
      min-height: 18vh;
      padding-top: 0.25rem;
    }
    
    .hero-section {
      min-height: 18vh;
      padding: 7.5rem 0 0.5rem;
      margin-bottom: 1rem;
    }
    
    .title-group h1 {
      font-size: 2.5rem;
    }
    
    .title-group h2 {
      font-size: 1.5rem;
    }
    
    .subtitle {
      font-size: 1rem;
    }
  }

  @media (max-width: 480px) {
    .decorative-elements {
      opacity: 0;
      display: none;
    }
    
    .hero-content {
      min-height: 16vh;
    }
    
    .hero-section {
      min-height: 16vh;
      padding: 8rem 0 0.5rem;
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

  .comment-section-checker {
    margin-top: 4rem;
    margin-bottom: 4rem;
    padding: 3rem 2rem;
    background: #fffdf4;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
  }

  .section-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: #000;
  }

  .section-description {
    font-size: 1.5rem;
    color: #333;
    line-height: 1.4;
    max-width: 800px;
    margin: 0 auto 2rem auto;
  }

  .cards-container {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 3rem;
    flex-wrap: wrap;
    padding: 0 1rem;
  }

  .process-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 2px solid #000;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    width: 300px;
    height: 300px;
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: #fffdf4;
  }

  .card-number {
    font-size: 5rem;
    font-weight: 700;
    position: absolute;
    top: 15px;
    left: 20px;
    color: #333;
    line-height: 1;
  }

  .card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding-top: 40px;
  }

  .card-icon {
    width: 100px;
    height: 100px;
    object-fit: contain;
    margin-bottom: 2.5rem;
  }

  .card-text {
    font-size: 1.25rem;
    color: #333;
    line-height: 1.4;
    font-weight: 600;
    text-align: center;
  }

  /* Card hover effects */
  .process-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .process-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  }
  
  .process-card:hover .card-icon {
    transform: scale(1.1);
  }
  
  .card-icon {
    transition: transform 0.3s ease;
  }

  /* Comments Response Scripts Section styles */
  .comments-scripts-section {
    margin: 3rem auto 4rem;
    max-width: 1200px;
    padding: 0 2rem;
    background-color: #f8f9fa;
    border-radius: 24px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    padding: 3rem 2rem;
    border: 2px solid #eaeaea;
  }
  
  .comments-scripts-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    color: #000;
    text-align: center;
    position: relative;
    display: inline-block;
  }
  
  .comments-scripts-title:after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: #e4f052;
    border-radius: 2px;
  }
  
  .search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto 2rem;
    border: 2px solid #000;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .search-input {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    font-size: 1.1rem;
    border: none;
    outline: none;
    background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23000000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") 12px center no-repeat;
  }
  
  .search-close-btn {
    background: none;
    border: none;
    font-size: 1.8rem;
    padding: 0 1rem;
    cursor: pointer;
    color: #000;
    transition: color 0.2s;
  }
  
  .search-close-btn:hover {
    color: #ff5252;
  }

  /* Added styles from CommentResponseScripts.vue */
  .highlight-box {
    background-color: #e4f052;
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 6px;
    font-weight: 700;
    margin-bottom: 0.2rem;
    font-size: 1.1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .click-hint {
    font-size: 0.9rem;
    color: #444;
    margin-bottom: 2.5rem;
    font-style: italic;
  }

  .gauge-grid {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 3rem;
    margin-bottom: 2rem;
    padding: 1rem;
  }

  .gauge-item {
    cursor: pointer;
    text-align: center;
    width: 160px;
    transition: all 0.3s ease;
    position: relative;
    padding-bottom: 1rem;
  }

  .gauge-item:hover {
    transform: translateY(-5px);
  }

  .gauge-item.active {
    transform: scale(1.05);
  }

  .gauge-item.active:after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 3px;
    background: #e4f052;
    border-radius: 2px;
  }

  .gauge-item.active .label {
    color: #1e88e5;
    font-weight: 800;
  }

  .gauge-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .percent-text {
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: -8px;
    color: #000;
  }

  .label {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1c1c1c;
    line-height: 1.3;
    transition: color 0.3s;
  }

  .strategy-section {
    margin-top: 4rem;
    background-color: #fff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border: 1px solid #eaeaea;
  }

  .strategy-title {
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 2rem;
    color: #1e293b;
    position: relative;
    display: inline-block;
  }
  
  .strategy-title:after {
    content: "";
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 60px;
    height: 3px;
    background: #e4f052;
    border-radius: 2px;
  }

  .nav-arrows {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .arrow {
    font-size: 2rem;
    cursor: pointer;
    font-weight: bold;
    padding: 0.5rem 1rem;
    user-select: none;
    transition: transform 0.2s, color 0.2s;
    color: #555;
  }
  
  .arrow:hover {
    transform: scale(1.2);
    color: #000;
  }

  .steps-grid {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
    margin: 0 2rem;
  }

  .step-box {
    background-color: #e4f052;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 1.2rem;
    width: 200px;
    font-weight: 600;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    min-height: 220px;
    transition: transform 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
  }
  
  .step-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  }

  .step-box strong {
    font-size: 1.1rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
    text-align: center;
    z-index: 1;
  }

  .step-box p {
    margin-top: 0.5rem;
    font-weight: normal;
    font-size: 0.95rem;
    text-align: center;
    color: #333;
    line-height: 1.4;
    z-index: 1;
  }

  .step-num {
    margin-top: auto;
    padding-top: 0.8rem;
    font-size: 1.2rem;
    font-weight: bold;
    color: #1e293b;
    position: relative;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.6);
    z-index: 1;
  }

  .qa-box {
    border: 2px solid #c4e7c2;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    background-color: #fff;
    max-width: 750px;
    margin: 2.5rem auto 0;
    text-align: left;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    position: relative;
  }

  .qa-box p {
    margin-bottom: 1rem;
    line-height: 1.5;
  }
  
  .qa-box p:last-child {
    margin-bottom: 0;
  }
  
  .qa-box p strong {
    color: #1e88e5;
    font-size: 1.1rem;
  }
  
  /* 添加响应式样式 */
  @media (max-width: 768px) {
    .steps-grid {
      gap: 1.5rem;
      margin: 0 1rem;
    }
    
    .step-box {
      width: 160px;
      min-height: 200px;
      padding: 1.2rem 1rem 1rem;
    }
    
    .gauge-grid {
      gap: 2rem;
    }
    
    .strategy-section {
      padding: 1.5rem;
    }
    
    .qa-box {
      padding: 1.2rem 1.5rem;
    }
  }
  
  @media (max-width: 640px) {
    .comments-scripts-title {
      font-size: 2rem;
    }
    
    .gauge-item {
      width: 130px;
    }
    
    .steps-grid {
      flex-direction: column;
      align-items: center;
    }
    
    .step-box {
      width: 80%;
      max-width: 250px;
    }
    
    .nav-arrows {
      flex-direction: column;
    }
    
    .arrow {
      padding: 0.2rem 0.5rem;
    }
  }
  </style>
