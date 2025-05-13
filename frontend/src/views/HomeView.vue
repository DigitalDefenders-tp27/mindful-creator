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
              <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Wide_Red.svg" alt="Wave" class="element hoverable">
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
          <video 
            controls
            autoplay
            muted
            loop
            width="100%"
            height="auto"
          >
            <source src="/media/Homepage_Video.mp4" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
        <div class="features-grid">
          <div class="feature">
            <img src="/src/assets/icons/elements/Eye.svg" alt="Eye icon" class="feature-icon">
            <h3>FOR YOUNG CREATORS</h3>
            <p>Grow confidently and safely in the digital space while avoiding unnecessary risks.</p>
          </div>
          <div class="feature">
            <img src="/src/assets/icons/elements/Jigsaw.svg" alt="Jigsaw icon" class="feature-icon">
            <h3>RICH & PRACTICAL CONTENT</h3>
            <p>Offer valuable insights with practical guides to support long-term success.</p>
          </div>
          <div class="feature">
            <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower icon" class="feature-icon">
            <h3>SAFE & POSITIVE SPACE</h3>
            <p>Learn how to foster a supportive and uplifting community around you.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Journey Section / 旅程部分 -->
    <section class="journey-section">
      <div class="journey-content">
        <h2>Discover your digital citizenship journey</h2>
        <div class="journey-grid">
          <div class="top-row">
            <router-link to="/ethic-influencer" class="journey-link">
              <FlipCard class="journey-card purple">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Leaves_Light_Purple.svg" alt="Leaves Light Purple" class="card-icon">
                  <div class="card-text">
                    <h3>Ethic</h3>
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
            </router-link>

            <router-link to="/creator-wellbeing" class="journey-link">
              <FlipCard class="journey-card beige">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Medication.svg" alt="Medication" class="card-icon">
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
            </router-link>

            <router-link to="/critical-response" class="journey-link">
              <FlipCard class="journey-card orange">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Circle_blue.svg" alt="Circle Blue" class="card-icon">
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
            </router-link>
          </div>

          <div class="bottom-row">
            <router-link to="/privacy" class="journey-link">
              <FlipCard class="journey-card orange-light">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Leaves_Blue.svg" alt="Leaves Blue" class="card-icon">
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
            </router-link>

            <router-link to="/copyright" class="journey-link">
              <FlipCard class="journey-card blue-light">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Leaves_Purple.svg" alt="Leaves Purple" class="card-icon">
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
            </router-link>
            
            <router-link to="/relaxation" class="journey-link">
              <FlipCard class="journey-card pink">
                <div class="card-content">
                  <img src="/src/assets/icons/elements/Flower_Orange.svg" alt="Flower Pink" class="card-icon white-filter">
                  <div class="card-text">
                    <h3>Relaxation</h3>
                    <h3>Zone</h3>
                  </div>
                </div>
                <template #back>
                  <div class="card-content">
                    <ul class="feature-list">
                      <li>Take mindful breaks to reset your creative energy.</li>
                      <li>Learn techniques to manage digital stress and anxiety.</li>
                      <li>Discover activities designed for creators' mental wellbeing.</li>
                    </ul>
                  </div>
                </template>
              </FlipCard>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Testimonials Section / 推荐部分 -->
    <!-- <section class="testimonials-section">
      <div class="section-background">
        <img src="../assets/icons/elements/BG_Gradient_Green.svg" alt="Background" class="bg-gradient">
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
    </section> -->
  </div>
</template>

<script setup>
import { FlipCard } from '@/components/ui/flip-card'

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'instant'
  })
}
</script>

<style scoped>
.home-container {
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  width: 100%;
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
    #e75a97 20%,
    #4d8cd5 40%,
    #4d8cd5 60%,
    #e75a97 80%
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
  padding: 0 0 0.2em;
  transform: translateY(-0.05em);
  overflow: visible;
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(231, 90, 151, 0.5));
  transform: none;
  animation: liquidFlow 2s linear infinite;
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
}

