<template>
  <div class="ethic-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Ethic Influencer</h1>
            <h2>Building Trust Through Authenticity</h2>
          </div>
          <p class="subtitle">Learn to create content that makes a positive impact</p>
        </div>
        <div class="decorative-elements">
          <!-- 右上角第一排 / Top Row Right -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Z_Red.svg" alt="Wave" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Switch_Red.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content Sections / 内容部分 -->
    <section class="content-section">
      <div class="gradient-overlay"></div>
      <div class="content-grid">
        <!-- First Row / 第一行  -->
        <div class="content-row">
          <CardSpotlight
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <div class="card-text">
                <div class="card-title">
                  <img src="/src/assets/icons/elements/Eye.svg" alt="Impact" class="card-icon">
                  <h3>Understanding Your Impact</h3>
                </div>
                <div class="card-description">
                  Shape audience perceptions<br>with mindful content
                </div>
              </div>
            </div>
          </CardSpotlight>

          <CardSpotlight
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('guidelines')"
          >
            <div class="preview-content">
              <div v-html="marked(previewContent)" class="preview-text"></div>
              <InteractiveHoverButton text="Read More" class="read-more-button" />
            </div>
          </CardSpotlight>
        </div>

        <!-- Second Row / 第二行 -->
        <div class="content-row">
          <CardSpotlight
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <div class="card-text">
                <div class="card-title">
                  <img src="/src/assets/icons/elements/Jigsaw.svg" alt="Relationships" class="card-icon">
                  <h3>Building Authentic Relationships</h3>
                </div>
                <div class="card-description">
                  Develop genuine connections<br>with transparency
                </div>
              </div>
            </div>
          </CardSpotlight>

          <CardSpotlight
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('practices')"
          >
            <div class="preview-content">
              <div v-html="marked(bestPracticesPreview)" class="preview-text"></div>
              <InteractiveHoverButton text="Read More" class="read-more-button" />
            </div>
          </CardSpotlight>
        </div>

        <!-- Third Row / 第三行 -->
        <div class="content-row">
          <!-- 左侧圆形卡片 -->
          <CardSpotlight
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <div class="card-text">
                <div class="card-title">
                  <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Ethics" class="card-icon">
                  <h3>Ethical Content Creation</h3>
                </div>
                <div class="card-description">
                  Create aligned content<br>with integrity
                </div>
              </div>
            </div>
          </CardSpotlight>

          <!-- Right Capsule Card / 右侧胶囊形卡片 -->
          <CardSpotlight
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('principles')"
          >
            <div class="preview-content">
              <div v-html="marked(keyPrinciplesPreview)" class="preview-text"></div>
              <InteractiveHoverButton text="Read More" class="read-more-button" />
            </div>
          </CardSpotlight>
        </div>

        <!-- Quiz Card / 测验卡片 -->
        <div class="quiz-row">
          <QuizCard />
        </div>
      </div>
    </section>

    <!-- Expanded card container / 展开的卡片容器 -->
    <div v-if="isCardExpanded" class="expanded-card-container" @click.self="closeCard">
      <div class="expanded-card">
        <div class="card-content">
          <h3>{{ getExpandedCardTitle }}</h3>
          <div class="full-content">
            <div
              v-html="marked(getExpandedCardContent)"
              class="markdown-content"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { marked } from 'marked'
import { CardSpotlight } from '../components/ui/card-spotlight'
import QuizCard from '@/components/ui/quiz-card.vue'
import InteractiveHoverButton from '@/components/ui/interactive-hover-button.vue'

// Import Markdown files
import impactMD from '../content/understanding-impact.md?raw'
import relationshipsMD from '../content/authentic-relationships.md?raw'
import principlesMD from '../content/ethical-principles.md?raw'
import impactPreviewMD from '../content/impact-preview.md?raw'
import relationshipsPreviewMD from '../content/relationships-preview.md?raw'
import principlesPreviewMD from '../content/principles-preview.md?raw'

const contentGuidelinesMarkdown = ref('')
const bestPracticesMarkdown = ref('')
const keyPrinciplesMarkdown = ref('')
const selectedCard = ref(null)
const isCardExpanded = ref(false)

// Preview Content
const previewContent = computed(() => contentGuidelinesMarkdown.value)
const bestPracticesPreview = computed(() => bestPracticesMarkdown.value)
const keyPrinciplesPreview = computed(() => keyPrinciplesMarkdown.value)

