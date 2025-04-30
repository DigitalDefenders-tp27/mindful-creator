<template>
  <div class="comment-script-container">
    <h1 class="main-title">Comments Response Scripts</h1>
    <div class="highlight-box">Negative Comment Type</div>
    <p class="click-hint">(Click on a comment type to see the response strategy)</p>

    <div class="gauge-grid">
      <div 
        v-for="(item, idx) in gaugeData" 
        :key="idx" 
        class="gauge-item" 
        @click="selectedIndex = idx"
        :class="{ active: selectedIndex === idx }">
        <div class="gauge-wrapper">
          <HalfDonutChart :percentage="item.value" :color="item.color" />
          <div class="percent-text">{{ item.value }}%</div>
        </div>
        <p class="label">{{ item.label }}</p>
      </div>
    </div>

    <div 
      v-if="selectedType" 
      class="strategy-section">
      <h2 class="strategy-title">Step-by-Step Response Strategy</h2>

      <div class="nav-arrows">
        <span class="arrow" @click="prevType">&lt;</span>

        <div class="steps-grid">
          <div v-for="(step, index) in selectedType.strategy" :key="index" class="step-box">
            <strong>{{ step.title }}</strong>
            <p>{{ step.text }}</p>
            <div class="step-num">{{ index + 1 }}</div>
          </div>
        </div>

        <span class="arrow" @click="nextType">&gt;</span>
      </div>

      <div class="qa-box">
        <p><strong>Q:</strong> "{{ selectedType.q }}"</p>
        <p><strong>A:</strong> "{{ selectedType.a }}"</p>
      </div>
    </div>
  </div>

  <!-- Floating Chatbot Button and Window -->

  <div class="chatbot-container" @click="toggleChat">
    💬
  </div>

  <div v-if="showChat" class="chat-window">
    <div class="chat-header">Mindful Assistant 🤖</div>
    <div class="chat-messages">
      <div v-for="(msg, idx) in chatHistory" :key="idx" :class="msg.role">{{ msg.text }}</div>
    </div>
    <div class="chat-input">
      <input v-model="userMessage" @keyup.enter="sendMessage" placeholder="Ask something..." />
      <button @click="sendMessage">Send</button>
    </div>

    <!-- ───── NEW dynamic results; appears only when store has data ───── -->
  <section
    v-if="hasData"
    class="analysis-section mt-16 p-6 bg-white rounded-lg shadow max-w-5xl mx-auto"
  >
    <!-- ① Original comment ---------------------------------------------------->
    <div class="mb-8 p-4 bg-gray-50 rounded border">
      <p class="font-medium mb-1">Original Comment</p>
      <p class="whitespace-pre-wrap">{{ data.analysis.input_text }}</p>
    </div>

    <!-- ② Sentiment pie ------------------------------------------------------->
    <div class="mb-12">
      <ApexChart
        type="pie"
        height="320"
        :series="sentSeries"
        :options="sentOptions"
      />
    </div>

    <!-- ③ Toxicity gauges ----------------------------------------------------->
    <div class="grid grid-cols-2 md:grid-cols-3 gap-8 mb-12">
      <div
        v-for="(label, key) in toxicityLabels"
        :key="key"
        class="text-center"
      >
        <HalfDonutChart
          :percentage="(toxicity[key].probability * 100).toFixed(1)"
          :color="toxicityColors[key]"
        />
        <p class="mt-2 font-medium">{{ label }}</p>
        <p class="text-sm">
          {{ (toxicity[key].probability * 100).toFixed(1) }} % 
          ({{ toxicity[key].prediction }})
        </p>
      </div>
    </div>

    <!-- ④ Strategy text ------------------------------------------------------->
    <div class="p-4 bg-gray-50 rounded">
      <h3 class="font-medium mb-2">Response Strategy</h3>
      <p class="whitespace-pre-wrap">{{ strategy }}</p>
    </div>
  </section>
  </div>

</template>

<script setup>

// ─── New: import Pinia store & ApexCharts for analysis display ─────────
import { useAnalysisStore } from '@/stores/analysisStore'
import ApexChart from 'vue3-apexcharts'
import { useRoute } from 'vue-router'

/* reactive refs pulled via storeToRefs isn't required because we don't
   destructure – we keep the whole `store` object */
const hasData  = computed(() => store.hasData)
const data     = computed(() => store.data ?? {})            // safe default
const toxicity = computed(() => data.value.analysis?.toxicity_details ?? {})

const route = useRoute()
const store = useAnalysisStore()
const showAnalysisResults = computed(() => Boolean(store.data?.analysis))

const showDynamicResults = computed(() => {
  return route.query.fromAnalysis === 'true' && store.data !== null
})

const analyzedComment = computed(() => {
  return store.data?.analysis?.input_text || 'No comment available'
})

const responseStrategy = computed(() => {
  if (!store.data?.strategy) return 'No strategy generated'
  return typeof store.data.strategy === 'string' 
    ? store.data.strategy 
    : JSON.stringify(store.data.strategy, null, 2)
})

