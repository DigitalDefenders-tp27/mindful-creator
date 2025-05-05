<template>
    <div class="critical-response-view">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="hero-content">
          <div class="slogan">
            <div class="title-group">
              <h1>Critical Response</h1>
              <h2>Navigating Feedback with Resilience</h2>
            </div>
            <p class="subtitle">Transform challenging interactions into growth opportunities</p>
          </div>
          <div class="decorative-elements">
            <!-- 右上角第一排 / Top Row Right -->
            <div class="top-row">
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Feeling Box -->
      <div class="feeling-box">
        <div class="bell-container">
          <img :src="bell" alt="Bell" class="bell-icon" />
        </div>
        <h2>HOW ARE YOU FEELING NOW?</h2>
        <div class="emotions">
          <div class="emoji-option" v-for="(emoji, index) in emojis" :key="index">
            <img
              :src="emoji.src"
              :alt="emoji.alt"
              class="emoji-img"
              :class="{ selected: selectedEmotion === emoji.alt }"
              @click="handleDotClick(emoji.alt)"
            />
          </div>
        </div>
      </div>

      <!-- Emotional Check-in Pop-up -->
      <div v-if="showCheckIn" class="overlay">
        <div class="popup">
          <h2>Would you like to take a moment to relax before continuing?</h2>
          <div class="buttons">
            <button @click="goToRelaxation">Yes, let me try</button>
            <button @click="closePopup">No, thanks. I'm ok to continue</button>
          </div>
        </div>
      </div>

      <!-- Comparison Section -->
      <div class="comparison">
        <div class="comparison-header">
          <div class="col">Constructive Criticism<br /><span>(Helpful Feedback 👍)</span></div>
          <div class="col label">What's the goal?</div>
          <div class="col">Cyberbullying<br /><span>(Harmful Attacks 🚨)</span></div>
        </div>

        <div class="comparison-row" v-for="(label, i) in labels" :key="i">
          <div class="cell left">{{ leftCol[i] }}</div>
          <div class="cell label">{{ label }}</div>
          <div class="cell right">{{ rightCol[i] }}</div>
        </div>
      </div>

      <!-- Seek Help Link -->
      <div class="seek-help">
        <RippleButton
          class="help-button"
          rippleColor="rgba(255, 255, 255, 0.6)"
          @click="handleSeekHelp"
        >
          SEEK HELP
        </RippleButton>
      </div>

      <!-- Check Your Comment Section -->
      <div class="comment-section-checker">
        <h2 class="section-title">🔍 Check Your Comment Section</h2>
        
        <p class="section-description">
          Not sure if your Youtube comment section is a space for healthy
          discussion or if there's negativity creeping in?
        </p>
        
        <div class="cards-container">
          <div class="process-card">
            <div class="card-number">1</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/video.png" alt="Smartphone icon" class="card-icon">
              <p class="card-text">Open your Youtube video.</p>
            </div>
          </div>
          
          <div class="process-card">
            <div class="card-number">2</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/copy.png" alt="Copy icon" class="card-icon">
              <p class="card-text">Copy the URL.</p>
            </div>
          </div>
          
          <div class="process-card">
            <div class="card-number">3</div>
            <div class="card-content">
              <img src="/src/assets/icons/elements/paste.png" alt="Link icon" class="card-icon">
              <p class="card-text">Paste it into the box below.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Comments Response Scripts Section -->
      <div class="youtube-analysis-section">
        <div class="analysis-container mt-8 mb-12 p-6 border-2 border-black rounded-lg shadow-md bg-white mx-auto">
          <h3 class="section-title">YouTube Comment Analysis</h3>
          <div class="input-group">
            <input 
              v-model="youtubeUrl" 
              type="text" 
              class="youtube-input"
              placeholder="Enter YouTube video URL (https://www.youtube.com/watch?v=...)"
            />
            <button 
              @click="analyzeYoutubeComments" 
              class="analyze-button"
              :disabled="isLoading"
            >
              <span v-if="isLoading" class="loading-spinner"></span>
              {{ isLoading ? 'Analysing...' : 'Analyse Comments' }}
            </button>
          </div>
          <p v-if="analysisError" class="error-message">
            <strong>Strewth!</strong> {{ analysisError }}
            <button @click="retryAnalysis" class="retry-button">Give it another go</button>
          </p>
          <p v-if="isLoading" class="loading-message">
            <span class="loading-spinner"></span>
            Grabbing and checking those comments. Hang in there, mate...
          </p>
        </div>
      </div>
      
      <!-- Analysis Results Modal -->
      <div v-if="showResultsModal" class="modal-overlay" @click="closeModal">
        <div class="analysis-modal" @click.stop>
          <div class="modal-header">
            <h2>YouTube Comments Analysis Results</h2>
            <button class="close-button" @click="closeModal">×</button>
          </div>
          
          <div class="modal-content">
            <!-- Video Info -->
            <div class="video-info-section section-divider">
              <p><strong>Video URL:</strong> {{ youtubeUrl }}</p>
              <p><strong>Comments Analysed:</strong> {{ analysisResult.total_comments || 0 }}</p>
            </div>
            
            <!-- WebSocket Error Warning -->
            <div v-if="analysisResult.wsError" class="websocket-warning section-divider">
              <div class="warning-icon">⚠️</div>
              <div class="warning-content">
                <h4>Fair Dinkum Results (Not Perfect)</h4>
                <p>The sentiment and toxicity analysis service is having a bit of a wobbly, but we've still managed to work out some helpful response strategies and examples based on your video comments.</p>
                <p class="warning-note">Note: The sentiment and toxicity scores are our best guess.</p>
              </div>
            </div>
            
            <!-- Debug Information (Add after video info section) -->
            <div class="debug-info section-divider">
              <p class="note-message"><strong>Debug Info:</strong></p>
              <details>
                <summary>Response Data Structure</summary>
                <pre class="debug-data">{{ JSON.stringify(analysisResult, null, 2) }}</pre>
              </details>
            </div>
            
            <!-- Results Grid -->
            <div class="results-grid section-divider">
              <!-- Sentiment Analysis Results -->
              <div class="result-card">
                <h3>Sentiment Analysis</h3>
                <div class="sentiment-stats">
                  <div class="stat-box positive">
                    <div class="stat-number">{{ analysisResult?.analysis?.sentiment?.positive_count || 0 }}</div>
                    <div class="stat-label">Positive</div>
                  </div>
                  <div class="stat-box neutral">
                    <div class="stat-number">{{ analysisResult?.analysis?.sentiment?.neutral_count || 0 }}</div>
                    <div class="stat-label">Neutral</div>
                  </div>
                  <div class="stat-box negative">
                    <div class="stat-number">{{ analysisResult?.analysis?.sentiment?.negative_count || 0 }}</div>
                    <div class="stat-label">Negative</div>
                  </div>
                </div>
              </div>
              
              <!-- Total Toxic Comments Card -->
              <div class="result-card">
                <h3>Toxic Comments Overview</h3>
                <div class="toxic-count">
                  <div class="stat-number">{{ analysisResult?.analysis?.toxicity?.toxic_count || 0 }}</div>
                  <div class="stat-label">Total Toxic Comments ({{ (analysisResult?.analysis?.toxicity?.toxic_percentage || 0).toFixed(1) }}%)</div>
                </div>
                <p class="toxic-explanation">These are comments that may require moderation or careful consideration when responding.</p>
              </div>
            </div>
            
            <!-- Donut Charts Section -->
            <div class="charts-section section-divider" v-if="analysisResult?.analysis?.toxicity?.toxic_types">
              <h3>Toxicity Breakdown</h3>
              <p class="toxicity-subtitle">Breakdown of the {{ analysisResult?.analysis?.toxicity?.toxic_count || 0 }} toxic comments by category</p>
              <div class="donut-charts">
                <div v-for="(count, type) in analysisResult?.analysis?.toxicity?.toxic_types" :key="type" class="donut-item">
                  <HalfDonutChart 
                    :percentage="calculatePercentage(count, analysisResult?.analysis?.toxicity?.toxic_count)" 
                    :color="getToxicityColor(formatToxicityType(type).toLowerCase())" 
                  />
                  <p class="donut-label">{{ formatToxicityType(type) }}</p>
                  <p class="donut-percent">{{ count }} ({{ calculatePercentage(count, analysisResult?.analysis?.toxicity?.toxic_count) }}%)</p>
                </div>
              </div>
            </div>
            
            <!-- Strategies Section (修改) -->
            <div class="strategies-section section-divider" v-if="analysisResult?.strategies">
              <h3>Response Strategies</h3>
              <div class="strategy-content" v-html="formatStrategies(analysisResult.strategies)"></div>
            </div>
            
            <!-- Example Comments Section (修改) -->
            <div class="examples-section section-divider" v-if="analysisResult?.example_comments && analysisResult.example_comments.length > 0">
              <h3>Example Responses</h3>
              <div class="example-cards">
                <div v-for="(example, index) in analysisResult.example_comments" :key="index" class="example-card">
                  <div class="example-comment">
                    <h4>Original Comment:</h4>
                    <p>{{ example.comment }}</p>
                  </div>
                  <div class="example-response">
                    <h4>Suggested Response:</h4>
                    <p>{{ example.response }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Recommendations Section -->
            <!-- <div class="recommendations-section">
              <h3>Recommendations</h3>
              <p>Based on the analysis of your YouTube comments, we recommend:</p>
              <ul class="recommendations-list">
                <li>Review comments with high toxicity scores to moderate as needed</li>
                <li>Engage positively with constructive feedback</li>
                <li>Consider addressing common concerns in your next video</li>
                <li>Set healthy boundaries with toxic commenters</li>
              </ul>
            </div> -->
          </div>
        </div>
      </div>
    </div>
  </template>

  <script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import InteractiveHoverButton from '@/components/ui/interactive-hover-button.vue'
  import RippleButton from '@/components/ui/ripple-button.vue'
  import HalfDonutChart from '@/components/ui/HalfDonutChart.vue'
  import CommentInput from '@/components/CommentInput.vue'

  import { useAnalysisStore } from '@/stores/analysisStore'
  const analysisStore = useAnalysisStore()
  analysisStore.$reset()

  import bell from '../assets/emojis/bell.png'
  import happy from '../assets/emojis/Happy.png'
  import peace from '../assets/emojis/Peace.png'
  import angry from '../assets/emojis/Angry.png'
  import sad from '../assets/emojis/Sad.png'
  import mda from '../assets/emojis/Mad.png'

  const router = useRouter()
  const showCheckIn = ref(false)
  const selectedEmotion = ref(null)

  // YouTube analysis variables
  const youtubeUrl = ref('')
  const isLoading = ref(false)
  const analysisError = ref(null)
  const showResultsModal = ref(false)
  const analysisResult = ref({})

  // Format toxicity type names to more readable format
  const formatToxicityType = (type) => {
    // 处理后端返回的可能格式（首字母大写或全小写）
    const typeMap = {
      // 后端返回格式
      'Toxic': 'General Toxicity',
      'Severe Toxic': 'Severe Toxicity',
      'Obscene': 'Obscene',
      'Threat': 'Threat',
      'Insult': 'Insult',
      'Identity Hate': 'Identity Hate',
      // 前端原有格式（向后兼容）
      'toxic': 'General Toxicity',
      'severe_toxic': 'Severe Toxicity',
      'obscene': 'Obscene',
      'threat': 'Threat',
      'insult': 'Insult',
      'identity_hate': 'Identity Hate'
    }
    return typeMap[type] || type
  }
  
  // Format strategies with HTML
  const formatStrategies = (strategies) => {
    if (!strategies) return '';
    
    // Replace line breaks with <br> and convert bullet points to HTML
    return strategies
      .replace(/\n/g, '<br>')
      .replace(/•/g, '&bull;')
      .replace(/- /g, '&bull; ');
  }
  
  // Calculate percentage for toxicity types
  const calculatePercentage = (count, total) => {
    if (!total || total === 0) return 0
    return Math.round((count / total) * 100)
  }
  
  // Get color for toxicity type
  const getToxicityColor = (type) => {
    const colorMap = {
      'general toxicity': '#EF5350',        // Red
      'severe toxicity': '#D32F2F',         // Dark Red
      'obscene': '#FF7043',                 // Orange
      'threat': '#AB47BC',                  // Purple
      'insult': '#FFA726',                  // Amber
      'identity hate': '#7E57C2'            // Deep Purple
    }
    return colorMap[type.toLowerCase()] || '#888888'
  }

  // Analyse YouTube comments
  const analyzeYoutubeComments = async () => {
    // Reset state
    analysisError.value = null
    
    // Validate URL
    if (!youtubeUrl.value) {
      analysisError.value = 'Please enter a YouTube video URL, mate'
      return
    }
    
    // Validate URL format
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})(\S*)?$/
    if (!youtubeRegex.test(youtubeUrl.value)) {
      analysisError.value = 'Please enter a valid YouTube URL, that one\'s not right'
      return
    }
    
    // Set loading state
    isLoading.value = true
    
    // API URL options - will try alternatives if primary fails
    const apiUrls = [
      'https://api.tiezhu.org/api/youtube/analyse',  // Primary URL
    ]
    let primaryApiUrl = apiUrls[0]
    
    try {
      console.log('Starting YouTube analysis process...')
      console.log('Using API URL:', primaryApiUrl)
      
      // Create AbortController for the request with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 120000) // 2 minute timeout
      
      // First make a simple GET request to check if the server is responding at all
      let serverAvailable = false
      try {
        console.log('Performing health check...')
        const healthCheck = await fetch('https://api.tiezhu.org/api/health', {
          method: 'GET',
          signal: AbortSignal.timeout(5000)
        })
        
        console.log('Basic connectivity check response:', healthCheck.status, healthCheck.statusText)
        serverAvailable = true
      } catch (healthError) {
        console.warn('Server health check failed:', healthError.message)
        // Continue anyway - will try the actual request
      }
      
      console.log('Sending API request to:', primaryApiUrl)
      
      let response
      try {
        // Send request to backend API with improved error handling
        console.log('Sending POST request to API endpoint...')
        
        // Try multiple URL formats if needed
        let fetchError = null
        for (let i = 0; i < apiUrls.length; i++) {
          try {
            console.log(`Attempt ${i+1}/${apiUrls.length} with URL: ${apiUrls[i].replace('/analyse', '/analyse_full')}`)
            
            // 发送请求到API端点
            response = await fetch(apiUrls[i].replace('/analyse', '/analyse_full'), {
              method: 'POST',
              mode: 'cors',
              credentials: 'omit',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify({
                youtube_url: youtubeUrl.value,
                limit: 100
              }),
              signal: controller.signal
            })
            
            console.log(`Response from attempt ${i+1}:`, response.status, response.statusText)
            
            // If we got a successful response, break the loop
            if (response.ok) {
              console.log('Successful response received')
              break
            }
          } catch (error) {
            console.warn(`Attempt ${i+1} failed:`, error.message)
            fetchError = error
            // Continue to next URL if available
          }
        }
        
        // If we tried all URLs and still have no valid response
        if (!response || !response.ok) {
          throw fetchError || new Error('All API endpoints failed')
        }
      } catch (fetchError) {
        console.error('Fetch operation failed:', fetchError)
        
        if (fetchError.name === 'AbortError') {
          throw new Error('Request timed out. The server might be too busy right now.')
        }
        
        if (fetchError.message.includes('Failed to fetch') || 
            fetchError.message.includes('NetworkError') ||
            fetchError.message.includes('Load failed')) {
          throw new Error('The server appears to be down. Please try again later.')
        }
        
        throw fetchError
      } finally {
        clearTimeout(timeoutId)
      }
      
      // Check for HTTP errors
      if (!response.ok) {
        console.error('API error status:', response.status, response.statusText)
        
        if (response.status === 502 || response.status === 503 || response.status === 504) {
          // These are gateway/availability errors - server is likely down
          throw new Error('The server is currently unavailable. The backend might be restarting or down for maintenance.')
        }
        
        throw new Error(`Server returned error ${response.status}: ${response.statusText}`)
      }
      
      // Parse response
      const data = await response.json()
      console.log('API response received', data)
      
      // 处理返回的数据
      if (data.success && data.analysis) {
        // 如果是完整的分析结果
        console.log('Received complete analysis result:', data)
        
        // 适配后端返回的数据结构
        const sentiment = data.analysis.sentiment || {};
        const toxicityCounts = data.analysis.toxicity?.counts || {};
        
        // 计算毒性评论总数
        const toxicTotal = Object.values(toxicityCounts).reduce((sum, val) => sum + (val || 0), 0);
        
        analysisResult.value = {
          total_comments: (sentiment.Positive || 0) + (sentiment.Neutral || 0) + (sentiment.Negative || 0),
          analysis: {
            sentiment: {
              positive_count: sentiment.Positive || 0,
              negative_count: sentiment.Negative || 0,
              neutral_count: sentiment.Neutral || 0
            },
            toxicity: {
              toxic_count: toxicTotal,
              toxic_types: toxicityCounts,
              toxic_percentage: toxicTotal > 0 ? 
                (toxicTotal / ((sentiment.Positive || 0) + (sentiment.Neutral || 0) + (sentiment.Negative || 0)) * 100) : 0
            }
          },
          strategies: data.strategies || "• Thank users for taking time to watch your video\n• Stay positive even when facing negative comments\n• Accept constructive criticism graciously\n• Avoid getting into arguments",
          example_comments: data.example_comments || []
        }
        
        showResultsModal.value = true
        isLoading.value = false
        return
      } else if (Array.isArray(data)) {
        // 向后兼容：如果收到的是评论数组，需要构建分析结果对象
        // 如果收到的是评论数组，需要构建分析结果对象
        const comments = data
        // 简单情感分析
        const positiveWords = ["good", "great", "awesome", "amazing", "love", "best", "excellent", "fantastic", "brilliant"]
        const negativeWords = ["bad", "terrible", "awful", "hate", "worst", "poor", "horrible", "disappointing"]
        
        let positiveCount = 0
        let negativeCount = 0
        let neutralCount = 0
        
        // 对每条评论进行简单的情感分析
        comments.forEach(comment => {
          const commentLower = comment.toLowerCase()
          const positiveMatches = positiveWords.filter(word => commentLower.includes(word)).length
          const negativeMatches = negativeWords.filter(word => commentLower.includes(word)).length
          
          if (positiveMatches > negativeMatches) positiveCount++
          else if (negativeMatches > positiveMatches) negativeCount++
          else neutralCount++
        })
        
        // 构建分析结果对象
        analysisResult.value = {
          total_comments: comments.length,
          raw_comments: comments,
          analysis: {
            sentiment: {
              positive_count: positiveCount,
              negative_count: negativeCount,
              neutral_count: neutralCount,
              positive_percentage: (positiveCount / comments.length * 100).toFixed(1),
              negative_percentage: (negativeCount / comments.length * 100).toFixed(1),
              neutral_percentage: (neutralCount / comments.length * 100).toFixed(1)
            },
            toxicity: {
              toxic_count: negativeCount, // 简单起见，将负面评论数作为毒性评论数
              non_toxic_count: positiveCount + neutralCount,
              toxic_percentage: (negativeCount / comments.length * 100).toFixed(1)
            }
          },
          // 生成一些示例回复策略
          strategies: "• 感谢用户花时间观看你的视频并留下评论\n• 保持积极态度，即使面对负面评论\n• 诚恳接受建设性批评，并向观众表示感谢\n• 避免陷入争论，保持专业和友好",
          example_comments: [
            {
              comment: comments.find(c => c.toLowerCase().includes("love") || c.toLowerCase().includes("good")) || "I love this video!",
              response: "谢谢你的支持！很高兴你喜欢这个视频。"
            },
            {
              comment: comments.find(c => c.toLowerCase().includes("hate") || c.toLowerCase().includes("bad")) || "I didn't like this content.",
              response: "感谢你的反馈。我会继续努力改进内容质量。有什么具体建议吗？"
            }
          ]
        }
        
        showResultsModal.value = true
        isLoading.value = false
        return
      }
      
      // 如果返回的不是数组而是对象，检查API响应状态
      if (data.status === 'error') {
        console.error('API returned error:', data.message)
        analysisError.value = data.message || 'Analysis failed, please try again later'
        isLoading.value = false
        return
      }
      
      // Check for WebSocket error cases
      if (data.analysis && data.analysis.note && data.analysis.note.includes('API Error: server rejected WebSocket connection')) {
        console.warn('Detected WebSocket connection issue, but we still received analysis data')
        
        // Add a note to the displayed result about the partial analysis
        data.wsError = true
      }
      
      // Update analysis result and display modal
      analysisResult.value = data
      showResultsModal.value = true
      isLoading.value = false
      
    } catch (error) {
      console.error('API request error:', error)
      
      // 添加一个直接的错误对象记录，帮助查找问题
      const errorDetails = {
        message: error.message,
        name: error.name,
        stack: error.stack,
        time: new Date().toISOString()
      }
      console.log('Full error details:', errorDetails)
      
      // Handle specific errors with user-friendly messages
      if (error.message.includes('NetworkError') || 
          error.message.includes('Failed to fetch') || 
          error.message.includes('Load failed') ||
          error.message.includes('server is down') ||
          error.message.includes('server is currently unavailable')) {
        analysisError.value = "Crikey! The server's having a bit of a lie-down right now. Try again in a few minutes. (Error: " + error.message + ")"
      } else if (error.name === 'AbortError' || error.message.includes('timed out')) {
        analysisError.value = "Fair dinkum, that's taking ages! The request timed out. Give it another go when the server's less busy."
      } else if (error.message.includes('CORS') || error.message.includes('access control checks')) {
        analysisError.value = "Strewth! There's a browser security issue connecting to the server. Try refreshing the page or using a different browser."
      } else {
        analysisError.value = `Looks like we hit a snag: ${error.message}. Please try again.`
      }
      
      isLoading.value = false
    }
  }

  // Close the modal
  const closeModal = () => {
    showResultsModal.value = false
  }

  const closePopup = () => (showCheckIn.value = false)
  const handleDotClick = (emotion) => {
    selectedEmotion.value = emotion
    showCheckIn.value = true
  }

  const handleSeekHelp = () => {
    window.open('https://www.betterhealth.vic.gov.au/health/healthyliving/Cyberbullying', '_blank')
  }

  const emojis = [
    { src: happy, alt: 'Happy' },
    { src: peace, alt: 'Sad' },
    { src: angry, alt: 'Angry' },
    { src: sad, alt: 'Confused' },
    { src: mda, alt: 'Frustrated' },
  ]

  const labels = [
    "What's the goal? 🎯",
    'How does it sound? 🗣️',
    'What do they say? 💬',
    'Where does it happen? 📍',
    'How does it make you feel? 😊',
  ]

  const leftCol = [
    'To help you improve. The person wants to share advice or opinions to make your content better. ✨',
    'Respectful, clear, and focused on your content. 🤝',
    '"Your video is great, but the sound could be clearer. Maybe try using a different mic?" 🎤',
    'Often in a thoughtful comment, private message, or a discussion space. 📱',
    'Encouraged to improve and learn. 🌱',
  ]

  const rightCol = [
    'To hurt, embarrass, or bring you down. The person is trying to make you feel bad. 👎',
    'Mean, rude, and often personal. 😠',
    '"Your voice is so annoying, just stop making videos!" ❌',
    'Usually in public comments, DMs, or even shared posts to mock you. 📢',
    'Upset, anxious, or even scared to post again. 😔',
  ]

  // Added from CommentResponseScripts.vue
  const selectedIndex = ref(0)
  const selectedType = computed(() => gaugeData[selectedIndex.value])

  function prevType() {
    selectedIndex.value = (selectedIndex.value - 1 + gaugeData.length) % gaugeData.length
  }

  function nextType() {
    selectedIndex.value = (selectedIndex.value + 1) % gaugeData.length
  }

  const gaugeData = [
    {
      label: 'Accusatory Comments',
      value: 40,
      color: '#FF3B30',
      strategy: [
        {
          title: 'Acknowledge the criticism',
          text: 'Validate their perspective and thank them for the feedback'
        },
        {
          title: 'Provide brief context',
          text: 'Share relevant information without being defensive'
        },
        {
          title: 'Offer a positive path forward',
          text: 'Suggest a constructive next step or solution'
        }
      ],
      q: 'This is such a biased take. You only presented one perspective and completely ignored the other side of the argument. Disappointing content.',
      a: "Thanks 🙏 Fair point on balance – definitely working with time limits but that's on me. Planning a follow-up with more perspectives soon! Any recommendations for sources? Always looking to improve! 💯"
    },
    {
      label: 'Emotional Comments',
      value: 25,
      color: '#FFA726',
      strategy: [
        {
          title: 'Acknowledge their emotions',
          text: 'Recognise the intensity and validate their feelings'
        },
        {
          title: 'Stay calm and neutral',
          text: 'Respond without escalating the emotional tone'
        },
        {
          title: 'Invite further conversation',
          text: 'Show openness to hearing more constructively'
        }
      ],
      q: "Why do you always talk like you know everything? This is so annoying!",
      a: "Appreciate you chiming in! Definitely not my intention to come off that way – I'll keep it more conversational next time 🙏"
    },
    {
      label: 'Misunderstanding Comments',
      value: 15,
      color: '#FF7043',
      strategy: [
        {
          title: 'Clarify gently',
          text: 'Provide accurate info without implying fault'
        },
        {
          title: 'Use simple language',
          text: 'Keep the explanation clear and concise'
        },
        {
          title: 'Offer resources',
          text: 'Suggest links or follow-up posts for context'
        }
      ],
      q: "Wait, are you saying everyone should quit their job and do this instead?",
      a: "Not quite! I meant this approach works *for some* – not one-size-fits-all. Thanks for pointing that out, I'll make it clearer!"
    },
    {
      label: 'Attacking Comments',
      value: 10,
      color: '#66BB6A',
      strategy: [
        {
          title: 'Avoid engaging emotionally',
          text: "Don't match their tone or insults"
        },
        {
          title: 'Set boundaries',
          text: 'Politely assert your intent to keep it respectful'
        },
        {
          title: 'Redirect to the topic',
          text: 'Bring focus back to the content or idea'
        }
      ],
      q: "You're such a clown. This is garbage advice!",
      a: "Let's keep it constructive here. Open to hearing thoughtful counterpoints if you have suggestions!"
    },
    {
      label: 'Constructive Comments',
      value: 10,
      color: '#81C784',
      strategy: [
        {
          title: 'Appreciate the input',
          text: 'Thank them for thoughtful feedback'
        },
        {
          title: 'Engage with the idea',
          text: 'Build upon or reflect on their suggestion'
        },
        {
          title: 'Show willingness to act',
          text: 'Indicate any upcoming improvements or plans'
        }
      ],
      q: "I think this could be stronger if you added more sources.",
      a: "Love that suggestion! I'm adding more citations in the next update – stay tuned and feel free to share any links!"
    }
  ]

  // Restore the goToRelaxation function
  const goToRelaxation = () => router.push('/relaxation')

  // Retry analysis function
  const retryAnalysis = () => {
    if (youtubeUrl.value) {
      analyzeYoutubeComments()
    }
  }
  </script>

  <style scoped>
  .critical-response-view {
    background: #fffdf4;
    font-family: Avenir, Helvetica, sans-serif;
    text-align: center;
  }

  .hero-section {
    min-height: 40vh;
    background-color: rgb(255, 252, 244);
    display: flex;
    align-items: center;
    overflow: visible;
    position: relative;
    z-index: 1;
    padding: 6rem 0 1rem;
    margin-bottom: 2rem;
  }

  .hero-content {
    position: relative;
    width: 100%;
    min-height: 40vh;
    display: flex;
    align-items: center;
    padding-left: 2rem;
    margin: 0 auto;
    overflow: visible;
  }

  .slogan {
    max-width: 800px;
    position: relative;
    z-index: 2;
    margin-left: 2rem;
    text-align: left;
  }

  .title-group {
    margin-bottom: 0.5rem;
    text-align: left;
  }

  .title-group h1 {
    font-size: 4rem;
    font-weight: bold;
    position: relative;
    background: linear-gradient(
      to right,
      #FF6B6B 20%,
      #4ECDC4 40%,
      #4ECDC4 60%,
      #FF6B6B 80%
    );
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    animation: liquidFlow 4s linear infinite;
    filter: drop-shadow(0 0 1px rgba(0, 0, 0, 0.2));
    transition: all 0.3s ease;
    line-height: 1.3;
    display: inline-block;
    margin-bottom: 1rem;
    white-space: nowrap;
    text-align: left;
    padding: 0 0 0.15em;
    transform: translateY(-0.05em);
  }

  .title-group h1:hover {
    filter: drop-shadow(0 0 2px rgba(255, 107, 107, 0.5));
    transform: scale(1.02);
    animation: liquidFlow 2s linear infinite; /* Speed up animation on hover */
  }

  @keyframes liquidFlow {
    0% {
      background-position: 0% center;
    }
    100% {
      background-position: 200% center;
    }
  }

  .title-group h2 {
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
    line-height: 1.2;
    display: block;
    white-space: nowrap;
    text-align: left;
    overflow: visible;
  }

  .subtitle {
    font-size: 1.25rem;
    color: #666;
    line-height: 1.4;
    margin-top: 1.5rem;
    white-space: normal;
    text-align: left;
    max-width: 100%;
  }

  @media (min-width: 640px) {
    .title-group h1 {
      font-size: 3rem;
    }
    .title-group h2 {
      font-size: 1.875rem;
    }
    .subtitle {
      font-size: 1.125rem;
    }
  }

  @media (min-width: 768px) {
    .title-group h1 {
      font-size: 3.75rem;
    }
    .title-group h2 {
      font-size: 2.25rem;
    }
    .subtitle {
      font-size: 1.25rem;
    }
  }

  @media (min-width: 1024px) {
    .title-group h1 {
      font-size: 4.5rem;
    }
    .title-group h2 {
      font-size: 3rem;
    }
    .subtitle {
      font-size: 1.5rem;
      white-space: nowrap;
    }
  }

  @media (min-width: 1280px) {
    .title-group h1 {
      font-size: 6rem;
    }
    .title-group h2 {
      font-size: 3.75rem;
    }
    .subtitle {
      font-size: 1.875rem;
      white-space: nowrap;
    }
  }

  .decorative-elements {
    position: absolute;
    top: 0;
    right: 0;
    width: 960px;
    height: 100%;
    display: grid;
    grid-template-columns: repeat(6, 160px);
    grid-template-rows: auto;
    row-gap: 1rem;
    padding: 2rem 0;
    z-index: 1;
    pointer-events: none;
    transform: translateX(0);
    justify-content: end;
  }

  .top-row {
    display: grid;
    grid-template-columns: repeat(3, 160px);
    gap: 0.5rem;
    align-items: start;
    margin: 0;
    padding: 0;
    grid-column: 4 / 7;
    grid-row: 1;
    justify-self: end;
  }

  .element-wrapper {
    width: 160px;
    height: 120px;
    position: relative;
    margin: 0;
    padding: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    pointer-events: auto;
    transition: transform 0.5s ease;
  }

  .element {
    width: 100%;
    height: 100%;
    object-fit: contain;
    display: block;
    margin: 0;
    padding: 0;
    transition: all 0.5s ease;
  }

  .top-row .element:hover {
    transform: rotate(-15deg) scale(1.1);
  }

  @media (max-width: 1800px) {
    .decorative-elements {
      width: 840px;
      grid-template-columns: repeat(6, 140px);
      opacity: 0.9;
      transform: translateX(0);
      justify-content: end;
    }
  }

  @media (max-width: 1536px) {
    .decorative-elements {
      width: 720px;
      grid-template-columns: repeat(6, 120px);
      opacity: 0.8;
      transform: translateX(0);
      justify-content: end;
    }
  }

  @media (max-width: 1280px) {
    .decorative-elements {
      width: 600px;
      grid-template-columns: repeat(6, 100px);
      opacity: 0.7;
      transform: translateX(0);
      row-gap: 0.75rem;
      justify-content: end;
    }
    
    .subtitle {
      white-space: normal;
    }
  }

  @media (max-width: 1024px) {
    .hero-section {
      min-height: 40vh;
      padding: 6rem 0 1rem;
    }
    
    .hero-content {
      min-height: 40vh;
    }
    
    .slogan {
      margin-left: 1.5rem;
    }
    
    .decorative-elements {
      transform: translateX(0) scale(0.9);
      opacity: 0.5;
      row-gap: 0.5rem;
      justify-content: end;
    }
    
    .title-group h1 {
      @apply text-5xl;
    }
    
    .title-group h2 {
      @apply text-4xl;
    }
    
    .subtitle {
      @apply text-xl;
    }
  }

  @media (max-width: 768px) {
    .hero-section {
      min-height: 22vh;
      padding: 7rem 0 0.5rem;
    }
    
    .hero-content {
      min-height: 22vh;
      flex-direction: column;
      align-items: flex-start;
      padding-top: 0.75rem;
    }
    
    .slogan {
      margin-left: 1rem;
      max-width: 90%;
    }
    
    .decorative-elements {
      opacity: 0.1;
      transform: translateX(0) scale(0.8);
    }

    .title-group h1 {
      @apply text-4xl;
    }
    
    .title-group h2 {
      @apply text-3xl;
    }
    
    .subtitle {
      @apply text-lg;
    }
  }

  @media (max-width: 640px) {
    .decorative-elements {
      opacity: 0;
      transform: translateX(0) scale(0.7);
    }
    
    .hero-section {
      min-height: 18vh;
      padding: 7.5rem 0 0.5rem;
      margin-bottom: 1rem;
    }

    .hero-content {
      padding: 0 1rem;
      min-height: 18vh;
      padding-top: 0.25rem;
    }
    
    .slogan {
      padding-top: 0;
    }
    
    .title-group h1 {
      @apply text-3xl;
    }
    
    .title-group h2 {
      @apply text-2xl;
    }
    
    .subtitle {
      @apply text-base;
    }
  }

  @media (max-width: 480px) {
    .decorative-elements {
      opacity: 0;
      display: none;
    }
    
    .hero-section {
      min-height: 16vh;
      padding: 8rem 0 0.5rem;
    }
    
    .hero-content {
      min-height: 16vh;
    }
  }

  .feeling-box {
    border: 2px solid #333;
    padding: 2rem 1rem 1rem;
    border-radius: 24px;
    width: 90%;
    max-width: 1200px;
    margin: 30px auto 4rem;
    position: relative;
    background: white;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
    z-index: 5;
  }

  .bell-container {
    position: absolute;
    top: -48px;
    left: 50%;
    transform: translateX(-50%);
    background: white;
    border: 2px solid #333;
    border-radius: 50%;
    width: 96px;
    height: 96px;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 6;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: transform 0.3s ease;
  }

  .bell-container:hover {
    animation: bell-shake 0.5s ease-in-out infinite;
  }

  .bell-icon {
    width: 96px;
    transition: transform 0.2s ease;
  }

  @keyframes bell-shake {
    0% {
      transform: translateX(-50%) rotate(0deg);
    }
    25% {
      transform: translateX(-50%) rotate(5deg);
    }
    50% {
      transform: translateX(-50%) rotate(0deg);
    }
    75% {
      transform: translateX(-50%) rotate(-5deg);
    }
    100% {
      transform: translateX(-50%) rotate(0deg);
    }
  }

  .feeling-box h2 {
    font-size: 36px;
    font-weight: 700;
    margin-top: 60px;
    margin-bottom: 30px;
    letter-spacing: 1px;
  }

  .emotions {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 2rem 0 1.5rem;
  }

  .emoji-option {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .emoji-img {
    width: 150px;
    height: 150px;
    object-fit: contain;
    transition: 0.25s ease;
    cursor: pointer;
    border-radius: 50%;
    padding: 8px;
    border: 5px solid transparent;
  }

  .emoji-img:hover {
    transform: scale(1.15);
    box-shadow: 0 0 20px rgba(212, 238, 90, 0.6);
  }

  .emoji-img.selected {
    border-radius: 50%;
    border: 5px solid rgb(212, 238, 90);
    box-shadow: 0 0 0 8px rgba(212, 238, 90, 0.4);
  }

  .emoji-option:last-child .emoji-img {
    width: 160px;
    height: 160px;
    margin-top: -12px;
  }

  /* 删除圆点相关样式并不显示圆点 */
  .dot {
    display: none;
  }

  .comparison {
    margin-top: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 3rem;
  }

  .comparison-header,
  .comparison-row {
    display: grid;
    grid-template-columns: 3fr 2fr 3fr;
    width: 90%;
    max-width: 1200px;
  }

  .comparison-header .col {
    font-weight: bold;
    padding: 1.5rem;
    background: #fffbf3;
    border: 2px solid #000;
    font-size: 18px;
    text-align: center;
  }

  .comparison-header .col:first-child {
    border-top-left-radius: 16px;
  }

  .comparison-header .col:last-child {
    border-top-right-radius: 16px;
  }

  .comparison-header .label {
    background: #fffbf3;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: none;
    border-right: none;
  }

  .comparison-row .cell {
    padding: 1.5rem;
    font-size: 16px;
    line-height: 1.6;
    text-align: left;
    border-left: 2px solid #000;
    border-right: 2px solid #000;
    border-bottom: 2px solid #000;
  }

  .comparison-row:last-child .cell:first-child {
    border-bottom-left-radius: 16px;
  }

  .comparison-row:last-child .cell:last-child {
    border-bottom-right-radius: 16px;
  }

  .comparison-row .left {
    background: #e1f37e;
  }

  .comparison-row .right {
    background: #ff914d;
  }

  .comparison-row .label {
    font-weight: bold;
    color: #2c3e50;
    background: #fffbf3;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    border-left: none;
    border-right: none;
  }

  .seek-help {
    margin-top: 2rem;
    margin-bottom: 3rem;
    font-weight: bold;
    font-size: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .popup {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    max-width: 400px;
    text-align: center;
  }

  .popup h2 {
    margin-bottom: 1.5rem;
  }

  .popup .buttons {
    display: flex;
    flex-direction: column;
    gap: 15px;
    margin-top: 20px;
  }

  .popup .buttons button {
    margin: 0;
    padding: 12px 20px;
    border: none;
    border-radius: 8px;
    background-color: #6c63ff;
    color: white;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
  }

  .popup .buttons button:hover {
    background-color: #5a52d5;
    transform: translateY(-2px);
  }

  .popup .buttons button:first-child {
    background-color: #7963ff;
  }

  .popup .buttons button:last-child {
    background-color: #9290a6;
  }

  /* 为 InteractiveHoverButton 组件添加样式 */
  .read-more-button {
    position: absolute;
    right: 0;
    top: 50%;
    transform: translateY(-50%);
    z-index: 2;
    margin-right: 3.5rem;
    --tw-border-opacity: 0.3;
    background-color: transparent !important;
    color: #1E6A42;
  }

  .read-more-button :deep(.bg-primary) {
    background-color: #1E6A42 !important;
  }

  .read-more-button :deep(.text-primary-foreground) {
    color: white !important;
  }

  .read-more-button:hover {
    transform: translateY(-50%) translateX(5px);
  }

  /* Responsive button position adjustment */
  @media (max-width: 1280px) {
    .read-more-button {
      margin-right: 2.5rem;
    }
  }

  @media (max-width: 1024px) {
    .read-more-button {
      margin-right: 2rem;
    }
  }

  @media (max-width: 768px) {
    .read-more-button {
      margin-right: 1.5rem;
    }
  }

  @media (max-width: 640px) {
    .read-more-button {
      margin-right: 1rem;
    }
  }

  .help-button {
    font-size: 26px;
    font-weight: 700;
    padding: 1.25rem 4rem;
    background-color: #FF6B6B;
    color: white;
    border: 2px solid black;
    border-radius: 12px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
    transition: all 0.3s ease;
    min-width: 300px;
    text-align: center;
  }

  .help-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
    background-color: #FF5252;
  }

  .comment-section-checker {
    margin-top: 4rem;
    margin-bottom: 4rem;
    padding: 3rem 2rem;
    background: #fffdf4;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
  }

  .section-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    color: #000;
  }

  .section-description {
    font-size: 1.5rem;
    color: #333;
    line-height: 1.4;
    max-width: 800px;
    margin: 0 auto 2rem auto;
  }

  .cards-container {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    margin-top: 3rem;
    flex-wrap: wrap;
    padding: 0 1rem;
  }

  .process-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 2px solid #000;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    width: 300px;
    height: 300px;
    display: flex;
    flex-direction: column;
    position: relative;
    background-color: #fffdf4;
  }

  .card-number {
    font-size: 5rem;
    font-weight: 700;
    position: absolute;
    top: 15px;
    left: 20px;
    color: #333;
    line-height: 1;
  }

  .card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding-top: 40px;
  }

  .card-icon {
    width: 100px;
    height: 100px;
    object-fit: contain;
    margin-bottom: 2.5rem;
  }

  .card-text {
    font-size: 1.25rem;
    color: #333;
    line-height: 1.4;
    font-weight: 600;
    text-align: center;
  }

  /* Card hover effects */
  .process-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .process-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  }
  
  .process-card:hover .card-icon {
    transform: scale(1.1);
  }
  
  .card-icon {
    transition: transform 0.3s ease;
  }

  /* Comments Response Scripts Section styles */
  .comments-scripts-section {
    margin: 3rem auto 4rem;
    max-width: 1200px;
    padding: 0 2rem;
    background-color: #f8f9fa;
    border-radius: 24px;
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    padding: 3rem 2rem;
    border: 2px solid #eaeaea;
  }
  
  .comments-scripts-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 2rem;
    color: #000;
    text-align: center;
    position: relative;
    display: inline-block;
  }
  
  .comments-scripts-title:after {
    content: "";
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: #e4f052;
    border-radius: 2px;
  }
  
  .search-container {
    position: relative;
    max-width: 500px;
    margin: 0 auto 2rem;
    border: 2px solid #000;
    border-radius: 12px;
    overflow: hidden;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .search-input {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    font-size: 1.1rem;
    border: none;
    outline: none;
    background: #fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23000000' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") 12px center no-repeat;
  }
  
  .search-close-btn {
    background: none;
    border: none;
    font-size: 1.8rem;
    padding: 0 1rem;
    cursor: pointer;
    color: #000;
    transition: color 0.2s;
  }
  
  .search-close-btn:hover {
    color: #ff5252;
  }

  /* Added styles from CommentResponseScripts.vue */
  .highlight-box {
    background-color: #e4f052;
    display: inline-block;
    padding: 0.4rem 1.2rem;
    border-radius: 6px;
    font-weight: 700;
    margin-bottom: 0.2rem;
    font-size: 1.1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .click-hint {
    font-size: 0.9rem;
    color: #444;
    margin-bottom: 2.5rem;
    font-style: italic;
  }

  .gauge-grid {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 3rem;
    margin-bottom: 2rem;
    padding: 1rem;
  }

  .gauge-item {
    cursor: pointer;
    text-align: center;
    width: 160px;
    transition: all 0.3s ease;
    position: relative;
    padding-bottom: 1rem;
  }

  .gauge-item:hover {
    transform: translateY(-5px);
  }

  .gauge-item.active {
    transform: scale(1.05);
  }

  .gauge-item.active:after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 3px;
    background: #e4f052;
    border-radius: 2px;
  }

  .gauge-item.active .label {
    color: #1e88e5;
    font-weight: 800;
  }

  .gauge-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .percent-text {
    font-size: 1.3rem;
    font-weight: 700;
    margin-top: -8px;
    color: #000;
  }

  .label {
    font-size: 0.95rem;
    font-weight: 700;
    color: #1c1c1c;
    line-height: 1.3;
    transition: color 0.3s;
  }

  .strategy-section {
    margin-top: 4rem;
    background-color: #fff;
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    border: 1px solid #eaeaea;
  }

  .strategy-title {
    font-size: 1.6rem;
    font-weight: 800;
    margin-bottom: 2rem;
    color: #1e293b;
    position: relative;
    display: inline-block;
  }
  
  .strategy-title:after {
    content: "";
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 60px;
    height: 3px;
    background: #e4f052;
    border-radius: 2px;
  }

  .nav-arrows {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .arrow {
    font-size: 2rem;
    cursor: pointer;
    font-weight: bold;
    padding: 0.5rem 1rem;
    user-select: none;
    transition: transform 0.2s, color 0.2s;
    color: #555;
  }
  
  .arrow:hover {
    transform: scale(1.2);
    color: #000;
  }

  .steps-grid {
    display: flex;
    justify-content: center;
    gap: 2rem;
    flex-wrap: wrap;
    margin: 0 2rem;
  }

  .step-box {
    background-color: #e4f052;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 1.2rem;
    width: 200px;
    font-weight: 600;
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    min-height: 220px;
    transition: transform 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
  }
  
  .step-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
  }

  .step-box strong {
    font-size: 1.1rem;
    color: #1e293b;
    margin-bottom: 0.5rem;
    text-align: center;
    z-index: 1;
  }

  .step-box p {
    margin-top: 0.5rem;
    font-weight: normal;
    font-size: 0.95rem;
    text-align: center;
    color: #333;
    line-height: 1.4;
    z-index: 1;
  }

  .step-num {
    margin-top: auto;
    padding-top: 0.8rem;
    font-size: 1.2rem;
    font-weight: bold;
    color: #1e293b;
    position: relative;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background-color: rgba(255, 255, 255, 0.6);
    z-index: 1;
  }

  .qa-box {
    border: 2px solid #c4e7c2;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    background-color: #fff;
    max-width: 750px;
    margin: 2.5rem auto 0;
    text-align: left;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    position: relative;
  }

  .qa-box p {
    margin-bottom: 1rem;
    line-height: 1.5;
  }
  
  .qa-box p:last-child {
    margin-bottom: 0;
  }
  
  .qa-box p strong {
    color: #1e88e5;
    font-size: 1.1rem;
  }
  
  @media (max-width: 768px) {
    .steps-grid {
      gap: 1.5rem;
      margin: 0 1rem;
    }
    
    .step-box {
      width: 160px;
      min-height: 200px;
      padding: 1.2rem 1rem 1rem;
    }
    
    .gauge-grid {
      gap: 2rem;
    }
    
    .strategy-section {
      padding: 1.5rem;
    }
    
    .qa-box {
      padding: 1.2rem 1.5rem;
    }
  }
  
  @media (max-width: 640px) {
    .comments-scripts-title {
      font-size: 2rem;
    }
    
    .gauge-item {
      width: 130px;
    }
    
    .steps-grid {
      flex-direction: column;
      align-items: center;
    }
    
    .step-box {
      width: 80%;
      max-width: 250px;
    }
    
    .nav-arrows {
      flex-direction: column;
    }
    
    .arrow {
      padding: 0.2rem 0.5rem;
    }
  }

  /* YouTube Analysis Section Styles */
  .youtube-analysis-section {
    width: 100%;
    max-width: 970px;
    margin: 0 auto 12rem;
  }

  .analysis-container {
    width: 100%;
    text-align: center;
  }

  .analysis-container h3 {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: #333;
    font-weight: 600;
  }

  .input-group {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .youtube-input {
    flex: 1;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s;
  }

  .youtube-input:focus {
    border-color: #7db3d9;
    box-shadow: 0 0 0 2px rgba(125, 179, 217, 0.2);
  }

  .analyze-button {
    padding: 0.5rem 1.5rem;
    background-color: #e75a97; /* Changed from blue to pink */
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s, transform 0.2s;
  }

  .analyze-button:not(:disabled):hover {
    background-color: #d4407f; /* Changed from darker blue to darker pink */
    transform: translateY(-2px);
  }

  .analyze-button:disabled {
    background-color: #f5a5c4; /* Changed from light blue to light pink */
    cursor: not-allowed;
  }

  .error-message {
    color: #e74c3c;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
  }
  
  .loading-message {
    color: #3498db;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
  }
  
  .loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    border-top-color: white;
    margin-right: 8px;
    animation: spin 1s linear infinite;
  }
  
  .loading-message .loading-spinner {
    border: 2px solid rgba(52, 152, 219, 0.3);
    border-top-color: #3498db;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  /* Modal Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 999;
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(3px);
  }

  .analysis-modal {
    background-color: white;
    border-radius: 12px;
    width: 90%;
    max-width: 1200px;
    max-height: 85vh;
    overflow-y: auto;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #eee;
    position: sticky;
    top: 0;
    background-color: white;
    z-index: 10;
  }

  .modal-header h2 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #333;
    margin: 0;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 2rem;
    color: #666;
    cursor: pointer;
    line-height: 1;
    transition: color 0.3s;
  }

  .close-button:hover {
    color: #e74c3c;
  }

  .modal-content {
    padding: 2rem;
  }

  /* Video Info Section */
  .video-info-section {
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #eee;
  }

  .video-info-section p {
    margin: 0.5rem 0;
    color: #333;
  }

  /* Results Grid */
  .results-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-bottom: 2.5rem;
  }

  .result-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .result-card h3 {
    font-size: 1.4rem;
    margin-bottom: 1.2rem;
    color: #333;
    font-weight: 600;
    text-align: center;
  }

  /* Sentiment Stats */
  .sentiment-stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .stat-box {
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
  }

  .stat-box.positive {
    background-color: rgba(76, 175, 80, 0.15);
  }

  .stat-box.neutral {
    background-color: rgba(158, 158, 158, 0.15);
  }

  .stat-box.negative {
    background-color: rgba(244, 67, 54, 0.15);
  }

  .stat-number {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
  }

  .stat-label {
    font-size: 0.9rem;
    color: #555;
  }

  /* Toxicity Section */
  .toxic-count {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  
  .toxic-explanation {
    font-size: 0.95rem;
    color: #555;
    text-align: center;
    line-height: 1.5;
  }

  .toxicity-subtitle {
    text-align: center;
    color: #555;
    margin-bottom: 2rem;
    font-size: 1rem;
  }

  .types-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }

  .type-item {
    font-size: 0.9rem;
    color: #555;
  }

  /* Donut Charts Section */
  .charts-section {
    margin-bottom: 2.5rem;
  }

  .charts-section h3 {
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
    color: #333;
    font-weight: 600;
    text-align: center;
  }

  .donut-charts {
    display: flex;
    justify-content: space-around;
    flex-wrap: wrap;
    gap: 1.5rem;
  }

  .donut-item {
    text-align: center;
    width: 130px;
  }

  .donut-label {
    font-size: 0.9rem;
    font-weight: 600;
    margin: 0.5rem 0 0.2rem;
    color: #333;
  }

  .donut-percent {
    font-size: 1.1rem;
    font-weight: 700;
    color: #555;
  }

  /* Strategies Section */
  .strategies-section {
    margin-bottom: 2.5rem;
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .strategies-section h3 {
    font-size: 1.6rem; 
    margin-bottom: 1.8rem;
    color: #333;
    font-weight: 600;
    text-align: center;
  }

  .strategy-content {
    color: #555;
    line-height: 2;
    text-align: left;
    font-size: 1.05rem;
  }

  /* Example Comments Section */
  .examples-section {
    margin-bottom: 2.5rem;
  }

  .examples-section h3 {
    font-size: 1.4rem;
    margin-bottom: 1.5rem;
    color: #333;
    font-weight: 600;
    text-align: center;
  }

  .example-cards {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
  }

  .example-card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    overflow: hidden;
    border: 1px solid #eee;
    width: 100%;
  }

  .example-comment {
    background-color: #f0f7fa;
    padding: 1.2rem;
    border-bottom: 1px solid #eee;
  }

  .example-comment h4 {
    font-weight: 600;
    color: #3b7a9e;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }

  .example-response {
    background-color: #f2f8f2;
    padding: 1.2rem;
  }

  .example-response h4 {
    font-weight: 600;
    color: #3c8a56;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }

  .example-comment p,
  .example-response p {
    margin: 0;
    color: #333;
    line-height: 1.5;
  }

  /* Recommendations Section */
  .recommendations-section {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .recommendations-section h3 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: #333;
    font-weight: 600;
  }

  .recommendations-section p {
    margin-bottom: 1rem;
    color: #555;
  }

  .recommendations-list {
    padding-left: 1.5rem;
  }

  .recommendations-list li {
    margin-bottom: 0.5rem;
    color: #555;
  }

  /* Responsive Media Queries */
  @media (max-width: 768px) {
    .input-group {
      flex-direction: column;
    }
    
    .results-grid {
      grid-template-columns: 1fr;
    }
    
    .donut-charts {
      gap: 1.5rem;
    }
    
    .donut-item {
      width: 120px;
    }
    
    .example-cards {
      gap: 1rem;
    }
    
    .example-comment,
    .example-response {
      padding: 1rem;
    }
  }

  @media (max-width: 480px) {
    .analysis-container h3 {
      font-size: 1.5rem;
    }
    
    .modal-header h2 {
      font-size: 1.5rem;
    }
    
    .sentiment-stats {
      grid-template-columns: 1fr;
      gap: 0.8rem;
    }
    
    .types-grid {
      grid-template-columns: 1fr;
    }
    
    .modal-content {
      padding: 1.5rem;
    }
    
    .strategies-section h3,
    .examples-section h3 {
      font-size: 1.3rem;
    }
    
    .example-comment h4,
    .example-response h4 {
      font-size: 0.9rem;
    }
  }

  /* Debug Information Styles */
  .debug-info {
    margin: 1rem 0;
    padding: 1rem;
    background-color: #fff8e1;
    border: 1px solid #ffecb3;
    border-radius: 8px;
  }
  
  .note-message {
    color: #ff6f00;
    margin-bottom: 0.5rem;
  }
  
  .debug-data {
    background-color: #f5f5f5;
    padding: 0.5rem;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.8rem;
    white-space: pre-wrap;
    overflow-x: auto;
    max-height: 300px;
    overflow-y: auto;
  }

  /* 添加部分分隔线样式 */
  .section-divider {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 2rem;
    margin-bottom: 2rem;
  }

  .section-divider:last-child {
    border-bottom: none;
    margin-bottom: 0;
  }

  .retry-button {
    background-color: #6ca3c9;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 0.3rem 0.6rem;
    margin-left: 0.5rem;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .retry-button:hover {
    background-color: #5a94ba;
  }

  /* Add these styles to the <style> section */
  .websocket-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeeba;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
  }

  .warning-icon {
    font-size: 2rem;
    margin-top: 0.25rem;
  }

  .warning-content h4 {
    font-size: 1.1rem;
    color: #856404;
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }

  .warning-content p {
    color: #856404;
    margin: 0 0 0.5rem 0;
  }

  .warning-content .warning-note {
    font-size: 0.9rem;
    font-style: italic;
    margin-top: 0.5rem;
  }
  </style>
