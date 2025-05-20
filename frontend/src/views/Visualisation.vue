<template>
  <div class="visualisation-view">
    <h1 class="section-title">Digital Impact Analysis Dashboard</h1>
    <p class="section-subtitle">Explore how your usage patterns affect wellbeing based on real data</p>
    
    <div class="debug-panel" v-if="showDebug">
      <h3>Debug Panel</h3>
      <div class="debug-actions">
        <button @click="testApiConnection">Test API Connection</button>
        <button @click="testDbConnection">Test Database Connection</button>
        <button @click="testComprehensiveConnection">Comprehensive Test</button>
        <button @click="debugDataSchema">Debug Data Schema</button>
      </div>
      <div class="debug-results" v-if="debugResults">
        <h4>Results:</h4>
        <pre>{{ JSON.stringify(debugResults, null, 2) }}</pre>
      </div>
    </div>
    
    <!-- Start of Extractable Visualization Component -->
    <div class="visualization-component">
      <div class="tabs">
        <div class="tabs-slider" :style="sliderStyle"></div>
        <div v-for="(tab, index) in tabs" :key="index" class="tab" :class="{ active: currentTab === index }"
          @click="switchTab(index)" ref="tabElements">
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
            <button @click="fetchDataAndRender">Try Again</button>
          </div>
          <canvas v-else ref="chartCanvas" id="mainChart"></canvas>
        </div>
        <div class="insight-area">
          <h3 class="insight-heading">Key Insights</h3>
          <div v-for="(insight, i) in tabs[currentTab].insights" :key="i" class="insight-box">
            {{ insight }}
          </div>
        </div>
      </div>
    </div>
    <!-- End of Extractable Visualization Component -->
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, computed } from 'vue'
import Chart from 'chart.js/auto'
import axios from 'axios'

// State variables
const currentTab = ref(0)
const chartCanvas = ref(null)
const tabElements = ref([])
const sliderStyle = computed(() => {
  if (!tabElements.value || tabElements.value.length === 0 || !tabElements.value[currentTab.value]) {
    return { left: '0', width: '25%' }
  }
  const activeTab = tabElements.value[currentTab.value]
  const containerRect = activeTab.parentElement.getBoundingClientRect()
  const tabRect = activeTab.getBoundingClientRect()
  
  // For mobile (vertical layout)
  if (window.innerWidth <= 768) {
    return {
      top: `${activeTab.offsetTop}px`,
      left: '5px',
      width: 'calc(100% - 10px)',
      height: `${tabRect.height}px`,
      transform: 'translateY(0)',
    }
  }
  
  // For desktop (horizontal layout)
  return {
    left: `${activeTab.offsetLeft}px`,
    width: `${tabRect.width}px`,
    height: '80%',
    transform: 'translateY(-50%)',
  }
})
const tabs = [
  { 
    name: 'Screen Time and Emotional Wellbeing', 
    insights: [
      'Excessive screen time strongly correlates with increased negative emotions and decreased wellbeing.',
      'Users who limit daily screen time to under 2 hours report 30% better emotional health scores.',
      'Implementing regular digital detox periods shows significant improvement in mood regulation.'
    ]
  },
  {
    name: 'Digital Habits and Sleep Health', 
    insights: [
      'Late-night device usage disrupts melatonin production, resulting in 40% poorer sleep quality.',
      'Consistent bedtime device restrictions lead to faster sleep onset and deeper rest cycles.',
      'Blue light exposure within 2 hours of sleep delays REM sleep by an average of 45 minutes.'
    ]
  },
  {
    name: 'Engagement Metrics and Emotional Rewards', 
    insights: [
      'Quality over quantity: meaningful interactions yield 3x greater satisfaction than passive scrolling.',
      'Content creators who engage authentically report 60% less anxiety about performance metrics.',
      'Strategic posting schedules that avoid constant checking reduce stress hormones by 25%.'
    ]
  },
  {
    name: 'Screen Time and Anxiety', 
    insights: [
      'Each hour over 3 hours of daily usage correlates with a 27% increase in anxiety symptoms.',
      'Structured breaks every 90 minutes decrease stress markers and improve cognitive function.',
      'Mindfulness practices during technology use reduce reported anxiety by up to 35%.'
    ]
  }
]

// Chart instance reference
let chartInstance = null

// Debug variables
const showDebug = ref(true) // Set to false in production
const debugResults = ref(null)

