<template>
  <div class="ethic-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Ethical Influencer</h1>
            <h2>Building Trust Through Authenticity</h2>
          </div>
          <p class="subtitle">Learn to create content that makes a positive impact</p>
        </div>
        <div class="decorative-elements">
          <!-- 右上角第一排 -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Wide_Red.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第一排 -->
          <div class="bottom-row-1">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Z_Red.svg" alt="Z" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第二排 -->
          <div class="bottom-row-2">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Z_Pink.svg" alt="Z" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Switch_Red.svg" alt="Switch" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/7_Bold_Pink.svg" alt="7" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_red.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Green.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content Sections -->
    <section class="content-section">
      <div class="gradient-overlay"></div>
      <div class="content-grid">
        <div class="content-row">
          <CardSpotlight 
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <img src="/src/components/icons/elements/Eye.svg" alt="Impact" class="card-icon">
              <div class="card-text">
                <h3>Understanding Your Impact</h3>
                <p>Learn how your content affects your audience and shapes online discourse.</p>
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
              <div class="read-more">Click to read more...</div>
            </div>
          </CardSpotlight>
        </div>

        <div class="content-row">
          <CardSpotlight 
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <img src="/src/components/icons/elements/Jigsaw.svg" alt="Relationships" class="card-icon">
              <div class="card-text">
                <h3>Building Authentic Relationships</h3>
                <p>Develop genuine connections with your audience through transparent communication.</p>
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
              <div class="read-more">Click to read more...</div>
            </div>
          </CardSpotlight>
        </div>

        <div class="content-row">
          <CardSpotlight 
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Ethics" class="card-icon">
              <div class="card-text">
                <h3>Ethical Content Creation</h3>
                <p>Create content that aligns with your values while maintaining integrity.</p>
              </div>
            </div>
          </CardSpotlight>
          
          <CardSpotlight 
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('principles')"
          >
            <div class="preview-content">
              <div v-html="marked(keyPrinciplesPreview)" class="preview-text"></div>
              <div class="read-more">Click to read more...</div>
            </div>
          </CardSpotlight>
        </div>
      </div>
    </section>

    <!-- Expanded card container -->
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

const guideData = ref({
  title: 'Mindful Creator',
  sections: []
})

const practices = ref([])
const contentGuidelinesMarkdown = ref('')
const bestPracticesMarkdown = ref('')
const keyPrinciplesMarkdown = ref('')
const selectedCard = ref(null)
const isCardExpanded = ref(false)

// Helper function to get preview content
const getPreviewContent = (content) => {
  if (!content) return ''
  const lines = content
    .split('\n')
    .filter(line => line.trim() && !line.startsWith('#'))
  return lines.slice(0, 5).join('\n')
}

const previewContent = computed(() => getPreviewContent(contentGuidelinesMarkdown.value))
const bestPracticesPreview = computed(() => getPreviewContent(bestPracticesMarkdown.value))
const keyPrinciplesPreview = computed(() => getPreviewContent(keyPrinciplesMarkdown.value))

