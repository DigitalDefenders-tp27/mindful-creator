<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Mindful Creator</h1>
            <h2>Balancing Influence with Responsibility</h2>
          </div>
          <p class="subtitle">A digital citizenship journey for the young creators</p>
        </div>
        <div class="decorative-elements">
          <!-- 右上角第一排 / Top Row Right -->
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
          <!-- 右下角第一排 / Bottom Row 1 Right -->
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
          <!-- 右下角第二排 / Bottom Row 2 Right -->
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

    <!-- 2. About Section / 关于我们部分 -->
    <section class="about-section">
      <div class="about-content">
        <h2>About Our Website</h2>
        <div class="video-container">
          <div class="play-button">▶</div>
        </div>
        <div class="features-grid">
          <div class="feature">
            <img src="/src/components/icons/elements/Eye.svg" alt="Eye icon" class="feature-icon">
            <h3>FOR YOUNG CREATORS</h3>
            <p>Grow confidently and safely in the digital space while avoiding unnecessary risks.</p>
          </div>
          <div class="feature">
            <img src="/src/components/icons/elements/Jigsaw.svg" alt="Jigsaw icon" class="feature-icon">
            <h3>RICH & PRACTICAL CONTENT</h3>
            <p>Offer valuable insights with practical guides to support long-term success.</p>
          </div>
          <div class="feature">
            <img src="/src/components/icons/elements/Flower_Pink_round.svg" alt="Flower icon" class="feature-icon">
            <h3>SAFE & POSITIVE SPACE</h3>
            <p>Learn how to foster a supportive and uplifting community around you.</p>
          </div>
        </div>
        <button class="explore-button">EXPLORE MORE OF US</button>
      </div>
    </section>

    <!-- 3. Journey Section / 旅程部分 -->
    <section class="journey-section">
      <div class="journey-content">
        <h2>Discover your digital citizenship journey</h2>
        <div class="journey-grid">
          <div class="top-row">
            <FlipCard class="journey-card purple">
              <div class="card-content">
                <img src="/src/components/icons/elements/Leaves_Light_Purple.svg" alt="Leaves Light Purple" class="card-icon">
                <div class="card-text">
                  <h3>Ethical</h3>
                  <h3>Influencer</h3>
                </div>
              </div>
              <template #back>
                <div class="card-content">
                  <ul class="feature-list">
                    <li>Promote truth and accountability in your content.</li>
                    <li>Engage respectfully, encouraging constructive discussions.</li>
                    <li>Influence responsibly, considering the ethical implications of your message.</li>
                  </ul>
                </div>
              </template>
            </FlipCard>

            <FlipCard class="journey-card beige">
              <div class="card-content">
                <img src="/src/components/icons/elements/Medication.svg" alt="Medication" class="card-icon">
                <div class="card-text">
                  <h3>Creator</h3>
                  <h3>Wellbing</h3>
                </div>
              </div>
              <template #back>
                <div class="card-content">
                  <ul class="feature-list">
                    <li>Balance online presence with offline activities.</li>
                    <li>Recognize signs of digital fatigue and burnout.</li>
                    <li>Foster healthy habits, such as setting content creation boundaries and managing screen time.</li>
                  </ul>
                </div>
              </template>
            </FlipCard>

            <FlipCard class="journey-card orange">
              <div class="card-content">
                <img src="/src/components/icons/elements/Circle_blue.svg" alt="Circle Blue" class="card-icon">
                <div class="card-text">
                  <h3>Critical</h3>
                  <h3>Response</h3>
                </div>
              </div>
              <template #back>
                <div class="card-content">
                  <ul class="feature-list">
                    <li>Address feedback professionally and objectively.</li>
                    <li>Manage criticism constructively without compromising integrity.</li>
                    <li>Turn challenging conversations into opportunities for growth and learning.</li>
                  </ul>
                </div>
              </template>
            </FlipCard>
          </div>

          <div class="bottom-row">
            <FlipCard class="journey-card orange-light">
              <div class="card-content">
                <img src="/src/components/icons/elements/Leaves_Blue.svg" alt="Leaves Blue" class="card-icon">
                <div class="card-text">
                  <h3>Privacy</h3>
                </div>
              </div>
              <template #back>
                <div class="card-content">
                  <ul class="feature-list">
                    <li>Understand and manage personal data sharing practices.</li>
                    <li>Utilize privacy settings effectively across platforms.</li>
                    <li>Encourage your audience to value and protect their online privacy.</li>
                  </ul>
                </div>
              </template>
            </FlipCard>

            <FlipCard class="journey-card blue-light">
              <div class="card-content">
                <img src="/src/components/icons/elements/Leaves_Purple.svg" alt="Leaves Purple" class="card-icon">
                <div class="card-text">
                  <h3>Copyright</h3>
                </div>
              </div>
              <template #back>
                <div class="card-content">
                  <ul class="feature-list">
                    <li>Create original content or appropriately credit sources.</li>
                    <li>Learn about fair use guidelines to navigate content sharing responsibly.</li>
                    <li>Protect your own content and respect the intellectual property of others.</li>
                  </ul>
                </div>
              </template>
            </FlipCard>
          </div>
        </div>
      </div>
      <div class="wave-bottom">
        <img src="/src/components/icons/elements/Wave_Loooooooong.svg" alt="Wave">
      </div>
    </section>

    <!-- 4. Testimonials Section / 推荐部分 -->
    <section class="testimonials-section">
      <div class="section-background">
        <img src="../components/icons/elements/BG_Gradient_Green.svg" alt="Background" class="bg-gradient">
      </div>
      <div class="testimonials-content">
        <h2>What people are saying</h2>
        <div class="testimonials-slider">
          <div class="testimonial-card">
            <p class="quote">"I learned how to handle negative comments and no longer let malicious attacks affect my emotions!"</p>
            <p class="author">- Sarah M., Content Creator</p>
          </div>
        </div>
        <div class="slider-controls">
          <button class="prev">←</button>
          <button class="next">→</button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { FlipCard } from '@/components/ui/flip-card'
