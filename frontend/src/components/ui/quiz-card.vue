<template>
  <CardSpotlight 
    class="quiz-card"
    :gradientSize="250"
    gradientColor="#f0f0f0"
    :gradientOpacity="0.5"
    @click="openQuiz"
  >
    <div class="quiz-content">
      <div class="quiz-icon">
        <img src="/src/components/icons/elements/quiz.png" alt="Quiz" class="icon">
      </div>
      <div class="quiz-text">
        <h3>Check Your Understanding</h3>
        <p>Test your knowledge about ethical content creation</p>
      </div>
    </div>
  </CardSpotlight>

  <!-- Quiz Modal -->
  <div v-if="isQuizOpen" class="quiz-modal" @click.self="closeQuiz">
    <div class="quiz-modal-content">
      <div class="quiz-header">
        <h2>Understanding Your Impact</h2>
        <button class="close-button" @click="closeQuiz">&times;</button>
      </div>
      
      <div class="quiz-progress" v-if="!quizCompleted">
        <div class="progress-text">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
      </div>

      <div class="quiz-body">
        <div v-if="!quizCompleted" class="question-container">
          <h3>{{ currentQuestion.question }}</h3>
          <div class="options">
            <button 
              v-for="(option, key) in currentQuestion.options" 
              :key="key"
              :class="['option-button', { 
                'selected': selectedAnswer === key,
                'correct': showAnswer && key === currentQuestion.correctAnswer,
                'incorrect': showAnswer && selectedAnswer === key && key !== currentQuestion.correctAnswer
              }]"
              @click="selectAnswer(key)"
              :disabled="showAnswer"
            >
              {{ key }}. {{ option }}
            </button>
          </div>
          <div class="quiz-controls">
            <button 
              v-if="!showAnswer" 
              class="submit-button"
              @click="checkAnswer"
              :disabled="!selectedAnswer"
            >
              Submit Answer
            </button>
            <button 
              v-else 
              class="next-button"
              @click="nextQuestion"
            >
              {{ isLastQuestion ? 'Finish Quiz' : 'Next Question' }}
            </button>
          </div>
        </div>
        
        <div v-else class="quiz-results">
          <h3>Quiz Completed!</h3>
          <p>Your score: {{ score }} out of {{ questions.length }}</p>
          <button class="restart-button" @click="restartQuiz">Try Again</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { marked } from 'marked'

const isQuizOpen = ref(false)
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const showAnswer = ref(false)
const score = ref(0)
const quizCompleted = ref(false)

// 从 Markdown 文件加载问题 / Load questions from Markdown file
const questions = ref([
  {
    question: "What is digital citizenship?",
    options: {
      A: "Using social media frequently",
      B: "Posting viral content regularly",
      C: "Responsible and ethical participation online",
      D: "Achieving a high follower count"
    },
    correctAnswer: "C"
  },
  {
    question: "How does constructive engagement benefit your audience?",
    options: {
      A: "Encourages misinformation",
      B: "Promotes healthy discussions and understanding",
      C: "Increases follower count",
      D: "Limits audience interaction"
    },
    correctAnswer: "B"
  },
  {
    question: "Transparency with your audience primarily builds:",
    options: {
      A: "Popularity",
      B: "Trust and credibility",
      C: "Higher revenue",
      D: "Increased followers instantly"
    },
    correctAnswer: "B"
  },
  {
    question: "What best illustrates genuine audience engagement?",
    options: {
      A: "Ignoring negative feedback",
      B: "Posting only promotional content",
      C: "Regularly responding sincerely to comments and questions",
      D: "Avoiding personal stories and experiences"
    },
    correctAnswer: "C"
  },
  {
    question: "Ethical content creation involves:",
    options: {
      A: "Posting whatever gets the most views",
      B: "Creating content aligned with core values and integrity",
      C: "Avoiding audience opinions completely",
      D: "Changing values frequently to match trends"
    },
    correctAnswer: "B"
  },
  {
    question: "Accountability in content creation means:",
    options: {
      A: "Ignoring mistakes",
      B: "Shifting blame when errors occur",
      C: "Acknowledging and correcting errors openly",
      D: "Posting controversial content without moderation"
    },
    correctAnswer: "C"
  }
])

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.value.length - 1)

// 添加进度计算 / Add progress calculation
const progressPercentage = computed(() => {
  return (currentQuestionIndex.value / questions.value.length) * 100
})

const openQuiz = () => {
  isQuizOpen.value = true
  resetQuiz()
}

const closeQuiz = () => {
  isQuizOpen.value = false
  resetQuiz()
}

