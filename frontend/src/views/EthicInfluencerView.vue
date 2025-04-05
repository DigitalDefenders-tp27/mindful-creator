<template>
  <div class="ethic-influencer-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1 class="gradient-text">Ethical Influencer</h1>
            <h2>Building Trust and</h2>
            <h2>Authenticity Online</h2>
          </div>
          <p class="subtitle">Guide to responsible content creation and digital influence</p>
        </div>
        <div class="decorative-elements">
          <div class="top-elements">
            <img src="/src/components/icons/elements/Wave_Wide_Red.svg" alt="Decorative" class="element">
            <img src="/src/components/icons/elements/Flower_Pink.svg" alt="Decorative" class="element">
            <img src="/src/components/icons/elements/Flower_Orange.svg" alt="Decorative" class="element">
          </div>
          <div class="middle-elements">
            <img src="/src/components/icons/elements/Wave_Green.svg" alt="Decorative" class="element">
            <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Decorative" class="element">
          </div>
          <div class="bottom-elements">
            <img src="/src/components/icons/elements/Wave_Wide_Red.svg" alt="Decorative" class="element">
            <img src="/src/components/icons/elements/Flower_Pink.svg" alt="Decorative" class="element">
            <img src="/src/components/icons/elements/Wave_Green.svg" alt="Decorative" class="element">
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
.ethic-influencer-container {
  @apply w-full;
  background-color: rgb(255, 252, 244);
}

.hero-section {
  @apply py-4 px-6 md:px-12 relative;
  min-height: 45vh;
  background-color: rgb(255, 252, 244);
  display: flex;
  align-items: center;
}

.hero-content {
  @apply max-w-7xl mx-auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: center;
  width: 100%;
}

.slogan {
  @apply space-y-4;
  padding-top: 0;
}

.title-group {
  @apply space-y-2;
}

.title-group h1 {
  @apply text-6xl md:text-7xl font-bold;
  background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
}

.title-group h2 {
  @apply text-5xl md:text-6xl font-bold text-neutral-800 dark:text-neutral-100;
  line-height: 1.2;
}

.subtitle {
  @apply text-2xl md:text-3xl text-neutral-600 dark:text-neutral-400;
  max-width: 600px;
  line-height: 1.4;
  margin-top: 1.5rem;
}

.decorative-elements {
  @apply relative;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  height: 100%;
  justify-content: space-between;
  padding: 1rem 0 2rem;
}

.top-elements, .middle-elements {
  @apply flex gap-4 justify-end;
  width: 100%;
  margin-bottom: 1rem;
}

.bottom-elements {
  @apply flex gap-4 justify-end;
  width: 90%;
  margin-top: auto;
}

.element {
  @apply object-contain;
  width: 120px;
  height: 120px;
  transition: transform 0.5s ease;
}

/* 第一行元素 */
.top-elements .element:nth-child(1):hover {
  transform: rotate(-8deg);
}

.top-elements .element:nth-child(2):hover {
  transform: rotate(12deg);
}

.top-elements .element:nth-child(3):hover {
  transform: rotate(-15deg);
}

/* 中间行元素 */
.middle-elements .element:nth-child(1):hover {
  transform: rotate(10deg);
}

.middle-elements .element:nth-child(2):hover {
  transform: rotate(-12deg);
}

/* 底部行元素 */
.bottom-elements .element:nth-child(1):hover {
  transform: rotate(-10deg);
}

.bottom-elements .element:nth-child(2):hover {
  transform: rotate(15deg);
}

.bottom-elements .element:nth-child(3):hover {
  transform: rotate(-8deg);
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