@media (max-width: 1024px) {
  .hero-section {
    min-height: 40vh;
    padding: 6rem 0 1rem;
  }
  
  .hero-content {
    min-height: 40vh;
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
  }
  
  .subtitle {
    @apply text-xl;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: 22vh;
    padding: 7rem 0 0.5rem;
  }
  
  .hero-content {
    min-height: 22vh;
    flex-direction: column;
    align-items: flex-start;
    padding-top: 0.75rem;
  }
  
  .slogan {
    margin-left: 1rem;
    max-width: 90%;
  }
  
  .decorative-elements {
    opacity: 0.1;
    transform: translateX(0) scale(0.8);
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
    min-height: 18vh;
    padding: 7.5rem 0 0.5rem;
    margin-bottom: 1rem;
  }

  .hero-content {
    padding: 0 1rem;
    min-height: 18vh;
    padding-top: 0.25rem;
  }

  .slogan {
    padding-top: 0;
  }

  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.7);
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

@media (max-width: 480px) {
  .hero-section {
    min-height: 16vh;
    padding: 8rem 0 0.5rem;
  }
  
  .hero-content {
    min-height: 16vh;
  }
  
  .decorative-elements {
    opacity: 0;
    display: none;
  }
}

/* About Section */
.about-section {
  position: relative;
  padding: 0 0rem 4rem;
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
  padding: 1rem;
}

.feature-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 0.5rem;
  transition: transform 0.3s ease;
}

.feature:hover .feature-icon {
  transform: none;
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

.button-container {
  display: none;
}

/* 移除不需要的视频容器相关样式 / Remove unnecessary video container styles */
.video-container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto 3rem;
  position: relative;
  padding-bottom: 56.25%; /* 固定的16:9比例 */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

@media (min-width: 800px) {
  .video-container {
    padding-bottom: 450px; /* 固定高度，仅用于大于800px的屏幕 */
  }
}

.video-container video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 12px;
  object-fit: contain; /* 改为contain以保持视频比例 */
}

.play-button {
  display: none;
}

/* 移除不需要的背景图片 / Remove unnecessary background images */
.section-background {
  display: none;
}

/* Journey Section */
.journey-section {
  position: relative;
  padding: 0 0 8rem;
  background-color: rgb(255, 252, 244);
  width: 100%;
  margin-top: 0;
}

.journey-content {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
  padding: 4rem 2rem 0;
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

.bottom-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

/* Card styles - ensuring no green shadows or flashes */
.journey-card {
  @apply rounded-xl;
  min-height: 360px;
  aspect-ratio: 1;
  border-radius: 1rem;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  border: 1px solid rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  transform: scale(1);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  width: 100%;
}

.journey-card:hover {
  transform: scale(1.05);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

/* Reset any green hover color for card headings */
.journey-section .journey-card:hover .card-text h3,
.journey-section .journey-card:hover h3,
.journey-section .journey-link:hover .card-text h3,
.journey-section .journey-link:hover h3,
.journey-section .journey-link:hover .journey-card .card-text h3 {
  color: inherit !important;
  text-shadow: none !important;
}

/* Explicitly override the known green color */
.journey-section *:hover h3[style*="#1E6A42"],
.journey-section *:hover *[style*="#1E6A42"],
.journey-section h3:hover,
.journey-section .card-text h3:hover,
.journey-section .journey-card:hover .card-text h3,
.journey-section .journey-link:hover .journey-card h3 {
  color: inherit !important;
}

/* Specifically target the FlipCard component's text */
.journey-section .journey-card:hover :deep(h3),
.journey-section .journey-card:hover :deep(.card-text h3) {
  color: inherit !important;
}

/* Card links with clean transitions */
.journey-link {
  text-decoration: none;
  color: inherit;
  display: block;
  width: calc((100% - 4rem) / 3);
  transform: translateY(0);
  transition: transform 0.3s ease;
  padding: 5px;
}

.journey-link:hover {
  transform: translateY(-5px);
  filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.1));
}

/* 翻转卡片动画 - updated for cleaner effects */
:deep(.flip-card) {
  transition: transform 0.6s;
  transform-style: preserve-3d;
  border: none;
  box-shadow: none;
  background: transparent;
  height: 100%;
  width: 100%;
}

:deep(.flip-card:hover) {
  transform: rotateY(180deg);
  box-shadow: none;
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
  border: none;
  box-shadow: none;
  outline: none;
}

:deep(.flip-card-inner) {
  border: none;
  box-shadow: none;
  outline: none;
}

/* Update all journey cards to use consistent background-color property */
.journey-card.beige { 
  background-color: rgb(239, 225, 185);
  border-color: rgba(239, 225, 185, 0.8);
}
.journey-card.beige .card-icon {
  opacity: 1;
}
.journey-card.beige h3 {
  color: rgb(85, 85, 85);
}
.journey-card.beige :deep(.flip-card-back) {
  background-color: rgb(239, 225, 185);
}
.journey-card.beige :deep(.feature-list) {
  color: rgb(85, 85, 85);
  font-weight: 700;
}

