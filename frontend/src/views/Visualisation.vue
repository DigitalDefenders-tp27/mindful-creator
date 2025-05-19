<template>
  <div class="visualisation-view">
    <h1 class="section-title">Digital Impact Analysis Dashboard</h1>
    <p class="section-subtitle">Explore how your usage patterns affect wellbeing based on real data</p>
    
    <div v-if="usingFallbackData" class="fallback-notice">
      Note: Showing sample data visualization. Database connection unavailable.
    </div>
    
    <div class="debug-panel" v-if="showDebug">
      <h3>Debug Panel</h3>
      <div class="debug-actions">
        <button @click="testApiConnection">Test API Connection</button>
        <button @click="testDbConnection">Test Database Connection</button>
        <button @click="testComprehensiveConnection">Comprehensive Test</button>
      </div>
      <div class="debug-results" v-if="debugResults">
        <h4>Results:</h4>
        <pre>{{ JSON.stringify(debugResults, null, 2) }}</pre>
      </div>
    </div>
    
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

// Debug variables
const showDebug = ref(true) // Set to false in production
const debugResults = ref(null)

// API configuration - update with your backend URL
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'https://gleaming-celebration-production-66cb.up.railway.app'
console.log('Using backend URL:', BACKEND_URL)

// Loading state
const isLoading = ref(true)
const error = ref(null)

// Add a reactive variable to track if we're using fallback data
const usingFallbackData = ref(false)

// Testing functions
const testApiConnection = async () => {
  try {
    debugResults.value = { status: "Testing API connection..." }
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/test`)
    debugResults.value = response.data
    console.log('API test result:', response.data)
  } catch (err) {
    console.error('API test failed:', err)
    debugResults.value = { 
      status: "error", 
      message: `Failed to connect to API: ${err.message}`,
      error: err.toString(),
      config: err.config ? {
        url: err.config.url,
        method: err.config.method,
        headers: err.config.headers
      } : 'No config available'
    }
  }
}

const testDbConnection = async () => {
  try {
    debugResults.value = { status: "Testing database connection..." }
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/db-test`)
    debugResults.value = response.data
    console.log('Database test result:', response.data)
  } catch (err) {
    console.error('Database test failed:', err)
    debugResults.value = { 
      status: "error", 
      message: `Failed to test database: ${err.message}`,
      error: err.toString() 
    }
  }
}

const testComprehensiveConnection = async () => {
  try {
    debugResults.value = { status: "Running comprehensive connection test..." }
    console.log(`Attempting to connect to ${BACKEND_URL}/api/visualisation/connection-test`)
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/connection-test`, {
      timeout: 60000, // 60 second timeout for this comprehensive test
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    debugResults.value = response.data
    console.log('Comprehensive test result:', response.data)
    
    // Add timestamp to show when test was run
    debugResults.value.testRunAt = new Date().toISOString();
    
    // Add recommendations based on results
    if (response.data.db_connection && response.data.db_connection.connection === "successful") {
      // Check if required tables have data
      const trainTableOk = response.data.table_tests && 
                         response.data.table_tests.train_cleaned && 
                         response.data.table_tests.train_cleaned.status === "success";
      const smmhTableOk = response.data.table_tests && 
                        response.data.table_tests.smmh_cleaned && 
                        response.data.table_tests.smmh_cleaned.status === "success";
      
      if (trainTableOk && smmhTableOk) {
        debugResults.value.recommendation = "Database connection and tables look good. If visualizations aren't loading, the issue might be with data processing or rendering.";
      } else {
        debugResults.value.recommendation = "Database connection succeeded but one or more required tables may have issues. Check the table_tests section for details.";
      }
    } else {
      debugResults.value.recommendation = "Database connection failed. The Railway PostgreSQL database may be experiencing issues or timeouts. Try again later or contact your administrator.";
    }
  } catch (err) {
    console.error('Comprehensive test failed:', err)
    debugResults.value = { 
      status: "error", 
      message: `Failed to run comprehensive test: ${err.message}`,
      error: err.toString(),
      errorDetails: err.response ? 
        {
          status: err.response.status,
          statusText: err.response.statusText,
          data: err.response.data
        } : "No response details available",
      config: err.config ? {
        url: err.config.url,
        method: err.config.method,
        timeout: err.config.timeout
      } : 'No config available',
      recommendation: "API connection failed. Check if the backend server is running and accessible."
    }
  }
}

// Function to fetch data from backend API
const fetchChartData = async (endpoint) => {
  try {
    console.log(`Attempting to fetch data from ${BACKEND_URL}/api/visualisation/${endpoint}`)
    isLoading.value = true
    error.value = null
    
    // Use a longer timeout to match backend settings
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/${endpoint}`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      timeout: 30000 // 30 second timeout (increased from 5 seconds)
    })
    
    console.log(`Data received from ${endpoint}:`, response.data)
    return response.data
  } catch (err) {
    console.error(`Error fetching data from ${endpoint}:`, err)
    // Show error to user when fetch fails
    error.value = `Failed to load data: ${err.message}. Please try again later.`
    usingFallbackData.value = false
    throw err
  } finally {
    isLoading.value = false
  }
}

// Switch tab and render the appropriate chart
const switchTab = async (index) => {
  currentTab.value = index
  // Reset the fallback flag when switching tabs
  usingFallbackData.value = false
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
    error.value = null
    
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
    error.value = `Failed to load visualization data: ${err.message}. The database might be temporarily unavailable. Please try the connection test above or try again later.`
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

.debug-panel {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 5px;
  padding: 15px;
  margin-bottom: 20px;
}

.debug-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.debug-actions button {
  background-color: #2196f3;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.debug-actions button:hover {
  background-color: #0b7dda;
}

.debug-results {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  overflow: auto;
  max-height: 300px;
}

.debug-results pre {
  margin: 0;
  white-space: pre-wrap;
}

.fallback-notice {
  background-color: #fff3cd;
  color: #856404;
  padding: 10px 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  text-align: center;
  font-weight: 500;
  border-left: 4px solid #ffeeba;
}
</style>