// API configuration - update with your backend URL
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'https://api.tiezhu.org'
console.log('Using backend URL:', BACKEND_URL)

// Loading state
const isLoading = ref(true)
const error = ref(null)

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

const debugDataSchema = async () => {
  try {
    debugResults.value = { status: "Fetching data schema..." };
    isLoading.value = true;
    error.value = null;
    console.log(`Attempting to fetch schema from ${BACKEND_URL}/api/visualisation/debug-data-schema`);
    const response = await axios.get(`${BACKEND_URL}/api/visualisation/debug-data-schema`);
    debugResults.value = response.data;
    console.log('Data schema response:', response.data);

    let schemaError = false;
    let schemaErrorReason = "Debug schema response structure was unexpected."; // Default reason

    if (response.data && response.data.chart_data_shapes) {
      schemaError = false; // Assume okay unless an error is found
      for (const chartKey in response.data.chart_data_shapes) {
        if (response.data.chart_data_shapes[chartKey] && response.data.chart_data_shapes[chartKey].error) {
          schemaErrorReason = `Backend reported error for chart '${chartKey}' in debug schema: ${response.data.chart_data_shapes[chartKey].error}`;
          console.warn(`debugDataSchema: ${schemaErrorReason}`);
          schemaError = true;
          break;
        }
      }
    } else if (!response.data || Object.keys(response.data).length === 0) {
      schemaErrorReason = "Debug schema response was empty or malformed.";
      schemaError = true;
    } else if (!response.data.chart_data_shapes) {
      schemaErrorReason = "Debug schema response missing 'chart_data_shapes' key.";
      schemaError = true;
    }


    if (schemaError) {
      console.warn(`debugDataSchema: Schema error detected. Reason: ${schemaErrorReason}`);
      // We can set error.value here if we want debugDataSchema to impact the main error display
      // For now, just logging for the debug panel's own operation.
      // error.value = `Schema issue found by debugDataSchema: ${schemaErrorReason}`;
    }

  } catch (err) {
    console.error('Data schema fetch failed (debugDataSchema):', err);
    debugResults.value = {
      status: "error",
      message: `Failed to fetch data schema: ${err.message}`,
      error: err.toString()
    };
    error.value = "Could not load data schema from the backend (debug check).";
  } finally {
    isLoading.value = false;
    // REMOVED renderChart() call from here as it's not appropriate for debugDataSchema
    // if (!error.value) {
    //     await nextTick();
    //     renderChart(); 
    // }
  }
};