.journey-card.purple { 
  background-color: rgb(199, 170, 204);
  border-color: rgba(199, 170, 204, 0.8);
}
.journey-card.purple .card-icon {
  opacity: 1;
}
.journey-card.purple .card-text h3,
.journey-card.purple:hover .card-text h3,
.journey-card.purple .card-text h3:hover,
.journey-card.purple:hover h3,
.journey-card.purple h3:hover,
:deep(.journey-card.purple .flip-card-front .card-text h3),
:deep(.journey-card.purple .flip-card-back .card-text h3),
:deep(.journey-card.purple:hover .flip-card-front .card-text h3),
:deep(.journey-card.purple:hover .flip-card-back .card-text h3) {
  color: rgb(255, 255, 255) !important;
}
.journey-card.purple :deep(.flip-card-back) {
  background-color: rgb(199, 170, 204);
}
.journey-card.purple :deep(.feature-list) {
  color: rgb(252, 244, 223);
  font-weight: 700;
}

.journey-card.orange { 
  background-color: rgb(227, 107, 46);
  border-color: rgba(227, 107, 46, 0.8);
}
.journey-card.orange .card-icon {
  opacity: 1;
}
.journey-card.orange h3 {
  color: rgb(255, 255, 255);
}
.journey-card.orange :deep(.flip-card-back) {
  background-color: rgb(227, 107, 46);
}
.journey-card.orange :deep(.feature-list) {
  color: rgb(255, 255, 255);
  font-weight: 700;
}

.journey-card.orange-light { 
  background-color: rgb(227, 107, 46);
  border-color: rgba(227, 107, 46, 0.8);
}
.journey-card.orange-light .card-icon {
  opacity: 1;
}
.journey-card.orange-light h3 {
  color: rgb(255, 255, 255);
}
.journey-card.orange-light :deep(.flip-card-back) {
  background-color: rgb(227, 107, 46);
}
.journey-card.orange-light :deep(.feature-list) {
  color: rgb(255, 255, 255);
  font-weight: 700;
}

.journey-card.blue-light { 
  background-color: rgb(217, 231, 246);
  border-color: rgba(217, 231, 246, 0.8);
}
.journey-card.blue-light .card-icon {
  opacity: 1;
}
.journey-card.blue-light h3 {
  color: rgb(171, 146, 191);
}
.journey-card.blue-light :deep(.flip-card-back) {
  background-color: rgb(217, 231, 246);
}
.journey-card.blue-light :deep(.feature-list) {
  color: rgb(171, 146, 191);
  font-weight: 700;
}

.journey-card.pink { 
  background-color: rgb(232, 162, 184);
  border-color: rgba(232, 162, 184, 0.8);
}
.journey-card.pink .card-icon {
  opacity: 1;
}
.journey-card.pink h3 {
  color: rgb(255, 255, 255);
}
.journey-card.pink :deep(.flip-card-back) {
  background-color: rgb(232, 162, 184);
}
.journey-card.pink :deep(.feature-list) {
  color: rgb(255, 255, 255);
  font-weight: 700;
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
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
}

.feature-list {
  @apply text-left space-y-4;
  color: inherit;
  padding: 0;
  font-size: 1.2rem;
  width: 100%;
  font-weight: 700;
}

.feature-list li {
  position: relative;
  padding-left: 1rem;
  line-height: 1.5;
  width: 100%;
  padding-right: 0.1rem;
  font-weight: 700;
}

.feature-list li::before {
  content: "•";
  color: inherit;
  position: absolute;
  left: 0;
  font-weight: 600;
}

/* Responsive card flip design - adjust card back text size */
@media (max-width: 1200px) {
  .feature-list {
    font-size: 1.1rem;
    padding: 0 0.5rem;
  }
  
  .feature-list li {
    line-height: 1.4;
    margin-bottom: 0.5rem;
  }
}

/* 添加950px到850px之间的媒体查询 */
@media (max-width: 950px) {
  .journey-card {
    min-height: 340px;
  }
  
  .card-icon {
    width: 100px;
    height: 100px;
    margin-bottom: 1.5rem;
  }
  
  .card-text h3 {
    font-size: 1.6rem;
  }
  
  .feature-list {
    font-size: 0.95rem;
    padding: 0 0.5rem;
  }
  
  .feature-list li {
    line-height: 1.3;
    margin-bottom: 0.5rem;
    padding-right: 0.3rem;
  }
}

