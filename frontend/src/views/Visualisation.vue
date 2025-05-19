<template>
  <div class="visualisation-view">
    <h1 class="section-title">Digital Impact Analysis Dashboard</h1>
    <p class="section-subtitle">Explore how your usage patterns affect wellbeing based on real data</p>
    
    <div class="tabs">
      <div v-for="(tab, index) in tabs" :key="index" class="tab" :class="{ active: currentTab === index }"
        @click="switchTab(index)">
        <span v-if="index === 0">
          <span>Screen Time</span>
          <span>& Emotions</span>
        </span>
        <span v-else-if="index === 1">
          <span>Digital Habits</span>
          <span>& Sleep</span>
        </span>
        <span v-else-if="index === 2">
          <span>Engagement</span>
          <span>& Rewards</span>
        </span>
        <span v-else-if="index === 3">
          <span>Screen Time</span>
          <span>& Anxiety</span>
        </span>
      </div>
    </div>

    <div class="visualisation-container">
      <div class="chart-area">
        <div v-if="isLoading" class="loading-indicator">
          <span class="loading-spinner"></span>
          <p>Loading data...</p>
        </div>
        <div v-else-if="error" class="error-message">
          <p>{{ error }}</p>
          <button @click="renderChart">Try Again</button>
        </div>
        <canvas v-else id="mainChart"></canvas>
      </div>
      <div class="insight-area">
        <h3 class="insight-heading">Key Insights</h3>
        <div v-for="(insight, i) in tabs[currentTab].insights" :key="i" class="insight-box">
          {{ insight }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

// State variables
const currentTab = ref(0)
const tabs = [
  { 
    name: 'Screen Time and Emotional Wellbeing', 
    insights: [
      'Increased screen time is associated with more negative emotions such as anxiety and sadness.',
      'Maintaining lower daily screen time correlates with better emotional wellbeing.',
      'Balanced digital habits foster more positive and neutral emotional states.'
    ]
  },
  {
    name: 'Digital Habits and Sleep Health', 
    insights: [
      'More than 3 hours of daily social media use is linked with sleep disturbances.',
      'Sleep issues worsen significantly when daily usage exceeds 4 hours.',
      'Reducing evening screen time can improve sleep quality and mental health.'
    ]
  },
  {
    name: 'Engagement Metrics and Emotional Rewards', 
    insights: [
      'Moderate posting and interaction (likes, comments) are positively linked with emotional wellbeing.',
      'Creators focusing on authentic engagement rather than maximizing metrics report higher satisfaction.',
      'A balanced posting schedule correlates with more positive emotional outcomes.'
    ]
  },
  {
    name: 'Screen Time and Anxiety', 
    insights: [
      'Higher daily screen time is associated with increased anxiety levels.',
      'Taking regular digital breaks correlates with reduced anxiety symptoms.',
      'Mindful technology use can help mitigate negative impacts on mental wellbeing.'
    ]
  }
]

// Chart instance reference
let chartInstance = null

// API configuration - update with your backend URL
const BACKEND_URL = 'https://gleaming-celebration-production-66cb.up.railway.app'

// Loading state
const isLoading = ref(true)
const error = ref(null)

// Function to fetch data from backend API
const fetchChartData = async (endpoint) => {
  try {
    isLoading.value = true
    error.value = null
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/${endpoint}`)
    return response.data
  } catch (err) {
    console.error(`Error fetching data from ${endpoint}:`, err)
    error.value = `Failed to load data: ${err.message}`
    return null
  } finally {
    isLoading.value = false
  }
}

// Switch tab and render the appropriate chart
const switchTab = async (index) => {
  currentTab.value = index
  await renderChart()
}

// Render chart based on current tab
const renderChart = async () => {
  const ctx = document.getElementById('mainChart')
  if (!ctx) return
  
  if (chartInstance) {
    chartInstance.destroy()
  }
  
  let chartData
  let chartType
  let chartOptions
  
  try {
    isLoading.value = true
    
    // Choose which endpoint to call based on the current tab
    switch(currentTab.value) {
      case 0: // Screen Time and Emotions
        chartData = await fetchChartData('screen-time-emotions')
        chartType = 'bar'
        chartOptions = {
          responsive: true,
          plugins: { title: { display: false } },
          scales: {
            x: {
              stacked: true,
              title: { display: true, text: 'Daily Screen Time (hours)' }
            },
            y: {
              stacked: true,
              title: { display: true, text: 'Percentage of Users (%)' }
            }
          }
        }
        break
        
      case 1: // Digital Habits and Sleep
        chartData = await fetchChartData('sleep-quality')
        chartType = 'line'
        chartOptions = {
          responsive: true,
          plugins: { title: { display: false } },
          scales: {
            x: { 
              title: { display: true, text: 'Daily Social Media Usage Time' } 
            },
            y: {
              min: 1,
              max: 5,
              title: { display: true, text: 'Sleep Problem Frequency (1-5)' }
            }
          }
        }
        break
        
      case 2: // Engagement Metrics
        chartData = await fetchChartData('engagement')
        chartType = 'bar'
        chartOptions = {
          responsive: true,
          plugins: { title: { display: false } },
          scales: {
            x: {
              title: { display: true, text: 'Daily Screen Time (hours)' }
            },
            y: {
              title: { display: true, text: 'Engagement Score' }
            }
          }
        }
        break
        
      case 3: // Screen Time and Anxiety
        chartData = await fetchChartData('anxiety')
        chartType = 'line'
        chartOptions = {
          responsive: true,
          plugins: { title: { display: false } },
          scales: {
            x: {
              title: { display: true, text: 'Daily Screen Time' }
            },
            y: {
              min: 1,
              max: 5,
              title: { display: true, text: 'Average Anxiety Level (1-5)' }
            }
          }
        }
        break
    }
    
    if (chartData) {
      chartInstance = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: chartOptions
      })
    }
  } catch (err) {
    console.error('Error rendering chart:', err)
    error.value = `Failed to render chart: ${err.message}`
  } finally {
    isLoading.value = false
  }
}

// Initialize chart on component mount
onMounted(async () => {
  await renderChart()
})
</script>

<style scoped>
.visualisation-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fffcf5;
}

.section-title {
  font-size: 2.5rem;
  color: #000;
  text-align: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.section-subtitle {
  font-size: 1.2rem;
  color: #333;
  text-align: center;
  margin-bottom: 3rem;
  line-height: 1.5;
  white-space: normal;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.tab {
  padding: 0.5rem 1.5rem;
  cursor: pointer;
  color: white;
  position: relative;
  background-color: #e75a97;
  border-radius: 20px;
  font-weight: 500;
  margin: 0 0.5rem;
  transition: all 0.3s ease;
  white-space: normal;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  text-align: center;
}

.tab.active {
  background-color: #d4407f;
  transform: translateY(-3px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.visualisation-container {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-wrap: wrap;
  margin-top: 30px;
}

.chart-area {
  flex: 1;
  min-width: 500px;
  max-width: 700px;
  height: 400px;
  padding: 10px;
}

.chart-area canvas {
  width: 100% !important;
  height: 100% !important;
}

.insight-area {
  flex: 0.7;
  min-width: 320px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.insight-heading {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  font-weight: 600;
  text-align: center;
}

.insight-box {
  background: #fff8e1;
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 1rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.05);
  text-align: center;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    align-items: center;
  }

  .tab {
    width: 100%;
    max-width: 320px;
  }

  .chart-area {
    min-width: 100%;
  }

  .insight-area {
    min-width: 100%;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.8rem;
  }

  .section-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }
}

/* Add loading spinner and error message styles */
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.loading-spinner {
  display: inline-block;
  width: 40px;
  height: 40px;
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: #e75a97;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #d32f2f;
  text-align: center;
  padding: 20px;
}

.error-message button {
  margin-top: 15px;
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.error-message button:hover {
  background-color: #c64482;
}
</style>
