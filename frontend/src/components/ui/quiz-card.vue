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
          <div class="question-content">
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
          
          <!-- Try Again button moved between score and review -->
          <div class="quiz-controls-final">
            <button class="restart-button" @click="restartQuiz">Try Again</button>
          </div>
          
          <!-- Review Section -->
          <div class="review-section">
            <h4>Review Your Answers</h4>
            
            <div class="review-categories">
              <div 
                v-for="(category, index) in reviewCategories" 
                :key="index"
                class="review-category"
              >
                <h5>{{ category.name }}</h5>
                <div 
                  v-for="questionIndex in category.questions" 
                  :key="questionIndex"
                  :class="['review-question', getQuestionReviewClass(questionIndex)]"
                >
                  <div class="review-question-header">
                    <span class="review-question-number">Question {{ questionIndex + 1 }}</span>
                    <span 
                      :class="['review-status', userAnswers[questionIndex] === questions[questionIndex].correctAnswer ? 'correct' : 'incorrect']"
                    >
                      {{ userAnswers[questionIndex] === questions[questionIndex].correctAnswer ? '✓' : '✗' }}
                    </span>
                  </div>
                  
                  <div class="review-question-content">
                    <p class="review-question-text">{{ questions[questionIndex].question }}</p>
                    <div class="review-answer">
                      <span class="user-answer">Your answer: <strong>{{ getUserAnswerText(questionIndex) }}</strong></span>
                      <span 
                        v-if="userAnswers[questionIndex] !== questions[questionIndex].correctAnswer"
                        class="correct-answer"
                      >
                        Correct answer: <strong>{{ getCorrectAnswerText(questionIndex) }}</strong>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Recommendations Section -->
            <div v-if="recommendedCategories.length > 0" class="recommendations">
              <h4>Recommended Review</h4>
              <p>Based on your answers, we recommend reviewing these topics:</p>
              <ul class="recommended-topics">
                <li 
                  v-for="(category, index) in recommendedCategories" 
                  :key="index"
                  class="recommended-topic"
                >
                  {{ category }}
                </li>
              </ul>
            </div>
          </div>
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
const userAnswers = ref([])

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
    },
    category: "Understanding Your Impact"
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
    },
    category: "Understanding Your Impact"
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
    },
    category: "Building Authentic Relationships"
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
    },
    category: "Building Authentic Relationships"
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
    },
    category: "Ethical Content Creation"
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
    },
    category: "Ethical Content Creation"
  }
])

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value])
const isLastQuestion = computed(() => currentQuestionIndex.value === questions.value.length - 1)

// 添加进度计算 / Add progress calculation
const progressPercentage = computed(() => {
  return (currentQuestionIndex.value / questions.value.length) * 100
})

// 复习部分的类别 / Categories for review section
const reviewCategories = computed(() => {
  const categories = [
    {
      name: "Understanding Your Impact",
      questions: [0, 1],
    },
    {
      name: "Building Authentic Relationships",
      questions: [2, 3],
    },
    {
      name: "Ethical Content Creation",
      questions: [4, 5],
    }
  ]
  
  return categories
})

