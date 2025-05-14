<template>
  <div v-if="showPasswordInput" class="password-protect">
    <h2>Enter Password</h2>
    <input v-model="password" type="password" placeholder="Password" @keyup.enter="checkPassword" />
    <button @click="checkPassword">Submit</button>
  </div>
  <div v-else>
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
                :style="`background-image: url('/bentoImages/${activity.image}')`"
              ></div>
            </template>
          </BentoGridCard>
        </BentoGrid>
      </div>

      <!-- Activity Modal -->
      <div v-if="showActivityModal" class="modal">
        <div class="modal-content activity-modal">
          <span class="close" @click="closeModal">&times;</span>
          
          <!-- Activity Content -->
          <div class="activity-content">
            <div class="activity-inner-content">
              <component 
                :is="currentActivityComponent" 
                v-if="currentActivityComponent"
                @journal-submitted="onJournalSubmitted"
              />
            </div>
          </div>
          <div class="activity-divider"></div>
          <!-- Journal Feedback -->
          <div v-if="currentActivity === 'journal' && journalSubmitted" class="journal-feedback">
            <div class="encouragement">
              <h3>{{ currentEncouragement }}</h3>
              <p class="privacy-notice">Your journal entry is not stored - by writing it down and letting it go, you've already taken a step forward. ��</p>
            </div>
          </div>
          
          <!-- Rating Section -->
          <div class="feedback">
            <h2>How effective was this relaxation activity?</h2>
            <p class="total-ratings">{{ totalRatings }} people have rated this activity</p>
            <div class="stars">
              <span v-for="n in 5" :key="n" @click="rating = n" class="star-wrapper">
                <img :src="n <= rating ? starFilledIcon : starEmptyIcon" 
                     alt="star" 
                     class="star"
                     @mouseover="hoverRating = n"
                     @mouseleave="hoverRating = 0" />
              </span>
            </div>
            <button @click="submitFeedback" 
                    :disabled="rating === 0" 
                    class="submit-button"
                    :class="{ 'button-disabled': rating === 0 }">
              Submit Feedback
            </button>
          </div>

          <!-- Thank You Message -->
          <div v-if="submitted" class="thank-you">
            <h3>Thank you for your feedback!</h3>
          </div>
        </div>
      </div>

      <!-- Continue Buttons -->
      <div class="continue-section">
        <router-link to="/critical-response">
          <button class="continue-btn">Jump to Critical Response</button>
        </router-link>
        <router-link to="/creator-wellbeing">
          <button class="continue-btn wellbeing-btn">Jump to Creator Wellbeing</button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, markRaw, shallowRef } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import BentoGrid from '@/components/Activities/Bento/BentoGrid.vue'
import BentoGridCard from '@/components/Activities/Bento/BentoGridCard.vue'

// Star Icons
import starFilledIcon from '../assets/star-filled.svg'
import starEmptyIcon from '../assets/star-empty.svg'
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
    description: 'Follow a guided breathing pattern to calm your mind.',
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
    description: 'Listen to calming sounds like rain or forest.',
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
    class: 'lg:col-span-1 row-span-1 lg:row-span-2 md:col-span-1 lg:h-[34rem]' // Colour Breathing - same size as Affirmation
  }
]);

// Encouraging messages
const encouragingMessages = [
  "You're brave for expressing your feelings. Remember, tomorrow is a new day! 🌅",
  "By acknowledging your emotions, you've already begun healing. Keep going! 🌱",
  "Every feeling is valid, and every moment is a chance to begin again. 🦋",
  "You've taken a moment for yourself - that's an act of self-care! ✨",
  "Writing it down and letting go - that's the first step to feeling lighter. 🕊️",
  "Your honesty with yourself is admirable. Keep taking care of you! 🌸",
  "Remember: this moment will pass, and you're growing stronger. 🌈",
  "You're doing great by taking time to reflect. Keep moving forward! ⭐",
  "Thank you for sharing with yourself. Each word written is a step toward peace. 🍃",
  "Your feelings matter, and so does your journey to better days. 🌟"
]

// States
const showActivityModal = ref(false)
const rating = ref(0)
const hoverRating = ref(0)
const submitted = ref(false)
const currentActivity = ref(null)
const currentActivityComponent = shallowRef(null)
const totalRatings = ref(0)
const journalSubmitted = ref(false)
const currentEncouragement = ref('')

