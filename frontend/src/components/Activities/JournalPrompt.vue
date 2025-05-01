<template>
  <div class="journal-prompt">
    <h2>Mini Journal Moment</h2>
    <p class="description">Take a moment to write down how you're feeling right now. Sometimes, just putting our thoughts into words can help us process them better.</p>
    
    <div class="prompt-container" v-if="!isSubmitted">
      <textarea 
        v-model="journalEntry"
        placeholder="Write one sentence about your current feelings..."
        :maxlength="maxLength"
        @input="updateCharCount"
      ></textarea>
      <div class="char-count">{{ charCount }}/{{ maxLength }}</div>
      <button 
        @click="submitEntry"
        class="submit-btn"
        :disabled="!journalEntry.trim()"
      >
        Release & Let Go
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['journal-submitted'])

const journalEntry = ref('')
const isSubmitted = ref(false)
const maxLength = 200
const charCount = ref(0)

const updateCharCount = () => {
  charCount.value = journalEntry.value.length
}

const submitEntry = () => {
  if (journalEntry.value.trim()) {
    isSubmitted.value = true
    emit('journal-submitted')
    // Clear the entry (symbolically letting it go)
    journalEntry.value = ''
  }
}
</script>

<style scoped>
.journal-prompt {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 1rem;
  text-align: center;
}

.description {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 2rem;
  text-align: center;
  line-height: 1.6;
}

.prompt-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

textarea {
  width: 100%;
  min-height: 120px;
  padding: 1rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  line-height: 1.5;
  resize: vertical;
  transition: border-color 0.3s ease;
  font-family: inherit;
}

textarea:focus {
  outline: none;
  border-color: #6c63ff;
  box-shadow: 0 0 0 3px rgba(108, 99, 255, 0.1);
}

.char-count {
  align-self: flex-end;
  color: #666;
  font-size: 0.9rem;
}

.submit-btn {
  background: linear-gradient(135deg, #6c63ff 0%, #4CAF50 100%);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 25px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(108, 99, 255, 0.2);
}

.submit-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 640px) {
  .journal-prompt {
    padding: 1rem;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  .description {
    font-size: 1rem;
  }
  
  textarea {
    min-height: 100px;
  }
  
  .submit-btn {
    font-size: 1rem;
    padding: 0.7rem 1.5rem;
  }
}
</style>
  