const resetQuiz = () => {
  currentQuestionIndex.value = 0
  selectedAnswer.value = null
  showAnswer.value = false
  score.value = 0
  quizCompleted.value = false
}

const selectAnswer = (answer) => {
  if (!showAnswer.value) {
    selectedAnswer.value = answer
  }
}

const checkAnswer = () => {
  showAnswer.value = true
  if (selectedAnswer.value === currentQuestion.value.correctAnswer) {
    score.value++
  }
}

const nextQuestion = () => {
  if (isLastQuestion.value) {
    quizCompleted.value = true
  } else {
    currentQuestionIndex.value++
    selectedAnswer.value = null
    showAnswer.value = false
  }
}

const restartQuiz = () => {
  resetQuiz()
}
</script>

<style scoped>
/* 卡片容器 / Card Container */
.quiz-card {
  @apply bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-lg;
  @apply flex flex-col items-center text-center;
  @apply transform transition-all duration-300;
  height: 100%;
  border: none;
}

/* 图标样式 / Icon Styles */
.quiz-icon {
  @apply w-16 h-16 mb-4 text-blue-500;
  transition: transform 0.3s ease;
}

/* 图标悬停效果 / Icon Hover Effect */
.quiz-card:hover .quiz-icon {
  transform: scale(1.2);
}

/* 标题样式 / Title Styles */
.quiz-card h3 {
  @apply text-xl font-semibold mb-2 text-neutral-900 dark:text-white;
}

/* 描述文本样式 / Description Text Styles */
.quiz-card p {
  @apply text-neutral-600 dark:text-neutral-400;
}

/* 进度条容器 / Progress Bar Container */
.progress-container {
  @apply w-full mt-4;
}

/* 进度条样式 / Progress Bar Styles */
.progress-bar {
  @apply h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden;
}

/* 进度条填充 / Progress Bar Fill */
.progress-fill {
  @apply h-full bg-blue-500 transition-all duration-300;
}

/* 进度文本样式 / Progress Text Styles */
.progress-text {
  @apply text-sm text-neutral-600 dark:text-neutral-400 mt-2;
}

/* 响应式调整 / Responsive Adjustments */
@media (max-width: 768px) {
  .quiz-card {
    @apply p-4;
  }

  .quiz-icon {
    @apply w-12 h-12 mb-3;
  }

  .quiz-card h3 {
    @apply text-lg;
  }
}

.quiz-modal {
  @apply fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4;
}

.quiz-modal-content {
  @apply bg-white dark:bg-neutral-800 rounded-xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto;
}

.quiz-header {
  @apply flex items-center justify-between p-6 border-b border-neutral-200 dark:border-neutral-700;
}

.quiz-header h2 {
  @apply text-2xl font-bold text-neutral-900 dark:text-white;
}

.close-button {
  @apply text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 text-2xl;
}

.quiz-body {
  @apply p-6;
}

.question-container {
  @apply space-y-6;
}

.question-container h3 {
  @apply text-xl font-semibold text-neutral-900 dark:text-white;
}

.options {
  @apply space-y-3;
}

.option-button {
  @apply w-full p-4 text-left rounded-lg border border-neutral-200 dark:border-neutral-700;
  @apply bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white;
  @apply hover:bg-neutral-50 dark:hover:bg-neutral-700 transition-colors;
}

.option-button.selected {
  @apply border-blue-500 bg-blue-50 dark:bg-blue-900/20;
}

.option-button.correct {
  @apply border-green-500 bg-green-50 dark:bg-green-900/20;
}

.option-button.incorrect {
  @apply border-red-500 bg-red-50 dark:bg-red-900/20;
}

.quiz-controls {
  @apply flex justify-end mt-6;
}

.submit-button, .next-button, .restart-button {
  @apply px-6 py-2 rounded-lg font-medium transition-colors;
}

.submit-button {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.next-button {
  @apply bg-green-500 text-white hover:bg-green-600;
}

.restart-button {
  @apply bg-blue-500 text-white hover:bg-blue-600;
}

.quiz-results {
  @apply text-center space-y-4;
}

.quiz-results h3 {
  @apply text-2xl font-bold text-neutral-900 dark:text-white;
}

.quiz-results p {
  @apply text-xl text-neutral-600 dark:text-neutral-400;
}

.quiz-progress {
  @apply px-6 py-3 border-b border-neutral-200 dark:border-neutral-700;
}

.progress-text {
  @apply text-sm text-neutral-600 dark:text-neutral-400 mb-2;
}

.progress-bar {
  @apply h-2 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden;
}

.progress-fill {
  @apply h-full bg-blue-500 transition-all duration-300 ease-in-out;
}
</style> 