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
          <!-- 右上角第一排 / Top Row Right -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Z_Red.svg" alt="Wave" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Switch_Red.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
          <!-- 右上角第二排 / Top Row 2 Right -->
          <div class="top-row-2">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Red.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第一排 / Bottom Row 1 Right -->
          <div class="bottom-row-1">
            <!-- <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_red.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Narrow_Pink.svg" alt="Z" class="element hoverable">
            </div> -->
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Green.svg" alt="Flower" class="element hoverable">
            </div>
          </div>
          <!-- 右下角第二排 / Bottom Row 2 Right -->
          <div class="bottom-row-2">
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink.svg" alt="Z" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Wave_Wide_Red.svg" alt="Switch" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/7_Bold_Pink.svg" alt="7" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/components/icons/elements/Z_Pink.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content Sections / 内容部分 -->
    <section class="content-section">
      <div class="gradient-overlay"></div>
      <div class="content-grid">
        <!-- 第一行 -->
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
                  <img src="/src/components/icons/elements/Eye.svg" alt="Impact" class="card-icon">
                  <h3>Understanding Your Impact</h3>
                </div>
                <div class="card-description">
                  Learn how your content affects your audience and shapes online discourse.
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
              <div class="read-more">Read More</div>
            </div>
          </CardSpotlight>
        </div>

        <!-- 第二行 -->
        <div class="content-row">
          <CardSpotlight 
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('practices')"
          >
            <div class="preview-content">
              <div v-html="marked(bestPracticesPreview)" class="preview-text"></div>
              <div class="read-more">Read More</div>
            </div>
          </CardSpotlight>

          <CardSpotlight 
            class="main-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
          >
            <div class="card-content-wrapper">
              <div class="card-text">
                <div class="card-title">
                  <img src="/src/components/icons/elements/Jigsaw.svg" alt="Relationships" class="card-icon">
                  <h3>Building Authentic Relationships</h3>
                </div>
                <div class="card-description">
                  Develop genuine connections with your audience through transparent communication.
                </div>
              </div>
            </div>
          </CardSpotlight>
        </div>

        <!-- 第三行 -->
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
                  <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Ethics" class="card-icon">
                  <h3>Ethical Content Creation</h3>
                </div>
                <div class="card-description">
                  Create content that aligns with your values while maintaining integrity.
                </div>
              </div>
            </div>
          </CardSpotlight>

          <!-- 右侧胶囊形卡片 -->
          <CardSpotlight 
            class="long-card"
            :gradientSize="250"
            gradientColor="#f0f0f0"
            :gradientOpacity="0.5"
            @click="expandCard('principles')"
          >
            <div class="preview-content">
              <div v-html="marked(keyPrinciplesPreview)" class="preview-text"></div>
              <div class="read-more">Read More</div>
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
  return lines.slice(0, 7).join('\n')
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

    // 更新预览内容
    const previewContent = `Understanding Your Impact as a Content Creator

Your content has the power to shape thoughts, beliefs, and actions. Learn how to create content that positively influences your audience while maintaining ethical responsibility.

Key aspects:
- The power of influence
- Ethical responsibility
- Engaging responsibly`

    const bestPracticesPreview = `Building Authentic Relationships

Discover how to build genuine connections with your audience through transparent communication and authentic interactions.

Key strategies:
- Importance of transparency
- Personal storytelling
- Constructive engagement
- Handling criticism`

    const keyPrinciplesPreview = `Ethical Content Creation Principles

Learn the essential principles for creating content that aligns with your values while respecting your audience's rights and perspectives.

Core principles:
- Honesty and accuracy
- Consistency in values
- Accountability
- Respect and inclusivity`

    // 设置预览内容
    contentGuidelinesMarkdown.value = previewContent
    bestPracticesMarkdown.value = bestPracticesPreview
    keyPrinciplesMarkdown.value = keyPrinciplesPreview
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
  overflow-x: hidden;
  position: relative;
}

.hero-section {
  @apply py-4 relative;
  min-height: 75vh;
  background-color: rgb(255, 252, 244);
  display: flex;
  align-items: center;
  overflow: hidden;
  position: relative;
  z-index: 1;
}

