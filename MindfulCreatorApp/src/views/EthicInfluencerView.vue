<template>
  <div class="ethic-influencer-container">
    <!-- 1. Slogan Section -->
    <section class="slogan-section">
      <div class="slogan-content">
        <h1>Mindful Creator</h1>
        <h2>Navigating Digital Influence with Integrity</h2>
        <p class="slogan-description">
          A comprehensive guide to becoming a responsible and ethical digital creator
        </p>
      </div>
    </section>

    <!-- 2. Know Your Power Section -->
    <section class="power-section">
      <div class="section-content">
        <h2>Know Your Power</h2>
        <p class="section-subtitle">Understanding your role and influence as a content creator</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <h3>What It Means to Be an Influencer</h3>
            <p>Explore the responsibilities and impact of digital influence in today's connected world.</p>
            <div class="resource-tags">
              <span class="tag">Digital Identity</span>
              <span class="tag">Influence</span>
            </div>
          </div>
          
          <div class="resource-card">
            <h3>Your Voice, Your Reach</h3>
            <p>Understanding the power of your digital presence and how to use it responsibly.</p>
            <div class="resource-tags">
              <span class="tag">Audience Impact</span>
              <span class="tag">Responsibility</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Create with Integrity Section -->
    <section class="integrity-section">
      <div class="section-content">
        <h2>Create with Integrity</h2>
        <p class="section-subtitle">Making ethical choices when creating and sharing content</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <h3>Avoiding Clickbait Ethics</h3>
            <p>Learn how to create engaging content without resorting to misleading tactics.</p>
            <div class="resource-tags">
              <span class="tag">Content Ethics</span>
              <span class="tag">Misinformation</span>
            </div>
          </div>
          
          <div class="resource-card">
            <h3>Fact-Check Before You Post</h3>
            <p>Essential guidelines for verifying information before sharing with your audience.</p>
            <div class="resource-tags">
              <span class="tag">Fact Checking</span>
              <span class="tag">Responsibility</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 4. Lead by Example Section -->
    <section class="lead-section">
      <div class="section-content">
        <h2>Lead by Example</h2>
        <p class="section-subtitle">Being a positive force in digital communities</p>
        
        <div class="resource-grid">
          <div class="resource-card">
            <h3>Calling In vs. Calling Out</h3>
            <p>Effective strategies for addressing problematic content while maintaining respect.</p>
            <div class="resource-tags">
              <span class="tag">Community Building</span>
              <span class="tag">Conflict Resolution</span>
            </div>
          </div>
          
          <div class="resource-card">
            <h3>How to Handle Trolls Gracefully</h3>
            <p>Maintaining professionalism and positivity when facing online negativity.</p>
            <div class="resource-tags">
              <span class="tag">Online Civility</span>
              <span class="tag">Community Management</span>
            </div>
          </div>
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
  min-height: 40vh;
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

/* Common Section Styles */
.section-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.section-content h2 {
  text-align: center;
  color: #1976d2;
  margin-bottom: 1rem;
}

.section-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

/* Resource Grid */
.resource-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.resource-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.resource-card:hover {
  transform: translateY(-5px);
}

.resource-card h3 {
  color: #1976d2;
  margin-bottom: 1rem;
}

.resource-tags {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.tag {
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
}

/* Section-specific backgrounds */
.power-section {
  background: #f5f5f5;
}

.integrity-section {
  background: white;
}

.lead-section {
  background: #f5f5f5;
}
</style> 