// Function to fetch data and render chart
const fetchDataAndRender = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    console.log(`fetchDataAndRender: Performing pre-flight schema check from ${BACKEND_URL}/api/visualisation/debug-data-schema`);
    const schemaResponse = await axios.get(`${BACKEND_URL}/api/visualisation/debug-data-schema`, { timeout: 20000 });
    console.log('fetchDataAndRender: Pre-flight schema check response:', schemaResponse.data);

    let schemaHasIssues = false;
    let schemaIssueReason = "Pre-flight schema check: Response missing 'chart_data_shapes' or was empty."; // Default reason

    if (schemaResponse.data && schemaResponse.data.chart_data_shapes && Object.keys(schemaResponse.data.chart_data_shapes).length > 0) {
      schemaHasIssues = false; // Assume okay unless an error is found
      for (const chartKey in schemaResponse.data.chart_data_shapes) {
        if (schemaResponse.data.chart_data_shapes[chartKey] && schemaResponse.data.chart_data_shapes[chartKey].error) {
          schemaIssueReason = `Pre-flight schema check: Backend reported error for chart '${chartKey}': ${schemaResponse.data.chart_data_shapes[chartKey].error}`;
          console.warn(`fetchDataAndRender: ${schemaIssueReason}`);
          schemaHasIssues = true;
          break;
        }
      }
      if (!schemaHasIssues) {
          console.log("fetchDataAndRender: Pre-flight schema check passed. No errors found in chart_data_shapes.");
      }
    } else {
      // This block means schemaResponse.data is null, or chart_data_shapes is missing/empty
      console.warn(`fetchDataAndRender: Pre-flight schema check failed. Reason: ${schemaIssueReason}`);
      schemaHasIssues = true; // Set to true if chart_data_shapes is not as expected
    }
    
    // Additional check for smmh_cleaned_columns to ensure they contain required fields
    if (schemaResponse.data && schemaResponse.data.smmh_cleaned_columns) {
      const requiredSmmhColumns = ['usage_time_group', 'q20_sleep_issues_scale', 'q12_easily_distracted_scale', 
                                   'q13_bothered_by_worries_scale', 'q14_difficulty_concentrating_scale'];
      const missingColumns = requiredSmmhColumns.filter(col => 
        !schemaResponse.data.smmh_cleaned_columns.includes(col));
      
      if (missingColumns.length > 0) {
        const missingMsg = `Missing required SMMH columns: ${missingColumns.join(', ')}`;
        console.warn(`fetchDataAndRender: ${missingMsg}`);
        if (missingColumns.includes('usage_time_group')) {
          schemaHasIssues = true;
          schemaIssueReason = `Critical column 'usage_time_group' is missing. Sleep quality and anxiety charts may not load.`;
        }
      }
    }
    
    if (schemaHasIssues) {
      console.warn(`fetchDataAndRender: Aborting main chart data fetch due to pre-flight schema issue. Reason: ${schemaIssueReason}`);
      error.value = `Schema validation failed before fetching chart data: ${schemaIssueReason}. Visualizations may not load.`;
      isLoading.value = false;
      return; // Exit if pre-flight check indicates issues
    }

    // If pre-flight schema check is okay, proceed to fetch actual data for the current tab
    const tabEndpoints = [
      '/api/visualisation/screen-time-emotions',
      '/api/visualisation/sleep-quality',
      '/api/visualisation/engagement',
      '/api/visualisation/anxiety'
    ];
    const endpoint = tabEndpoints[currentTab.value];
    console.log(`fetchDataAndRender: Fetching chart data from ${BACKEND_URL}${endpoint}`);
    
    // Special handling for sleep-quality and anxiety endpoints
    if (endpoint.includes('sleep-quality') || endpoint.includes('anxiety')) {
      console.log(`fetchDataAndRender: This endpoint (${endpoint}) requires SMMH data with usage_time_group column.`);
      // Check if we have the required columns from the schema check
      if (schemaResponse.data && schemaResponse.data.smmh_cleaned_columns) {
        if (!schemaResponse.data.smmh_cleaned_columns.includes('usage_time_group')) {
          throw new Error(`Required column 'usage_time_group' is missing for ${endpoint} endpoint.`);
        }
        
        // For sleep-quality endpoint
        if (endpoint.includes('sleep-quality') && !schemaResponse.data.smmh_cleaned_columns.includes('q20_sleep_issues_scale')) {
          throw new Error(`Required column 'q20_sleep_issues_scale' is missing for sleep-quality endpoint.`);
        }
        
        // For anxiety endpoint
        if (endpoint.includes('anxiety')) {
          const anxietyColumns = ['q12_easily_distracted_scale', 'q13_bothered_by_worries_scale', 'q14_difficulty_concentrating_scale'];
          const missingAnxietyColumns = anxietyColumns.filter(col => 
            !schemaResponse.data.smmh_cleaned_columns.includes(col));
          
          if (missingAnxietyColumns.length > 0) {
            throw new Error(`Required columns for anxiety endpoint are missing: ${missingAnxietyColumns.join(', ')}`);
          }
        }
      }
    }
    
    const response = await axios.get(`${BACKEND_URL}${endpoint}`, { timeout: 30000 });
    
    if (!response.data || Object.keys(response.data).length === 0 || !response.data.labels || !response.data.datasets) {
        console.error('fetchDataAndRender: Empty or invalid data returned from backend for chart endpoint:', endpoint, 'Data:', response.data);
        throw new Error('Empty or invalid data returned from backend for chart.');
    }
    
    console.log('fetchDataAndRender: Chart data received:', response.data);
    isLoading.value = false; 
    await nextTick();
    renderChart(response.data);

  } catch (err) {
    console.error('fetchDataAndRender: Failed to fetch chart data or schema:', err);
    
    // Provide more specific error messages based on the tab
    const tabSpecificErrors = [
      "Screen Time & Emotions: Check if train_cleaned table has the required columns.",
      "Sleep Quality: Check if smmh_cleaned table has 'usage_time_group' and 'q20_sleep_issues_scale' columns.",
      "Engagement: Check if train_cleaned table has engagement metrics columns.",
      "Anxiety: Check if smmh_cleaned table has anxiety scale columns (q12-q14)."
    ];
    
    let errorMsg = `Failed to load visualisation: ${err.message}.`;
    
    // Add tab-specific help
    if (currentTab.value >= 0 && currentTab.value < tabSpecificErrors.length) {
      errorMsg += ` ${tabSpecificErrors[currentTab.value]}`;
    }
    
    error.value = errorMsg;
    isLoading.value = false;
  }
};