const fetchData = async () => {
  try {
    // Load full content
    contentGuidelinesMarkdown.value = impactPreviewMD
    bestPracticesMarkdown.value = relationshipsPreviewMD
    keyPrinciplesMarkdown.value = principlesPreviewMD
  } catch (error) {
    console.error('Error loading content:', error)
  }
}

const expandCard = (cardId) => {
  selectedCard.value = cardId
  isCardExpanded.value = true
  document.body.style.overflow = 'hidden'
}

const closeCard = () => {
  isCardExpanded.value = false
  document.body.style.overflow = 'auto'
  setTimeout(() => {
    selectedCard.value = null
  }, 300)
}

// Get the expanded card title and content
const getExpandedCardTitle = computed(() => {
  switch (selectedCard.value) {
    case 'guidelines':
      return 'Content Guidelines'
    case 'practices':
      return 'Best Practices'
    case 'principles':
      return 'Key Principles'
    default:
      return ''
  }
})

const getExpandedCardContent = computed(() => {
  switch (selectedCard.value) {
    case 'guidelines':
      return impactMD
    case 'practices':
      return relationshipsMD
    case 'principles':
      return principlesMD
    default:
      return ''
  }
})

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.ethic-container {
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  overflow-x: hidden;
  position: relative;
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
  font-size: 4rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #ff5f6d 20%,
    #ffc371 40%,
    #ffc371 60%,
    #ff5f6d 80%
  );
  background-size: 200% auto;
  color: transparent;
  -webkit-background-clip: text;
  background-clip: text;
  animation: liquidFlow 4s linear infinite;
  filter: drop-shadow(0 0 1px rgba(0, 0, 0, 0.2));
  transition: all 0.3s ease;
  line-height: 1.3;
  display: inline-block;
  margin-bottom: 1rem;
  white-space: nowrap;
  text-align: left;
  padding: 0 0 0.15em;
  transform: translateY(-0.05em);
  overflow: visible;
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(255, 95, 109, 0.5));
  transform: none;
  animation: liquidFlow 2s linear infinite; /* Speed up animation on hover */
}

@keyframes liquidFlow {
  0% {
    background-position: 0% center;
  }
  100% {
    background-position: 200% center;
  }
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
  white-space: normal;
  text-align: left;
  max-width: 100%;
}

/* Enhanced responsive styles for title section */
@media (max-width: 480px) {
  .hero-section {
    min-height: 25vh;
    padding: 5rem 0 0.5rem;
    margin-bottom: 1rem;
  }
  
  .hero-content {
    min-height: 25vh;
    padding-left: 1rem;
    align-items: flex-start;
  }
  
  .slogan {
    margin-left: 0.5rem;
    max-width: 95%;
  }
  
  .title-group h1 {
    font-size: 2.25rem;
    margin-bottom: 0.5rem;
  }
  
  .title-group h2 {
    font-size: 1.25rem;
    white-space: normal;
  }
  
  .subtitle {
    font-size: 0.9rem;
    margin-top: 0.75rem;
  }
}

@media (min-width: 481px) and (max-width: 640px) {
  .hero-section {
    min-height: 28vh;
    padding: 5.5rem 0 0.75rem;
  }
  
  .hero-content {
    min-height: 28vh;
    padding-left: 1.25rem;
  }
  
  .slogan {
    margin-left: 0.75rem;
    max-width: 90%;
  }
  
  .title-group h1 {
    font-size: 2.75rem;
  }
  
  .title-group h2 {
    font-size: 1.5rem;
    white-space: normal;
  }
  
  .subtitle {
    font-size: 1rem;
    margin-top: 1rem;
  }
}

