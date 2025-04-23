<template>
  <div class="relaxation-container">
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Relaxation Zone</h1>
            <h2>Mindfulness Moments for Creators</h2>
          </div>
          <p class="subtitle">Take a break with guided practices designed for digital wellbeing</p>
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

    <!-- Activities -->
    <div class="activities-container">
      <h2 class="activities-title">Featured Relaxation Activities</h2>
      <p class="activities-subtitle">Choose any activity to give yourself a moment of calm</p>
      <BentoGrid class="activities-bento">
        <BentoGridCard
          v-for="(activity, index) in activitiesWithLayout"
          :key="index"
          :name="activity.title"
          :description="activity.description"
          :class="activity.class"
          @click="startActivity(activity.type)"
        >
          <template v-if="activity.image" #background>
            <div
              class="absolute inset-0 bg-cover bg-center transition-transform duration-700 ease-out group-hover:scale-110 will-change-transform"
              :style="`background-image: url('/src/assets/images/bento/${activity.image}')`"
            ></div>
          </template>
        </BentoGridCard>
      </BentoGrid>
    </div>

    <!-- Dynamic Activity Components in Modal -->
    <div v-if="showActivityModal" class="activity-modal-overlay" @click="closeModal">
      <div class="activity-modal" @click.stop>
        <button class="close-modal-btn" @click="closeModal">&times;</button>
        <div class="activity-modal-content">
          <component :is="currentActivityComponent" v-if="currentActivityComponent" />
          
          <!-- Feedback inside modal -->
          <div v-if="showRating" class="feedback">
            <h2>How effective was this relaxation activity?</h2>
            <div class="stars">
              <span v-for="n in 5" :key="n" @click="rating = n">
                <img :src="n <= rating ? filledStar : emptyStar" alt="star" class="star" />
              </span>
            </div>

            <textarea
              v-model="comment"
              placeholder="Share your thoughts about this experience..."
              class="comment-box"
              rows="4"
            ></textarea>

            <button class="submit-btn" @click="submitFeedback">Submit Feedback</button>

            <p v-if="submitted" class="thank-you">Thank you for your feedback!</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Continue Button -->
    <div class="continue-section">
      <router-link to="/critical-response">
        <button class="continue-btn">Jump to Critical Response</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import BentoGrid from '@/components/Activities/Bento/BentoGrid.vue'
import BentoGridCard from '@/components/Activities/Bento/BentoGridCard.vue'

// Star Icons
import filledStar from '../assets/icons/elements/star-filled.png'
import emptyStar from '../assets/icons/elements/star-empty.png'
import GroundingGuide from '../components/Activities/GroundingGuide.vue'
import NatureSounds from '../components/Activities/NatureSounds.vue'
import StretchingRoutine from '../components/Activities/StretchingRoutine.vue'
import ColorBreathing from '../components/Activities/ColorBreathing.vue'
import AffirmationReflection from '../components/Activities/AffirmationReflection.vue'
import JournalPrompt from '../components/Activities/JournalPrompt.vue'

// Importing all activity components
import BreathingVideo from '../components/Activities/BreathingVideo.vue'
import MeditationAudio from '../components/Activities/MeditationAudio.vue'

// Activities
const activities = [
  {
    title: 'Breathing Exercise',
    description: 'Follow a guided 4-7-8 breathing pattern to calm your mind.',
    type: 'breathing',
    image: 'BreathingExercise.png'
  },
  {
    title: 'Guided Meditation',
    description: 'Listen to a short meditation audio to relax and refocus.',
    type: 'meditation',
    image: 'Meditation.png'
  },
  {
    title: 'Sensory Grounding',
    description: 'Try a 5-4-3-2-1 activity to bring yourself into the present.',
    type: 'grounding',
    image: 'SensoryGrounding.png'
  },
  {
    title: 'Nature Sounds',
    description: 'Listen to calming sounds like rain, ocean waves, or forest.',
    type: 'nature',
    image: 'NatureSounds.jpg'
  },
  {
    title: 'Stretching Routine',
    description: 'Follow a short guide to stretch your body and ease tension.',
    type: 'stretching',
    image: 'StretchingRoutine.png'
  },
  {
    title: 'Colour Breathing',
    description: 'Visualise breathing in calming colours and breathing out stress.',
    type: 'color-breathing',
    image: 'ColorBreathing.jpg'
  },
  {
    title: 'Affirmation Reflection',
    description: 'Read and reflect on positive affirmations for a mental reset.',
    type: 'affirmation',
    image: 'Affirmation.jpg'
  },
  {
    title: 'Mini Journal Prompt',
    description: 'Write one sentence about how you are feeling right now.',
    type: 'journal',
    image: 'MiniJournalPrompt.png'
  }
]