const fetchData = async () => {
  try {
    // Guidelines content
    contentGuidelinesMarkdown.value = `# Understanding Your Impact as a Content Creator

Creating digital content is more accessible than ever, but understanding how your content impacts your audience and online communities is essential. As a content creator, your posts, videos, and comments significantly influence your viewers, potentially shaping their thoughts, beliefs, and even actions.

## The Power of Influence

Your content reaches beyond mere entertainment or information; it carries the potential to educate, inspire, or harm. Positive content can foster healthy discussions, support mental well-being, and build inclusive communities. Conversely, harmful or insensitive content can promote misunderstanding, misinformation, and polarization.

## Ethical Responsibility

Every creator holds ethical responsibility for the impact of their work. Before posting, consider:

- **Accuracy**: Is the information verified and trustworthy?
- **Respectfulness**: Does your content respect diversity and avoid perpetuating stereotypes?
- **Constructiveness**: Does it contribute positively to the discussion?

## Engaging Responsibly

Engagement doesn't stop after posting. Active moderation, responding thoughtfully to feedback, and correcting misinformation are critical. Engaging with your audience constructively demonstrates digital citizenship, fostering a respectful community around your content.`

    // Best Practices content
    bestPracticesMarkdown.value = `# Building Authentic Relationships

Authenticity and trust are the foundations of meaningful relationships with your audience. Genuine interactions create deeper bonds, leading to a more engaged and loyal community.

## The Importance of Transparency

Transparency involves openly sharing your intentions, decisions, and processes. It builds credibility and reassures your audience that you genuinely value their trust. Transparent creators admit when they're wrong, clearly communicate their goals, and don't shy away from difficult conversations.

## Practical Strategies for Authenticity

- **Share personal stories and experiences**: Show vulnerability and humanize your interactions.
- **Consistently engage with your audience**: Regularly respond to comments and messages to build trust.
- **Encourage dialogue and feedback**: Promote two-way communication and actively involve your audience in discussions.
- **Handle criticism constructively**: Welcome feedback openly, acknowledge shortcomings, and show a commitment to improvement.

By emphasizing transparency and genuine interactions, you strengthen relationships and foster a supportive and authentic online community.`

    // Key Principles content
    keyPrinciplesMarkdown.value = `# Ethical Content Creation Principles

Ethical content creation means crafting content that reflects your personal and professional values while respecting the rights and perspectives of your audience.

## Understanding Ethical Responsibility

Every content creator faces ethical decisions. Whether you're addressing sensitive social issues, navigating partnerships, or presenting facts, your integrity defines your credibility and influence.

## Key Principles for Ethical Creation

- **Honesty**: Always present accurate and truthful information.
- **Consistency**: Align your content consistently with your core values and beliefs.
- **Accountability**: Acknowledge and correct mistakes openly to maintain trust.
- **Respectfulness**: Create content that respects diversity, promotes inclusivity, and avoids harmful stereotypes.

## Real-World Applications

Ethical creators actively reflect on the consequences of their content. They consider the potential effects their messages may have, especially on vulnerable groups, and they continuously strive to uplift and positively contribute to their communities.

Creating ethical content helps build trust, maintain credibility, and ensures long-term positive impact on your audience and broader online communities.`
  } catch (error) {
    console.error('Error setting content:', error)
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

// Add computed properties for expanded card
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
      return contentGuidelinesMarkdown.value
    case 'practices':
      return bestPracticesMarkdown.value
    case 'principles':
      return keyPrinciplesMarkdown.value
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
  overflow: hidden;
}

.hero-section {
  @apply py-4 relative;
  min-height: 45vh;
  background-color: rgb(255, 252, 244);
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-content {
  @apply container mx-auto px-6;
  position: relative;
  width: 100%;
  min-height: 600px;
}

.slogan {
  @apply space-y-4;
  padding-top: 4rem;
  max-width: 800px;
  position: relative;
  z-index: 2;
}

.title-group {
  @apply space-y-2;
}

.title-group h1 {
  @apply text-6xl md:text-7xl lg:text-8xl font-bold;
  background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  display: block;
  margin-bottom: 1rem;
}

.title-group h2 {
  @apply text-4xl sm:text-5xl md:text-6xl font-bold text-neutral-800 dark:text-neutral-100;
  line-height: 1.2;
  display: block;
  white-space: nowrap;
}

.subtitle {
  @apply text-xl sm:text-2xl md:text-3xl text-neutral-600 dark:text-neutral-400;
  line-height: 1.4;
  margin-top: 1.5rem;
  white-space: nowrap;
}

.decorative-elements {
  position: absolute;
  top: 0;
  right: 0;
  width: 960px;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(6, 160px);
  grid-template-rows: auto 160px auto auto;
  gap: 0;
  padding: 2rem 0;
  z-index: 1;
  pointer-events: none;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(3, 160px);
  gap: 0;
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
  gap: 0;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 4 / 7;
  grid-row: 3;
  justify-self: end;
}

.bottom-row-2 {
  display: grid;
  grid-template-columns: repeat(6, 160px);
  gap: 0;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 1 / 7;
  grid-row: 4;
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
}

.element {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  margin: 0;
  padding: 0;
  transition: transform 0.3s ease;
}

/* Wave元素的特殊尺寸 */
.element-wrapper:has(img[src*="Wave_Wide_Red"]),
.element-wrapper:has(img[src*="Wave_Green"]) {
  width: 240px;
  height: 120px;
}

/* Z元素的特殊尺寸 */
.element-wrapper:has(img[src*="Z_"]) {
  width: 120px;
  height: 160px;
}

/* 7元素的特殊尺寸 */
.element-wrapper:has(img[src*="7_Bold"]) {
  width: 100px;
  height: 160px;
}

/* Hover效果 */
.top-row .element:hover {
  transform: rotate(-15deg);
}

.bottom-row-1 .element:hover {
  transform: rotate(-10deg);
}

.bottom-row-2 .element:hover {
  transform: rotate(15deg);
}

/* Flower元素的特殊hover效果 */
.element-wrapper:has(img[src*="Flower"]) .element:hover {
  transform: rotate(-25deg);
}

.hoverable {
  transition: transform 0.3s ease;
  transform: rotate(0deg);
}

/* hover效果 - 只应用于非square元素 */
.hoverable:hover {
  transform: rotate(-15deg);
}

.top-row .hoverable:hover {
  transform: rotate(-15deg);
}

.bottom-row-1 .hoverable:hover {
  transform: rotate(-10deg);
}

.bottom-row-2 .hoverable:hover {
  transform: rotate(15deg);
}

/* 响应式调整 */
@media (max-width: 1800px) {
  .decorative-elements {
    width: 840px;
    grid-template-columns: repeat(6, 140px);
    transform: translateX(0);
    opacity: 0.9;
  }
}

@media (max-width: 1536px) {
  .decorative-elements {
    width: 720px;
    grid-template-columns: repeat(6, 120px);
    transform: translateX(5%);
    opacity: 0.8;
  }
}

@media (max-width: 1280px) {
  .decorative-elements {
    width: 600px;
    grid-template-columns: repeat(6, 100px);
    transform: translateX(10%);
    opacity: 0.6;
  }
}

@media (max-width: 1024px) {
  .hero-section {
    min-height: auto;
    padding: 2rem 0;
  }

  .hero-content {
    min-height: auto;
  }

  .slogan {
    padding-top: 2rem;
  }

  .title-group h1 {
    @apply text-4xl sm:text-5xl md:text-6xl;
    white-space: normal;
    margin-bottom: 0.5rem;
  }

  .title-group h2 {
    @apply text-2xl sm:text-3xl md:text-4xl;
    white-space: normal;
  }

  .subtitle {
    @apply text-base sm:text-lg md:text-xl;
    white-space: normal;
    margin-top: 1rem;
  }

  .decorative-elements {
    transform: translateX(20%);
    opacity: 0.3;
  }
}

@media (max-width: 768px) {
  .decorative-elements {
    display: none;
  }

  .hero-content {
    min-height: auto;
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

  h2 {
    font-size: 1.75rem !important;
  }

  h3 {
    font-size: 1rem !important;
  }

  p {
    font-size: 0.875rem !important;
  }
}

.content-section {
  @apply relative;
  position: relative;
  margin-top: 0;
  padding: 1rem 1.5rem;
  position: relative;
  z-index: 1;
}

.content-section::before {
  content: '';
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: linear-gradient(to top,
    rgb(228, 245, 138) 0%,
    rgba(228, 245, 138, 0.3) 30%,
    rgba(228, 245, 138, 0) 70%
  );
  z-index: -1;
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
  margin-bottom: 1.5rem;
  grid-template-columns: minmax(auto, 300px) 1fr;
}

.main-card {
  @apply h-full p-6;
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.long-card {
  @apply h-full p-6;
  min-height: 200px;
  display: flex;
  flex-direction: column;
}

.card-content-wrapper {
  display: flex;
  align-items: flex-start;
  gap: 1.5rem;
  height: 100%;
}

.card-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  margin-top: 0.25rem;
}

.card-text {
  flex-grow: 1;
}

.card-text h3 {
  @apply text-xl font-semibold mb-3 text-neutral-900 dark:text-white;
}

.card-text p {
  @apply text-base text-neutral-600 dark:text-neutral-400;
  line-height: 1.5;
}

.preview-content {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.preview-text {
  flex-grow: 1;
  overflow: hidden;
  position: relative;
}

.read-more {
  @apply mt-4 text-sm text-neutral-500 dark:text-neutral-400 italic;
  margin-top: auto;
  padding: 0.5rem 0 0;
  text-align: right;
  background: none;
}

/* 3D effect styles */
.main-card, .long-card {
  @apply transform-gpu transition-all duration-300;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.main-card:hover, .long-card:hover {
  transform: translateY(-5px) rotateX(5deg);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

/* Dark mode adjustments */
.dark .main-card, .dark .long-card {
  @apply bg-neutral-800;
}

.dark .main-card:hover, .dark .long-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1);
}

.dark .card-text h3 {
  @apply text-white;
}

.dark .card-text p {
  @apply text-neutral-400;
}

/* Expanded Card Styles */
.expanded-card-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
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

/* Markdown content styles */
.expanded-card :deep(.markdown-content) {
  h1 {
    font-size: 2.2rem;
    margin-bottom: 2rem;
    color: #232323;
  }

  h2 {
    font-size: 1.8rem;
    margin: 2rem 0 1.2rem;
    color: #333;
  }

  p {
    margin-bottom: 1.2rem;
    color: #444;
    line-height: 1.8;
    font-size: 1.1rem;
  }

  ul, ol {
    margin: 1.2rem 0 1.2rem 2rem;
  }

  li {
    margin-bottom: 0.8rem;
    color: #444;
    line-height: 1.6;
    font-size: 1.1rem;
  }

  strong {
    color: #232323;
    font-weight: 600;
  }
}

/* Preview Content */
.preview-content {
  display: block;
  color: #444;
  position: relative;
  max-height: 150px;
  overflow: hidden;
  padding: 1.2rem;
  background: transparent;
  border-radius: 12px;
}

.preview-text {
  margin-bottom: 1.5rem;
}

.preview-content :deep(p) {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
  line-height: 1.6;
}

.preview-content :deep(h1) {
  font-size: 1.8rem;
  margin-bottom: 1.2rem;
  font-weight: 600;
}

.preview-content :deep(h2) {
  font-size: 1.4rem;
  margin: 1.2rem 0 0.8rem;
  font-weight: 600;
}

.read-more {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 1.5rem 0 1rem;
  background: linear-gradient(transparent, rgba(255, 255, 255, 0.9) 40%);
  text-align: center;
  color: #007AFF;
  font-weight: 500;
  font-size: 1.1rem;
  cursor: pointer;
}

/* Remove the separate overlay styles since we're using the container */
.card-overlay {
  display: none;
}
</style> 