const toxicityData = computed(() => {
  return store.data?.analysis?.toxicity_details || {}
})


// Prepare the pie-chart series & options
const sentSeries = computed(() => {
  if (!hasData.value) return []

  const conf = Number(data.value.analysis.sentiment_confidence) || 0
  return [ +(conf * 100).toFixed(1), +(100 - conf * 100).toFixed(1) ]
})
const sentOptions = computed(() => ({
  labels: [
    data.value.analysis?.predicted_sentiment ?? 'Sentiment',
    'Other'
  ],
  legend: { position: 'bottom' }
}))

// Toxicity labels & colors
const toxicityLabels = {
  toxic:         'Toxic',
  severe_toxic:  'Severe Toxic',
  obscene:       'Obscene',
  threat:        'Threat',
  insult:        'Insult',
  identity_hate: 'Identity Hate'
}

const getToxicityColor = (key) =>
  ({
    toxic:         '#EF5350',
    severe_toxic:  '#D32F2F',
    obscene:       '#FF7043',
    threat:        '#AB47BC',
    insult:        '#FFA726',
    identity_hate: '#7E57C2'
  }[key] || '#888')

/* ------------------------------------------------------------------------
   Strategy text
   -----------------------------------------------------------------------*/
const strategy = computed(() =>
  typeof data.value.strategy === 'string'
    ? data.value.strategy
    : JSON.stringify(data.value.strategy, null, 2)
)

// ─────────────────────────────────────────────────────────────────────

import { ref, computed, onMounted } from 'vue'
import HalfDonutChart from '@/components/ui/HalfDonutChart.vue'
import axios from 'axios'

const showChat = ref(false)
const userMessage = ref('')
const chatHistory = ref([])

const toggleChat = () => {
  showChat.value = !showChat.value
}

const sendMessage = async () => {
  if (userMessage.value.trim()) {
    chatHistory.value.push({ role: 'user', text: userMessage.value })
    try {
      const res = await axios.post('https://mindful-creator-production.up.railway.app/api/chatbot', {
        message: userMessage.value,
      })
      chatHistory.value.push({ role: 'bot', text: res.data.reply })
    } catch (err) {
      chatHistory.value.push({ role: 'bot', text: 'Sorry, I had trouble replying.' })
    }
    userMessage.value = ''
  }
}

const gaugeData = [
  {
    label: 'Accusatory Comments',
    value: 40,
    color: '#FF3B30',
    strategy: [
      {
        title: 'Acknowledge the criticism',
        text: 'Validate their perspective and thank them for the feedback',
      },
      {
        title: 'Provide brief context',
        text: 'Share relevant information without being defensive',
      },
      {
        title: 'Offer a positive path forward',
        text: 'Suggest a constructive next step or solution',
      },
    ],
    q: 'This is such a biased take. You only presented one perspective and completely ignored the other side of the argument. Disappointing content.',
    a: 'Tks🙏 Fair point on balance – def working with time limits but that's on me. Planning a follow-up with more perspectives soon! Any recs for sources? Always looking to improve! 💯',
  },
  {
    label: 'Emotional Comments',
    value: 25,
    color: '#FFA726',
    strategy: [
      {
        title: 'Acknowledge their emotions',
        text: 'Recognise the intensity and validate their feelings',
      },
      {
        title: 'Stay calm and neutral',
        text: 'Respond without escalating the emotional tone',
      },
      {
        title: 'Invite further conversation',
        text: 'Show openness to hearing more constructively',
      },
    ],
    q: "Why do you always talk like you know everything? This is so annoying!",
    a: "Appreciate you chiming in! Definitely not my intention to come off that way – I'll keep it more conversational next time 🙏",
  },
  {
    label: 'Misunderstanding Comments',
    value: 15,
    color: '#FF7043',
    strategy: [
      {
        title: 'Clarify gently',
        text: 'Provide accurate info without implying fault',
      },
      {
        title: 'Use simple language',
        text: 'Keep the explanation clear and concise',
      },
      {
        title: 'Offer resources',
        text: 'Suggest links or follow-up posts for context',
      },
    ],
    q: "Wait, are you saying everyone should quit their job and do this instead?",
    a: "Not quite! I meant this approach works *for some* – not one-size-fits-all. Thanks for pointing that out, I'll make it clearer!",
  },
  {
    label: 'Attacking Comments',
    value: 10,
    color: '#66BB6A',
    strategy: [
      {
        title: 'Avoid engaging emotionally',
        text: 'Don't match their tone or insults',
      },
      {
        title: 'Set boundaries',
        text: 'Politely assert your intent to keep it respectful',
      },
      {
        title: 'Redirect to the topic',
        text: 'Bring focus back to the content or idea',
      },
    ],
    q: "You're such a clown. This is garbage advice!",
    a: "Let's keep it constructive here. Open to hearing thoughtful counterpoints if you have suggestions!",
  },
  {
    label: 'Constructive Comments',
    value: 10,
    color: '#81C784',
    strategy: [
      {
        title: 'Appreciate the input',
        text: 'Thank them for thoughtful feedback',
      },
      {
        title: 'Engage with the idea',
        text: 'Build upon or reflect on their suggestion',
      },
      {
        title: 'Show willingness to act',
        text: 'Indicate any upcoming improvements or plans',
      },
    ],
    q: "I think this could be stronger if you added more sources.",
    a: "Love that suggestion! I'm adding more citations in the next update – stay tuned and feel free to share any links!",
  },
]