/* 专门针对850px的媒体查询 */
@media (max-width: 850px) {
  .journey-card {
    min-height: 300px;
  }
  
  .card-content {
    padding: 0.3rem;
  }
  
  .card-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 1rem;
  }
  
  .card-text h3 {
    font-size: 1.4rem;
    line-height: 1.1;
  }
  
  .feature-list {
    font-size: 0.85rem;
    padding: 0 0.25rem;
    line-height: 1.2;
    margin-top: 0.5rem;
  }
  
  .feature-list li {
    line-height: 1.2;
    margin-bottom: 0.35rem;
    padding-left: 0.7rem;
    padding-right: 0.2rem;
  }
  
  .journey-link {
    padding: 3px;
  }
  
  /* 调整翻转卡片布局 */
  :deep(.flip-card-back) {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  :deep(.flip-card-back .card-content) {
    padding: 0.4rem 0.3rem;
  }
}

/* Add media query for 768px */
@media (max-width: 768px) {
  .journey-card {
    min-height: 290px;
  }
  
  .feature-list {
    font-size: 0.82rem;
    padding: 0 0.2rem;
    margin-top: 0.3rem;
  }
  
  .feature-list li {
    line-height: 1.15;
    padding-left: 0.65rem;
    margin-bottom: 0.3rem;
  }
  
  .card-content {
    padding: 0.4rem 0.2rem;
  }
  
  .card-icon {
    width: 75px;
    height: 75px;
    margin-bottom: 1rem;
  }
  
  .card-text h3 {
    font-size: 1.25rem;
    line-height: 1.05;
  }
  
  .journey-link {
    width: calc((100% - 2rem) / 3);
  }
  
  .top-row, .bottom-row {
    gap: 1rem;
  }
}

/* Add media query for 640px */
@media (max-width: 640px) {
  .journey-card {
    min-height: 270px;
  }
  
  .feature-list {
    font-size: 0.75rem;
    padding: 0 0.15rem;
    margin-top: 0.2rem;
  }
  
  .feature-list li {
    line-height: 1.1;
    padding-left: 0.6rem;
    margin-bottom: 0.25rem;
  }
  
  .card-content {
    padding: 0.3rem 0.15rem;
  }
  
  .card-icon {
    width: 65px;
    height: 65px;
    margin-bottom: 0.75rem;
  }
  
  .card-text h3 {
    font-size: 1.15rem;
    line-height: 1;
  }
  
  .journey-link {
    width: calc((100% - 1rem) / 3);
  }
  
  .top-row, .bottom-row {
    gap: 0.5rem;
  }
}

/* 添加480px的媒体查询，针对特别小的屏幕 */
@media (max-width: 480px) {
  .journey-card {
    min-height: 250px;
  }
  
  .feature-list {
    font-size: 0.7rem;
    padding: 0 0.1rem;
  }
  
  .feature-list li {
    line-height: 1.05;
    padding-left: 0.55rem;
    margin-bottom: 0.2rem;
  }
  
  .card-content {
    padding: 0.25rem 0.1rem;
  }
  
  .card-icon {
    width: 55px;
    height: 55px;
    margin-bottom: 0.6rem;
  }
  
  .card-text h3 {
    font-size: 1rem;
  }
  
  .journey-link {
    padding: 2px;
  }
  
  .top-row, .bottom-row {
    gap: 0.4rem;
  }
}

