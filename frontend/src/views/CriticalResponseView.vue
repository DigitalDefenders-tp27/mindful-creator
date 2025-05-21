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
            <!-- Top Row Right -->
            <div class="top-row">
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Green.svg" alt="Flower" class="element hoverable rotating">
              </div>
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable rotating">
              </div>
            </div>
            
            <!-- Second Row -->
            <div class="second-row">
              <div class="element-wrapper">
                <img src="/src/assets/icons/elements/Flower_Pink.svg" alt="Flower" class="element hoverable rotating">
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
            <div class="emoji-label">{{ emoji.alt }}</div>
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

      <!-- Positive Emotion Popup -->
      <div v-if="showPositiveMessage" class="overlay">
        <div class="popup positive-popup">
          <h2>Great to know you're feeling good! Let's continue with our journey.</h2>
          <div class="buttons">
            <button @click="closePopup">Let's go!</button>
          </div>
        </div>
      </div>

      <!-- Banner Section Title -->
      <div class="banner-section-title-container">
        <h2 class="banner-section-title">Criticism VS. Cyberbully</h2>
      </div>

      <!-- Banner Sections -->
      <div class="banners-container">
        <button class="banner-nav prev-banner" @click="prevBanner">
          <span class="arrow-icon">❮</span>
        </button>
        
        <transition name="slide-fade">
          <div 
            :key="currentBannerIndex" 
            class="banner-section"
            :style="{ background: bannerData[currentBannerIndex].gradient }"
            ref="bannerSection"
          >
            <div class="banner-content">
              <h2 class="banner-title">{{ bannerData[currentBannerIndex].title }}</h2>
              <div class="comparison-content">
                <div class="constructive">
                  <h3>Constructive Criticism</h3>
                  <p>{{ bannerData[currentBannerIndex].constructive }}</p>
                </div>
                <div class="cyberbullying">
                  <h3>Cyberbullying</h3>
                  <p>{{ bannerData[currentBannerIndex].cyberbullying }}</p>
                </div>
              </div>
              <div class="banner-pagination">
                <span 
                  v-for="(_, index) in bannerData" 
                  :key="index" 
                  :class="['dot', { active: currentBannerIndex === index }]"
                  @click="setBanner(index)"
                ></span>
              </div>
            </div>
          </div>
        </transition>

        <button class="banner-nav next-banner" @click="nextBanner">
          <span class="arrow-icon">❯</span>  
        </button>
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
          <div class="process-card no-hover">
            <div class="card-number">1</div>
            <div class="card-content">
              <img src="/public/icons/elements/video.png" alt="Smartphone icon" class="card-icon">
              <p class="card-text">Open your Youtube video.</p>
            </div>
          </div>
          
          <div class="process-card no-hover">
            <div class="card-number">2</div>
            <div class="card-content">
              <img src="/public/icons/elements/copy.png" alt="Copy icon" class="card-icon">
              <p class="card-text">Copy the URL.</p>
            </div>
          </div>
          
          <div class="process-card no-hover">
            <div class="card-number">3</div>
            <div class="card-content">
              <img src="/public/icons/elements/paste.png" alt="Link icon" class="card-icon">
              <p class="card-text">Paste it into the box below.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Comments Response Scripts Section -->
      <div class="youtube-analysis-section">
        <div class="analysis-container mt-8 mb-12 p-6 border-2 border-black rounded-lg shadow-md bg-white mx-auto">
          <h3 class="section-title">YouTube Comments Analysis</h3>
          <div class="input-group">
            <input 
              v-model="youtubeUrl" 
              type="text" 
              class="youtube-input"
              placeholder="Enter YouTube video URL (https://www.youtube.com/watch?v=...)"
              @input="analysisError = null"
            />
            <button 
              v-if="youtubeUrl" 
              @click="youtubeUrl = ''" 
              class="clear-button"
              type="button"
              aria-label="Clear input"
            >
              ×
            </button>
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
          </p>
          <p v-if="isLoading" class="loading-message">
            <span class="loading-spinner"></span>
            Grabbing and checking those comments. Hang in there, mate...
          </p>
        </div>
      </div>
      
      <!-- Analysis Results Modal -->
      <div v-if="showResults" class="modal-overlay">
        <div class="analysis-modal">
          <div class="modal-header">
            <h2>YouTube Comments Analysis Results</h2>
            <button class="close-button" @click="closeModal">×</button>
          </div>
          
          <div class="modal-content">
            <!-- Video Info -->
            <div class="video-info-section section-divider">
              <p class="video-info-item"><strong>Video URL:</strong> {{ youtubeUrl }}</p>
              <p class="video-info-item"><strong>Comments Analysed:</strong> {{ analysisResult?.total_comments || 0 }}</p>
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
            
            <!-- Disclaimers -->
            <div class="disclaimer-section section-divider">
              <div class="disclaimer-content">
                <h4><span style="white-space: nowrap; font-weight: 800;">⚠️ Important Disclaimers</span></h4>
                <ul class="disclaimer-list">
                  <li>This page may display insulting or offensive content from YouTube comments.</li>
                  <li>The analysis may include comments in languages other than English.</li>
                  <li>Our system has limited capability in processing comments written in non-English languages.</li>
                  <li>The quantity of negative comments and toxic comments may differ as they are classified using different criteria.</li>
                  <li>The statistics, analysis, and response strategies are generated by NLP and LLM models which may occasionally make mistakes or provide imperfect suggestions.</li>
                </ul>
              </div>
            </div>
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
            
            <!-- Strategies Section -->
            <div class="strategies-section section-divider" v-if="analysisResult?.strategies">
              <h3>Response Strategies</h3>
              <div class="strategy-content" v-html="formatStrategies(analysisResult.strategies)"></div>
            </div>
            
            <!-- Example Comments Section -->
                          <div v-if="analysisResult?.example_comments && analysisResult.example_comments.length > 0" class="mb-8 mt-8">
                <h3 class="comments-section-title">Comments & Response Suggestions</h3>
              <div class="space-y-6">
                <div v-for="(example, index) in analysisResult.example_comments" :key="index" class="bg-white rounded-lg shadow-md overflow-hidden">
                  <div class="flex flex-col">
                    <div class="bg-blue-50 px-6 py-4 border-b border-blue-100">
                      <h4 class="font-bold text-blue-700 mb-2 flex items-center">
                        Original Comment:
                      </h4>
                      <p class="mb-0 text-gray-800 whitespace-pre-wrap font-medium bg-white p-4 rounded-md border border-blue-100 shadow-sm mx-2">{{ example.comment || 'No example comment provided' }}</p>
                    </div>
                    <div class="px-6 py-4 bg-green-50">
                      <h4 class="font-bold text-blue-700 mb-2 flex items-center">
                        <span class="mr-2">✅</span>
                        Suggested Response:
                      </h4>
                      <p class="text-gray-800 whitespace-pre-wrap bg-white p-4 rounded-md border border-green-100 shadow-sm mx-2">{{ example.response || 'No response suggestion available' }}</p>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            <div v-else class="mb-8 p-6 bg-yellow-50 border-l-4 border-yellow-400 rounded-md shadow-sm">
              <div class="flex items-center">
                <div class="text-yellow-500 mr-3">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                </div>
                <div>
                  <h4 class="font-bold text-yellow-700">No comments found</h4>
                  <p class="text-yellow-600">There are no comments to analyze for this video or they couldn't be retrieved.</p>
                </div>
              </div>
              <div class="mt-2 text-xs text-gray-400">
                Debug: {{ JSON.stringify({
                    analysisResult_type: typeof analysisResult,
                    has_example_comments: !!analysisResult?.example_comments,
                    example_comments_type: analysisResult?.example_comments ? typeof analysisResult.example_comments : 'undefined',
                    is_array: Array.isArray(analysisResult?.example_comments),
                    length: analysisResult?.example_comments ? analysisResult.example_comments.length : 0
                  }) }}
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

      <div v-if="showResults" class="results-container">
        <div class="header-section">
          <h2>Analysis Results</h2>
          <div class="analysis-source-tabs">
            <button 
              :class="['tab-button', { active: activeTab === 'combined' }]" 
              @click="activeTab = 'combined'"
            >
              Combined View
            </button>
            <button 
              v-if="analysisResult?.nlp_analysis" 
              :class="['tab-button', { active: activeTab === 'nlp' }]" 
              @click="activeTab = 'nlp'"
            >
              NLP Analysis
            </button>
            <button 
              v-if="analysisResult?.llm_analysis" 
              :class="['tab-button', { active: activeTab === 'llm' }]" 
              @click="activeTab = 'llm'"
            >
              LLM Analysis
            </button>
          </div>
        </div>

        <div class="analysis-content">
          <!-- Sentiment Analysis Section -->
          <div class="sentiment-section">
            <h3>Sentiment Breakdown</h3>
            <div class="sentiment-charts">
              <!-- Combined/Default Sentiment View -->
              <template v-if="activeTab === 'combined'">
                <div class="chart-container">
                  <h4>Total Comments: {{ analysisResult?.total_comments || 0 }}</h4>
                  <pie-chart
                    :chart-data="getSentimentChartData(analysisResult?.analysis?.sentiment)"
                    :options="chartOptions"
                  />
                </div>
              </template>
              
              <!-- NLP Sentiment View -->
              <template v-else-if="activeTab === 'nlp' && analysisResult?.nlp_analysis">
                <div class="chart-container">
                  <h4>NLP Analysis</h4>
                  <h5>Total Comments: {{ 
                    (analysisResult.nlp_analysis.sentiment?.Positive || 0) + 
                    (analysisResult.nlp_analysis.sentiment?.Negative || 0) + 
                    (analysisResult.nlp_analysis.sentiment?.Neutral || 0) 
                  }}</h5>
                  <pie-chart
                    :chart-data="getSentimentChartData(analysisResult.nlp_analysis.sentiment, true)"
                    :options="chartOptions"
                  />
                </div>
              </template>
              
              <!-- LLM Sentiment View -->
              <template v-else-if="activeTab === 'llm' && analysisResult?.llm_analysis">
                <div class="chart-container">
                  <h4>LLM Analysis</h4>
                  <h5>Total Comments: {{ 
                    (analysisResult.llm_analysis.sentiment?.Positive || 0) + 
                    (analysisResult.llm_analysis.sentiment?.Negative || 0) + 
                    (analysisResult.llm_analysis.sentiment?.Neutral || 0) 
                  }}</h5>
                  <pie-chart
                    :chart-data="getSentimentChartData(analysisResult.llm_analysis.sentiment, true)"
                    :options="chartOptions"
                  />
                </div>
              </template>
            </div>
          </div>
          
          <!-- Toxicity Analysis Section -->
          <div v-if="activeTab === 'combined' && analysisResult?.analysis?.toxicity?.toxic_types" class="toxicity-section">
            <h3>Toxicity Breakdown</h3>
            <div class="toxicity-header">
              <h4>{{ 
                analysisResult.analysis.toxicity.toxic_count || 0 
              }} toxic comment{{ analysisResult.analysis.toxicity.toxic_count === 1 ? '' : 's' }}</h4>
              <h5>{{ analysisResult.analysis.toxicity.toxic_percentage.toFixed(1) }}% of all comments</h5>
            </div>
            <div class="toxicity-charts">
              <div 
                v-for="(count, type) in analysisResult.analysis.toxicity.toxic_types" 
                :key="type" 
                class="toxicity-chart"
                v-show="count > 0"
              >
                <donut-chart 
                  :chart-data="getDonutChartData(count, type)" 
                  :options="donutOptions" 
                />
                <div class="toxicity-label">
                  <span class="toxicity-type">{{ formatToxicityType(type) }}</span>
                  <span class="toxicity-count">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- NLP Toxicity View -->
          <div v-else-if="activeTab === 'nlp' && analysisResult?.nlp_analysis?.toxicity" class="toxicity-section">
            <h3>NLP Toxicity Analysis</h3>
            <div class="toxicity-header">
              <h4>{{ getToxicCount(analysisResult.nlp_analysis.toxicity) }} toxic comment(s)</h4>
              <h5>{{ getToxicPercentage(analysisResult.nlp_analysis) }}% of all comments</h5>
            </div>
            <div class="toxicity-charts">
              <div 
                v-for="(count, type) in getToxicTypes(analysisResult.nlp_analysis.toxicity)" 
                :key="type" 
                class="toxicity-chart"
                v-show="count > 0"
              >
                <donut-chart 
                  :chart-data="getDonutChartData(count, type)" 
                  :options="donutOptions" 
                />
                <div class="toxicity-label">
                  <span class="toxicity-type">{{ formatToxicityType(type) }}</span>
                  <span class="toxicity-count">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- LLM Toxicity View -->
          <div v-else-if="activeTab === 'llm' && analysisResult?.llm_analysis?.toxicity" class="toxicity-section">
            <h3>LLM Toxicity Analysis</h3>
            <div class="toxicity-header">
              <h4>{{ getToxicCount(analysisResult.llm_analysis.toxicity) }} toxic comment(s)</h4>
              <h5>{{ getToxicPercentage(analysisResult.llm_analysis) }}% of all comments</h5>
            </div>
            <div class="toxicity-charts">
              <div 
                v-for="(count, type) in getToxicTypes(analysisResult.llm_analysis.toxicity)" 
                :key="type" 
                class="toxicity-chart"
                v-show="count > 0"
              >
                <donut-chart 
                  :chart-data="getDonutChartData(count, type)" 
                  :options="donutOptions" 
                />
                <div class="toxicity-label">
                  <span class="toxicity-type">{{ formatToxicityType(type) }}</span>
                  <span class="toxicity-count">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Strategies Section - Always visible regardless of tab -->
          <div class="strategies-section">
            <h3>Response Strategies</h3>
            <div class="strategies-content">
              <p v-for="(strategy, index) in strategiesList" :key="index">{{ strategy }}</p>
            </div>
          </div>

          <!-- Example Comments Section - Always visible regardless of tab -->
          <div v-if="analysisResult?.example_comments?.length" class="examples-section">
            <h3>Example Comments & Responses</h3>
            <div class="examples-container">
              <div v-for="(example, index) in analysisResult.example_comments" :key="index" class="example-card">
                <div class="comment">
                  <h4>Comment:</h4>
                  <p>{{ example.comment }}</p>
                </div>
                <div class="response">
                  <h4>Suggested Response:</h4>
                  <p>{{ example.response }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
  </template>

  <script setup>
  import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
  import { useRouter } from 'vue-router'
  import InteractiveHoverButton from '@/components/ui/interactive-hover-button.vue'
  import RippleButton from '@/components/ui/ripple-button.vue'
  import HalfDonutChart from '@/components/ui/HalfDonutChart.vue'
  import CommentInput from '@/components/CommentInput.vue'

  import { useAnalysisStore } from '@/stores/analysisStore'
  const analysisStore = useAnalysisStore()
  analysisStore.$reset()

  import bell from '/public/emojis/bell.png'
  import happy from '/public/emojis/Happy.png'
  import peace from '/public/emojis/Peace.png'
  import angry from '/public/emojis/Angry.png'
  import sad from '/public/emojis/Sad.png'
  import mda from '/public/emojis/Mad.png'

  const router = useRouter()
  const showCheckIn = ref(false)
  const showPositiveMessage = ref(false) // New state for positive emotion message
  const selectedEmotion = ref(null)

  // Banner carousel variables and functions
  const currentBannerIndex = ref(0)
  const autoplayInterval = ref(null)
  
  // Banner data
  const bannerData = [
    {
      title: "What's the goal? 🎯",
      constructive: "To help you improve. The person wants to share advice or opinions to make your content better. ✨",
      cyberbullying: "To hurt, embarrass, or bring you down. The person is trying to make you feel bad. 👎",
      gradient: "linear-gradient(135deg, #FFD1D1, #A2FFEF, #FFF5B0)" // Light Pink -> Light Aqua -> Soft Yellow
    },
    {
      title: "How does it sound? 🗣️",
      constructive: "Respectful, clear, and focused on your content. 🤝",
      cyberbullying: "Mean, rude, and often personal. 😠",
      gradient: "linear-gradient(135deg, #D1FFF8, #c1fba4, #B0CFFF)" // Light Aqua -> Soft Mint -> Pale Blue
    },
    {
      title: "What do they say? 💬",
      constructive: "\"Your video is great, but the sound could be clearer. Maybe try using a different mic?\" 🎤",
      cyberbullying: "\"Your voice is so annoying, just stop making videos!\" ❌",
      gradient: "linear-gradient(135deg, #ffdab9, #ffefd5, #FFFBD1)" // Soft Peach -> Light Orange -> Pale Yellow
    },
    {
      title: "Where does it happen? 📍",
      constructive: "Often in a thoughtful comment, private message, or a discussion space. 📱",
      cyberbullying: "Usually in public comments, DMs, or even shared posts to mock you. 📢",
      gradient: "linear-gradient(135deg, #FFF5B0, #b0f2c2, #a2d2ff)" // Light Yellow -> Pale Green -> Light Sky Blue
    },
    {
      title: "How does it make you feel? 😊",
      constructive: "Encouraged to improve and learn. 🌱",
      cyberbullying: "Upset, anxious, or even scared to post again. 😔",
      gradient: "linear-gradient(135deg, #F0D1FF, #ffc0cb, #e8e0ff)" // Light Lavender -> Soft Pink -> Pale Lilac
    }
  ]
  
  // Banner navigation functions
  const nextBanner = () => {
    currentBannerIndex.value = (currentBannerIndex.value + 1) % bannerData.length
    resetAutoplay()
  }
  
  const prevBanner = () => {
    currentBannerIndex.value = (currentBannerIndex.value - 1 + bannerData.length) % bannerData.length
    resetAutoplay()
  }
  
  const setBanner = (index) => {
    currentBannerIndex.value = index
    resetAutoplay()
  }
  
  const resetAutoplay = () => {
    if (autoplayInterval.value) {
      clearInterval(autoplayInterval.value)
    }
    startAutoplay()
  }
  
  const startAutoplay = () => {
    autoplayInterval.value = setInterval(() => {
      nextBanner()
    }, 5000) // Change banner every 5 seconds
  }
  
  // Setup and cleanup
  onMounted(() => {
    startAutoplay()
  })
  
  onBeforeUnmount(() => {
    if (autoplayInterval.value) {
      clearInterval(autoplayInterval.value)
    }
  })

  // YouTube analysis variables
  const youtubeUrl = ref('')
  const isLoading = ref(false)
  const analysisError = ref(null)
  const showResultsModal = ref(false)
  const analysisResult = ref({})

  // Computed property to check if the URL is valid
  const isValidYoutubeUrl = computed(() => {
    if (!youtubeUrl.value) return false
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})(\S*)?$/
    return youtubeRegex.test(youtubeUrl.value)
  })

  // Helper function to normalize YouTube URLs
  const normalizeYoutubeUrl = (url) => {
    if (!url) return url
    
    // If URL starts with youtube.com or youtu.be without protocol, add https://
    if (url.match(/^(youtube\.com|youtu\.be)/)) {
      return `https://${url}`
    }
    
    // If URL starts with www. without protocol, add https://
    if (url.match(/^www\./)) {
      return `https://${url}`
    }
    
    // If URL doesn't have protocol, assume https://
    if (!url.match(/^https?:\/\//)) {
      return `https://${url}`
    }
    
    return url
  }

  // Method to set an example URL
  const setExampleUrl = () => {
    youtubeUrl.value = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    analysisError.value = null
  }

  // Format toxicity type names to more readable format
  const formatToxicityType = (type) => {
    // Handle different formats returned by backend (capitalised or lowercase)
    const typeMap = {
      // Backend return format
      'Toxic': 'General Toxicity',
      'Severe Toxic': 'Severe Toxicity',
      'Obscene': 'Obscene',
      'Threat': 'Threat',
      'Insult': 'Insult',
      'Identity Hate': 'Identity Hate',
      // Original frontend format (for backwards compatibility)
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
    
    // Remove markdown code block markers
    let cleanedStrategies = strategies
      .replace(/```markdown\n?/g, '')
      .replace(/```/g, '');
    
    // Clean up formatting and add extra spacing between strategies
    cleanedStrategies = cleanedStrategies.trim();
    
    // Process each line - add bold to the beginning of each strategy
    return cleanedStrategies
      .split('\n')
      .map(line => {
        line = line.trim();
        if (line.length > 0) {
          // If line starts with a word followed by a colon, make it bold
          if (/^[A-Za-z0-9\s]+:/.test(line)) {
            const parts = line.split(':');
            if (parts.length >= 2) {
              return `<strong>${parts[0]}:</strong>${parts.slice(1).join(':')}`;
            }
          }
          
          // Find the first significant word and make it bold
          const words = line.split(' ');
          if (words.length > 1) {
            return `<strong>${words[0]}</strong> ${words.slice(1).join(' ')}`;
          }
        }
        return line;
      })
      .filter(line => line.length > 0)
      .join('<br><br>'); // Add extra line break between strategies
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

  // Add these functions before the script setup section
  const getDonutChartData = (count, type) => {
    return {
      labels: [formatToxicityType(type)],
      datasets: [{
        data: [count],
        backgroundColor: [getToxicityColor(type.toLowerCase())],
        borderWidth: 0
      }]
    }
  }

  const donutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '70%',
    plugins: {
      legend: {
        display: false
      }
    }
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          font: {
            size: 14
          }
        }
      }
    }
  }

  // Analyse YouTube comments
  const analyzeYoutubeComments = async () => {
    console.log('=== Starting YouTube analysis process ===')
    
    // Reset state
    analysisError.value = null
    
    // Validate URL
    if (!youtubeUrl.value) {
      console.warn('No YouTube URL provided')
      analysisError.value = 'Please enter a YouTube video URL, mate'
      return
    }
    
    // Normalize the URL first
    const normalizedUrl = normalizeYoutubeUrl(youtubeUrl.value)
    
    // Validate URL format
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})(\S*)?$/
    if (!youtubeRegex.test(normalizedUrl)) {
      console.warn('Invalid YouTube URL format:', normalizedUrl)
      analysisError.value = 'Please entre a valid YouTube URL, that one\'s not right.'
      return
    }
    
    console.log('URL validation passed:', normalizedUrl)
    
    // Set loading state
    isLoading.value = true
    
    // API URL options - will try alternatives if primary fails
    const apiUrls = [
      `${import.meta.env.BACKEND_URL || 'https://api.tiezhu.org'}/api/youtube/analyse_full`,  // Use the full analysis endpoint
    ]
    let primaryApiUrl = apiUrls[0]
    
    try {
      console.log('Starting API request process...')
      console.log('Using API URL:', primaryApiUrl)
      
      // Create AbortController for the request with timeout
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 120000) // 2 minute timeout
      
      // First make a simple GET request to check if the server is responding at all
      let serverAvailable = false
      try {
        console.log('Performing health check...')
        const healthCheck = await fetch(`${import.meta.env.BACKEND_URL || 'https://api.tiezhu.org'}/api/health`, {
          method: 'GET',
          signal: AbortSignal.timeout(5000)
        })
        
        console.log('Health check response:', {
          status: healthCheck.status,
          statusText: healthCheck.statusText,
          ok: healthCheck.ok
        })
        serverAvailable = true
      } catch (healthError) {
        console.warn('Server health check failed:', healthError.message)
        // Continue anyway - will try the actual request
      }
      
      console.log('Sending API request to:', primaryApiUrl)
      
      let response
      try {
        // Send request to backend API with improved error handling
        console.log('Preparing POST request with data:', {
          url: normalizedUrl,
          youtube_url: normalizedUrl,  // Include both formats for compatibility
          limit: 100
        })
        
        // Try multiple URL formats if needed
        let fetchError = null
        for (let i = 0; i < apiUrls.length; i++) {
          try {
            console.log(`Attempt ${i+1}/${apiUrls.length} with URL: ${apiUrls[i]}`)
            
            // Send request to API endpoint
            response = await fetch(apiUrls[i], {
              method: 'POST',
              mode: 'cors',
              credentials: 'omit',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify({
                url: normalizedUrl,
                youtube_url: normalizedUrl,  // Include both formats for compatibility
                limit: 100
              }),
              signal: controller.signal
            })
            
            console.log(`Response from attempt ${i+1}:`, {
              status: response.status,
              statusText: response.statusText,
              ok: response.ok
            })
            
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
        console.error('API error status:', {
          status: response.status,
          statusText: response.statusText
        })
        
        if (response.status === 502 || response.status === 503 || response.status === 504) {
          // These are gateway/availability errors - server is likely down
          throw new Error('The server is currently unavailable. The backend might be restarting or down for maintenance.')
        }
        
        throw new Error(`Server returned error ${response.status}: ${response.statusText}`)
      }
      
      // Parse response
      const data = await response.json()
      console.log('API response received:', data)
      
      // Process the returned data
      if (data.success) {
        console.log('Processing successful API response...')
        
        // Build the analysis result with the processed data
        analysisResult.value = {
          total_comments: data.totalComments || 0,
          analysis: {
            sentiment: {
              positive_count: data.sentiment?.positive || 0,
              neutral_count: data.sentiment?.neutral || 0,
              negative_count: data.sentiment?.negative || 0
            },
            toxicity: {
              toxic_count: data.toxicity?.total || 0,
              toxic_percentage: data.toxicity?.percentage || 0,
              toxic_types: data.toxicity?.types || {}
            }
          },
          strategies: data.strategies || "",
          example_comments: data.example_comments || []
        }
        
        console.log('Final analysis result:', analysisResult.value)
        
        // Show the results modal
        showResultsModal.value = true
        showResults.value = true
        isLoading.value = false
        console.log('=== Analysis process completed successfully ===')
      } else {
        console.error('API returned error:', data.message)
        analysisError.value = data.message || 'Analysis failed, please try again later'
        isLoading.value = false
      }
      
    } catch (error) {
      console.error('=== Analysis process failed ===')
      console.error('Error details:', {
        message: error.message,
        name: error.name,
        stack: error.stack,
        time: new Date().toISOString()
      })
      
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
    showResultsModal.value = false;
    showResults.value = false;  // Add this line to close the results container
  }

  const closePopup = () => {
    showCheckIn.value = false
    showPositiveMessage.value = false
  }
  
  const handleDotClick = (emotion) => {
    selectedEmotion.value = emotion
    // Show different popups based on emotion type
    if (emotion === 'Angry' || emotion === 'Sad' || emotion === 'Mad') {
      showCheckIn.value = true
      showPositiveMessage.value = false
    } else if (emotion === 'Happy' || emotion === 'Peace') {
      showPositiveMessage.value = true
      showCheckIn.value = false
    }
  }

  const handleSeekHelp = () => {
    window.open('https://www.betterhealth.vic.gov.au/health/healthyliving/Cyberbullying', '_blank')
  }

  const emojis = [
    { src: happy, alt: 'Happy' },
    { src: peace, alt: 'Peace' },
    { src: angry, alt: 'Angry' },
    { src: sad, alt: 'Sad' },
    { src: mda, alt: 'Mad' },
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

  const showResults = ref(false)
  const activeTab = ref('combined')  // 新增：当前激活的标签页

  // 新增辅助函数，用于从不同格式的毒性数据中获取统计信息
  function getToxicTypes(toxicity) {
    if (!toxicity) return {};
    if (toxicity.toxic_types) return toxicity.toxic_types;
    if (toxicity.counts) return toxicity.counts;
    return {};
  }

  function getToxicCount(toxicity) {
    if (!toxicity) return 0;
    if (toxicity.toxic_count !== undefined) return toxicity.toxic_count;
    if (toxicity.total_toxic_comments !== undefined) return toxicity.total_toxic_comments;
    
    // 尝试从类型统计中计算总数
    const types = getToxicTypes(toxicity);
    return Object.values(types).reduce((sum, val) => sum + (val || 0), 0);
  }

  function getToxicPercentage(analysis) {
    if (!analysis || !analysis.sentiment) return 0;
    
    const toxicCount = getToxicCount(analysis.toxicity || {});
    const totalComments = 
      (analysis.sentiment.Positive || 0) + 
      (analysis.sentiment.Negative || 0) + 
      (analysis.sentiment.Neutral || 0);
    
    if (totalComments === 0) return 0;
    return ((toxicCount / totalComments) * 100).toFixed(1);
  }

  // 调整现有的getSentimentChartData函数，增加一个参数用于处理直接的API格式
  function getSentimentChartData(sentiment, isDirectApiFormat = false) {
    if (!sentiment) {
      return {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{ data: [0, 0, 0], backgroundColor: ['#4CAF50', '#FFC107', '#F44336'] }]
      }
    }
    
    // 如果是直接从API获取的格式（有大写键名）
    if (isDirectApiFormat) {
      return {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
          data: [
            sentiment.Positive || 0,
            sentiment.Neutral || 0,
            sentiment.Negative || 0
          ],
          backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
        }]
      }
    }
    
    // 标准前端格式（小写键名加下划线）
    return {
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [{
        data: [
          sentiment.positive_count || 0,
          sentiment.neutral_count || 0,
          sentiment.negative_count || 0
        ],
        backgroundColor: ['#4CAF50', '#FFC107', '#F44336']
      }]
    }
  }
  </script>

  <style scoped>
  .critical-response-view {
    background: #fffdf4;
    font-family: Avenir, Helvetica, sans-serif;
    text-align: center;
  }

  /* Add only the essential new styles */
  .clear-button {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    font-size: 1.5rem;
    color: #999;
    cursor: pointer;
    padding: 0;
    width: 24px;
    height: 24px;
    line-height: 24px;
    border-radius: 50%;
  }

  .clear-button:hover {
    color: #555;
    background-color: #f5f5f5;
  }

  .url-examples {
    margin-top: 0.75rem;
    font-size: 0.9rem;
    color: #666;
  }

  .example-url-button {
    background: none;
    border: none;
    color: #7e78d2;
    text-decoration: underline;
    cursor: pointer;
    padding: 0;
    font-family: inherit;
    font-size: inherit;
  }

  .example-url-button:hover {
    color: #65c9a4;
  }

  /* Existing styles */
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
    z-index: 3; /* 增加z-index值 */
    margin-left: 2rem;
    text-align: left;
    width: 100%; /* Ensure full width */
  }

  .title-group {
    margin-bottom: 0.5rem;
    text-align: left;
    width: 100%; /* Full width container */
  }

  .title-group h1 {
    font-size: 4rem;
    font-weight: bold;
    position: relative;
    background: linear-gradient(
      to right,
      #65c9a4 20%,
      #7e78d2 40%,
      #7e78d2 60%,
      #65c9a4 80%
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
    white-space: normal; /* Allow wrapping */
    text-align: left;
    padding: 0 0 0.15em;
    transform: translateY(-0.05em);
    max-width: 100%; /* Ensure text doesn't overflow */
    overflow-wrap: break-word; /* Break long words if needed */
  }

  .title-group h1:hover {
    filter: drop-shadow(0 0 2px rgba(101, 201, 164, 0.5));
    transform: none;
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
    white-space: normal; /* Enable text wrapping */
    text-align: left;
    overflow: visible;
    max-width: 100%; /* Ensure text doesn't overflow container */
    word-wrap: break-word; /* Allow long words to be broken */
  }

  .subtitle {
    font-size: 1.25rem;
    color: #666;
    line-height: 1.4;
    margin-top: 1.5rem;
    white-space: normal;
    text-align: left;
    max-width: 100%;
    word-wrap: break-word;
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
      white-space: nowrap; /* Keep on one line for large screens */
    }
    .subtitle {
      font-size: 1.875rem;
      white-space: nowrap; /* Keep nowrap for very large screens only */
    }
  }

  /* Add a new breakpoint to handle mid-size screens */
  @media (min-width: 1024px) and (max-width: 1279px) {
    .title-group h2 {
      font-size: 2.75rem;
      white-space: nowrap; /* Ensure it stays on one line for medium-large screens too */
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
    grid-template-rows: auto auto;
    row-gap: 1rem;
    padding: 2rem 0;
    z-index: 1;
    pointer-events: none;
    transform: translateX(0);
    justify-content: end;
    opacity: 1; /* 默认完全显示 */
    transition: opacity 0.3s ease; /* 添加过渡效果 */
  }

  /* 确保文字内容在装饰元素上层 */
  .slogan, .title-group {
    position: relative;
    z-index: 3; /* 增加z-index值，确保文字在装饰元素上方 */
  }
  
  .top-row {
    display: grid;
    grid-template-columns: repeat(2, 160px);
    gap: 0.5rem;
    align-items: start;
    margin: 0;
    padding: 0;
    grid-column: 5 / 7;
    grid-row: 1;
    justify-self: end;
  }

  .second-row {
    display: grid;
    grid-template-columns: 160px;
    gap: 0.5rem;
    align-items: start;
    margin: 0;
    padding: 0;
    grid-column: 6 / 7;
    grid-row: 2;
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
    animation: slowRotate 5s linear infinite;
  }

  .second-row .element:hover {
    transform: rotate(-15deg) scale(1.1);
    animation: slowRotate 5s linear infinite;
  }
  
  /* 大屏幕：正常显示装饰元素 */
  @media (min-width: 1281px) {
    .decorative-elements {
      opacity: 1;
    }
  }

  /* 响应式调整 */
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
  
  /* 中等屏幕：淡化装饰元素 */
  @media (max-width: 1280px) {
    .decorative-elements {
      width: 600px;
      grid-template-columns: repeat(6, 100px);
      opacity: 0.6; /* 淡化效果 */
      transform: translateX(0);
      row-gap: 0.75rem;
      justify-content: end;
    }
    
    .title-group h2,
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
      width: 90%; /* Constrain width for better readability */
    }
    
    .decorative-elements {
      opacity: 0.4; /* 更加淡化 */
      transform: translateX(0) scale(0.9);
      row-gap: 0.5rem;
    }
    
    .title-group h1 {
      font-size: 3rem;
      white-space: normal; /* Allow wrapping */
    }
    
    .title-group h2 {
      font-size: 2.5rem;
      white-space: normal; /* Allow wrapping */
      hyphens: auto; /* Enable hyphenation */
    }
    
    .subtitle {
      font-size: 1.25rem;
      white-space: normal;
      overflow-wrap: break-word;
      max-width: 100%;
    }
    
    /* 从992px移至这里的样式 */
    .emotions {
      gap: 30px;
    }
    
    .emoji-img {
      width: 140px;
      height: 140px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 150px;
      height: 150px;
    }
    
    .banner-content {
      padding: 0 3rem;
    }
    
    .banner-title {
      font-size: 2rem;
    }
    
    .decorative-elements {
      opacity: 0.25; /* 更低的透明度 */
      transform: scale(0.8);
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
      max-width: 95%;
      width: 95%;
    }

    .title-group {
      width: 100%;
    }

    .title-group h1 {
      font-size: 2.5rem;
      white-space: normal;
      max-width: 100%; /* Enforce max width */
      display: block; /* Change to block for full width */
      overflow-wrap: break-word; /* Break words if needed */
      hyphens: auto; /* Enable hyphenation */
    }
    
    .title-group h2 {
      font-size: 2rem;
      white-space: normal;
      max-width: 100%;
      overflow-wrap: break-word;
      display: block; /* Change to block for full width */
    }
    
    .subtitle {
      font-size: 1.125rem;
      white-space: normal;
      overflow-wrap: break-word;
      max-width: 100%;
    }
    
    .emotions {
      gap: 20px;
      justify-content: space-evenly;
    }
    
    .emoji-option {
      min-width: 110px;
      margin-bottom: 1rem;
    }
    
    .emoji-img {
      width: 120px;
      height: 120px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 130px;
      height: 130px;
    }
    
    .emoji-label {
      font-size: 1rem;
      margin-top: 8px;
    }

    /* Bell size adjustments for 768px */
    .feeling-box {
      margin-top: 70px; 
    }

    .feeling-box h2 {
      font-size: 28px; 
      margin-top: 50px; 
      margin-bottom: 25px;
    }

    .decorative-elements {
      opacity: 0.1;
      transform: translateX(0) scale(0.8);
    }
    
    .comparison-content {
      flex-direction: column;
      gap: 1.5rem;
    }

    .banner-section {
      padding-top: 2rem;
      padding-bottom: 3rem;
      height: auto;
      min-height: 660px;
    }
    
    .banners-container {
      height: auto;
      min-height: 660px;
    }

    .banner-title {
      font-size: 1.8rem;
    }

    .constructive h3, .cyberbullying h3 {
      font-size: 1.3rem;
    }

    .constructive p, .cyberbullying p {
      font-size: 1rem;
    }
    
    .banner-nav {
      width: 40px;
      height: 40px;
    }
    
    .prev-banner {
      left: 10px;
    }
    
    .next-banner {
      right: 15px;
    }
  }
  
  @media (max-width: 640px) {
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

    .decorative-elements {
      opacity: 0;
      transform: translateX(0) scale(0.7);
    }

    .title-group h1 {
      font-size: 3rem;
      white-space: nowrap;
    }
    
    .title-group h2 {
      font-size: 2rem;
      white-space: normal;
    }
    
    .subtitle {
      font-size: 1rem;
      white-space: normal;
    }
    
    .emotions {
      gap: 15px;
    }
    
    .emoji-img {
      width: 100px;
      height: 100px;
      padding: 4px;
      border: 3px solid transparent;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 120px;
      height: 120px;
    }
    
    .emoji-img.selected {
      border: 3px solid rgb(212, 238, 90);
      box-shadow: 0 0 0 5px rgba(212, 238, 90, 0.4);
    }
    
    .emoji-label {
      font-size: 0.9rem;
      margin-top: 6px;
    }
    
    .banner-content {
      padding: 0 1.5rem;
    }
    
    .banner-title {
      font-size: 1.5rem;
    }
    
    .constructive, .cyberbullying {
      padding: 1.5rem;
    }
    
    .banner-nav {
      width: 36px;
      height: 36px;
    }
    
    .arrow-icon {
      font-size: 16px;
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
      width: 100%;
    }
    
    .slogan {
      width: 95%;
      margin-left: 1rem;
      padding-right: 1rem;
    }
    
    .title-group {
      width: 95%;
    }

    .title-group h1 {
      font-size: 2.5rem;
      white-space: normal;
      max-width: 100%;
      line-height: 1.2;
      display: block;
      word-break: break-word;
    }
    
    .title-group h2 {
      font-size: 1.5rem;
      line-height: 1.3;
      white-space: normal;
      max-width: 100%;
      display: block;
      word-break: break-word;
    }

    .subtitle {
      white-space: normal;
      overflow-wrap: break-word; 
      max-width: 100%;
      font-size: 1rem;
      line-height: 1.3;
    }
    
    .emotions {
      gap: 10px;
      flex-wrap: wrap;
      justify-content: space-evenly;
    }
    
    .emoji-option {
      min-width: 70px;
      margin-bottom: 1.5rem;
    }
    
    .emoji-img {
      width: 80px;
      height: 80px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 100px;
      height: 100px;
      margin-top: 0;
    }
    
    .emoji-label {
      font-size: 0.85rem;
      margin-top: 5px;
      white-space: nowrap;
    }
  }

  /* Feeling box styling */
  .feeling-box {
    border: 2px solid black;
    padding: 2rem 1rem 1rem;
    border-radius: 24px;
    width: 90%;
    max-width: 1200px;
    margin: 100px auto 4rem;  /* Increased from 60px to 100px */
    position: relative;
    background-color: #fff;
    background-image: linear-gradient(to bottom, #fff, rgba(255, 255, 255, 0.95));
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
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
    margin-bottom: 40px;
    letter-spacing: 1px;
  }

  @media (max-width: 768px) {
    .feeling-box h2 {
      font-size: 28px; 
      margin-top: 50px; 
      margin-bottom: 35px;
    }
  }

  @media (max-width: 576px) {
    .feeling-box h2 {
      font-size: 24px;
      margin-top: 45px;
      margin-bottom: 30px;
    }
  }

  @media (max-width: 480px) {
    .feeling-box h2 {
      font-size: 22px;
      margin-top: 40px;
      margin-bottom: 25px;
      padding: 0 10px;
    }
  }

  .emotions {
    display: flex;
    justify-content: center;
    gap: 48px;
    margin: 2rem 0 1.5rem;
    flex-wrap: wrap;
  }

  .emoji-option {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: auto;
    min-width: 90px;
    margin-bottom: 1rem;
  }

  .emoji-img {
    width: 180px;
    height: 180px;
    object-fit: contain;
    transition: 0.25s ease;
    cursor: pointer;
    border-radius: 50%;
    padding: 8px;
    border: 5px solid transparent;
  }

  .emoji-img:hover {
    transform: scale(1.15);
    /* 移除以下光圈效果 */
    /* box-shadow: 0 0 20px rgba(212, 238, 90, 0.6); */
  }

  .emoji-img.selected {
    border-radius: 50%;
    border: 5px solid rgb(212, 238, 90);
    box-shadow: 0 0 0 8px rgba(212, 238, 90, 0.4);
  }

  .emoji-option:last-child .emoji-img {
    width: 200px;
    height: 200px;
    margin-top: -12px;
  }

  /* Emoji label styles */
  .emoji-label {
    margin-top: 10px;
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
    text-align: center;
    white-space: nowrap;
  }

  /* Hide dot styles and don't display dots */
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
    display: flex;
    justify-content: center;
    margin: 2rem auto 4rem;
  }

  .help-button {
    padding: 0.75rem 2rem;
    background-color: #7e78d2;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .help-button:hover {
    background-color: #65c9a4;
    transform: translateY(-2px);
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 100vw;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    backdrop-filter: blur(8px);
    animation: fadeIn 0.3s ease;
  }
  
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  /* Popup styling */
  .popup {
    background: linear-gradient(135deg, #7e78d2 0%, #9b94e3 100%);
    padding: 2.5rem;
    border-radius: 20px;
    max-width: 600px;
    width: 90%;
    text-align: center;
    box-shadow: 0 8px 32px rgba(126, 120, 210, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transform: translateY(0);
    animation: slideUp 0.4s ease;
  }
  
  @keyframes slideUp {
    from { transform: translateY(30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }

  .popup h2 {
    margin-top: 0;
    color: white;
    font-size: 1.8rem;
    margin-bottom: 2rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    line-height: 1.4;
  }
  
  .positive-popup {
    background: linear-gradient(135deg, #f5f3ff, #ede9fe);
    box-shadow: 0 8px 32px rgba(126, 120, 210, 0.25);
    border-radius: 20px;
    border: 1px solid rgba(126, 120, 210, 0.2);
    color: #4c1d95;
  }
  
  .positive-popup h2 {
    color: #6d28d9;
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 2.5rem;
    line-height: 1.3;
    text-shadow: none;
  }
  
  .buttons {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 2.5rem;
    flex-wrap: wrap;
  }
  
  .buttons button {
    padding: 0.9rem 2rem;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 30px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    backdrop-filter: blur(5px);
    min-width: 180px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  .buttons button:first-child {
    background: rgba(255, 255, 255, 0.95);
    color: #7e78d2;
    border-color: transparent;
  }
  
  .buttons button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  }
  
  .buttons button:first-child:hover {
    background: white;
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.3);
  }
  
  .positive-popup .buttons button {
    background: linear-gradient(90deg, #7e78d2, #9b94e3);
    color: white;
    font-weight: 700;
    padding: 1rem 2.5rem;
    font-size: 1.2rem;
    border-radius: 50px;
    box-shadow: 0 4px 15px rgba(126, 120, 210, 0.4);
    border: none;
    text-transform: uppercase;
    letter-spacing: 1px;
    min-width: 200px;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .positive-popup .buttons button:hover {
    background: linear-gradient(90deg, #9b94e3, #7e78d2);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(126, 120, 210, 0.5);
  }
  
  @media (max-width: 768px) {
    .popup {
      padding: 2rem;
      width: 85%;
    }
    
    .popup h2 {
      font-size: 1.5rem;
      margin-bottom: 1.5rem;
    }
    
    .buttons {
      flex-direction: column;
      gap: 1rem;
    }
    
    .buttons button {
      width: 100%;
      padding: 0.8rem 1.5rem;
      font-size: 1rem;
      min-width: unset;
    }
  }
  
  @media (max-width: 480px) {
    .popup {
      padding: 1.5rem;
      width: 90%;
    }
    
    .popup h2 {
      font-size: 1.3rem;
      margin-bottom: 1.2rem;
    }
  }

  /* Add styles for InteractiveHoverButton component */
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

  /* CSS to disable hover effect for specific cards */
  .process-card.no-hover:hover {
    transform: translateY(0); /* Reset transform */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1); /* Reset to original box-shadow */
  }

  .process-card.no-hover:hover .card-icon {
    transform: scale(1); /* Reset icon transform */
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
    margin: 0 auto 6rem;
  }

  .analysis-container {
    width: 100%;
    text-align: center;
    background-color: #fff;
    background-image: linear-gradient(to bottom, #fff, rgba(255, 255, 255, 0.98));
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(230, 239, 182, 0.3);
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
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.3s;
  }

  .youtube-input:focus {
    border-color: #65c9a4;
    box-shadow: 0 0 0 2px rgba(101, 201, 164, 0.2);
  }

  .analyze-button {
    padding: 0.75rem 1.5rem;
    background-color: #7e78d2;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .analyze-button:not(:disabled):hover {
    background-color: #65c9a4;
    transform: translateY(-2px);
  }

  .analyze-button:disabled {
    background-color: #b4b0e2;
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
    text-align: left;
  }

  .video-info-item {
    margin: 0.5rem 0;
    color: #333;
    font-size: 1.1rem;
    padding: 0.5rem 0;
  }
  
  /* Disclaimer Section */
  .disclaimer-section {
    background-color: #fff8e1;
    border: 1px solid #ffecb3;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 2rem;
  }
  
  .disclaimer-icon {
    font-size: 2rem;
    margin-top: 0.25rem;
  }
  
  .disclaimer-content h4 {
    font-size: 1.3rem;
    color: #856404;
    margin-top: 0;
    margin-bottom: 1rem;
    font-weight: 700;
    text-align: center;
    white-space: nowrap;
  }
  
  .disclaimer-list {
    padding-left: 1.5rem;
    margin: 0;
    text-align: left;
  }
  
  .disclaimer-list li {
    color: #856404;
    margin-bottom: 0.75rem;
    line-height: 1.4;
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
    padding: 2rem;
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
    line-height: 1.8;
    text-align: left;
    font-size: 1.05rem;
    padding: 1.5rem;
  }

  .strategy-content br {
    margin-bottom: 0.5rem;
    display: block;
    content: "";
  }
  
  .strategy-content strong {
    color: #333;
    font-weight: 700;
    font-size: 1.1rem;
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

  /* Add section divider styles */
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

  .results-container {
    margin-top: 2rem;
    padding: 2rem;
    background-color: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
  }

  .analysis-source-tabs {
    display: flex;
    gap: 1rem;
  }

  .tab-button {
    padding: 0.75rem 1rem;
    border: none;
    border-radius: 8px;
    background-color: #f0f0f0;
    color: #333;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .tab-button.active {
    background-color: #6c63ff;
    color: white;
  }

  .analysis-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
  }

  .sentiment-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .sentiment-charts {
    display: flex;
    justify-content: space-around;
    gap: 1rem;
  }

  .chart-container {
    text-align: center;
  }

  .chart-container h4 {
    font-size: 1.4rem;
    margin-bottom: 0.5rem;
    color: #333;
  }

  .chart-container h5 {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 1rem;
  }

  .toxicity-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .toxicity-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .toxicity-charts {
    display: flex;
    justify-content: space-around;
    gap: 1rem;
  }

  .toxicity-chart {
    text-align: center;
  }

  .toxicity-label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5rem;
  }

  .toxicity-type {
    font-size: 0.9rem;
    color: #555;
  }

  .toxicity-count {
    font-size: 1.2rem;
    font-weight: 700;
    color: #333;
  }

  .strategies-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .strategies-content {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .examples-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .examples-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .example-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  }

  .example-comment,
  .example-response {
    background-color: #fff;
    border-radius: 8px;
    padding: 0.75rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .example-comment h4,
  .example-response h4 {
    font-size: 1rem;
    margin-bottom: 0.25rem;
    color: #333;
  }

  .example-comment p,
  .example-response p {
    margin: 0;
    color: #555;
    line-height: 1.5;
  }

  /* 响应式设计: 确保表情在各种屏幕尺寸下都有合适的大小 */
  @media (max-width: 1200px) {
    .emotions {
      gap: 40px;
    }
    
    .emoji-img {
      width: 170px;
      height: 170px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 190px;
      height: 190px;
    }
  }

  @media (max-width: 1024px) {
    /* 从992px移至这里的样式 */
    .emotions {
      gap: 30px;
    }
    
    .emoji-img {
      width: 140px;
      height: 140px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 160px;
      height: 160px;
    }
  }
  
  @media (max-width: 768px) {
    .emotions {
      gap: 20px;
      justify-content: space-evenly;
    }
    
    .emoji-option {
      min-width: 110px;
      margin-bottom: 1rem;
    }
    
    .emoji-img {
      width: 120px;
      height: 120px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 140px;
      height: 140px;
    }
  }
  
  @media (max-width: 640px) {
    .emoji-img {
      width: 100px;
      height: 100px;
      padding: 4px;
      border: 3px solid transparent;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 120px;
      height: 120px;
    }
  }
  
  @media (max-width: 480px) {
    .emoji-img {
      width: 80px;
      height: 80px;
    }
    
    .emoji-option:last-child .emoji-img {
      width: 100px;
      height: 100px;
      margin-top: 0;
    }
  }

  /* Banner Section Styles */
  .banners-container {
    width: 100%;
    margin: 0 0 5rem;
    position: relative;
    height: 400px; /* Fixed height to prevent content shifting */
    overflow: hidden;
  }
  
  .banner-section {
    position: absolute; /* Position absolutely within container */
    padding: 3rem 0;
    border-radius: 0;
    overflow: hidden;
    width: 100%;
    box-shadow: none;
    border: none;
    transition: all 0.3s ease;
    top: 0;
    left: 0;
    height: 100%;
  }
  
  .banner-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  .banner-title {
    font-size: 1.8rem;
    color: #333;
    margin-bottom: 1.5rem;
    font-weight: 600;
    text-align: center;
  }
  
  .comparison-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin: 0 auto;
    max-width: 950px;
  }
  
  .constructive, .cyberbullying {
    padding: 1.8rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    position: relative;
    transition: transform 0.3s ease;
    min-height: 200px;
    display: flex;
    flex-direction: column;
  }
  
  .constructive {
    background: linear-gradient(135deg, #f1f9ea, #e5f4d5);
    border-left: 5px solid #65c9a4;
    color: #2c4a30;
  }
  
  .constructive::before {
    content: "👍";
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 1.6rem;
    opacity: 0.2;
  }
  
  .cyberbullying {
    background: linear-gradient(135deg, #fff1f0, #ffe4e1);
    border-left: 5px solid #ff7d6e;
    color: #742f29;
  }
  
  .cyberbullying::before {
    content: "👎";
    position: absolute;
    top: 15px;
    right: 15px;
    font-size: 1.6rem;
    opacity: 0.2;
  }
  
  .constructive h3, .cyberbullying h3 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    font-weight: 700;
    position: relative;
    display: inline-block;
    padding-bottom: 0.5rem;
  }
  
  .constructive h3 {
    color: #1a7652;
  }
  
  .constructive h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: #65c9a4;
    border-radius: 1.5px;
  }
  
  .cyberbullying h3 {
    color: #d44333;
  }
  
  .cyberbullying h3::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: #ff7d6e;
    border-radius: 1.5px;
  }
  
  .constructive p, .cyberbullying p {
    line-height: 1.6;
    font-size: 1.1rem;
  }
  
  .constructive:hover, .cyberbullying:hover {
    transform: translateY(-3px);
  }
  
  .banner-nav {
    background-color: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(230, 239, 182, 0.3);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    z-index: 5;
  }
  
  .prev-banner {
    left: 20px;
  }
  
  .next-banner {
    right: 20px;
  }
  
  .banner-nav:hover {
    background-color: #65c9a4;
    color: white;
    transform: translateY(-50%) scale(1.1);
  }
  
  .arrow-icon {
    font-size: 1rem;
    display: inline-block;
  }
  
  /* Banner pagination dots */
  .banner-pagination {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 2rem;
  }
  
  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ddd;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .dot.active {
    background-color: #65c9a4;
    transform: scale(1.3);
  }

  @media (max-width: 992px) {
    .banner-content {
      padding: 0 3rem;
    }
    
    .banner-title {
      font-size: 2rem;
    }
  }

  @media (max-width: 768px) {
    .comparison-content {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }

    .banner-section {
      padding-top: 2rem;
      padding-bottom: 3rem;
      height: auto;
      min-height: 660px;
    }
    
    .banners-container {
      height: auto;
      min-height: 660px;
    }

    .banner-title {
      font-size: 1.8rem;
    }

    .constructive h3, .cyberbullying h3 {
      font-size: 1.3rem;
    }

    .constructive p, .cyberbullying p {
      font-size: 1rem;
    }
    
    .banner-nav {
      width: 40px;
      height: 40px;
    }
    
    .prev-banner {
      left: 10px;
    }
    
    .next-banner {
      right: 10px;
    }
  }
  
  @media (max-width: 576px) {
    .banner-content {
      padding: 0 1.5rem;
    }
    
    .banner-title {
      font-size: 1.5rem;
    }
    
    .constructive, .cyberbullying {
      padding: 1.5rem;
    }
    
    .banner-nav {
      width: 36px;
      height: 36px;
    }
    
    .arrow-icon {
      font-size: 16px;
    }
  }

  /* Transition animations for banners */
  .slide-fade-enter-active,
  .slide-fade-leave-active {
    transition: transform 0.6s cubic-bezier(0.22, 1, 0.36, 1);
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    backface-visibility: hidden;
    will-change: transform;
  }

  .slide-fade-enter-from {
    transform: translateX(100%);
    opacity: 1;
  }

  .slide-fade-leave-to {
    transform: translateX(-100%);
    opacity: 1;
  }

  .slide-fade-enter-to,
  .slide-fade-leave-from {
    transform: translateX(0);
    opacity: 1;
  }

  /* Positive popup styling */
  .positive-popup {
    border: none;
    background: linear-gradient(135deg, #f0f8ff, #f5fbff);
    box-shadow: 0 8px 32px rgba(79, 195, 247, 0.3);
    border-radius: 16px;
    transform: scale(1.02);
    transition: all 0.3s ease;
  }

  .positive-popup h2 {
    color: #42a5f5;
    font-size: 1.8rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  }
  
  /* Remove the h2:after pseudo-element for positive-popup */
  .positive-popup h2:after {
    display: none;
  }

  .positive-popup .buttons button {
    background: linear-gradient(90deg, #29b6f6, #4fc3f7);
    color: white;
    font-weight: 700;
    padding: 12px 28px;
    font-size: 1.1rem;
    border-radius: 30px;
    box-shadow: 0 4px 15px rgba(41, 182, 246, 0.3);
    border: none;
  }

  .positive-popup .buttons button:hover {
    background: linear-gradient(90deg, #4fc3f7, #29b6f6);
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(41, 182, 246, 0.4);
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
      width: 100%;
    }
    
    .slogan {
      width: 95%;
      margin-left: 1rem;
      padding-right: 1rem;
    }
    
    .title-group {
      width: 95%;
    }

    .title-group h1 {
      font-size: 2rem;
      white-space: normal;
      max-width: 100%;
      line-height: 1.2;
      display: block;
      word-break: break-word;
    }
    
    .title-group h2 {
      font-size: 1.5rem;
      line-height: 1.3;
      white-space: normal;
      max-width: 100%;
      display: block;
      word-break: break-word;
    }

    .subtitle {
      white-space: normal;
      overflow-wrap: break-word; 
      max-width: 100%;
      font-size: 0.875rem;
      line-height: 1.3;
    }
  }

  /* Common section styles */
  .section-title,
  .section-subtitle {
    position: relative;
    z-index: 2;
  }

  /* Banner Section Title Styling */
  .banner-section-title-container {
    text-align: center;
    margin: 3rem auto 2rem;
    position: relative;
  }

  .banner-section-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #333;
    display: inline-block;
    position: relative;
    margin: 0 auto;
    padding-bottom: 0.5rem;
  }

  .banner-section-title::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #7e78d2, #65c9a4);
    border-radius: 2px;
  }

  @media (max-width: 768px) {
    .banner-section-title {
      font-size: 2.2rem;
    }
  }

  @media (max-width: 480px) {
    .banner-section-title {
      font-size: 1.8rem;
    }
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

  section {
    padding: 3rem 0 5rem;
    position: relative;
    border-bottom: none;
    margin-bottom: 5rem;
  }

  section:last-child {
    margin-bottom: 3rem;
  }

  section:not(:last-child)::after {
    display: none;
  }

  .next-banner {
    right: 15px;
  }
  
  .banner-nav:hover {
    background-color: #65c9a4;
    color: white;
    transform: translateY(-50%) scale(1.1);
  }
  
  .arrow-icon {
    font-size: 1rem;
    display: inline-block;
  }
  
  /* Banner pagination dots */
  .banner-pagination {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-top: 2rem;
  }
  
  .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ddd;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .dot.active {
    background-color: #65c9a4;
    transform: scale(1.3);
  }

  @media (max-width: 992px) {
    .banner-content {
      padding: 0 3rem;
    }
    
    .banner-title {
      font-size: 2rem;
    }
  }

  .comment-icon {
    font-size: 2rem;
    margin-top: 0.25rem;
  }
  
  /* Comments Section Title */
  .comments-section-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 2rem 0;
    color: #333;
    text-align: center;
    padding: 1.5rem 0 1rem;
    position: relative;
  }
  
  .comments-section-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background-color: #e0e0e0;
  }

  /* Add rotation animation */
  @keyframes slowRotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  .rotating {
    animation: slowRotate 30s linear infinite;
  }
  </style>