const selectedIndex = ref(0)
const selectedType = computed(() => gaugeData[selectedIndex.value])

function prevType() {
  selectedIndex.value = (selectedIndex.value - 1 + gaugeData.length) % gaugeData.length
}

function nextType() {
  selectedIndex.value = (selectedIndex.value + 1) % gaugeData.length
}
defineExpose({ ApexChart
})

</script>

<style scoped>
.comment-script-container {
  text-align: center;
  padding: 5rem 1rem 2rem;
  background: linear-gradient(to bottom, #fffde7, transparent);
}

.main-title {
  font-size: 2.4rem;
  font-weight: 800;
  margin-bottom: 0.6rem;
  color: #000;
}

.highlight-box {
  background-color: #e4f052;
  display: inline-block;
  padding: 0.4rem 1.2rem;
  border-radius: 6px;
  font-weight: 700;
  margin-bottom: 0.2rem;
  font-size: 1.1rem;
}

.click-hint {
  font-size: 0.9rem;
  color: #444;
  margin-bottom: 2.5rem;
}

.gauge-grid {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 3rem;
}

.gauge-item {
  cursor: pointer;
  text-align: center;
  width: 160px;
  transition: transform 0.2s;
}

.gauge-item:hover {
  transform: scale(1.05);
}

.gauge-item.active .label {
  color: #1e88e5;
}

.gauge-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
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
}

.strategy-section {
  margin-top: 4rem;
}

.strategy-title {
  font-size: 1.6rem;
  font-weight: 800;
  margin-bottom: 2rem;
  color: #1e293b;
}

.nav-arrows {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.arrow {
  font-size: 2rem;
  cursor: pointer;
  font-weight: bold;
  padding: 0 1rem;
  user-select: none;
}

.steps-grid {
  display: flex;
  justify-content: center;
  gap: 2rem;
  flex-wrap: wrap;
}

.step-box {
  background-color: #e4f052;
  border-radius: 16px;
  padding: 1rem 1rem 0.8rem;
  width: 180px;
  font-weight: 600;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  min-height: 200px;
}

.step-box p {
  margin-top: 0.5rem;
  font-weight: normal;
  font-size: 0.95rem;
  text-align: center;
}

.step-num {
  margin-top: auto;
  padding-top: 0.8rem;
  font-size: 1.2rem;
  font-weight: bold;
  color: #1e293b;
}

.qa-box {
  border: 2px solid #c4e7c2;
  border-radius: 10px;
  padding: 1rem 1.5rem;
  background-color: #fff;
  max-width: 750px;
  margin: 2rem auto 0;
  text-align: left;
  font-size: 1rem;
}

.qa-box p {
  margin-bottom: 0.5rem;
}

.chatbot-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #2e7d32;
  color: white;
  border-radius: 50%;
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  z-index: 999;
}

.chat-window {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 300px;
  background: white;
  border: 2px solid #2e7d32;
  border-radius: 10px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  max-height: 400px;
}

.chat-header {
  background: #2e7d32;
  color: white;
  padding: 0.5rem;
  font-weight: bold;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem;
}

.chat-input {
  display: flex;
  border-top: 1px solid #ddd;
}

.chat-input input {
  flex: 1;
  padding: 0.4rem;
  border: none;
}

.chat-input button {
  background: #2e7d32;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.user {
  text-align: right;
  margin: 0.3rem 0;
}

.bot {
  text-align: left;
  margin: 0.3rem 0;
}

/* New styles for dynamic results section */
.dynamic-results-section {
  margin: 4rem auto;
  padding: 2rem;
  max-width: 1200px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.results-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1a365d;
  margin-bottom: 2rem;
  text-align: center;
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.comment-display,
.strategy-display,
.sentiment-analysis,
.toxicity-analysis {
  padding: 1.5rem;
  background: #f8fafc;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 1rem;
}

.comment-content,
.strategy-content {
  white-space: pre-wrap;
  line-height: 1.6;
}

.chart-container {
  margin: 0 auto;
  max-width: 380px;
}

.gauges-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-top: 1rem;
}

.toxicity-gauge {
  text-align: center;
}

.toxicity-gauge h4 {
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.toxicity-value {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

/* Responsive adjustments */
@media (min-width: 768px) {
  .results-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .sentiment-analysis,
  .toxicity-analysis {
    grid-column: span 2;
  }
}

@media (min-width: 1024px) {
  .results-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .toxicity-analysis {
    grid-column: span 3;
  }
}

</style>