/* Testimonials Section */
.testimonials-section {
  position: relative;
  padding: 0 2rem 6rem;
  text-align: center;
  background-color: rgb(254, 251, 244);
  margin-top: -4rem;
  width: 100%;
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

/* Wave effect responsive */
@media (max-width: 1024px) {
  .wave-bottom {
    display: none;
  }
}

@media (max-width: 768px) {
  .wave-bottom {
    display: none;
  }
}

@media (max-width: 640px) {
  .wave-bottom {
    display: none;
  }
}

.button-section {
  width: 100%;
  text-align: center;
  background-color: rgb(255, 252, 244);
  padding: 0 2rem 4rem;
  margin-top: -2rem;
  position: relative;
  z-index: 5;
}

.explore-link {
  text-decoration: none;
  display: inline-block;
  background: none;
}

.explore-button {
  display: block;
  margin: 0 auto;
  padding: 1rem 3rem;
  background: #FF69B4;
  color: white;
  border: none;
  border-radius: 100px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.explore-button:hover {
  transform: translateY(-2px);
}

/* Remove the width calculation from .top-row .journey-card and .bottom-row .journey-card */
.top-row .journey-card,
.bottom-row .journey-card {
  width: 100%;
}

/* 确保journey卡片文字颜色无论鼠标位置如何都保持一致 */

/* 紫色卡片文字固定为浅色 */
.journey-card.purple .card-text h3,
.journey-card.purple:hover .card-text h3,
.journey-card.purple .card-text h3:hover,
.journey-card.purple:hover h3,
.journey-card.purple h3:hover,
:deep(.journey-card.purple .flip-card-front .card-text h3),
:deep(.journey-card.purple .flip-card-back .card-text h3),
:deep(.journey-card.purple:hover .flip-card-front .card-text h3),
:deep(.journey-card.purple:hover .flip-card-back .card-text h3) {
  color: rgb(255, 255, 255) !important;
}

/* 橙色卡片文字固定为白色 */
.journey-card.orange h3,
.journey-card.orange:hover h3,
.journey-card.orange h3:hover,
:deep(.journey-card.orange .flip-card-front h3),
:deep(.journey-card.orange .flip-card-back h3),
:deep(.journey-card.orange:hover .flip-card-front h3),
:deep(.journey-card.orange:hover .flip-card-back h3) {
  color: rgb(255, 255, 255) !important;
}

/* 浅橙色卡片文字固定为白色 */
.journey-card.orange-light h3,
.journey-card.orange-light:hover h3,
.journey-card.orange-light h3:hover,
:deep(.journey-card.orange-light .flip-card-front h3),
:deep(.journey-card.orange-light .flip-card-back h3),
:deep(.journey-card.orange-light:hover .flip-card-front h3),
:deep(.journey-card.orange-light:hover .flip-card-back h3) {
  color: rgb(255, 255, 255) !important;
}

/* 淡蓝色卡片文字固定为紫色 */
.journey-card.blue-light h3,
.journey-card.blue-light:hover h3,
.journey-card.blue-light h3:hover,
:deep(.journey-card.blue-light .flip-card-front h3),
:deep(.journey-card.blue-light .flip-card-back h3),
:deep(.journey-card.blue-light:hover .flip-card-front h3),
:deep(.journey-card.blue-light:hover .flip-card-back h3) {
  color: rgb(171, 146, 191) !important;
}

/* 米色卡片文字固定为深灰色 */
.journey-card.beige h3,
.journey-card.beige:hover h3,
.journey-card.beige h3:hover,
:deep(.journey-card.beige .flip-card-front h3),
:deep(.journey-card.beige .flip-card-back h3),
:deep(.journey-card.beige:hover .flip-card-front h3),
:deep(.journey-card.beige:hover .flip-card-back h3) {
  color: rgb(85, 85, 85) !important;
}

/* Pink card text overrides */
.journey-section .journey-card.pink h3[style],
.journey-section .journey-card.pink .card-text h3[style],
.journey-section .journey-card.pink:hover h3[style],
.journey-section .journey-card.pink:hover .card-text h3[style],
.journey-section .journey-card.pink :deep(.flip-card-front) h3[style],
.journey-section .journey-card.pink :deep(.flip-card-back) h3[style] {
  color: rgb(255, 255, 255) !important;
}

/* Pink card deep selector overrides */
.journey-section .journey-card.pink h3,
.journey-section .journey-card.pink .card-text h3,
.journey-section .journey-card.pink:hover h3,
.journey-section .journey-card.pink:hover .card-text h3,
.journey-section .journey-card.pink:active h3,
.journey-section .journey-card.pink:active .card-text h3,
.journey-section .journey-link:hover .journey-card.pink h3,
.journey-section .journey-link:hover .journey-card.pink .card-text h3,
.journey-section .journey-card.pink :deep(.flip-card-front) h3,
.journey-section .journey-card.pink :deep(.flip-card-back) h3,
.journey-section .journey-card.pink:hover :deep(.flip-card-front) h3,
.journey-section .journey-card.pink:hover :deep(.flip-card-back) h3 {
  color: rgb(255, 255, 255) !important;
}

/* White filter for SVG images */
.white-filter {
  filter: brightness(0) invert(1);
}
</style>