</script>

<style scoped>
.home-container {
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
  min-height: 45vh;
  display: flex;
  align-items: center;
}

.slogan {
  @apply space-y-4;
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

/* 波浪元素的特殊尺寸 / Special dimensions for Wave elements */
.element-wrapper:has(img[src*="Wave_Wide_Red"]),
.element-wrapper:has(img[src*="Wave_Green"]) {
  width: 240px;
  height: 120px;
}

/* Z元素的特殊尺寸 / Special dimensions for Z elements */
.element-wrapper:has(img[src*="Z_"]) {
  width: 120px;
  height: 160px;
}

/* 7元素的特殊尺寸 / Special dimensions for 7 elements */
.element-wrapper:has(img[src*="7_Bold"]) {
  width: 100px;
  height: 160px;
}

/* Hover效果 / Hover effects */
.top-row .element:hover {
  transform: rotate(-15deg);
}

.bottom-row-1 .element:hover {
  transform: rotate(-10deg);
}

.bottom-row-2 .element:hover {
  transform: rotate(15deg);
}

/* Flower元素的特殊hover效果 / Special hover effects for Flower elements */
.element-wrapper:has(img[src*="Flower"]) .element:hover {
  transform: rotate(-25deg);
}

/* 调整底部行的布局 / Adjust bottom row layout */
.bottom-row-1, .bottom-row-2 {
  margin-left: auto;
  width: auto;
  justify-content: flex-end;
}

/* 部分背景样式 / Section Background Styles */
.section-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

.bg-gradient {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wave-overlay {
  position: absolute;
  bottom: -30%;
  left: 0;
  width: 100%;
  transform: scale(1.2);
}

.wave-overlay.bottom {
  bottom: -50%;
  transform: scale(1.2) rotate(180deg);
}

/* About Section */
.about-section {
  position: relative;
  padding: 0 2rem 4rem;
  color: #232323;
  background-color: rgb(255, 252, 244);
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.about-content h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 3rem;
  color: #232323;
  line-height: 1.2;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
  margin: 2rem auto;
  max-width: 1000px;
}

.feature {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  cursor: pointer;
}

.feature-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 0.5rem;
  transition: transform 0.3s ease;
}

.feature:hover .feature-icon {
  transform: scale(1.2);
}

.feature h3 {
  @apply text-lg font-bold tracking-wider;
  color: #232323;
  margin: 0;
}

.feature p {
  @apply text-base leading-relaxed;
  color: #666;
  max-width: 280px;
  margin: 0 auto;
}

.explore-button {
  display: block;
  margin: 4rem auto 2rem;
  padding: 1rem 3rem;
  background: #FF69B4;
  color: white;
  border: none;
  border-radius: 100px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.explore-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 105, 180, 0.3);
}

/* 移除不需要的视频容器相关样式 / Remove unnecessary video container styles */
.video-container, .play-button {
  display: none;
}

/* 移除不需要的背景图片 / Remove unnecessary background images */
.section-background {
  display: none;
}

/* Journey Section */
.journey-section {
  position: relative;
  padding: 0 2rem 8rem;
  background: linear-gradient(to top,
    rgb(227, 245, 137) 0%,
    rgb(227, 245, 137) 50%,
    rgba(227, 245, 137, 0) 100%
  );
  overflow: hidden;
}