const activityRatings = ref({
  'breathing': 0,
  'meditation': 0,
  'grounding': 0
})

const activityComponents = {
  breathing: markRaw(BreathingVideo),
  meditation: markRaw(MeditationAudio),
  grounding: markRaw(GroundingGuide),
  nature: markRaw(NatureSounds),
  stretching: markRaw(StretchingRoutine),
  'color-breathing': markRaw(ColorBreathing),
  affirmation: markRaw(AffirmationReflection),
  journal: markRaw(JournalPrompt)
}

// Actions
const onJournalSubmitted = () => {
  journalSubmitted.value = true
  // Randomly select an encouraging message
  const randomIndex = Math.floor(Math.random() * encouragingMessages.length)
  currentEncouragement.value = encouragingMessages[randomIndex]
}

const startActivity = async (type) => {
  currentActivity.value = type
  currentActivityComponent.value = activityComponents[type]
  showActivityModal.value = true
  submitted.value = false
  rating.value = 0
  journalSubmitted.value = false // Reset journal submission state
  totalRatings.value = activityRatings.value[type] || 0
  document.body.style.overflow = 'hidden'
}

const onActivityCompleted = () => {
  showActivityModal.value = true
}

const closeModal = () => {
  showActivityModal.value = false
  document.body.style.overflow = 'auto'
  currentActivityComponent.value = null
}

const submitFeedback = async () => {
  if (rating.value === 0) {
    alert('Please provide a rating before submitting.')
    return
  }

  try {
    // Update local rating count
    activityRatings.value[currentActivity.value] = (activityRatings.value[currentActivity.value] || 0) + 1
    totalRatings.value = activityRatings.value[currentActivity.value]
    submitted.value = true
  } catch (error) {
    console.error('Error submitting rating:', error)
    alert('Failed to submit rating. Please try again.')
  }
}

const router = useRouter()
const password = ref('')
const correctPassword = 'your_password_here' // TODO: Replace with your real password
const showPasswordInput = ref(false)

onMounted(() => {
  if (sessionStorage.getItem('authenticated') !== 'true') {
    router.push({ name: 'password' })
  }
})

function checkPassword() {
  if (password.value === correctPassword) {
    localStorage.setItem('authenticated', 'true')
    router.push('/')
  } else {
    alert('Incorrect password!')
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
  font-size: 4rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #6CBDB5 20%,
    #9BCCA6 40%,
    #9BCCA6 60%,
    #6CBDB5 80%
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
  overflow: visible;
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(108, 189, 181, 0.5));
  transform: none;
  animation: liquidFlow 2s linear infinite; /* Speed up animation on hover */
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

/* Ensure bento card titles are always pure white */
:deep(.bento-grid-card h3),
:deep(h3[class*="text-"]),
:deep(.group:hover h3),
:deep([role="button"] h3),
:deep(.relative h3) {
  color: white !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6) !important;
  font-weight: bold !important;
}

/* Add additional selectors to override any possible parent styles */
:deep([class*="bento"] *) h3,
:deep([class*="card"] *) h3,
:deep([class*="grid"] *) h3 {
  color: white !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.6) !important;
}