// Adding layout classes to create different card sizes
const activitiesWithLayout = computed(() => [
  // Left column
  { 
    ...activities[0], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-2 md:col-span-1 xl:h-[28rem]' // Breathing Exercise - tall card
  }, 
  { 
    ...activities[2], 
    class: 'lg:col-span-1 row-span-1 md:col-span-1 lg:h-[16rem]' // Sensory Grounding - standard height
  }, 
  
  // Middle column - Meditation as a super tall card
  { 
    ...activities[1], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-3 md:col-span-2 xl:h-[44rem]' // Guided Meditation - super tall card
  },
  
  // Right column - Affirmation in the middle position
  { 
    ...activities[3], 
    class: 'lg:col-span-1 row-span-1 md:col-span-1 lg:h-[14rem]' // Nature Sounds - small card
  },
  { 
    ...activities[6], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-2 md:col-span-1 lg:h-[34rem]' // Affirmation Reflection - extended card
  },
  { 
    ...activities[4], 
    class: 'lg:col-span-1 row-span-1 lg:row-span-1 md:col-span-1 lg:h-[18rem]' // Stretching Routine - adjusted height
  },
  
  // Bottom row
  { 
    ...activities[5], 
    class: 'lg:col-span-2 row-span-1 md:col-span-1 lg:h-[20rem] lg:col-start-2' // Colour Breathing - right-aligned
  },
  { 
    ...activities[7], 
    class: 'lg:col-span-3 row-span-1 md:col-span-2 lg:h-[16rem]' // Mini Journal Prompt - full width card
  }
]);

// States
const showRating = ref(false)
const showActivityModal = ref(false)
const rating = ref(0)
const comment = ref('')
const submitted = ref(false)
const currentActivity = ref(null)
const currentActivityComponent = ref(null)

const activityComponents = {
  breathing: BreathingVideo,
  meditation: MeditationAudio,
  grounding: GroundingGuide,
  nature: NatureSounds,
  stretching: StretchingRoutine,
  'color-breathing': ColorBreathing,
  affirmation: AffirmationReflection,
  journal: JournalPrompt
}

// Actions
const startActivity = (type) => {
  currentActivity.value = type
  currentActivityComponent.value = activityComponents[type]
  showRating.value = true
  showActivityModal.value = true
  submitted.value = false
  rating.value = 0
  comment.value = ''
  
  // Prevent body scrolling when modal is open
  document.body.style.overflow = 'hidden'
}

const closeModal = () => {
  showActivityModal.value = false
  
  // Re-enable body scrolling when modal is closed
  document.body.style.overflow = 'auto'
}

const submitFeedback = async () => {
  if (rating.value === 0 || comment.value.trim() === '') {
    alert('Please provide both a rating and comment before submitting.')
    return
  }

  submitted.value = true

  try {
    await axios.post('https://your-api-endpoint.com/submit-rating', {
      activity: currentActivity.value,
      rating: rating.value,
      comment: comment.value,
      timestamp: new Date().toISOString()
    })
    console.log('Feedback submitted')
    
    // Close modal after a short delay to show the thank you message
    setTimeout(() => {
      closeModal()
    }, 1500)
  } catch (err) {
    console.error('Failed to submit feedback:', err)
  }
}
</script>

<style scoped>
.relaxation-container {
  background-color: rgb(254, 251, 244);
  min-height: 100vh;
  overflow-x: hidden;
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
  font-size: 5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #6CBDB5 0%, #9BCCA6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.4;
  display: block;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  text-align: left;
  overflow: visible;
  padding-right: 1rem;
  padding-bottom: 0.5rem;
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
  white-space: nowrap;
  text-align: left;
  overflow: visible;
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
  transform: translateX(0);
  justify-content: end;
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

.top-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
}

section:not(:last-child)::after {
  display: none;
}

.activities-container {
  padding: 3rem 2rem;
  max-width: 1400px;
  margin: 0 auto;
  background-color: rgb(250, 247, 240);
  border-radius: 2rem;
  margin-top: -1rem;
  position: relative;
  z-index: 2;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
}

.activities-title {
  font-size: 2.5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #4ECDC4 0%, #6c63ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.75rem;
  text-align: center;
}

.activities-subtitle {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 2.5rem;
  text-align: center;
}

.activities-bento {
  width: 100%;
}

.activity-bento-item {
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f5f9ff;
  border: 1px solid rgba(0, 0, 0, 0.05);
  height: 100%;
}

.activity-bento-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: rgba(0, 0, 0, 0.1);
}

.bento-icon {
  width: 100%;
  height: 100%;
  object-fit: cover;
  margin: 0;
}

.feedback {
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center; 
}

.stars {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin: 1rem 0;
}

