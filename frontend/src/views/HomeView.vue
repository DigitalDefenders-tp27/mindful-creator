<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Mindful Creator</h1>
            <h2>Empowering Digital</h2>
            <h2>Wellbeing</h2>
          </div>
          <p class="subtitle">Guide to responsible and mindful content creation</p>
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

    <!-- 2. About Section -->
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

    <!-- 3. Journey Section -->
    <section class="journey-section">
      <div class="journey-content">
        <h2>Discover your digital citizenship journey</h2>
        <div class="journey-grid">
          <div class="top-row">
            <div class="journey-card purple">
              <div class="card-content">
                <div class="card-icon">
                  <img src="/src/components/icons/elements/Leaves_Light_Purple.svg" alt="Icon">
                </div>
                <h3>Ethical Influencer</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
            <div class="journey-card beige">
              <div class="card-content">
                <div class="card-icon">
                  <img src="/src/components/icons/elements/Medication.svg" alt="Icon">
                </div>
                <h3>Creator Wellbeing</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
            <div class="journey-card orange">
              <div class="card-content">
                <div class="card-icon">
                  <img src="/src/components/icons/elements/Circle_blue.svg" alt="Icon">
                </div>
                <h3>Critical Response</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
          </div>
          <div class="bottom-row">
            <div class="journey-card orange-light">
              <div class="card-content">
                <div class="card-icon">
                  <img src="/src/components/icons/elements/Leaves_Blue.svg" alt="Icon">
                </div>
                <h3>Privacy</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
            <div class="journey-card blue-light">
              <div class="card-content">
                <div class="card-icon">
                  <img src="/src/components/icons/elements/Leaves_Purple.svg" alt="Icon">
                </div>
                <h3>Copyright</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="wave-bottom">
        <img src="/src/components/icons/elements/Wave_Loooooooong.svg" alt="Wave">
      </div>
    </section>

    <!-- 4. Testimonials Section -->
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
// 移除 Card3d 导入，因为我们将使用自己的 CSS 3D 效果
</script>

<style scoped>
.home-container {
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  overflow: hidden;
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

/* Section Background Styles */
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
}

.feature-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 0.5rem;
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

/* 移除不需要的视频容器相关样式 */
.video-container, .play-button {
  display: none;
}

/* 移除不需要的背景图片 */
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
  max-width: 1000px;
  margin: 0 auto;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

.bottom-row {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.bottom-row .journey-card {
  width: calc((100% - 3rem) / 3);
}

.journey-card {
  aspect-ratio: 1;
  border-radius: 1rem;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.journey-card:hover {
  transform: translateY(-5px);
}

.card-content {
  height: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 2.5rem;
}

.card-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transform: scale(1.2);
}

.journey-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  margin-top: 0.5rem;
}

.card-hover {
  position: absolute;
  top: 1rem;
  right: 1rem;
}

.plus-icon {
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  color: #232323;
}

/* 卡片颜色 */
.journey-card.purple { 
  background: rgb(190, 177, 212);
}
.journey-card.purple h3 {
  color: rgb(252, 244, 223);
}

.journey-card.beige { 
  background: rgb(238, 226, 208);
}
.journey-card.beige h3 {
  color: rgb(126, 184, 121);
}

.journey-card.orange { 
  background: rgb(242, 153, 74);
}
.journey-card.orange h3 {
  color: rgb(255, 255, 255);
}

.journey-card.orange-light { 
  background: rgb(242, 153, 74);
}
.journey-card.orange-light h3 {
  color: rgb(255, 255, 255);
}

.journey-card.blue-light { 
  background: rgb(214, 234, 255);
}
.journey-card.blue-light h3 {
  color: rgb(171, 146, 191);
}

/* 波浪分割线 */
.wave-bottom {
  position: absolute;
  bottom: -50%;
  left: 0;
  width: 100%;
  z-index: 2;
}

.wave-bottom img {
  width: 100%;
  height: auto;
  display: block;
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
  padding: 3rem;
  border-radius: 12px;
}

.slider-controls {
  margin-top: 2rem;
}

.slider-controls button {
  background: none;
  border: none;
  font-size: 2rem;
  color: #232323;
  cursor: pointer;
  padding: 0 1rem;
}

.testimonials-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
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
</style>
