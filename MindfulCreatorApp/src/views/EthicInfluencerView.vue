<template>
  <div class="ethic-influencer-container">
    <section class="hero-section">
      <div class="hero-content">
        <h1>Ethical Influencer:</h1>
        <h1>Building Trust and</h1>
        <h1>Authenticity Online</h1>
        <p class="subtitle">Guide to responsible content creation and digital influence</p>
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

    <!-- Content Sections -->
    <section class="content-section">
      <div class="section-background">
        <img src="../components/icons/elements/BG_Gradient_Green.svg" alt="Background" class="bg-gradient">
      </div>
      <div class="content-grid">
        <div class="content-card">
          <img src="../components/icons/elements/Eye.svg" alt="Icon" class="content-icon">
          <h3>Understanding Your Impact</h3>
          <p>Learn how your content affects your audience and shapes online discourse.</p>
        </div>
        <div class="content-card">
          <img src="../components/icons/elements/Jigsaw.svg" alt="Icon" class="content-icon">
          <h3>Building Authentic Relationships</h3>
          <p>Develop genuine connections with your audience through transparent communication.</p>
        </div>
        <div class="content-card">
          <img src="../components/icons/elements/Flower_Pink_round.svg" alt="Icon" class="content-icon">
          <h3>Ethical Content Creation</h3>
          <p>Create content that aligns with your values while maintaining integrity.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const guideData = ref({
  title: 'Mindful Creator',
  sections: []
})

const practices = ref([])

const fetchData = async () => {
  try {
    const [guideResponse, practicesResponse] = await Promise.all([
      axios.get('http://localhost:5000/api/influencer-guide'),
      axios.get('http://localhost:5000/api/best-practices')
    ])
    
    guideData.value = guideResponse.data
    practices.value = practicesResponse.data.practices
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.ethic-influencer-container {
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

.element {
  width: 100%;
  height: auto;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.element:hover {
  transform: rotate(15deg);
}

/* Content Section */
.content-section {
  position: relative;
  padding: 6rem 2rem;
  color: #232323;
}

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

.content-grid {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.content-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  transform-style: preserve-3d;
  transition: transform 0.6s cubic-bezier(0.23, 1, 0.32, 1);
  cursor: pointer;
}

.content-card:hover {
  transform: translateY(-5px) rotateX(10deg) rotateY(10deg);
  box-shadow: 0 15px 35px rgba(0,0,0,0.1);
}

.content-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 1.5rem;
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