.hero-content {
  @apply container mx-auto px-6;
  position: relative;
  width: 100%;
  min-height: 75vh;
  display: flex;
  align-items: center;
  padding-left: 2rem;
}

.slogan {
  @apply space-y-4;
  max-width: 800px;
  position: relative;
  z-index: 2;
  margin-left: 2rem;
}

.title-group {
  @apply space-y-2;
}

.title-group h1 {
  @apply text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl font-bold;
  background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  display: block;
  margin-bottom: 1rem;
  white-space: normal;
}

.title-group h2 {
  @apply text-2xl sm:text-3xl md:text-4xl lg:text-5xl xl:text-6xl font-bold text-neutral-800 dark:text-neutral-100;
  line-height: 1.2;
  display: block;
  white-space: normal;
}

.subtitle {
  @apply text-base sm:text-lg md:text-xl lg:text-2xl xl:text-3xl text-neutral-600 dark:text-neutral-400;
  line-height: 1.4;
  margin-top: 1.5rem;
  white-space: normal;
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
  grid-template-columns: repeat(6, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 1 / 7;
  grid-row: 4;
  justify-self: end;
  margin-bottom: 2rem;
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

.top-row-2 .element:hover {
  transform: rotate(15deg) scale(1.1);
}

.bottom-row-1 .element:hover {
  transform: rotate(15deg) scale(1.1);
}

.bottom-row-2 .element:hover {
  transform: rotate(-10deg) scale(1.1);
}

/* 响应式调整 */
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
}

@media (max-width: 1024px) {
  .hero-section {
    min-height: 65vh;
  }
  
  .hero-content {
    min-height: 65vh;
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
}

@media (max-width: 768px) {
  .hero-section {
    min-height: 55vh;
  }
  
  .hero-content {
    min-height: 55vh;
  }
  
  .content-section {
    margin-top: 2rem;
  }
  
  .slogan {
    margin-left: 1rem;
  }
  
  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.8);
    transition: opacity 0.3s ease;
  }
  
  .top-row-2 {
    transform: translateY(0);
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

.content-section {
  @apply relative;
  position: relative;
  margin-top: 4rem;
  padding: 1rem 1.5rem;
  position: relative;
  z-index: 2;
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
}

/* 所有行的默认布局 */
.content-row {
  grid-template-columns: minmax(auto, 300px) 1fr;
}

/* 第二行特殊布局 */
.content-row:nth-child(2) {
  grid-template-columns: 1fr minmax(auto, 300px);
}

.quiz-row {
  @apply mt-6;
  display: flex;
  justify-content: center;
  width: 100%;
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
}

.long-card {
  border-radius: 9999px;
  width: 100%;
  height: 300px;
  justify-content: center;
  align-items: center;
  padding: 1.5rem 2rem;
  transition: all 0.3s ease;
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
}

.preview-text {
  flex-grow: 1;
  overflow: hidden;
  position: relative;
  padding: 1.5rem 6rem 3rem 4rem;
  max-height: 100%;
  mask-image: linear-gradient(to bottom, 
    black 0%,
    black 80%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(to bottom, 
    black 0%,
    black 80%,
    transparent 100%
  );
}

.preview-text :deep(h1) {
  @apply text-2xl font-bold text-neutral-900 dark:text-white;
  margin-bottom: 1rem;
  line-height: 1.2;
}

.preview-text :deep(p) {
  @apply text-base text-neutral-700 dark:text-neutral-300;
  line-height: 1.5;
  margin-bottom: 0.75rem;
}

.preview-text :deep(ul) {
  @apply text-base text-neutral-700 dark:text-neutral-300;
  list-style-type: none;
  padding-left: 1rem;
  margin-top: 0.5rem;
}

.preview-text :deep(li) {
  position: relative;
  padding-left: 1rem;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.preview-text :deep(li)::before {
  content: "•";
  position: absolute;
  left: -0.5rem;
  color: #007AFF;
}

.read-more {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  padding: 0.5rem 1.25rem;
  background-color: #007AFF;
  color: white;
  font-weight: 500;
  font-size: 1rem;
  cursor: pointer;
  z-index: 2;
  border-radius: 9999px;
  transition: all 0.3s ease;
  margin-right: 3.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  height: 100%;
  justify-content: center;
  align-items: center;
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
</style> 