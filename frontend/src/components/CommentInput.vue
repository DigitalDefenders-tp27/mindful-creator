<template>
  <div class="comment-input-section mt-8 mb-12 p-6 border-2 border-black rounded-lg shadow-md bg-white max-w-3xl mx-auto">
    <h3 class="text-xl font-semibold mb-4 text-center text-gray-700">Paste Your Comment Here</h3>
    <textarea
      v-model="commentText"
      rows="5"
      class="w-full p-3 border border-gray-400 rounded-md focus:ring-2 focus:ring-indigo-500 focus:outline-none transition duration-150 ease-in-out"
      placeholder="Paste the comment you copied here..."
    ></textarea>
    <div class="mt-4 flex justify-end">
      <button
        @click="submitComment"
        :disabled="isLoading || !commentText.trim()"
        class="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition duration-150 ease-in-out font-semibold"
      >
        <span v-if="isLoading">Analyzing...</span>
        <span v-else>Analyze Comment</span>
      </button>
    </div>
    <p v-if="error" class="text-red-600 mt-3 text-sm">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
// Consider using Pinia for state management:
// import { useAnalysisStore } from '@/stores/analysisStore'; // Example store path

import { useAnalysisStore } from '@/stores/analysisStore'
const analysisStore = useAnalysisStore()

const commentText = ref('');
const isLoading = ref(false);
const error = ref(null);
const router = useRouter();
// const analysisStore = useAnalysisStore(); // Example store instance

// Define the backend API URL - Use environment variables for production
const API_URL = import.meta.env.VITE_API_URL || 'https://gleaming-celebration.railway.internal/api/analyze_comment';

const submitComment = async () => {
  if (!commentText.value.trim()) {
    error.value = 'Please paste a comment.';
    return;
  }

  isLoading.value = true;
  error.value = null;
  console.log(`Submitting comment to ${API_URL}`);

  try {
    const response = await axios.post(API_URL, {
      comment: commentText.value,
    });

    console.log('API Response Received:', response.data);

    // Using sessionStorage to pass data (Simpler for now, but Pinia is recommended)
    analysisStore.set(response.data)
    router.push({ name: 'comment-response-scripts' }) // Navigate to results page

  } catch (err) {
    console.error('API Error:', err);
    if (err.response) {
      error.value = `Error: ${err.response.data?.error || 'Failed to analyze comment.'} (Status: ${err.response.status})`;
    } else if (err.request) {
      error.value = 'Error: Could not connect to the server. Is the backend running and CORS configured?';
    } else {
      error.value = `Error: ${err.message}`;
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Add specific styles if Tailwind isn't sufficient */
</style>