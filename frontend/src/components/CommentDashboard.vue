<template>
  <div class="comment-dashboard">
    <h2>Comment Type Overview</h2>
    <canvas id="commentChart"></canvas>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import Chart from 'chart.js/auto'

const chartData = {
  labels: ['Accusatory', 'Emotional', 'Misunderstanding', 'Attacking', 'Constructive'],
  datasets: [{
    label: 'Comment Distribution',
    data: [40, 25, 15, 10, 10],  // placeholder percentages
    backgroundColor: ['#ff4c4c', '#ffa64d', '#ffc94d', '#66cc99', '#66d9ef']
  }]
}

onMounted(() => {
  const ctx = document.getElementById('commentChart')
  new Chart(ctx, {
    type: 'doughnut',
    data: chartData,
    options: {
      responsive: true
    }
  })
})
</script>

<style scoped>
.comment-dashboard {
  max-width: 500px;
  margin: auto;
  padding: 2rem;
}
</style>