@media (min-width: 641px) and (max-width: 768px) {
  .hero-section {
    min-height: 30vh;
    padding: 6rem 0 1rem;
  }
  
  .hero-content {
    min-height: 30vh;
    padding-left: 1.5rem;
  }
  
  .slogan {
    margin-left: 1rem;
  }
  
  .title-group h1 {
    font-size: 3.25rem;
  }
  
  .title-group h2 {
    font-size: 1.875rem;
    white-space: normal;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .hero-content {
    padding-left: 1.75rem;
  }
  
  .slogan {
    margin-left: 1.5rem;
  }
  
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

@media (min-width: 1025px) and (max-width: 1280px) {
  .title-group h1 {
    font-size: 4.5rem;
  }
  
  .title-group h2 {
    font-size: 2.75rem;
  }
  
  .subtitle {
    font-size: 1.375rem;
    white-space: nowrap;
  }
}

@media (min-width: 1281px) {
  .title-group h1 {
    font-size: 5.5rem;
  }
  
  .title-group h2 {
    font-size: 3.25rem;
  }
  
  .subtitle {
    font-size: 1.5rem;
    white-space: nowrap;
  }
}

/* Remove duplicate media queries that were previously defined */
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
    white-space: nowrap;
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
    white-space: nowrap;
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
  grid-template-rows: auto;
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

.top-row-2, .bottom-row-1, .bottom-row-2 {
  display: none;
}

.top-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
}

/* Responsive adjustments */
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
  
  .content-row {
    display: flex;
    flex-direction: column;
    grid-template-columns: none;
    align-items: center;
    gap: 2rem;
  }
  
  /* Place circular cards at the top on mobile */
  .main-card {
    width: 100%;
    height: auto;
    min-height: 180px;
    margin: 0 auto 1rem;
    order: 1;
    border-radius: 16px;
  }
  
  /* Adjust capsule cards for better mobile presentation */
  .long-card {
    width: 100%;
    height: auto;
    min-height: 180px;
    border-radius: 16px;
    margin: 0 auto;
    order: 2;
  }
  
  /* Adjust read more button position for tablets */
  .read-more-button {
    transform: scale(0.9) translateY(-50%);
    margin-right: 1.5rem;
  }
}

/* Tablet portrait and smaller mobile devices */
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
  
  .content-row {
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  /* Further reduce circular card size */
  .main-card {
    width: 100%;
    height: auto;
    min-height: 150px;
    border-radius: 16px;
    padding: 1.2rem;
  }
  
  /* Adjust capsule card shape for smaller screens */
  .long-card {
    min-height: 130px;
    max-height: 180px;
    border-radius: 16px;
    padding: 1.2rem;
  }
  
  /* Optimise text padding and gradient mask for mobile */
  .preview-text {
    padding: 0.8rem 4rem 0.8rem 1rem;
  }
  
  .content-row .long-card .preview-text {
    padding: 0.8rem 4rem 0.8rem 1rem;
  }
  
  /* Reduce button size for smaller screens */
  .read-more-button {
    transform: scale(0.8) translateY(-50%);
    margin-right: 1.2rem;
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 1.2rem;
  }
  
  /* Adjust hover effect for button on touch devices */
  .content-row .long-card .read-more-button:hover {
    transform: scale(0.8) translateY(-50%);
  }
}

/* Small mobile devices */
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
  
  .content-row {
    gap: 1.25rem;
    margin-bottom: 1.5rem;
  }
  
  /* Compact circular card for mobile */
  .main-card {
    width: 100%;
    height: auto;
    min-height: 150px;
    border-radius: 16px;
    padding: 1.2rem;
  }
  
  /* More compact capsule card for smaller screens */
  .long-card {
    min-height: 120px;
    max-height: 160px;
    border-radius: 16px;
    padding: 1.2rem;
  }
  
  /* Reduce icon size for better proportions */
  .card-icon {
    width: 50px;
    height: 50px;
  }
  
  /* Optimise typography for smallest screens */
  .card-text h3 {
    font-size: 1rem;
  }
  
  .card-description {
    font-size: 0.85rem;
    line-height: 1.2;
  }
  
  /* Further adjust text padding for smallest screens */
  .preview-text {
    padding: 0.8rem 3.5rem 0.8rem 1.2rem;
  }
  
  .content-row .long-card .preview-text {
    padding: 0.8rem 3.5rem 0.8rem 1.2rem;
  }
  
  /* Adjust read more button position for smallest screens */
  .read-more-button {
    transform: scale(0.75) translateY(-50%);
    margin-right: 0.75rem;
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 0.75rem;
  }
  
  /* Clip text more aggressively to fit smaller container */
  .preview-text :deep(h1) {
    -webkit-line-clamp: 1;
  }
  
  .preview-text :deep(p) {
    -webkit-line-clamp: 1;
  }
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

/* Enhanced hover effect */
.top-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
}

.top-row-2 .element:hover {
  transform: rotate(15deg) scale(1.1);
}

.bottom-row-1 .element:hover {
  transform: rotate(15deg) scale(1.1);
}

.bottom-row-2 .element:hover {
  transform: rotate(-10deg) scale(1.1);
}