.star {
  width: 34px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.star:hover {
  transform: scale(1.2);
}

.comment-box {
  margin-top: 1rem;
  width: 80%;
  max-width: 500px;
  border-radius: 8px;
  border: 1px solid #ccc;
  padding: 12px;
  font-size: 14px;
  resize: none;
  font-family: inherit;
}

.submit-btn {
  margin-top: 1rem;
  background: #4f83ff;
  color: white;
  padding: 10px 20px;
  border: none;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.3s ease;
}
.submit-btn:hover {
  background: #375ecf;
}

.thank-you {
  color: #28a745;
  font-weight: bold;
  margin-top: 0.5rem;
}

.continue-section {
  margin-top: 2rem;
  margin-bottom: 6rem;
  text-align: center;
}

.continue-btn {
  background: linear-gradient(135deg, #8E2DE2 0%, #FF6B9B 100%);
  color: white;
  padding: 14px 28px;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(142, 45, 226, 0.25);
  letter-spacing: 0.5px;
}

.continue-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(142, 45, 226, 0.4);
}

/* Animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}
.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(20px);
}
.fade-slide-enter-to {
  opacity: 1;
  transform: translateY(0);
}

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
  
  .title-group h2,
  .subtitle {
    white-space: normal;
  }
}

@media (max-width: 1024px) {
  .decorative-elements {
    transform: translateX(0) scale(0.9);
    opacity: 0.5;
    row-gap: 0.5rem;
  }
  
  .title-group h1 {
    white-space: normal;
  }
}

@media (max-width: 768px) {
  .decorative-elements {
    opacity: 0.1;
    transform: translateX(0) scale(0.8);
  }
  
  .hero-content {
    flex-direction: column;
    align-items: flex-start;
    padding-top: 0.75rem;
    min-height: 22vh;
  }
  
  .hero-section {
    min-height: 22vh;
    padding: 7rem 0 0.5rem;
  }
  
  .slogan {
    max-width: 90%;
  }
  
  .title-group h1 {
    font-size: 3.5rem;
  }
  
  .title-group h2 {
    font-size: 2rem;
  }
}

@media (max-width: 640px) {
  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.7);
  }
  
  .hero-content {
    min-height: 18vh;
    padding-top: 0.25rem;
  }
  
  .hero-section {
    min-height: 18vh;
    padding: 7.5rem 0 0.5rem;
    margin-bottom: 1rem;
  }
  
  .title-group h1 {
    font-size: 2.5rem;
  }
  
  .title-group h2 {
    font-size: 1.5rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .decorative-elements {
    opacity: 0;
    display: none;
  }
  
  .hero-content {
    min-height: 16vh;
  }
  
  .hero-section {
    min-height: 16vh;
    padding: 8rem 0 0.5rem;
  }
}

.activity-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease;
}

.activity-modal {
  background-color: white;
  border-radius: 16px;
  width: 90%;
  max-width: 800px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  animation: slideUp 0.4s ease;
}

.activity-modal-content {
  padding: 2rem;
}

/* Make sure all activity components fill the modal width */
.activity-modal-content > div {
  width: 100%;
  padding: 0;
  margin: 0;
}

.activity-modal-content > div h2,
.breathing-video h2,
.meditation-audio h2,
.color-breathing h2,
.grounding-guide h2,
.nature-sounds h2,
.stretching-routine h2,
.affirmation-reflection h2,
.journal-prompt h2 {
  font-size: 36px !important;
  font-weight: bold !important;
  margin-bottom: 20px !important;
  color: #333 !important;
  text-align: center !important;
  line-height: 1.3 !important;
  background: linear-gradient(135deg, #4ECDC4 0%, #6c63ff 100%) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
  display: block !important;
  padding: 0.5rem 0 !important;
  animation: fadeInDown 0.6s ease forwards !important;
}

.activity-modal-content > div p:first-of-type,
.breathing-video p:first-of-type,
.meditation-audio p:first-of-type,
.color-breathing p:first-of-type,
.grounding-guide p:first-of-type,
.nature-sounds p:first-of-type,
.stretching-routine p:first-of-type,
.affirmation-reflection p:first-of-type,
.journal-prompt p:first-of-type {
  font-size: 18px !important;
  margin-bottom: 25px !important;
  line-height: 1.6 !important;
  color: #666 !important;
  text-align: center !important;
  max-width: 600px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}

.close-modal-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 30px;
  line-height: 30px;
  color: #666;
  cursor: pointer;
  z-index: 10;
  transition: color 0.2s ease;
}

.close-modal-btn:hover {
  color: #000;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { 
    opacity: 0;
    transform: translateY(30px); 
  }
  to { 
    opacity: 1;
    transform: translateY(0); 
  }
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Adjust feedback style inside modal */
.activity-modal .feedback {
  padding-top: 2rem;
  border-top: 1px solid #eee;
  margin-top: 2rem;
}

/* Override any padding from individual components */
.activity-modal-content .breathing-video,
.activity-modal-content .meditation-audio,
.activity-modal-content .color-breathing,
.activity-modal-content .grounding-guide,
.activity-modal-content .nature-sounds,
.activity-modal-content .stretching-routine,
.activity-modal-content .affirmation-reflection,
.activity-modal-content .journal-prompt {
  padding: 0 !important;
}
</style>