// 推荐复习的类别 / Recommended categories to review
const recommendedCategories = computed(() => {
  if (userAnswers.value.length === 0) return []
  
  const incorrectCategories = new Set()
  
  userAnswers.value.forEach((answer, index) => {
    if (answer !== questions.value[index].correctAnswer) {
      incorrectCategories.add(questions.value[index].category)
    }
  })
  
  return Array.from(incorrectCategories)
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
  userAnswers.value = Array(questions.value.length).fill(null)
}

const selectAnswer = (answer) => {
  if (!showAnswer.value) {
    selectedAnswer.value = answer
  }
}

const checkAnswer = () => {
  showAnswer.value = true
  
  // 保存用户答案 / Save user's answer
  userAnswers.value[currentQuestionIndex.value] = selectedAnswer.value
  
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

// 获取问题复习的CSS类 / Get CSS class for question review
const getQuestionReviewClass = (questionIndex) => {
  if (!userAnswers.value[questionIndex]) return ''
  return userAnswers.value[questionIndex] === questions.value[questionIndex].correctAnswer
    ? 'correct-question'
    : 'incorrect-question'
}

// 获取用户选择的答案文本 / Get user's answer text
const getUserAnswerText = (questionIndex) => {
  const answer = userAnswers.value[questionIndex]
  if (!answer) return 'Not answered'
  return `${answer}. ${questions.value[questionIndex].options[answer]}`
}

// 获取正确答案文本 / Get correct answer text
const getCorrectAnswerText = (questionIndex) => {
  const correctKey = questions.value[questionIndex].correctAnswer
  return `${correctKey}. ${questions.value[questionIndex].options[correctKey]}`
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
  padding-bottom: 0; /* 移除底部padding，使内容居中 */
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
  height: 100%; /* 添加高度100%确保占满空间 */
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
  height: 0; /* 修改为0，移除底部额外空间 */
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
    padding-bottom: 0; /* 移除底部padding */
    gap: 1.25rem;
  }
}

@media (max-width: 768px) {
  .quiz-card {
    width: 450px;
    height: 90px;
  }

  .quiz-content {
    padding: 0 2rem;
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
    padding: 0 1.5rem;
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

@media (max-width: 480px) {
  .quiz-card {
    width: 100%;
    height: 70px;
  }
  
  .quiz-content {
    padding: 0 1rem;
    gap: 0.5rem;
  }
  
  .quiz-text {
    width: 70%;
  }
  
  .quiz-icon {
    @apply w-10 h-10;
  }
  
  .quiz-card h3 {
    font-size: 0.85rem;
    margin-bottom: 0.2rem;
  }
  
  .quiz-card p {
    font-size: 0.7rem;
    line-height: 1.2;
  }
}

/* 确保卡片内文字可读 */
.quiz-card :deep(.rainbow-button) {
  background-color: white !important;
  display: flex;
  align-items: center;
  justify-content: center;
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
  @apply fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-2;
}

.quiz-modal-content {
  @apply bg-white dark:bg-neutral-800 rounded-xl shadow-2xl max-w-[1200px] w-full max-h-[90vh] overflow-y-auto;
  height: 840px; /* 进一步增大问答窗口高度 */
}

.quiz-header {
  @apply flex items-center justify-between py-6 px-8 border-b border-neutral-200 dark:border-neutral-700;
  height: 100px; /* 增大头部高度 */
  flex-shrink: 0;
}

.quiz-header h2 {
  @apply text-3xl font-bold text-neutral-900 dark:text-white;
}

.close-button {
  @apply text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 text-3xl;
}

.quiz-body {
  @apply p-8;
  height: calc(100% - 100px - 60px); /* 总高度减去头部高度和进度条高度 */
  overflow: hidden; /* 防止滚动条出现 */
  display: flex;
  flex-direction: column;
}

.question-container {
  @apply space-y-4;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: visible; /* 允许内容溢出 */
  position: relative; /* 添加相对定位，便于绝对定位按钮 */
  padding-bottom: 80px; /* 为按钮预留空间 */
}

.question-content {
  flex: 1;
  overflow: visible; /* 改为visible以避免滚动 */
  padding-right: 8px;
  margin-bottom: 0; /* 移除内容与按钮之间的距离 */
}

.question-container h3 {
  @apply text-xl font-semibold text-neutral-900 dark:text-white;
  margin-bottom: 1.5rem;
}

.options {
  @apply space-y-4; /* 减少选项之间的间距 */
  min-height: auto; /* 移除固定高度约束 */
  padding-bottom: 0; /* 移除底部留白 */
}

.option-wrapper {
  @apply w-full mb-3;
}

.option-button {
  @apply w-full p-4 text-left rounded-lg border border-neutral-200 dark:border-neutral-700 text-base;
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
  margin-bottom: 6px; /* 减少解释框底部留白 */
}

.explanation-content {
  @apply text-sm text-neutral-700 dark:text-neutral-300;
  line-height: 1.4;
}

.quiz-controls {
  @apply flex justify-end;
  height: 60px; /* 减小按钮区域高度 */
  margin-top: 0; /* 移除按钮区域的上方留白 */
  padding-bottom: 0; /* 移除底部留白 */
  flex-shrink: 0; /* 防止按钮区域被压缩 */
  position: absolute; /* 使用绝对定位 */
  bottom: 0; /* 固定在底部 */
  right: 0; /* 右对齐 */
  width: 100%; /* 宽度占满 */
}

.submit-button, .next-button, .restart-button {
  @apply px-8 py-3 rounded-lg font-medium transition-colors text-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px; /* 减小按钮高度 */
  line-height: 1;
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
  height: 100%;
  overflow-y: auto;
  padding: 0 1rem;
}

.quiz-results h3 {
  @apply text-2xl font-bold text-neutral-900 dark:text-white mt-4 mb-3;
}

.quiz-results p {
  @apply text-lg text-neutral-600 dark:text-neutral-400 mb-3;
}

.quiz-progress {
  @apply px-8 py-4 border-b border-neutral-200 dark:border-neutral-700;
  height: 60px; /* 增大进度条高度 */
}

.progress-text {
  @apply text-base text-neutral-600 dark:text-neutral-400 mb-2;
}

.progress-bar {
  @apply h-3 bg-neutral-200 dark:bg-neutral-700 rounded-full overflow-hidden;
}

.progress-fill {
  @apply h-full bg-blue-500 transition-all duration-300 ease-in-out;
}

.quiz-button {
  display: none;
}

/* Review Section Styles */
.review-section {
  @apply mt-4 text-left;
}

.review-section h4 {
  @apply text-lg font-semibold text-neutral-900 dark:text-white mb-4;
}

.review-categories {
  @apply space-y-5;
  display: block;
}

.review-category {
  @apply p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg mb-5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.review-category h5 {
  @apply text-base font-semibold text-neutral-900 dark:text-white mb-3;
  color: #1E6A42;
}

.review-question {
  @apply mb-4 p-3 rounded-md;
  @apply bg-neutral-50 dark:bg-neutral-800;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
}

.review-question.correct-question {
  @apply bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500;
}

.review-question.incorrect-question {
  @apply bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500;
}

.review-question-header {
  @apply flex justify-between items-center mb-2;
}

.review-question-number {
  @apply font-semibold text-neutral-700 dark:text-neutral-300;
}

.review-status {
  @apply font-bold text-xl;
}

.review-status.correct {
  @apply text-green-600 dark:text-green-400;
}

.review-status.incorrect {
  @apply text-red-600 dark:text-red-400;
}

.review-question-content {
  @apply ml-0;
}

.review-question-text {
  @apply font-medium text-base text-neutral-800 dark:text-neutral-200 mb-2;
}

.review-answer {
  @apply space-y-1;
}

.user-answer, .correct-answer {
  @apply block text-sm;
}

.user-answer {
  @apply text-neutral-700 dark:text-neutral-300;
}

.correct-answer {
  @apply text-green-600 dark:text-green-400;
}

/* Recommendations styles */
.recommendations {
  @apply mt-4 p-4 border border-neutral-200 dark:border-neutral-700 rounded-lg;
  @apply bg-blue-50 dark:bg-blue-900/20;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.recommendations h4 {
  @apply text-base font-semibold text-neutral-900 dark:text-white mb-2;
  color: #1E6A42;
}

.recommendations p {
  @apply text-sm text-neutral-700 dark:text-neutral-300 mb-3;
  text-align: left;
}

.recommended-topics {
  @apply list-disc pl-6 space-y-1;
  display: block;
}

.recommended-topic {
  @apply text-sm text-neutral-800 dark:text-neutral-200;
  font-weight: 500;
}

.quiz-controls-final {
  @apply flex justify-center;
  margin: 0.5rem 0 1rem;
}

.quiz-controls-final .restart-button {
  @apply px-6 py-2 text-base;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px; /* 减小按钮高度 */
  line-height: 1;
}

/* 响应式调整 / Responsive Adjustments for review section */
@media (max-width: 768px) {
  .quiz-modal-content {
    height: 520px;
  }
  
  .quiz-header {
    height: 70px;
  }
  
  .quiz-body {
    height: calc(100% - 70px - 40px);
  }
  
  .quiz-progress {
    height: 40px;
  }
  
  .options {
    min-height: 220px;
  }
  
  .review-question-header {
    @apply flex-col items-start space-y-1;
  }
  
  .review-status {
    @apply self-end;
  }
  
  .user-answer, .correct-answer {
    font-size: 0.8rem;
  }
  
  .review-question-text {
    font-size: 0.9rem;
  }
}

@media (max-width: 640px) {
  .quiz-modal-content {
    height: 480px;
  }
  
  .quiz-header {
    height: 65px;
    padding: 1rem;
  }
  
  .quiz-body {
    height: calc(100% - 65px - 36px);
    padding: 1rem;
  }
  
  .quiz-progress {
    height: 36px;
    padding: 0.75rem 1rem;
  }
  
  .options {
    min-height: 200px;
  }
  
  .option-button {
    padding: 0.75rem;
  }
}

/* 添加自定义滚动条样式 */
.question-content::-webkit-scrollbar,
.quiz-results::-webkit-scrollbar {
  width: 6px;
}

.question-content::-webkit-scrollbar-track,
.quiz-results::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.question-content::-webkit-scrollbar-thumb,
.quiz-results::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.question-content::-webkit-scrollbar-thumb:hover,
.quiz-results::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 