.content-section {
  @apply relative;
  position: relative;
  margin-top: 3rem;
  padding: 2rem;
  position: relative;
  z-index: 2;
  background-color: rgba(250, 250, 250, 0.5);
}

.content-section::before {
  display: none;
}

.ethic-container::after {
  display: none;
}

.gradient-overlay {
  display: none;
}

.content-grid {
  @apply max-w-7xl mx-auto;
  position: relative;
  z-index: 2;
  padding-top: 0;
}

.content-row {
  @apply grid gap-6;
  margin-bottom: 3rem;
  grid-template-columns: 300px minmax(300px, 1fr);
}

@media (max-width: 1024px) {
  .content-row {
    grid-template-columns: 250px minmax(250px, 1fr);
    gap: 2rem;
  }
  
  .content-section {
    padding: 1.5rem;
  }
}

@media (max-width: 768px) {
  .content-row {
    display: flex;
    flex-direction: column;
    grid-template-columns: none;
    align-items: center;
    gap: 2rem;
    margin-bottom: 2.5rem;
  }
  
  .content-section {
    padding: 1.25rem;
    margin-top: 2rem;
  }
}

@media (max-width: 640px) {
  .content-row {
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .content-section {
    padding: 1rem;
    margin-top: 1.5rem;
  }
}

.quiz-row {
  @apply mt-8;
  display: flex;
  justify-content: center;
  width: 100%;
  margin-bottom: 4rem;
}

.main-card, .long-card {
  @apply h-full p-6;
  min-height: 280px;
  height: 280px;
  display: flex;
  flex-direction: column;
  border: none;
  background-color: rgb(255, 255, 255);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.main-card {
  border-radius: 16px;
  width: 300px;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
  overflow: hidden;
}

.long-card {
  border-radius: 16px;
  width: 100%;
  justify-content: center;
  align-items: flex-start;
  padding: 1.5rem 2.5rem;
  position: relative;
  overflow: hidden !important;
  display: flex;
  cursor: pointer;
}

.long-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.9);
}

.main-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
}

.main-card:hover .card-text h3 {
  color: #1E6A42;
}

.long-card:hover .preview-text :deep(h1) {
  color: #1E6A42;
}

.preview-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  padding: 0;
  max-height: 100%;
  width: 100%;
  justify-content: center;
}

/* Special styles for the second row left card */
.content-row .long-card .preview-content {
  position: relative;
  padding: 0;
}

.content-row .long-card .preview-text :deep(*) {
  text-align: left !important;
}

.content-row .long-card .preview-text :deep(ul) {
  list-style-type: none;
  padding-left: 0;
  margin: 0.5rem 0;
}

.content-row .long-card .preview-text :deep(li) {
  position: relative;
  padding-left: 0;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #232323;
}

.content-row .long-card .preview-text :deep(li)::before {
  display: none;
}

/* Remove previous styles that might have caused right alignment */
.content-row .long-card .preview-text :deep(h1),
.content-row .long-card .preview-text :deep(p),
.content-row .long-card .preview-text :deep(ul),
.content-row .long-card .preview-text :deep(li) {
  text-align: left !important;
  direction: ltr;
}