const renderChart = (data) => {
  // Removed the isLoading check here, as the watcher should prevent premature calls.
  // if (isLoading.value) { 
  //   console.log("renderChart called while loading, deferring.");
  //   return;
  // }

  const canvasElement = chartCanvas.value; // Prefer ref directly
  if (!canvasElement) {
    console.error("renderChart: Canvas element ref 'chartCanvas' not found in DOM.");
    if (!error.value) {
        error.value = "Chart canvas could not be found. UI might be out of sync.";
    }
    return;
  }
  
  const ctx = canvasElement.getContext('2d');
  if (!ctx) {
    console.error('Failed to get 2D context from canvas element');
    error.value = "Could not initialize the chart. The browser might not support Canvas 2D.";
    return;
  }

  if (chartInstance) {
    chartInstance.destroy();
  }

  if (!data || Object.keys(data).length === 0 || !data.labels || !data.datasets) {
    console.warn('No valid data provided to renderChart. Displaying empty/error state.');
    // Clear the canvas by destroying any old instance (already done)
    // And ensure an error message is shown if not already.
    if (!error.value) { // Don't overwrite a more specific error
        error.value = "No data available to display for this visualization.";
    }
    // Optionally, you could draw a "No Data" message on the canvas itself
    // ctx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    // ctx.textAlign = 'center';
    // ctx.fillText('No data available', canvasElement.width / 2, canvasElement.height / 2);
    return; 
  }

  let chartType = 'bar'; 
  if (currentTab.value === 3 && data.datasets && data.datasets.length > 0 && data.datasets[0].type) {
    chartType = data.datasets[0].type; // Use type from data if available for line chart
  } else if (currentTab.value === 3) {
    chartType = 'line'; // Default to line for anxiety tab if not specified in data
  }
  // Potentially add more specific type detections from data if backend provides it
  // e.g. if (data.type) chartType = data.type;

  try {
    chartInstance = new Chart(ctx, {
      type: chartType,
      data: data,
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1500,
          easing: 'easeOutQuart',
          delay: (context) => context.dataIndex * 150
        },
        plugins: {
          title: {
            display: true,
            text: tabs[currentTab.value].name,
            font: {
              size: 20,
              weight: 'bold'
            },
            padding: {
              top: 10,
              bottom: 20
            },
            color: '#333'
          },
          legend: {
            labels: { color: '#333' }
          },
          tooltip: {
            backgroundColor: 'rgba(0,0,0,0.7)',
            titleColor: '#fff',
            bodyColor: '#fff',
            animation: {
              duration: 400
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            grace: '5%',
            ticks: { 
              color: '#666',
              count: 6,
              precision: 1
            },
            grid: { color: 'rgba(200, 200, 200, 0.2)' }
          },
          x: {
            ticks: { color: '#666' },
            grid: { color: 'rgba(200, 200, 200, 0.1)' }
          }
        }
      }
    });
    error.value = null; // Clear any previous error if rendering is successful
  } catch (e) {
    console.error("Error creating chart:", e);
    error.value = "An error occurred while creating the chart: " + e.message;
    // Optionally, display fallback if chart creation with real data fails
    if (!error.value) {
        console.log("Attempting to render fallback due to chart creation error with real data.");
        error.value = "An error occurred while creating the chart: " + e.message;
    }
  } finally {
    // isLoading.value should already be false if we reached here with data.
    // If data was bad, error.value would be set.
  }
};

// Switch tab function
const switchTab = (index) => {
  currentTab.value = index
  // When switching tab, always attempt to fetch new data or use fallback
  fetchDataAndRender()
}

// Update slider position when window resizes
const updateSliderPosition = () => {
  // Force recomputation of sliderStyle
  tabElements.value = tabElements.value.slice()
}

