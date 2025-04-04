<template>
  <div class="home-container">
    <section class="hero-section">
      <div class="hero-content">
        <h1>Mindful Creator:</h1>
        <h1>Balancing Influence with</h1>
        <h1>Responsibility</h1>
        <p class="subtitle">A digital citizenship journey for the young creators</p>
      </div>
      <div class="decorative-elements">
        <div class="top-elements">
          <img src="../components/icons/elements/Wave_Wide_Red.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Flower_Pink.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Square_Green.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Flower_Orange.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Wave_Green.svg" alt="Decorative" class="element">
        </div>
        <div class="bottom-elements">
          <img src="../components/icons/elements/Flower_Pink_round.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Square_Orange.svg" alt="Decorative" class="element">
          <img src="../components/icons/elements/Flower_red.svg" alt="Decorative" class="element">
        </div>
      </div>
    </section>

    <!-- 2. About Section -->
    <section class="about-section">
      <div class="section-background">
        <img src="../components/icons/elements/BG_Gradient_Green.svg" alt="Background" class="bg-gradient">
        <img src="../components/icons/elements/Wave_Loooooooong.svg" alt="Wave" class="wave-overlay">
      </div>
      <div class="about-content">
        <h2>About Our Website</h2>
        <div class="video-container">
          <div class="play-button">▶</div>
        </div>
        <div class="features-grid">
          <div class="feature">
            <img src="../components/icons/elements/Eye.svg" alt="Eye icon" class="feature-icon">
            <h3>FOR YOUNG CREATORS</h3>
            <p>Your guide to navigating the digital space while avoiding unnecessary risks.</p>
          </div>
          <div class="feature">
            <img src="../components/icons/elements/Jigsaw.svg" alt="Jigsaw icon" class="feature-icon">
            <h3>RICH & PRACTICAL CONTENT</h3>
            <p>Step-by-step practical guides to support long-term success.</p>
          </div>
          <div class="feature">
            <img src="../components/icons/elements/Flower_Pink_round.svg" alt="Flower icon" class="feature-icon">
            <h3>SAFE & POSITIVE SPACE</h3>
            <p>A supportive and uplifting community awaits you.</p>
          </div>
        </div>
        <button class="explore-button">EXPLORE MORE OF US</button>
      </div>
    </section>

    <!-- 3. Journey Section -->
    <section class="journey-section">
      <div class="section-background">
        <img src="../components/icons/elements/BG_Gradient_Green.svg" alt="Background" class="bg-gradient">
      </div>
      <div class="journey-content">
        <h2>Discover your digital citizenship journey</h2>
        <div class="journey-grid">
          <div class="top-row">
            <div class="journey-card purple">
              <div class="card-content">
                <div class="card-icon">
                  <img src="../components/icons/elements/Leaves_Light_Purple.svg" alt="Icon">
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
                  <img src="../components/icons/elements/Medication.svg" alt="Icon">
                </div>
                <h3>Creator Wellbing</h3>
              </div>
              <div class="card-hover">
                <div class="plus-icon">+</div>
              </div>
            </div>
            <div class="journey-card orange">
              <div class="card-content">
                <div class="card-icon">
                  <img src="../components/icons/elements/Circle_blue.svg" alt="Icon">
                </div>
                <h3>Critical Response</h3>
                <div class="response-steps">
                  <!-- <div class="step">
                    <span class="number">1</span>
                    <span class="text">Criticism Distinction</span>
                    <span class="desc">(constructive criticism or cyberbullying?)</span>
                  </div>
                  <div class="step">
                    <span class="number">2</span>
                    <span class="text">Capture my comment data (Youtube)</span>
                  </div>
                  <div class="step">
                    <span class="number">3</span>
                    <span class="text">How to respond?</span>
                  </div> -->
                </div>
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
                  <img src="../components/icons/elements/Leaves_Blue.svg" alt="Icon">
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
                  <img src="../components/icons/elements/Leaves_Purple.svg" alt="Icon">
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
  position: relative;
  padding: 6rem 2rem;
  margin-bottom: 4rem;
  max-width: 1440px;
  margin: 0 auto;
}

.hero-content {
  max-width: 900px;
  padding-right: 2rem;
}

.hero-content h1 {
  font-size: 4.5rem;
  line-height: 1.15;
  margin: 0;
  font-weight: bold;
  letter-spacing: -0.02em;
}

.subtitle {
  font-size: 2rem;
  color: #007AFF;
  margin-top: 2.5rem;
}

.decorative-elements {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: 400px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2rem 0;
}

.top-elements, .bottom-elements {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  padding: 1rem;
}

.top-elements {
  grid-template-areas: 
    "a b c"
    ". d e";
}

.bottom-elements {
  grid-template-columns: repeat(3, 1fr);
}

.element {
  width: 100%;
  height: auto;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.element:hover {
  transform: rotate(15deg);
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
  padding: 6rem 2rem;
  color: #232323;
}

.video-container {
  width: 100%;
  height: 400px;
  background: #ddd;
  border-radius: 12px;
  margin: 3rem 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.play-button {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  cursor: pointer;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin: 4rem 0;
}

.feature {
  text-align: center;
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1rem;
}

.explore-button {
  display: block;
  margin: 3rem auto;
  padding: 1rem 2rem;
  background: #FF69B4;
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  cursor: pointer;
}

/* Journey Section */
.journey-section {
  position: relative;
  padding: 6rem 2rem;
  background: rgb(219, 237, 178);
}

.journey-content {
  max-width: 1200px;
  margin: 0 auto;
}

.journey-content h2 {
  text-align: center;
  font-size: 3rem;
  margin-bottom: 4rem;
}

.journey-grid {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.top-row, .bottom-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
}

.journey-card {
  width: 300px;
  height: 400px;
  border-radius: 20px;
  overflow: hidden;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}

.journey-card:hover {
  transform: translateY(-5px) rotateX(10deg) rotateY(10deg);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.card-content {
  height: 100%;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: inherit;
  transform-style: preserve-3d;
  transform: translateZ(20px);
}

.card-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 1.5rem;
  transform: translateZ(40px);
}

.card-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.card-hover {
  position: absolute;
  top: 1rem;
  right: 1rem;
  transform: translateZ(30px);
}

.plus-icon {
  width: 30px;
  height: 30px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: #232323;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.journey-card.purple { background: rgb(227, 214, 235); }
.journey-card.beige { background: rgb(238, 226, 208); }
.journey-card.orange { background: rgb(242, 153, 74); }
.journey-card.orange-light { background: rgb(242, 153, 74); }
.journey-card.blue-light { background: rgb(214, 234, 255); }

.response-steps {
  margin-top: 2rem;
}

.step {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  text-align: left;
}

.number {
  width: 24px;
  height: 24px;
  background: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.text {
  font-size: 0.9rem;
  font-weight: 500;
}

.desc {
  font-size: 0.8rem;
  color: rgba(0, 0, 0, 0.6);
}

/* Testimonials Section */
.testimonials-section {
  position: relative;
  padding: 6rem 2rem;
  text-align: center;
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

h2 {
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: #232323;
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
