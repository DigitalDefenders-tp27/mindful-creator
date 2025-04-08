<template>
  <div class="relaxation-view">
    <h1>Relaxation Resources</h1>

    <!-- Activities -->
    <div class="activities">
      <div class="activity-card" v-for="activity in activities" :key="activity.title">
        <h3>{{ activity.title }}</h3>
        <p>{{ activity.description }}</p>
        <button @click="startActivity(activity.type)">Try it</button>
      </div>
    </div>

        <!-- Dynamic Activity Components -->
        <component :is="currentActivityComponent" v-if="currentActivityComponent" />

    <!-- Feedback -->
    <transition name="fade-slide">
      <div v-if="showRating" class="feedback">
        <h2>How effective was this relaxation activity?</h2>
        <div class="stars">
          <span v-for="n in 5" :key="n" @click="rating = n">
            <img :src="n <= rating ? filledStar : emptyStar" alt="star" class="star" />
          </span>
        </div>

        <textarea
          v-model="comment"
          placeholder="Leave your suggestion..."
          class="comment-box"
          rows="4"
        ></textarea>

        <button class="submit-btn" @click="submitFeedback">Submit Feedback</button>

        <p v-if="submitted" class="thank-you">Thank you for your feedback!</p>
      </div>
    </transition>

    <!-- Continue Button -->
    <div class="continue-section">
      <router-link to="/critical-response">
        <button class="continue-btn">Proceed to Critical Response</button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// Star Icons
import filledStar from '../components/icons/Elements/star-filled.png'
import emptyStar from '../components/icons/Elements/star-empty.png'
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
    type: 'breathing'
  },
  {
    title: 'Guided Meditation',
    description: 'Listen to a short meditation audio to relax and refocus.',
    type: 'meditation'
  },
  {
    title: 'Sensory Grounding',
    description: 'Try a 5-4-3-2-1 activity to bring yourself into the present.',
    type: 'grounding'
  },
  {
    title: 'Nature Sounds',
    description: 'Listen to calming sounds like rain, ocean waves, or forest.',
    type: 'nature'
  },
  {
    title: 'Stretching Routine',
    description: 'Follow a short guide to stretch your body and ease tension.',
    type: 'stretching'
  },
  {
    title: 'Color Breathing',
    description: 'Visualize breathing in calming colors and breathing out stress.',
    type: 'color-breathing'
  },
  {
    title: 'Affirmation Reflection',
    description: 'Read and reflect on positive affirmations for a mental reset.',
    type: 'affirmation'
  },
  {
    title: 'Mini Journal Prompt',
    description: 'Write one sentence about how you’re feeling right now.',
    type: 'journal'
  }
]

// States
const showRating = ref(false)
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
  submitted.value = false
  rating.value = 0
  comment.value = ''
}

const submitFeedback = async () => {
  if (rating.value === 0 || comment.value.trim() === '') {
    alert('Please provide both a rating and a comment.')
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
  } catch (err) {
    console.error('Failed to submit feedback:', err)
  }
}
</script>

<style scoped>
.relaxation-view {
  padding: 2rem;
  font-family: Avenir, Helvetica, sans-serif;
  background: #fefbf4;
  text-align: center;
}

.activities {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin: 2rem 0;
}

.activity-card {
  background: #e3f6f5;
  border-radius: 12px;
  padding: 1.5rem;
  width: 250px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.activity-card h3 {
  margin-bottom: 0.5rem;
}

.activity-card button {
  margin-top: 1rem;
  padding: 8px 16px;
  background: #3a86ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  transition: 0.3s;
}

.activity-card button:hover {
  background: #265ef2;
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
}

.continue-btn {
  background-color: #6c63ff;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}
.continue-btn:hover {
  background-color: #5848d3;
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
</style>
