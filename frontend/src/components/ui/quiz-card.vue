<template>
  <RainbowButton 
    class="quiz-card" 
    :speed="3"
    @click="openQuiz"
  >
    <div class="quiz-content">
      <div class="quiz-icon">
        <img src="/src/assets/icons/elements/quiz.png" alt="Quiz" class="icon">
      </div>
      <div class="quiz-text">
        <h3>Check Your Understanding</h3>
        <p>Test your knowledge about ethical content creation</p>
      </div>
      <div class="bottom-space"></div>
    </div>
  </RainbowButton>

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
            <div 
              v-for="(option, key) in currentQuestion.options" 
              :key="key"
              class="option-wrapper"
            >
              <button 
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
              <div 
                v-if="showAnswer && (key === currentQuestion.correctAnswer || selectedAnswer === key)" 
                class="option-explanation"
              >
                <div class="explanation-content">
                  {{ getExplanationForOption(currentQuestionIndex, key) }}
                </div>
              </div>
            </div>
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
import { RainbowButton } from '@/components/ui/rainbow-button'

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
    correctAnswer: "C",
    explanations: {
      A: "Digital citizenship is more than just frequent use of social media platforms; it involves responsible behavior online.",
      B: "Creating viral content is just one aspect of online activity, not the definition of digital citizenship.",
      C: "Digital citizenship is about being responsible, ethical, and respectful when participating in online communities.",
      D: "While followers are important for influencers, digital citizenship focuses on responsible online behavior rather than popularity metrics."
    }
  },
  {
    question: "How does constructive engagement benefit your audience?",
    options: {
      A: "Encourages misinformation",
      B: "Promotes healthy discussions and understanding",
      C: "Increases follower count",
      D: "Limits audience interaction"
    },
    correctAnswer: "B",
    explanations: {
      A: "Constructive engagement actually combats misinformation by encouraging thoughtful dialogue.",
      B: "When you engage constructively, you create space for meaningful conversations that lead to greater understanding among your audience.",
      C: "While engagement may increase followers, the primary benefit is building quality relationships through meaningful interactions.",
      D: "Constructive engagement expands rather than limits audience interaction by encouraging participation."
    }
  },
  {
    question: "Transparency with your audience primarily builds:",
    options: {
      A: "Popularity",
      B: "Trust and credibility",
      C: "Higher revenue",
      D: "Increased followers instantly"
    },
    correctAnswer: "B",
    explanations: {
      A: "Transparency may contribute to popularity, but its primary purpose is building authentic relationships.",
      B: "Being transparent about your values, processes, and partnerships creates trust with your audience, establishing long-term credibility.",
      C: "While trust can lead to better business outcomes, revenue isn't the primary benefit of transparency.",
      D: "Transparency builds followers gradually through authentic connection rather than providing instant growth."
    }
  },
  {
    question: "What best illustrates genuine audience engagement?",
    options: {
      A: "Ignoring negative feedback",
      B: "Posting only promotional content",
      C: "Regularly responding sincerely to comments and questions",
      D: "Avoiding personal stories and experiences"
    },
    correctAnswer: "C",
    explanations: {
      A: "Genuine engagement means addressing all feedback, including criticism, to build stronger relationships.",
      B: "Promotional content alone doesn't foster meaningful connections; authentic engagement requires diverse content.",
      C: "Taking time to personally respond to your audience shows that you value their input and are committed to building authentic relationships.",
      D: "Personal stories actually strengthen engagement by making authentic connections with your audience."
    }
  },
  {
    question: "Ethical content creation involves:",
    options: {
      A: "Posting whatever gets the most views",
      B: "Creating content aligned with core values and integrity",
      C: "Avoiding audience opinions completely",
      D: "Changing values frequently to match trends"
    },
    correctAnswer: "B",
    explanations: {
      A: "Chasing views without consideration for ethics can lead to harmful content and damage trust.",
      B: "Ethical creators maintain consistent values and produce content that reflects their authentic beliefs and intentions.",
      C: "Ethical creation should consider audience feedback while maintaining core values.",
      D: "Constantly shifting values for trends appears inauthentic and undermines credibility."
    }
  },
  {
    question: "Accountability in content creation means:",
    options: {
      A: "Ignoring mistakes",
      B: "Shifting blame when errors occur",
      C: "Acknowledging and correcting errors openly",
      D: "Posting controversial content without moderation"
    },
    correctAnswer: "C",
    explanations: {
      A: "Ignoring mistakes damages trust and prevents learning opportunities.",
      B: "Shifting blame demonstrates a lack of responsibility and damages credibility.",
      C: "Accountability means taking responsibility for errors, addressing them openly, and making visible corrections.",
      D: "Unmoderated controversial content shows a lack of responsibility toward your audience."
    }
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

const getExplanationForOption = (questionIndex, optionKey) => {
  const question = questions.value[questionIndex]
  return question.explanations[optionKey] || ''
}
</script>

<style scoped>
/* 卡片容器 / Card Container */
.quiz-card {
  @apply flex flex-col items-center justify-center;
  height: 120px;
  width: 800px;
  border-radius: 9999px !important; /* 胶囊形状 */
  transition: all 0.3s ease;
  transform-style: preserve-3d;
  perspective: 1000px;
  position: relative;
  margin: 0 auto;
  padding: 0;
  overflow: hidden;
  border-width: 3px !important;
}

/* 胶囊形状卡片的悬停效果 */
.quiz-card:hover {
  transform: translateY(-5px) rotateX(5deg);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.06), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.quiz-content {
  @apply w-full;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 4rem;
  position: relative;
  z-index: 2;
  flex-direction: row;
  padding-top: 0;
  padding-bottom: 20px;
  gap: 1.5rem;
}

.quiz-icon {
  @apply w-20 h-16;
  transition: transform 0.3s ease, filter 0.3s ease;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  filter: none;
  margin-right: 0;
  margin-bottom: 0;
}

.icon {
  width: 64px;
  height: 64px;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.quiz-text {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

/* 标题样式 / Title Styles */
.quiz-card h3 {
  @apply text-xl font-semibold mb-2;
  text-align: center;
  transition: transform 0.3s ease, color 0.3s ease;
  color: #1E6A42; /* 深绿色标题 */
  text-shadow: none;
  margin-top: 0;
}

/* 描述文本样式 / Description Text Styles */
.quiz-card p {
  text-align: center;
  transition: transform 0.3s ease, opacity 0.3s ease;
  color: #333;
  font-weight: 500;
  margin-bottom: 0;
}

/* 底部空白 / Bottom spacing */
.bottom-space {
  height: 20px;
  width: 100%;
  position: absolute;
  bottom: 0;
  left: 0;
}

/* 响应式调整 / Responsive Adjustments */
@media (max-width: 1024px) {
  .quiz-card {
    width: 650px;
    height: 110px;
  }
  
  .quiz-content {
    padding-bottom: 15px;
    gap: 1.25rem;
  }
}

@media (max-width: 768px) {
  .quiz-card {
    width: 450px;
    height: 90px;
  }

  .quiz-content {
    padding: 0 2rem 12px;
    gap: 1rem;
  }

  .quiz-icon {
    @apply w-16 h-12;
  }
  
  .quiz-card h3 {
    @apply text-lg mb-1;
    font-size: 1.1rem;
  }
  
  .quiz-card p {
    font-size: 0.9rem;
  }
}

@media (max-width: 640px) {
  .quiz-card {
    width: 100%;
    height: 80px;
    padding: 0;
  }
  
  .quiz-content {
    padding: 0 1.5rem 10px;
    gap: 0.75rem;
  }
  
  .quiz-icon {
    @apply w-12 h-10;
  }
  
  .quiz-card h3 {
    font-size: 0.95rem;
    margin-bottom: 0.25rem;
  }
  
  .quiz-card p {
    font-size: 0.8rem;
  }
}

/* 确保卡片内文字可读 */
.quiz-card :deep(.rainbow-button) {
  background-color: white !important;
}

/* 图标悬停效果 / Icon Hover Effect */
.quiz-card:hover .quiz-icon {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.quiz-card:hover .icon {
  transform: scale(1.05);
}

.quiz-card:hover h3 {
  color: #164a2e; /* 悬停时颜色变深 */
}

.quiz-card:hover p {
  color: #555;
}

/* Modal styles */
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

.option-wrapper {
  @apply w-full mb-4;
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

.option-explanation {
  @apply mt-2 px-4 py-3 rounded-lg bg-neutral-50 dark:bg-neutral-900/50;
  @apply border-l-4 border-neutral-400 dark:border-neutral-600;
  @apply text-sm text-neutral-700 dark:text-neutral-300;
}

.explanation-content {
  @apply text-sm text-neutral-700 dark:text-neutral-300;
  line-height: 1.5;
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

.quiz-button {
  display: none;
}
</style> 