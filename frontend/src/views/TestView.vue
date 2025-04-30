<template>
  <div class="test-container">
    <h1 class="text-2xl font-bold mb-4">YouTube Comment Analysis Test</h1>
    
    <div class="mb-6">
      <label class="block text-sm font-medium mb-2" for="youtube-url">
        Enter YouTube Video URL
      </label>
      <input 
        id="youtube-url" 
        v-model="youtubeUrl" 
        type="text" 
        class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
        placeholder="https://www.youtube.com/watch?v=..."
      />
    </div>
    
    <button 
      @click="analyzeComments" 
      class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition mb-6"
      :disabled="isLoading"
    >
      {{ isLoading ? 'Analyzing...' : 'Analyze Comments' }}
    </button>
    
    <div v-if="error" class="p-4 mb-6 bg-red-100 border border-red-400 text-red-700 rounded-md">
      {{ error }}
    </div>
    
    <div v-if="result && result.analysis" class="results-container">
      <h2 class="text-xl font-semibold mb-4">Analysis Results</h2>
      
      <div v-if="result.analysis.note" class="p-4 mb-4 bg-yellow-100 border border-yellow-400 text-yellow-700 rounded-md">
        <strong>Note:</strong> {{ result.analysis.note }}
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Sentiment analysis results -->
        <div v-if="result.analysis?.sentiment" class="p-4 border rounded-md bg-white">
          <h3 class="font-medium text-lg mb-3">Sentiment Analysis</h3>
          <div class="grid grid-cols-3 gap-2 text-center">
            <div class="p-2 bg-green-100 rounded-md">
              <div class="text-2xl font-bold">{{ result.analysis.sentiment?.positive_count || 0 }}</div>
              <div>Positive</div>
            </div>
            <div class="p-2 bg-gray-100 rounded-md">
              <div class="text-2xl font-bold">{{ result.analysis.sentiment?.neutral_count || 0 }}</div>
              <div>Neutral</div>
            </div>
            <div class="p-2 bg-red-100 rounded-md">
              <div class="text-2xl font-bold">{{ result.analysis.sentiment?.negative_count || 0 }}</div>
              <div>Negative</div>
            </div>
          </div>
        </div>
        
        <!-- Toxicity analysis results -->
        <div v-if="result.analysis?.toxicity" class="p-4 border rounded-md bg-white">
          <h3 class="font-medium text-lg mb-3">Toxicity Analysis</h3>
          <div class="mb-3">
            <div class="text-2xl font-bold">{{ result.analysis.toxicity?.toxic_count || 0 }}</div>
            <div>Toxic Comments ({{ (result.analysis.toxicity?.toxic_percentage || 0).toFixed(1) }}%)</div>
          </div>
          
          <div v-if="result.analysis.toxicity?.toxic_types" class="text-sm">
            <h4 class="font-medium mb-1">Toxicity Types:</h4>
            <ul class="grid grid-cols-2 gap-1">
              <li v-for="(count, type) in result.analysis.toxicity.toxic_types" :key="type">
                {{ formatToxicityType(type) }}: {{ count }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <!-- LLM Analysis Results -->
      <div v-if="result.strategies || result.example_comments" class="mt-6 p-4 border rounded-md bg-white">
        <h3 v-if="result.strategies" class="font-medium text-lg mb-3">Response Strategies</h3>
        <div v-if="result.strategies" class="mb-4 whitespace-pre-line">{{ result.strategies }}</div>
        
        <h3 v-if="result.example_comments?.length" class="font-medium text-lg mb-3">Example Responses</h3>
        <div v-for="(example, index) in result.example_comments" :key="index" class="mb-4 p-3 bg-gray-50 rounded-md">
          <div class="mb-2 font-medium">Comment:</div>
          <div class="mb-3 pl-2 border-l-2 border-gray-300">{{ example?.comment }}</div>
          <div class="mb-2 font-medium">Suggested Response:</div>
          <div class="pl-2 border-l-2 border-indigo-300">{{ example?.response }}</div>
        </div>
      </div>
      
      <div class="mt-6">
        <p class="text-gray-700">Analyzed {{ result.total_comments }} comments</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Reactive state
const youtubeUrl = ref('')
const result = ref(null)
const error = ref(null)
const isLoading = ref(false)

// Format toxicity type names
const formatToxicityType = (type) => {
  const typeMap = {
    'toxic': 'General Toxicity',
    'severe_toxic': 'Severe Toxicity',
    'obscene': 'Obscene',
    'threat': 'Threat',
    'insult': 'Insult',
    'identity_hate': 'Identity Hate'
  }
  return typeMap[type] || type
}

// Analyze comments method
const analyzeComments = async () => {
  // Reset state
  error.value = null
  result.value = null
  
  // Validate URL
  if (!youtubeUrl.value) {
    error.value = 'Please enter a YouTube video URL'
    return
  }
  
  // Set loading state
  isLoading.value = true
  
  try {
    // Send request to backend API
    const response = await fetch('https://mindful-creator-production.up.railway.app/api/youtube/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        video_url: youtubeUrl.value
      })
    })
    
    // Parse response
    const data = await response.json()
    
    // Check API response status
    if (data.status === 'error') {
      error.value = data.message || 'Analysis failed, please try again later'
      return
    }
    
    // Check if analysis data exists
    if (!data.analysis) {
      error.value = 'The analysis data is missing from the response'
      console.warn('Missing analysis data in response:', data)
      return
    }
    
    // Save result
    result.value = data
    console.log('Analysis result:', data)
    
  } catch (err) {
    console.error('API request error:', err)
    error.value = 'Failed to connect to backend service, please ensure the backend is running'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.test-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.results-container {
  background-color: #f9fafb;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}
</style> 