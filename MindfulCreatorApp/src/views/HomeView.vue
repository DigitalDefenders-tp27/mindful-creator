<template>
  <div class="home-container">
    <!-- 1. Slogan Section -->
    <section class="slogan-section">
      <div class="slogan-content">
        <h1>Mindful Creator</h1>
        <h2>Balancing Influence with Responsibility</h2>
        <p class="slogan-description">
          Empowering digital creators to make a positive impact while maintaining ethical standards
        </p>
      </div>
      <img class="slogan-svg" src="../components/icons/Elements/Flower_Orange.svg" alt="Decorative Shape" />
    </section>

    <!-- 2. About Section -->
    <section class="about-section">
      <div class="about-content">
        <h2>About Mindful Creator</h2>
        <div class="about-grid">
          <div class="about-card">
            <h3>Our Mission</h3>
            <p>To foster responsible digital citizenship and ethical content creation in the digital age.</p>
          </div>
          <div class="about-card">
            <h3>Our Vision</h3>
            <p>Creating a community where digital influence is used for positive social impact.</p>
          </div>
          <div class="about-card">
            <h3>Our Values</h3>
            <p>Integrity, Responsibility, and Positive Influence in the digital space.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Journey Section -->
    <section class="journey-section">
      <div class="journey-content">
        <h2>Discover Your Digital Citizenship Journey</h2>
        <div class="journey-steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Learn</h3>
            <p>Understand the principles of ethical digital citizenship</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Practice</h3>
            <p>Apply ethical guidelines in your digital presence</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Influence</h3>
            <p>Make a positive impact in your digital community</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Testimonials Section -->
    <section class="testimonials-section">
      <div class="testimonials-content">
        <h2>What People Are Saying</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card">
            <p class="quote">"Mindful Creator has transformed how I approach digital content creation."</p>
            <p class="author">- Sarah M., Content Creator</p>
          </div>
          <div class="testimonial-card">
            <p class="quote">"A valuable resource for understanding digital responsibility."</p>
            <p class="author">- James T., Educator</p>
          </div>
          <div class="testimonial-card">
            <p class="quote">"Essential guidance for anyone building an online presence."</p>
            <p class="author">- Emma L., Social Media Manager</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
// Component logic
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: sans-serif;
}

/* Slogan Section */
.slogan-section {
  position: relative;
  background: linear-gradient(135deg, #1976d2, #64b5f6);
  padding: 4rem 2rem;
  text-align: center;
  color: white;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slogan-content h1 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.slogan-content h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
}

.slogan-description {
  font-size: 1.2rem;
  max-width: 600px;
  margin: 0 auto;
}

.slogan-svg {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 200px;
  opacity: 0.3;
}

/* About Section */
.about-section {
  padding: 4rem 2rem;
  background: #f5f5f5;
}

.about-content {
  max-width: 1200px;
  margin: 0 auto;
}

.about-content h2 {
  text-align: center;
  color: #1976d2;
  margin-bottom: 3rem;
}

.about-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.about-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.about-card h3 {
  color: #1976d2;
  margin-bottom: 1rem;
}

/* Journey Section */
.journey-section {
  padding: 4rem 2rem;
  background: white;
}

.journey-content {
  max-width: 1200px;
  margin: 0 auto;
}

.journey-content h2 {
  text-align: center;
  color: #1976d2;
  margin-bottom: 3rem;
}

.journey-steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.step {
  text-align: center;
  padding: 2rem;
}

.step-number {
  width: 50px;
  height: 50px;
  background: #1976d2;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
  font-size: 1.5rem;
}

/* Testimonials Section */
.testimonials-section {
  padding: 4rem 2rem;
  background: #f5f5f5;
}

.testimonials-content {
  max-width: 1200px;
  margin: 0 auto;
}

.testimonials-content h2 {
  text-align: center;
  color: #1976d2;
  margin-bottom: 3rem;
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.testimonial-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.quote {
  font-style: italic;
  margin-bottom: 1rem;
}

.author {
  color: #666;
  font-weight: bold;
}
</style>