// Watch for changes in error or isLoading to potentially re-render or ensure canvas
watch([isLoading, error], async ([newLoading, newError], [oldLoading, oldError]) => {
  console.log(`Watcher: isLoading ${oldLoading}->${newLoading}, error '${oldError}'->'${newError}'`);
  
  // Case 1: Loading has just finished, and there is no error.
  if (oldLoading && !newLoading && !newError) {
    console.log("Watcher: Loading finished and no error. Render should ideally be handled by data fetcher after data is available.");
    // DO NOT call renderChart here without actual data. 
    // fetchDataAndRender is responsible for calling renderChart with data on its success path.
    // This block might be hit after initial setup (e.g. debugDataSchema finishes) before real data is fetched.
  }
  // Case 2: An error has just been set.
  else if (newError && (newError !== oldError)) { // Check if newError is truthy and different from oldError
    console.log("Watcher: An error has been set or changed. Clearing chart if it exists.");
    if (chartInstance) {
        chartInstance.destroy();
        chartInstance = null;
    }
  }
  // Case 3: An error was present and has just been cleared, and we are not currently loading.
  else if (oldError && !newError && !newLoading) {
    console.log("Watcher: Error was cleared, and not loading. Triggering data fetch and render.");
    fetchDataAndRender(); 
  }
});

onMounted(() => {
  // Add window resize listener for slider position
  window.addEventListener('resize', updateSliderPosition)
  
  // Initial comprehensive test to check backend status and data schema
  testComprehensiveConnection().then(() => {
    if (debugResults.value && debugResults.value.recommendation &&
        (debugResults.value.recommendation.includes("Database connection failed") ||
         debugResults.value.recommendation.includes("one or more required tables may have issues"))) {
      console.warn("Comprehensive test indicates issues. Charts may not load correctly.");
      error.value = debugResults.value.recommendation; 
      isLoading.value = false;
      // Watcher will handle this state change.
    } else if (debugResults.value && debugResults.value.chart_data_shapes) { 
        let schemaError = false;
        for (const chartKey in debugResults.value.chart_data_shapes) {
            if (debugResults.value.chart_data_shapes[chartKey] && debugResults.value.chart_data_shapes[chartKey].error) {
                console.warn(`Schema error for ${chartKey} from onMounted: ${debugResults.value.chart_data_shapes[chartKey].error}`);
                schemaError = true;
                break;
            }
        }
        if (schemaError) {
            console.warn("Schema issues found in comprehensive test. Charts may not load correctly.");
            error.value = "Data schema issues detected. Visualizations might be incomplete or unavailable.";
            isLoading.value = false;
            // Watcher will handle this state change.
        } else {
             console.log("Comprehensive test looks okay. Proceeding to fetch data for the initial tab.");
            fetchDataAndRender(); 
        }
    }
    else {
      console.log("Comprehensive test results unclear or passed. Proceeding to fetch data for initial tab.");
      fetchDataAndRender(); 
    }
  }).catch(err => {
      console.error("Error during initial comprehensive test in onMounted:", err);
      error.value = "Could not verify backend status. Visualizations may not load.";
      isLoading.value = false;
      // Watcher will handle this state change.
  });
  
  if (showDebug.value) {
      debugDataSchema();
  }
});
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
  margin-bottom: 2rem;
  background-color: #f2f2f2;
  border-radius: 30px;
  padding: 5px;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.tabs-slider {
  position: absolute;
  top: 50%;
  background-color: #e75a97;
  border-radius: 25px;
  z-index: 1;
  height: 80%;
  transition: all 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.tab {
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  color: #333;
  position: relative;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: normal;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  text-align: center;
  flex: 1;
  border-radius: 0;
  z-index: 2;
}

.tab:first-child {
  border-radius: 25px 0 0 25px;
}

.tab:last-child {
  border-radius: 0 25px 25px 0;
}

.tab.active {
  color: white;
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
  background: #ffe6f2;
  border-radius: 10px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 1rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0px 1px 5px rgba(231, 90, 151, 0.15);
  text-align: center;
  border-left: 4px solid #e75a97;
}

@media (max-width: 768px) {
  .tabs {
    flex-direction: column;
    align-items: stretch;
    border-radius: 15px;
    max-width: 320px;
  }
  
  .tabs-slider {
    top: 0;
    left: 5px !important;
    width: calc(100% - 10px) !important;
    border-radius: 10px;
    transform: none !important;
  }

  .tab {
    width: 100%;
    border-radius: 0;
  }

  .tab:first-child {
    border-radius: 10px 10px 0 0;
  }

  .tab:last-child {
    border-radius: 0 0 10px 10px;
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
