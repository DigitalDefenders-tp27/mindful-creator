<template>
  <div class="mt-4">
    <label for="commentInput" class="font-semibold">Enter your comment:</label>
    <input
      id="commentInput"
      v-model="commentText"
      @keyup.enter="analyzeComment"
      class="border rounded px-2 py-1 ml-2"
      placeholder="Type here..."
    />
    <button
      @click="analyzeComment"
      :disabled="isLoading"
      class="ml-2 px-3 py-1 rounded text-white"
      :class="isLoading ? 'bg-gray-400 cursor-wait' : 'bg-purple-600 hover:bg-purple-700'"
    >
      {{ isLoading ? 'Analyzing...' : 'Analyze Comment' }}
    </button>
    <button
      @click="resetAll"
      class="ml-4 text-sm text-red-600 underline"
    >
      Clear
    </button>
  </div>

  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">🧠 Comments Response Scripts</h1>
    
    <CriticismMenu
      v-model="selectedType"
      :data="data"
      :disabled="autoPredicted"
    />

    <transition name="fade">
      <div v-if="selectedStrategy" class="mt-4 transition-all duration-300">
        <StrategyDisplay :strategy="selectedStrategy" />
        <SampleResponse :response="selectedStrategy?.sample" />
      </div>
    </transition>

    <!-- Buttons -->
    <div class="mt-6 space-x-4">
      <button @click="openGuide" class="px-4 py-2 bg-blue-600 text-white rounded">Ethical Influencer Guide</button>
      <button @click="openPractices" class="px-4 py-2 bg-green-600 text-white rounded">Best Practices</button>
    </div>

    <!-- Modal -->
    <Modal v-if="showModal" :title="modalTitle" :content="modalContent" @close="showModal = false" />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import data from './responseData.json'
import CriticismMenu from './CriticismMenu.vue'
import StrategyDisplay from './StrategyDisplay.vue'
import SampleResponse from './SampleResponse.vue'
import Modal from './Modal.vue'

const commentText = ref('')
const selectedType = ref(null)
const autoPredicted = ref(false)
const isLoading = ref(false)

const selectedStrategy = computed(() =>
  selectedType.value ? data[selectedType.value] : null
)

// Modal state
const showModal = ref(false)
const modalTitle = ref('')
const modalContent = ref('')

function resetAll() {
  commentText.value = ''
  selectedType.value = null
  showModal.value = false
  modalTitle.value = ''
  modalContent.value = ''
  autoPredicted.value = false
}

async function openGuide() {
  try {
    const res = await fetch('http://127.0.0.1:5050/api/influencer-guide')
    const json = await res.json()
    modalTitle.value = json.title
    modalContent.value = json.sections
      .map(sec => `• ${sec.title}\n${sec.content}`)
      .join('\n\n')
    showModal.value = true
  } catch (err) {
    modalTitle.value = 'Error'
    modalContent.value = 'Failed to fetch guide content.'
    showModal.value = true
  }
}

async function openPractices() {
  try {
    const res = await fetch('http://127.0.0.1:5050/api/best-practices')
    const json = await res.json()
    modalTitle.value = 'Best Practices'
    modalContent.value = json.practices.map(p => `• ${p}`).join('\n')
    showModal.value = true
  } catch (err) {
    modalTitle.value = 'Error'
    modalContent.value = 'Failed to fetch best practices.'
    showModal.value = true
  }
}

async function analyzeComment() {
  isLoading.value = true
  try {
    const res = await fetch('http://127.0.0.1:5050/api/analyze-comment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ comment: commentText.value })
    })

    const json = await res.json()

    if (json.type) {
      selectedType.value = json.type
      autoPredicted.value = true
    } else {
      modalTitle.value = 'Unable to Detect Type'
      modalContent.value = json.error || 'Please try a more descriptive comment.'
      showModal.value = true
    }
  } catch (err) {
    modalTitle.value = 'Server Error'
    modalContent.value = 'Error contacting the server.'
    showModal.value = true
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