.preview-text {
  flex-grow: 1;
  overflow: hidden;
  position: relative;
  padding: 1.5rem 5rem 1.5rem 1.5rem;
  max-height: 100%;
  text-overflow: ellipsis;
  mask-image: linear-gradient(to bottom,
    black 0%,
    black 90%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(to bottom,
    black 0%,
    black 90%,
    transparent 100%
  );
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.content-row .long-card .preview-text {
  padding: 1.5rem 5rem 1.5rem 1.5rem;
}

.preview-text :deep(h1) {
  @apply text-2xl sm:text-2xl md:text-3xl font-bold;
  margin-bottom: 1rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  color: #222;
}

.preview-text :deep(p) {
  @apply text-base sm:text-base md:text-lg;
  line-height: 1.5;
  margin-bottom: 0.8rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #555;
}

.preview-text :deep(ul) {
  @apply text-base sm:text-base md:text-lg text-neutral-700 dark:text-neutral-300;
  list-style-type: none;
  padding-left: 0;
  margin-top: 0.7rem;
  overflow: hidden;
}

.preview-text :deep(li) {
  position: relative;
  padding-left: 0;
  margin-bottom: 0.7rem;
  line-height: 1.5;
  font-weight: bold;
  color: #232323;
  font-size: 1.05rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.preview-text :deep(li)::before {
  display: none;
}

.read-more {
  display: none;
}

.read-more-button {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  margin-right: 1.5rem;
  --tw-border-opacity: 0.3;
  background-color: transparent !important;
  transition: transform 0.3s ease;
}

.read-more-button:hover {
  transform: translateY(-50%) translateX(5px);
}

.read-more-button :deep(.bg-primary) {
  background-color: #e75a97 !important;
}

.read-more-button :deep(.text-primary-foreground) {
  color: white !important;
}

.read-more-button :deep(span) {
  color: #e75a97;
}

.read-more-button:hover :deep(.group-hover\:opacity-100 span) {
  color: white !important;
}

.content-row .long-card .read-more-button {
  right: 0;
  left: auto;
  margin-right: 1.5rem;
}

.preview-text :deep(h1) {
  @apply text-2xl sm:text-2xl md:text-3xl font-bold;
  margin-bottom: 1rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  color: #222;
}

.preview-text :deep(p) {
  @apply text-base sm:text-base md:text-lg;
  line-height: 1.5;
  margin-bottom: 0.8rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  color: #555;
}

@media (max-width: 768px) {
  .read-more-button {
    transform: scale(0.9) translateY(-50%);
    margin-right: 1.5rem;
  }
  
  .read-more-button:hover {
    transform: scale(0.9) translateY(-50%) translateX(5px);
  }
}

@media (max-width: 640px) {
  .read-more-button {
    transform: scale(0.8) translateY(-50%);
    margin-right: 1.2rem;
  }
  
  .read-more-button:hover {
    transform: scale(0.8) translateY(-50%) translateX(5px);
  }
  
  .card-icon {
    width: 50px;
    height: 50px;
  }
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  justify-content: center;
  align-items: center;
  overflow: visible;
}

.card-text {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
  align-items: center;
}

.card-title {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.2rem;
  min-height: 60px;
  padding-top: 5px;
  overflow: visible;
}

.card-icon {
  width: 70px;
  height: 70px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.main-card:hover .card-icon {
  transform: translateY(-3px);
}

.card-text h3 {
  @apply text-xl font-semibold text-neutral-900 dark:text-white;
  display: flex;
  align-items: center;
  height: 100%;
  margin: 0;
  text-align: center;
  line-height: 1.3;
  color: #333;
}

.card-description {
  width: 100%;
  @apply text-base text-neutral-600 dark:text-neutral-400;
  line-height: 1.5;
  text-align: center;
  color: #666;
}

/* Dark mode adjustments */
.dark .card-text h3 {
  @apply text-white;
}

.dark .card-description {
  @apply text-neutral-400;
}

/* Expanded Card Styles / Expanded card styles */
.expanded-card-container {
  position: fixed;
  inset: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.expanded-card {
  position: relative;
  width: 80vw;
  height: 80vh;
  max-width: 1200px;
  background: white;
  box-shadow: 0 20px 40px rgba(0,0,0,0.2);
  border-radius: 20px;
  overflow: hidden;
}

.expanded-card .card-content {
  height: 100%;
  padding: 2rem;
  background: white;
}

.expanded-card h3 {
  font-size: 1.8rem;
  margin-bottom: 2rem;
  color: #232323;
}

.expanded-card .full-content {
  height: calc(100% - 4rem);
  overflow-y: auto;
  padding-right: 1rem;
}

.expanded-card .markdown-content {
  padding: 0 1rem;
}

/* Markdown content styles / Markdown content styles */
.expanded-card :deep(.markdown-content) h1 {
  font-size: 2.2rem;
  margin-bottom: 2rem;
  color: #232323;
}

.expanded-card :deep(.markdown-content) h2 {
  font-size: 1.8rem;
  margin: 2rem 0 1.2rem;
  color: #333;
}

.expanded-card :deep(.markdown-content) p {
  margin-bottom: 1.2rem;
  color: #444;
  line-height: 1.8;
  font-size: 1.1rem;
}

.expanded-card :deep(.markdown-content) ul, 
.expanded-card :deep(.markdown-content) ol {
  margin: 1.2rem 0 1.2rem 2rem;
}

.expanded-card :deep(.markdown-content) li {
  margin-bottom: 0.8rem;
  color: #444;
  line-height: 1.6;
  font-size: 1.1rem;
}

.expanded-card :deep(.markdown-content) strong {
  color: #232323;
  font-weight: 600;
}

/* 响应式调整文字大小 / Responsive text size adjustments */
@media (max-width: 1200px) {
  .preview-text :deep(h1) {
    @apply text-2xl;
  }

  .preview-text :deep(p),
  .preview-text :deep(ul) {
    @apply text-base;
  }

  .preview-text :deep(li) {
    font-size: 1rem;
  }
}

/* Responsive design for circular and capsule cards */
@media (max-width: 1280px) {
  .main-card, .long-card {
    height: 250px;
    min-height: 250px;
  }
  
  .main-card {
    width: 280px;
    padding: 1.8rem;
  }

  .long-card {
    padding: 1.5rem 2rem;
  }
  
  .preview-text, .content-row .long-card .preview-text {
    padding: 1.5rem 4.5rem 1.5rem 1.5rem;
  }
  
  .card-icon {
    width: 70px;
    height: 70px;
  }

  .card-text h3 {
    font-size: 1.15rem;
  }

  .card-description {
    font-size: 0.95rem;
    line-height: 1.4;
  }
}

@media (max-width: 1024px) {
  .main-card, .long-card {
    height: 220px;
    min-height: 220px;
  }
  
  .main-card {
    width: 250px;
    padding: 1.5rem;
  }

  .long-card {
    padding: 1.2rem 1.8rem;
  }
  
  .preview-text, .content-row .long-card .preview-text {
    padding: 1.2rem 4rem 1.2rem 1.2rem;
  }
  
  .card-icon {
    width: 60px;
    height: 60px;
  }

  .card-text h3 {
    font-size: 1.1rem;
  }

  .card-description {
    font-size: 0.9rem;
    line-height: 1.3;
  }
  
  .preview-text :deep(h1) {
    font-size: 1.4rem;
    margin-bottom: 0.8rem;
  }

  .preview-text :deep(p) {
    font-size: 0.95rem;
    margin-bottom: 0.7rem;
    line-height: 1.4;
  }

  .preview-text :deep(li) {
    font-size: 0.95rem;
    margin-bottom: 0.6rem;
    line-height: 1.4;
  }
}

@media (max-width: 768px) {
  .main-card, .long-card {
    width: 100%;
    height: auto;
    min-height: 180px;
    justify-content: center;
  }
  
  .preview-text, .content-row .long-card .preview-text {
    padding: 1rem 4rem 1rem 1.2rem;
    justify-content: center;
  }
  
  .preview-content {
    justify-content: center;
  }
}

@media (max-width: 640px) {
  .main-card, .long-card {
    min-height: 150px;
    padding: 1rem;
    justify-content: center;
  }
  
  .preview-text, .content-row .long-card .preview-text {
    padding: 0.8rem 3.5rem 0.8rem 1rem;
    justify-content: center;
  }
  
  .preview-content {
    justify-content: center;
  }
  
  .preview-text :deep(h1) {
    font-size: 1rem;
    margin-bottom: 0.4rem;
    -webkit-line-clamp: 1;
  }

  .preview-text :deep(p) {
    font-size: 0.8rem;
    margin-bottom: 0.4rem;
    line-height: 1.2;
    -webkit-line-clamp: 1;
  }

  .preview-text :deep(li) {
    font-size: 0.8rem;
    margin-bottom: 0.4rem;
    line-height: 1.2;
  }
}

@media (max-width: 480px) {
  .main-card, .long-card {
    min-height: 130px;
  }
  
  .content-row .long-card .preview-text {
    padding: 0.8rem 3.5rem 0.8rem 0.8rem;
  }
}

section:not(:last-child)::after {
  display: none;
}

@media (min-width: 769px) and (max-width: 1280px) {
  .long-card {
    border-radius: 16px !important;
    height: 280px;
  }
  
  .main-card {
    border-radius: 16px !important;
  }
}

@media (max-width: 768px) {
  .main-card, .long-card {
    border-radius: 16px;
  }
}

@media (max-width: 640px) {
  .main-card, .long-card {
    border-radius: 16px;
    min-height: 150px;
  }
}

@media (max-width: 480px) {
  .main-card, .long-card {
    border-radius: 16px;
    min-height: 130px;
  }
  
  .content-row .long-card .preview-text {
    padding: 0.8rem 4rem 0.8rem 1rem;
  }
}

.read-more-button:hover :deep(.group-hover\:opacity-100 span) {
  color: white !important;
}

.long-card:hover .read-more-button :deep(span) {
  color: white !important;
}

.long-card:hover .read-more-button :deep(.group-hover\:opacity-100 span) {
  color: white !important;
}
</style>

