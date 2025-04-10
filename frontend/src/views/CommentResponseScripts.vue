<template>
  <div class="comment-script-container">
    <h1 class="main-title">Comments Response Scripts</h1>
    <div class="highlight-box">Negative Comment Type</div>
    <p class="click-hint">(Click on a comment type to see the response strategy)</p>

    <div class="gauge-grid">
      <div v-for="(item, idx) in gaugeData" :key="idx" class="gauge-item" @click="selectedIndex = idx"
        :class="{ active: selectedIndex === idx }">
        <div class="gauge-wrapper">
          <HalfDonutChart :percentage="item.value" :color="item.color" />
          <div class="percent-text">{{ item.value }}%</div>
        </div>
        <p class="label">{{ item.label }}</p>
      </div>
    </div>

    <div v-if="selectedType" class="strategy-section">
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
  </div>

</template>

<script setup>
import { ref, computed } from 'vue'
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
      const res = await axios.post('http://localhost:5000/api/chatbot', {
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
    a: 'Tks🙏 Fair point on balance – def working with time limits but that’s on me. Planning a follow-up with more perspectives soon! Any recs for sources? Always looking to improve! 💯',
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
    a: "Appreciate you chiming in! Definitely not my intention to come off that way – I’ll keep it more conversational next time 🙏",
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
    a: "Not quite! I meant this approach works *for some* – not one-size-fits-all. Thanks for pointing that out, I’ll make it clearer!",
  },
  {
    label: 'Attacking Comments',
    value: 10,
    color: '#66BB6A',
    strategy: [
      {
        title: 'Avoid engaging emotionally',
        text: 'Don’t match their tone or insults',
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
    a: "Let’s keep it constructive here. Open to hearing thoughtful counterpoints if you have suggestions!",
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
    a: "Love that suggestion! I’m adding more citations in the next update – stay tuned and feel free to share any links!",
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

</style>
