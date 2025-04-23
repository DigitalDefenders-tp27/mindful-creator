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
          <!-- 右上角第二排 / Top Row 2 Right -->
          <div class="top-row-2">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_red.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第一排 / Bottom Row 1 Right -->
          <div class="bottom-row-1">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Green.svg" alt="Flower" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第二排 / Bottom Row 2 Right -->
          <div class="bottom-row-2">
            <!-- <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Z" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Wide_Red.svg" alt="Switch" class="element hoverable">
            </div> -->
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/7_Bold_Pink.svg" alt="7" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Z_Pink.svg" alt="Wave" class="element hoverable">
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

// 引入 Markdown 文件
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

// Preview Content / 预览内容
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
  background: linear-gradient(135deg, #56D8C9 0%, #FF7676 100%);
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

.top-row-2 {
  display: grid;
  grid-template-columns: repeat(2, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 5 / 7;
  grid-row: 2;
  justify-self: end;
}

.bottom-row-1 {
  display: grid;
  grid-template-columns: repeat(1, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 6 / 7;
  grid-row: 3;
  justify-self: end;
}

.bottom-row-2 {
  display: grid;
  grid-template-columns: repeat(4, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 3 / 7;
  grid-row: 4;
  justify-self: end;
  margin-bottom: 2rem;
  width: fit-content;
  margin-left: auto;
  margin-right: 0;
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

/* Responsive adjustments */
@media (max-width: 1800px) {
  .decorative-elements {
    width: 840px;
    grid-template-columns: repeat(6, 140px);
    opacity: 0.9;
    transform: translateX(-1.5rem);
  }

  .top-row-2 {
    grid-template-columns: repeat(2, 140px);
  }

  .bottom-row-1 {
    grid-template-columns: repeat(1, 140px);
  }
}

@media (max-width: 1536px) {
  .decorative-elements {
    width: 720px;
    grid-template-columns: repeat(6, 120px);
    opacity: 0.8;
    transform: translateX(-1rem);
  }

  .top-row-2 {
    grid-template-columns: repeat(2, 120px);
  }

  .bottom-row-1 {
    grid-template-columns: repeat(1, 120px);
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

  .top-row-2 {
    grid-template-columns: repeat(2, 100px);
  }

  .bottom-row-1 {
    grid-template-columns: repeat(1, 100px);
  }

  .read-more-button {
    margin-right: 2.5rem;
  }

  .content-row:nth-child(2) .long-card .read-more-button {
    right: 0;
    left: auto;
    margin-right: 2.5rem;
  }

  .content-row:nth-child(2) .long-card .preview-content {
    padding: 0;
  }

  .preview-text {
    padding: 1.5rem 10rem 1.5rem 3.5rem;
  }

  .content-row:nth-child(2) .long-card .preview-text {
    padding: 1.5rem 10rem 1.5rem 3.5rem;
  }
}

@media (max-width: 1024px) {
  .content-row {
    margin-bottom: 2.5rem;
  }

  .content-section {
    margin-top: 3rem;
  }

  .slogan {
    margin-left: 1.5rem;
  }

  .decorative-elements {
    transform: translateX(0) scale(0.9);
    opacity: 0.5;
    row-gap: 0.5rem;
  }

  .top-row-2 {
    transform: translateY(-1rem);
  }

  .title-group h1 {
    @apply text-5xl;
  }

  .title-group h2 {
    @apply text-4xl;
  }

  .subtitle {
    @apply text-xl;
  }

  .read-more-button {
    margin-right: 2rem;
  }

  .content-row:nth-child(2) .long-card .read-more-button {
    left: auto;
    right: 0;
    margin-right: 2rem;
  }

  .content-row:nth-child(2) .long-card .preview-content {
    padding: 0;
  }

  .preview-text {
    padding: 1.5rem 8rem 1.5rem 3rem;
  }

  .content-row:nth-child(2) .long-card .preview-text {
    padding: 1.5rem 8rem 1.5rem 3rem;
  }
}

@media (max-width: 768px) {
  .content-row {
    grid-template-columns: 1fr !important;
    gap: 2rem;
  }

  .content-row:nth-child(2) {
    grid-template-columns: 1fr !important;
  }

  .main-card {
    width: 220px;
    height: 220px;
    padding: 1.2rem 1rem;
    margin: 0 auto;
  }

  .card-content-wrapper {
    gap: 0.8rem;
  }

  .long-card {
    height: 180px;
    width: 100%;
    border-radius: 9999px;
    overflow: hidden;
  }

  .card-icon {
    width: 45px;
    height: 45px;
    margin-bottom: 0.5rem;
  }

  .card-title {
    gap: 0.6rem;
  }

  .card-text h3 {
    font-size: 1rem;
    line-height: 1.2;
    margin-bottom: 0.2rem;
  }

  .card-description {
    font-size: 0.85rem;
    line-height: 1.2;
    margin-top: 0.3rem;
  }

  .preview-text {
    padding: 1rem 6rem 1rem 2rem;
  }

  .content-row:nth-child(2) .long-card .preview-text {
    padding: 1rem 6rem 1rem 2rem;
  }

  .read-more-button {
    margin-right: 1.5rem;
    transform: scale(0.9) translateY(-50%);
    position: absolute;
    top: 50%;
    z-index: 5;
  }

  .content-row:nth-child(2) .long-card .read-more-button {
    left: auto;
    right: 0;
    margin-right: 1.5rem;
  }

  .preview-text :deep(h1) {
    font-size: 1.2rem;
    margin-bottom: 0.6rem;
    -webkit-line-clamp: 1;
  }

  .preview-text :deep(p) {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    line-height: 1.3;
    -webkit-line-clamp: 2;
  }

  .preview-text :deep(li) {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
    line-height: 1.3;
  }
}

@media (max-width: 640px) {
  .main-card {
    width: 180px;
    height: 180px;
    padding: 0.8rem 0.5rem;
  }

  .card-content-wrapper {
    gap: 0.5rem;
  }

  .long-card {
    height: 150px;
    border-radius: 9999px;
  }

  .card-icon {
    width: 36px;
    height: 36px;
    margin-bottom: 0.4rem;
  }

  .card-title {
    gap: 0.4rem;
  }

  .card-text h3 {
    font-size: 0.9rem;
    line-height: 1.1;
    margin-bottom: 0.1rem;
  }

  .card-description {
    font-size: 0.8rem;
    line-height: 1.1;
    margin-top: 0.2rem;
  }

  .preview-text {
    padding: 0.8rem 4.5rem 0.8rem 1.5rem;
    -webkit-mask-image: linear-gradient(to bottom,
      black 0%,
      black 85%,
      transparent 100%
    );
    mask-image: linear-gradient(to bottom,
      black 0%,
      black 85%,
      transparent 100%
    );
  }

  .content-row:nth-child(2) .long-card .preview-text {
    padding: 0.8rem 4.5rem 0.8rem 1.5rem;
  }

  .read-more-button {
    margin-right: 1rem;
    transform: scale(0.8) translateY(-50%);
  }

  .content-row:nth-child(2) .long-card .read-more-button {
    left: auto;
    right: 0;
    margin-right: 1rem;
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

  .content-row {
    margin-bottom: 1.5rem;
  }
}

.content-section {
  @apply relative;
  position: relative;
  margin-top: 5rem;
  padding: 1rem 1.5rem;
  position: relative;
  z-index: 2;
}

.content-section::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top,
    rgba(209, 231, 125, 0.4) 0%,
    rgba(218, 237, 148, 0.25) 20%,
    rgba(225, 241, 158, 0.15) 40%,
    rgba(228, 245, 138, 0) 60%
  );
  z-index: -1;
  pointer-events: none;
}

/* Add an additional decorative element to ensure the gradient effect is visible in the card area but does not intrude on the title area */
.ethic-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 55%;
  background: linear-gradient(to top,
    rgba(209, 231, 125, 0.35) 0%,
    rgba(218, 237, 148, 0.2) 15%,
    rgba(225, 241, 158, 0.1) 50%,
    rgba(228, 245, 138, 0) 100%
  );
  z-index: 0;
  pointer-events: none;
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
  @apply grid grid-cols-1 md:grid-cols-2 gap-6;
  margin-bottom: 3rem;
}

/* Default layout for all rows */
.content-row {
  grid-template-columns: minmax(auto, 300px) 1fr;
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
  min-height: 200px;
  display: flex;
  flex-direction: column;
  border: 1px solid rgb(0, 0, 0);
  background-color: rgb(255, 255, 255);
}

.main-card {
  border-radius: 50%;
  aspect-ratio: 1;
  width: 300px;
  height: 300px;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
  overflow: hidden;
}

.long-card {
  border-radius: 9999px;
  width: 100%;
  height: 300px;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 2.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden !important;
  display: flex;
}

.long-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
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
  padding: 1.5rem 12rem 1.5rem 4rem;
  max-height: 100%;
  text-overflow: ellipsis;
  mask-image: linear-gradient(to bottom,
    black 0%,
    black 88%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(to bottom,
    black 0%,
    black 88%,
    transparent 100%
  );
}

/* 统一所有长卡片的文本内边距 */
.content-row .long-card .preview-text {
  padding: 1.5rem 12rem 1.5rem 4rem;
}

.preview-text :deep(h1) {
  @apply text-2xl sm:text-2xl md:text-3xl font-bold text-neutral-900 dark:text-white;
  margin-bottom: 1.2rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
}

.preview-text :deep(p) {
  @apply text-base sm:text-base md:text-lg text-neutral-700 dark:text-neutral-300;
  line-height: 1.5;
  margin-bottom: 0.9rem;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
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
  margin-right: 3rem;
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

/* 统一所有长卡片的按钮位置和悬停效果 */
.content-row .long-card .read-more-button {
  right: 0;
  left: auto;
  margin-right: 3rem;
}

/* Ensure the button has enough space to display when hovered */
.long-card {
  position: relative;
  overflow: visible !important;
}

/* 统一按钮悬停效果 */
.content-row .long-card .read-more-button:hover {
  transform: translateY(-50%) translateX(5px);
}

@media (max-width: 1280px) {
  .preview-text {
    padding: 1.5rem 10rem 1.5rem 3.5rem;
  }
  
  .content-row .long-card .preview-text {
    padding: 1.5rem 10rem 1.5rem 3.5rem;
  }
  
  .content-row .long-card .preview-content {
    padding: 0;
  }
  
  .read-more-button {
    margin-right: 2.5rem;
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 2.5rem;
  }
}

@media (max-width: 1024px) {
  .preview-text {
    padding: 1.5rem 8rem 1.5rem 3rem;
  }
  
  .content-row .long-card .preview-text {
    padding: 1.5rem 8rem 1.5rem 3rem;
  }
  
  .content-row .long-card .preview-content {
    padding: 0;
  }
  
  .read-more-button {
    margin-right: 2rem;
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 2rem;
  }
}

@media (max-width: 768px) {
  .preview-text {
    padding: 1rem 6rem 1rem 2rem;
  }
  
  .content-row .long-card .preview-text {
    padding: 1rem 6rem 1rem 2rem;
  }
  
  .read-more-button {
    margin-right: 1.5rem;
    transform: scale(0.9) translateY(-50%);
    position: absolute;
    top: 50%;
    z-index: 5;
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 1.5rem;
  }
}

@media (max-width: 640px) {
  .preview-text {
    padding: 0.8rem 4.5rem 0.8rem 1.5rem;
    -webkit-mask-image: linear-gradient(to bottom,
      black 0%,
      black 85%,
      transparent 100%
    );
    mask-image: linear-gradient(to bottom,
      black 0%,
      black 85%,
      transparent 100%
    );
  }
  
  .content-row .long-card .preview-text {
    padding: 0.8rem 4.5rem 0.8rem 1.5rem;
  }
  
  .read-more-button {
    margin-right: 1rem;
    transform: scale(0.8) translateY(-50%);
  }
  
  .content-row .long-card .read-more-button {
    margin-right: 1rem;
  }
  
  .content-row .long-card .read-more-button:hover {
    transform: translateY(-50%) translateX(5px) scale(0.8);
  }
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  justify-content: center;
  align-items: center;
  overflow: hidden;
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
  gap: 1.5rem;
  min-height: 60px;
}

.card-icon {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-text h3 {
  @apply text-xl font-semibold text-neutral-900 dark:text-white;
  display: flex;
  align-items: center;
  height: 100%;
  margin: 0;
  text-align: center;
  line-height: 1.3;
}

.card-description {
  width: 100%;
  @apply text-base text-neutral-600 dark:text-neutral-400;
  line-height: 1.5;
  text-align: center;
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
  .main-card {
    width: 280px;
    height: 280px;
    padding: 1.8rem;
  }

  .long-card {
    height: 280px;
    border-radius: 9999px;
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
  .main-card {
    width: 250px;
    height: 250px;
    padding: 1.5rem;
  }

  .long-card {
    height: 250px;
    border-radius: 9999px;
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

@media (max-width: 640px) {
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
</style>
