<template>
  <div class="comment-dashboard">
    <h2>Comment Type Overview</h2>

    <canvas id="commentChart"></canvas>

    <h3 class="mt-6">Fetched Comments</h3>
    <ul>
      <li v-for="comment in comments" :key="comment.id">{{ comment.comment_text }}</li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios';

const chartData = {
  labels: ['Accusatory', 'Emotional', 'Misunderstanding', 'Attacking', 'Constructive'],
  datasets: [
    {
      label: 'Comment Distribution',
      data: [40, 25, 15, 10, 10],
      backgroundColor: [
        '#ff4c4c', '#ffa64d', '#ffc94d', '#66cc99', '#66d9ef'
      ]
    }
  ]
}


import { ref } from 'vue'

const comments = ref([])

const fetchComments = async (videoId) => {
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL || 'https://api.tiezhu.org'}/api/comments/${videoId}`)
    const data = await response.json()
    comments.value = data
  } catch (error) {
    console.error('Error fetching comments:', error)
  }
}


onMounted(() => {
  fetchComments(1) // Replace 1 with actual video ID if needed

  const ctx = document.getElementById('commentChart')
  new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom' },
        title: { display: true, text: 'Comment Types (Static Example)' }
      }
    }
  })
})

</script>

<style scoped>
.comment-dashboard {
  max-width: 600px;
  margin: auto;
  padding: 2rem;
  text-align: center;
}
</style>
