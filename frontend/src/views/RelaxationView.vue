<template>
  <div class="relaxation-view">
    <!-- Relaxation page content will go here -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Relaxation Zone</h1>
            <h2>Take a moment to recharge</h2>
          </div>
          <p class="subtitle">Simple mindfulness activities to reduce stress and restore balance</p>
        </div>
        <div class="decorative-elements">
          <!-- Top Row Right -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable rotating">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Wide_Red.svg" alt="Wave" class="element hoverable rotating">
            </div>
          </div>
          
          <!-- Second Row -->
          <div class="second-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable rotating">
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Placeholder for relaxation content -->
    <section class="relaxation-content">
      <h2>Content coming soon</h2>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiFetch } from '../api/config'

// State variables
const rating = ref(0)
const currentActivity = ref('breathing')
const submitted = ref(false)
const totalRatings = ref(0)
const averageRating = ref(0)

// The submitFeedback function from the original file
const submitFeedback = async () => {
  if (rating.value === 0) {
    alert('Please give a rating before submitting.')
    return
  }

  try {
    console.log('Submitting rating:', currentActivity.value, rating.value)
    
    // Show processing status
    const feedbackElement = document.querySelector('.feedback')
    if (feedbackElement) {
      feedbackElement.style.opacity = '0.6'
    }
    
    // Construct request data
    const payload = {
      activity_key: currentActivity.value,
      rating: rating.value
    }
    
    console.log('Data to be submitted:', payload)
    
    // Try to use apiFetch to send rating request with proper HTTPS handling
    try {
      const result = await apiFetch('/api/ratings', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      
      console.log('Rating submission successful, server returned:', result)
      
      // Update statistics
      if (result && result.stats) {
        totalRatings.value = result.stats.total_ratings || result.stats.count || 0
        averageRating.value = result.stats.average_rating || 0
        console.log(`Updated statistics: Total ratings=${totalRatings.value}, Average rating=${averageRating.value}`)
      } else {
        // If no valid statistics received, manually calculate new statistics
        handleFallbackRatingUpdate()
      }
    } catch (fetchError) {
      console.error('API call failed, trying direct fetch:', fetchError)
      
      // As a fallback, try direct fetch with explicit HTTPS URL
      try {
        const apiUrl = 'https://api.tiezhu.org/api/ratings'
        console.log('Attempting direct fetch to:', apiUrl)
        
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify(payload),
          // Handle redirects automatically
          redirect: 'follow'
        })
    
        if (response.ok) {
          const result = await response.json()
          console.log('Direct fetch successful:', result)
    
          // Update statistics
          if (result && result.stats) {
            totalRatings.value = result.stats.total_ratings || result.stats.count || 0
            averageRating.value = result.stats.average_rating || 0
            console.log(`Updated statistics: Total ratings=${totalRatings.value}, Average rating=${averageRating.value}`)
          } else {
            // If no valid statistics received, manually calculate new statistics
            handleFallbackRatingUpdate()
          }
        } else {
          console.error(`Direct fetch failed: HTTP status code ${response.status}`)
          handleFallbackRatingUpdate()
        }
      } catch (directFetchError) {
        console.error('Direct fetch also failed:', directFetchError)
        handleFallbackRatingUpdate()
      }
    }
    
    // Show success message
    setTimeout(() => {
      if (feedbackElement) {
        feedbackElement.style.display = 'none'
      }
      
      submitted.value = true
      
      setTimeout(() => {
        const thankYouElement = document.querySelector('.thank-you-container')
        if (thankYouElement) {
          thankYouElement.style.display = 'block'
          thankYouElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
        }
      }, 100)
    }, 500)
  } catch (error) {
    console.error('Error submitting rating:', error)
    handleFallbackRatingUpdate()
    
    // Show success message (to provide good user experience even if there's an error)
    const feedbackElement = document.querySelector('.feedback')
    if (feedbackElement) {
      feedbackElement.style.display = 'none'
    }
    
    submitted.value = true
    
    setTimeout(() => {
      const thankYouElement = document.querySelector('.thank-you-container')
      if (thankYouElement) {
        thankYouElement.style.display = 'block'
        thankYouElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
      }
    }, 100)
  }
}

// Helper function for fallback rating update
const handleFallbackRatingUpdate = () => {
  // Manually update statistics
  const newTotal = totalRatings.value + 1
  const newAverage = ((averageRating.value * totalRatings.value) + rating.value) / newTotal
  totalRatings.value = newTotal
  averageRating.value = newAverage
  console.log(`Manually calculated statistics after error: Total ratings=${totalRatings.value}, Average rating=${averageRating.value}`)
}

onMounted(async () => {
  // You can fetch initial data here if needed
  try {
    const statsResponse = await apiFetch(`/api/ratings/${currentActivity.value}`)
    if (statsResponse && statsResponse.stats) {
      totalRatings.value = statsResponse.stats.total_ratings || statsResponse.stats.count || 0
      averageRating.value = statsResponse.stats.average_rating || 0
    }
  } catch (error) {
    console.error('Error fetching initial statistics:', error)
  }
})
</script>

<style scoped>
.relaxation-view {
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
  font-size: 6rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #FF6B98 20%,
    #65C9A4 40%,
    #65C9A4 60%,
    #FF6B98 80%
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
  padding: 0 0 0.15em;
  transform: translateY(-0.05em);
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(255, 107, 152, 0.5));
  transform: scale(1.02);
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
  font-size: 3.75rem;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
  display: block;
  white-space: nowrap;
  text-align: left;
  overflow: visible;
}

.subtitle {
  font-size: 1.875rem;
  color: #666;
  line-height: 1.4;
  margin-top: 1.5rem;
  white-space: nowrap;
  text-align: left;
  max-width: 100%;
}

.decorative-elements {
  position: absolute;
  top: 0;
  right: 0;
  width: 960px;
  height: 100%;
  display: grid;
  grid-template-columns: repeat(6, 160px);
  grid-template-rows: auto auto;
  row-gap: 1rem;
  padding: 2rem 0;
  z-index: 1;
  pointer-events: none;
  transform: translateX(0);
  justify-content: end;
}

.top-row {
  display: grid;
  grid-template-columns: repeat(2, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 5 / 7;
  grid-row: 1;
  justify-self: end;
}

.second-row {
  display: grid;
  grid-template-columns: 160px;
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 6 / 7;
  grid-row: 2;
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

/* Add rotation animation */
@keyframes slowRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.rotating {
  animation: slowRotate 30s linear infinite;
}

/* Adjust hover effect to combine with rotation */
.top-row .element:hover,
.second-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
  animation: slowRotate 5s linear infinite;
}

.relaxation-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

/* Responsive styles */
@media (max-width: 1024px) {
  .title-group h1 {
    font-size: 4.5rem;
  }
  .title-group h2 {
    font-size: 3rem;
  }
  .subtitle {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  .hero-section {
    min-height: 30vh;
    padding: 5rem 0 1rem;
  }
  .title-group h1 {
    font-size: 3.5rem;
  }
  .title-group h2 {
    font-size: 2.5rem;
    white-space: normal;
  }
  .subtitle {
    font-size: 1.25rem;
    white-space: normal;
  }
}

@media (max-width: 640px) {
  .hero-section {
    min-height: 25vh;
  }
  .title-group h1 {
    font-size: 2.5rem;
  }
  .title-group h2 {
    font-size: 1.8rem;
  }
  .subtitle {
    font-size: 1rem;
  }
}
</style>