.journey-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  padding-top: 4rem;
}

.journey-content h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 3rem;
  color: #232323;
  line-height: 1.2;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

.journey-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.top-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.top-row .journey-card {
  width: calc((100% - 4rem) / 3);
}

.bottom-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.bottom-row .journey-card {
  width: calc((100% - 4rem) / 3);
}

.journey-card {
  @apply rounded-xl;
  min-height: 360px;
  aspect-ratio: 1;
  border-radius: 1rem;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.journey-card:hover {
  transform: scale(1.02);
}

/* 翻转卡片动画 / Flip card animation */
:deep(.flip-card) {
  transition: transform 0.6s;
  transform-style: preserve-3d;
  border: none;
  box-shadow: none;
}

:deep(.flip-card:hover) {
  transform: rotateY(180deg);
}

:deep(.flip-card-front),
:deep(.flip-card-back) {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  border: none;
  box-shadow: none;
  outline: none;
}

:deep(.flip-card-back) {
  transform: rotateY(180deg);
  background: inherit;
  border: none;
  box-shadow: none;
  outline: none;
}

:deep(.flip-card-inner) {
  border: none;
  box-shadow: none;
  outline: none;
}

/* 卡片颜色 / Card colors */
.journey-card.purple { 
  background: rgb(199, 170, 204);
  border-color: rgba(199, 170, 204, 0.8);
}
.journey-card.purple .card-icon {
  opacity: 1;
}
.journey-card.purple h3 {
  color: rgb(252, 244, 223);
}
.journey-card.purple :deep(.flip-card-back) {
  background: rgb(199, 170, 204);
}
.journey-card.purple :deep(.feature-list) {
  color: rgb(252, 244, 223);
  font-weight: 600;
}

.journey-card.beige { 
  background: rgb(239, 225, 185);
  border-color: rgba(239, 225, 185, 0.8);
}
.journey-card.beige .card-icon {
  opacity: 1;
}
.journey-card.beige h3 {
  color: rgb(126, 184, 121);
}
.journey-card.beige :deep(.flip-card-back) {
  background: rgb(239, 225, 185);
}
.journey-card.beige :deep(.feature-list) {
  color: rgb(126, 184, 121);
  font-weight: 600;
}

.journey-card.orange { 
  background: rgb(227, 107, 46);
  border-color: rgba(227, 107, 46, 0.8);
}
.journey-card.orange .card-icon {
  opacity: 1;
}
.journey-card.orange h3 {
  color: rgb(255, 255, 255);
}
.journey-card.orange :deep(.flip-card-back) {
  background: rgb(227, 107, 46);
}
.journey-card.orange :deep(.feature-list) {
  color: rgb(255, 255, 255);
  font-weight: 600;
}

.journey-card.orange-light { 
  background: rgb(227, 107, 46);
  border-color: rgba(227, 107, 46, 0.8);
}
.journey-card.orange-light .card-icon {
  opacity: 1;
}
.journey-card.orange-light h3 {
  color: rgb(255, 255, 255);
}
.journey-card.orange-light :deep(.flip-card-back) {
  background: rgb(227, 107, 46);
}
.journey-card.orange-light :deep(.feature-list) {
  color: rgb(255, 255, 255);
  font-weight: 600;
}

.journey-card.blue-light { 
  background: rgb(217, 231, 246);
  border-color: rgba(217, 231, 246, 0.8);
}
.journey-card.blue-light .card-icon {
  opacity: 1;
}
.journey-card.blue-light h3 {
  color: rgb(171, 146, 191);
}
.journey-card.blue-light :deep(.flip-card-back) {
  background: rgb(217, 231, 246);
}
.journey-card.blue-light :deep(.feature-list) {
  color: rgb(171, 146, 191);
  font-weight: 600;
}

.card-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0.5rem;
  position: relative;
}

.card-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 2rem;
  opacity: 1;
}

.card-text {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card-text h3 {
  font-size: 1.75rem;
  font-weight: 500;
  line-height: 1.2;
  margin: 0;
}

.feature-list {
  @apply text-left space-y-4;
  color: inherit;
  padding: 0;
  font-size: 1.2rem;
  width: 100%;
  font-weight: 600;
}

.feature-list li {
  position: relative;
  padding-left: 1rem;
  line-height: 1.5;
  width: 100%;
  padding-right: 0.1rem;
}

.feature-list li::before {
  content: "•";
  color: inherit;
  position: absolute;
  left: 0;
  font-weight: 600;
}

/* 响应式调整 / Responsive adjustments */
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
  .decorative-elements {
    transform: translateX(20%);
    opacity: 0.3;
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
    @apply text-lg sm:text-xl md:text-2xl;
    white-space: normal;
    margin-top: 1rem;
    max-width: 100%;
  }

  .journey-card {
    min-height: 320px;
  }

  .card-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 1rem;
  }

  .card-text h3 {
    font-size: 1.3rem;
  }

  .feature-list {
    font-size: 0.85rem;
    space-y: 2;
    width: 100%;
  }

  .feature-list li {
    line-height: 1.4;
    padding-left: 0.75rem;
    padding-right: 0.1rem;
  }
}