/* Override any hover states */
:deep(*:hover h3),
:deep(.group:hover h3),
:deep([role="button"]:hover h3) {
  color: white !important;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.activity-modal {
  max-width: 800px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  padding-bottom: 2rem;
}

.activity-content-topline { display: none !important; }
.activity-content {
  background: #fff;
  border-radius: 22px;
  margin-top: 2.5rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.07);
  padding: 2.5rem 2rem;
  margin-bottom: 2.5rem;
  border-bottom: none;
  min-width: 0;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  position: relative;
  z-index: 2;
  color: #222;
  letter-spacing: 0.01em;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.activity-inner-content {
  max-width: 600px;
  margin: 0 auto;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.activity-content h1, .activity-content h2 {
  font-size: 2.7rem;
  font-weight: 700;
  margin-bottom: 1.2rem;
  margin-top: 0.5rem;
  color: #1a232b;
  letter-spacing: 0.01em;
}
.activity-content h3 {
  font-size: 1.7rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
  margin-top: 0.5rem;
  color: #2a3a3f;
}
.activity-content p {
  font-size: 1.25rem;
  font-weight: 400;
  margin: 1rem 0 1rem 0;
  line-height: 1.7;
  color: #444;
}
.activity-content ul {
  margin: 1.1rem 0 1.1rem 1.2rem;
  padding-left: 1.2rem;
  text-align: left;
  display: block;
}
.activity-content li {
  font-size: 1.25rem;
  font-weight: 400;
  margin: 0.4rem 0 0.4rem 0;
  color: #444;
  line-height: 1.6;
}
.activity-content span, .activity-content div {
  font-size: 1.18rem;
  font-weight: 400;
  color: #222;
}
.activity-divider {
  width: 100%;
  max-width: 700px;
  height: 0;
  border: none;
  border-top: 2px solid #e0e0e0;
  margin: 2.5rem auto 2.5rem auto;
  border-radius: 1px;
  box-shadow: none;
  background: none;
}
.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.close {
  position: absolute;
  right: 1rem;
  top: 0.5rem;
  font-size: 1.5rem;
  cursor: pointer;
}
.feedback {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f8f9ff 0%, #f5f6ff 100%);
  border-radius: 16px;
  margin-top: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}
.feedback h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.total-ratings {
  color: #666;
  font-size: 1rem;
  margin: 0.5rem 0 1.5rem;
  font-style: italic;
}
.stars {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin: 1.5rem 0;
}
.star-wrapper {
  cursor: pointer;
  padding: 8px;
  transition: transform 0.3s ease;
}
.star-wrapper:hover {
  transform: scale(1.15);
}
.star {
  width: 36px;
  height: 36px;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  transition: transform 0.2s ease, filter 0.2s ease;
}
.star:hover {
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.15));
}
.submit-button {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  color: white;
  padding: 0.8rem 2.5rem;
  border: none;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
  box-shadow: 0 4px 15px rgba(74, 144, 226, 0.2);
}
.submit-button:hover:not(.button-disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(74, 144, 226, 0.3);
  background: linear-gradient(135deg, #357abd 0%, #4a90e2 100%);
}
.button-disabled {
  background: linear-gradient(135deg, #cccccc 0%, #bbbbbb 100%);
  cursor: not-allowed;
  box-shadow: none;
}
.thank-you {
  text-align: center;
  padding: 1.5rem;
  color: #4a90e2;
  font-size: 1.2rem;
  font-weight: 500;
  animation: fadeInUp 0.5s ease;
}
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.continue-section {
  margin-top: 2rem;
  margin-bottom: 6rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
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
  width: 340px;
}
.continue-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(142, 45, 226, 0.4);
}
.wellbeing-btn {
  background: linear-gradient(135deg, #F9F871 0%, #7ECE73 100%);
  color: #333;
  box-shadow: 0 4px 15px rgba(126, 206, 115, 0.25);
}
.wellbeing-btn:hover {
  box-shadow: 0 8px 20px rgba(126, 206, 115, 0.4);
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
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-4xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-xl;
    white-space: normal;
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
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-3xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-lg;
    white-space: normal;
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
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-2xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-base;
    white-space: normal;
  }
}
@media (max-width: 480px) {
  .decorative-elements {
    opacity: 0;
    display: none;
  }
  
  .hero-section {
    min-height: 16vh;
    padding: 8rem 0 0.5rem;
  }
  
  .hero-content {
    min-height: 16vh;
  }

  .title-group h1 {
    font-size: 2.5rem;
    white-space: normal;
  }
  
  .title-group h2 {
    font-size: 1.5rem;
    white-space: normal;
  }
  
  .subtitle {
    font-size: 1rem;
    white-space: normal;
  }
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
.journal-feedback {
  text-align: center;
  padding: 2rem;
  background: linear-gradient(135deg, #f6f9ff 0%, #f9f6ff 100%);
  border-radius: 12px;
  margin-top: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.encouragement {
  max-width: 600px;
  margin: 0 auto;
}
.encouragement h3 {
  font-size: 1.5rem;
  color: #6c63ff;
  margin-bottom: 1rem;
  line-height: 1.4;
}
.privacy-notice {
  color: #666;
  font-size: 0.95rem;
  margin-top: 1.5rem;
  font-style: italic;
  line-height: 1.5;
}
.password-protect {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 4rem;
}
.password-protect input {
  margin: 1rem 0;
  padding: 0.5rem 1rem;
  font-size: 1.1rem;
}
.password-protect button {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
  background: #e573a6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>