@media (max-width: 768px) {
  .decorative-elements {
    display: none;
  }

  .hero-content {
    min-height: auto;
  }

  .journey-grid {
    gap: 1.5rem;
  }

  .top-row,
  .bottom-row {
    gap: 1.5rem;
  }

  .top-row .journey-card,
  .bottom-row .journey-card {
    width: calc((100% - 3rem) / 3);
  }

  .journey-card {
    min-height: 280px;
  }

  .card-icon {
    width: 60px;
    height: 60px;
    margin-bottom: 0.75rem;
  }

  .card-text h3 {
    font-size: 1.1rem;
  }

  .feature-list {
    font-size: 0.75rem;
    space-y: 1.5;
  }

  .feature-list li {
    padding-left: 0.75rem;
    padding-right: 0.1rem;
    line-height: 1.3;
  }

  .subtitle {
    @apply text-base sm:text-lg;
    padding: 0 1rem;
  }
}

@media (max-width: 640px) {
  .about-section {
    padding: 0 1rem 3rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .feature p {
    max-width: 100%;
  }

  .journey-grid {
    gap: 1rem;
  }

  .top-row,
  .bottom-row {
    gap: 1rem;
  }

  .top-row .journey-card,
  .bottom-row .journey-card {
    width: calc((100% - 2rem) / 3);
  }

  .journey-card {
    min-height: 240px;
  }

  .card-icon {
    width: 50px;
    height: 50px;
    margin-bottom: 0.5rem;
  }

  .card-text h3 {
    font-size: 0.9rem;
  }

  .feature-list {
    font-size: 0.65rem;
    space-y: 1;
  }

  .feature-list li {
    padding-left: 0.5rem;
    padding-right: 0.1rem;
    line-height: 1.2;
  }

  .card-content {
    padding: 0.5rem;
  }

  .hero-section {
    padding: 1.5rem 0;
  }

  .hero-content {
    padding: 0 1rem;
  }

  .slogan {
    padding-top: 1rem;
  }

  .subtitle {
    font-size: 1rem;
    line-height: 1.5;
  }
}

/* Testimonials Section */
.testimonials-section {
  position: relative;
  padding: 0 2rem 6rem;
  text-align: center;
  background-color: rgb(254, 251, 244);
  margin-top: -4rem;
}

.testimonial-card {
  max-width: 800px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.9);
  padding: 3rem 6rem;
  border-radius: 12px;
  position: relative;
}

.testimonial-card .quote {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.testimonial-card .author {
  font-style: italic;
  color: #666;
}

.slider-controls {
  position: absolute;
  top: 50%;
  left: -2rem;
  right: -2rem;
  transform: translateY(-50%);
  display: flex;
  justify-content: space-between;
  pointer-events: none;
}

.slider-controls button {
  background: none;
  border: none;
  font-size: 2.5rem;
  color: #232323;
  cursor: pointer;
  padding: 1rem;
  transition: transform 0.3s ease;
  pointer-events: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .testimonial-card {
    padding: 2rem 4rem;
  }

  .slider-controls {
    left: -1rem;
    right: -1rem;
  }

  .slider-controls button {
    font-size: 2rem;
    padding: 0.5rem;
  }

  .testimonial-card .quote {
    font-size: 1.1rem;
  }
}

@media (max-width: 640px) {
  .testimonial-card {
    padding: 1.5rem 3rem;
  }

  .slider-controls {
    left: -0.5rem;
    right: -0.5rem;
  }

  .slider-controls button {
    font-size: 1.8rem;
    padding: 0.25rem;
  }

  .testimonial-card .quote {
    font-size: 1rem;
  }
}

.testimonials-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.testimonials-content h2 {
  text-align: center;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 4rem;
  color: #232323;
  line-height: 1.2;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
}

h3 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #232323;
}

p {
  color: #666;
  line-height: 1.6;
}

/* 波浪效果响应式 / Wave effect responsive */
@media (max-width: 1024px) {
  .wave-bottom {
    bottom: -30%;
  }
}

@media (max-width: 768px) {
  .wave-bottom {
    bottom: -20%;
  }
}

@media (max-width: 640px) {
  .wave-bottom {
    bottom: -15%;
  }
}
</style>

