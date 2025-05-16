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
                  :class="['option-explanation', 
                    key === currentQuestion.correctAnswer ? 'correct' : 'incorrect'
                  ]"
                >
                  <div class="explanation-content">
                    <strong>Explanation: </strong>{{ getExplanationForOption(currentQuestionIndex, key) }}
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
            
            <!-- Recommendations Section - Moved to top -->
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
                  @click="toggleQuestionExpanded(questionIndex)"
                >
                  <div class="review-question-header">
                    <span class="review-question-number">Question {{ questionIndex + 1 }}</span>
                    <div class="review-header-right">
                      <span 
                        :class="['review-status', userAnswers[questionIndex] === questions[questionIndex].correctAnswer ? 'correct' : 'incorrect']"
                      >
                        {{ userAnswers[questionIndex] === questions[questionIndex].correctAnswer ? '✓' : '✗' }}
                      </span>
                      <span class="expand-icon">{{ isQuestionExpanded(questionIndex) ? '▼' : '▶' }}</span>
                    </div>
                  </div>
                  
                  <div class="review-question-content">
                    <p class="review-question-text">{{ questions[questionIndex].question }}</p>
                    
                    <!-- Basic answer info always visible -->
                    <div class="review-answer" v-if="!isQuestionExpanded(questionIndex)">
                      <span class="user-answer">Your answer: <strong>{{ getUserAnswerText(questionIndex) }}</strong></span>
                    </div>
                    
                    <!-- Expanded content with all options and explanations -->
                    <div v-if="isQuestionExpanded(questionIndex)" class="question-expanded-content">
                      <div 
                        v-for="(option, key) in questions[questionIndex].options" 
                        :key="key"
                        :class="['review-option', {
                          'selected-option': userAnswers[questionIndex] === key,
                          'correct-option': key === questions[questionIndex].correctAnswer,
                          'incorrect-option': userAnswers[questionIndex] === key && key !== questions[questionIndex].correctAnswer
                        }]"
                      >
                        <div class="option-text">
                          <span class="option-key">{{ key }}.</span> {{ option }}
                          <span 
                            v-if="key === questions[questionIndex].correctAnswer" 
                            class="option-check correct"
                          >✓</span>
                          <span 
                            v-else-if="userAnswers[questionIndex] === key" 
                            class="option-check incorrect"
                          >✗</span>
                        </div>
                        
                        <!-- Show explanation for all options -->
                        <div 
                          :class="['option-explanation', 
                            key === questions[questionIndex].correctAnswer ? 'correct' : 
                            userAnswers[questionIndex] === key ? 'incorrect' : 'neutral'
                          ]"
                        >
                          <div class="explanation-content">
                            <strong>Explanation: </strong>{{ getExplanationForOption(questionIndex, key) }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
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
const expandedQuestions = ref([])

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

const isQuestionExpanded = (questionIndex) => {
  return expandedQuestions.value.includes(questionIndex)
}

const toggleQuestionExpanded = (questionIndex) => {
  const index = expandedQuestions.value.indexOf(questionIndex)
  if (index === -1) {
    expandedQuestions.value.push(questionIndex)
  } else {
    expandedQuestions.value.splice(index, 1)
  }
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

/* Modal styles - updated for modern flat look */
.quiz-modal {
  @apply fixed inset-0 bg-black/30 backdrop-blur-sm z-50 flex items-center justify-center p-4;
  padding-top: 70px; /* Add top padding to move the modal down */
}

.quiz-modal-content {
  @apply bg-white dark:bg-neutral-900 rounded-xl shadow-lg max-w-[1000px] w-full max-h-[90vh] overflow-y-auto;
  height: 840px;
  border: none;
}

.quiz-header {
  @apply flex items-center justify-between py-5 px-6;
  height: 80px;
  flex-shrink: 0;
  border: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  background-color: #fff;
  position: relative;
}

.quiz-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 5%;
  right: 5%;
  height: 1px;
  background-color: #f5f5f5;
}

.quiz-header h2 {
  @apply text-2xl font-bold text-neutral-800 dark:text-white;
}

.close-button {
  @apply text-neutral-400 hover:text-neutral-600 dark:text-neutral-500 dark:hover:text-neutral-300 text-2xl;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.quiz-body {
  @apply p-6;
  height: calc(100% - 80px - 50px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.quiz-progress {
  @apply px-6 py-3;
  height: 50px;
  border: none;
  background-color: #fafafa;
}

.progress-text {
  @apply text-sm text-neutral-500 dark:text-neutral-400 mb-2;
}

.progress-bar {
  @apply h-2 bg-neutral-100 dark:bg-neutral-700 rounded-full overflow-hidden;
}

.progress-fill {
  @apply h-full bg-blue-500 transition-all duration-300 ease-in-out;
}

/* Question container styles */
.question-container {
  @apply space-y-4;
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  overflow: visible;
  position: relative;
  padding-bottom: 70px;
}

.question-content {
  flex: 1;
  overflow: visible;
  padding-right: 8px;
  margin-bottom: 0;
}

.question-container h3 {
  @apply text-xl font-semibold text-neutral-800 dark:text-white;
  margin-bottom: 1.5rem;
}

/* Options styling */
.options {
  @apply space-y-3;
  min-height: auto;
  padding-bottom: 0;
}

.option-wrapper {
  @apply w-full mb-3;
}

.option-button {
  @apply w-full p-4 text-left rounded-lg text-base;
  border: none;
  background-color: #f9f9f9;
  color: #333;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

.option-button:hover:not(:disabled) {
  @apply bg-neutral-100;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Add specific hover styles for selected, correct, and incorrect options */
.option-button.selected:hover {
  background-color: #c13072; /* Keep the same dark pink background on hover */
  color: white;
  box-shadow: 0 1px 3px rgba(193, 48, 114, 0.4); /* Slightly stronger shadow on hover */
}

.option-button.correct:hover {
  background-color: rgba(16, 185, 129, 0.08); /* Keep the same correct background */
  color: black; /* Ensure text is black for correct answers */
}

.option-button.incorrect:hover {
  background-color: rgba(255, 216, 216, 1); /* Keep the light red background */
  color: black;
}

.option-button.selected {
  background-color: #c13072; /* Darker, more saturated pink for better contrast */
  color: white;
  box-shadow: 0 1px 3px rgba(193, 48, 114, 0.3);
}

.option-button.correct {
  background-color: rgba(16, 185, 129, 0.08);
  color: black; /* Ensure text is black for correct answers */
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.1);
}

.option-button.incorrect {
  background-color: rgba(255, 216, 216, 1); /* Light red background */
  color: black; /* Black text */
  box-shadow: 0 1px 3px rgba(239, 68, 68, 0.2);
}

/* Quiz controls */
.quiz-controls {
  @apply flex justify-end;
  height: 60px;
  margin-top: 0;
  padding-bottom: 0;
  flex-shrink: 0;
  position: absolute;
  bottom: 0;
  right: 0;
  width: 100%;
}

.submit-button, .next-button, .restart-button {
  @apply px-8 py-2.5 rounded-lg font-medium transition-colors;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  height: 45px;
  line-height: 1;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  border: none;
}

.submit-button {
  background-color: #3b82f6;
  color: white;
}

.submit-button:hover:not(:disabled) {
  background-color: #2563eb;
}

.submit-button:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}

.next-button {
  background-color: #10b981;
  color: white;
}

.next-button:hover {
  background-color: #059669;
}

.restart-button {
  background-color: #3b82f6;
  color: white;
}

.restart-button:hover {
  background-color: #2563eb;
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

.quiz-button {
  display: none;
}

/* Modern flat review section styles */
.review-section {
  @apply mt-4 text-left;
}

.review-section h4:first-child {
  @apply mb-6;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.review-section h4 {
  @apply mb-4;
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}

.review-categories {
  @apply space-y-4;
  display: block;
}

.review-category {
  @apply p-4 rounded-lg mb-4;
  background-color: #fcfcfc;
  border: none;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.review-category h5 {
  @apply text-base mb-3;
  font-weight: 600;
  color: #5E6AD2;
}

.review-question {
  @apply mb-3 p-3 rounded-lg;
  background-color: white;
  border: none;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  cursor: pointer;
  transition: all 0.2s ease;
}

.review-question:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.06);
  background-color: #fcfcfc;
}

.review-question.correct-question {
  border: none;
  box-shadow: 0 1px 3px rgba(16, 185, 129, 0.15);
  background-color: rgba(16, 185, 129, 0.04);
  position: relative;
}

.review-question.correct-question::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #10b981;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

.review-question.incorrect-question {
  border: none;
  box-shadow: 0 1px 3px rgba(239, 68, 68, 0.15);
  background-color: rgba(239, 68, 68, 0.04);
  position: relative;
}

.review-question.incorrect-question::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #ef4444;
  border-top-left-radius: 8px;
  border-bottom-left-radius: 8px;
}

/* Option styling for review */
.review-option {
  @apply rounded-md p-3;
  background-color: #fafafa;
  border: none;
  position: relative;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
}

.review-option.selected-option {
  background-color: rgba(193, 48, 114, 0.15);
  box-shadow: 0 1px 2px rgba(193, 48, 114, 0.2);
}

.review-option.correct-option {
  background-color: rgba(16, 185, 129, 0.05);
  box-shadow: 0 1px 2px rgba(16, 185, 129, 0.1);
}

.review-option.incorrect-option {
  background-color: rgba(255, 216, 216, 0.8);
  color: black;
  box-shadow: 0 1px 2px rgba(239, 68, 68, 0.15);
}

/* Explanation box - modern and flat */
.option-explanation {
  @apply mt-2 px-3 py-2 rounded;
  @apply text-sm;
  background-color: rgba(224, 242, 254, 0.6);
  border: none;
  margin-top: 0.5rem;
  box-shadow: 0 1px 2px rgba(0,0,0,0.02);
  position: relative;
}

.option-explanation.correct::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #10b981;
  border-radius: 2px 0 0 2px;
}

.option-explanation.incorrect::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #ef4444;
  border-radius: 2px 0 0 2px;
}

.option-explanation.neutral::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background-color: #cbd5e0;
  border-radius: 2px 0 0 2px;
}

/* Recommendations box in modern flat style */
.recommendations {
  @apply mb-6 p-4 rounded-lg;
  background-color: rgba(224, 242, 254, 0.5);
  border: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.recommendations h4 {
  @apply text-base font-semibold text-neutral-900 dark:text-white mb-2;
  color: #2563eb; /* Blue color */
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
    height: auto;
    max-height: 85vh;
    margin: 0 0.5rem;
    width: calc(100% - 1rem);
  }

  .quiz-header {
    height: 60px;
    padding: 0.75rem 1rem;
  }

  .quiz-header h2 {
    font-size: 1.25rem;
  }

  .quiz-body {
    padding: 1rem;
    height: auto;
  }

  .quiz-progress {
    padding: 0.5rem 1rem;
    height: 40px;
  }

  .progress-text {
    font-size: 0.75rem;
  }

  .progress-bar {
    height: 4px;
  }

  .question-container {
    padding-bottom: 60px;
  }

  .question-container h3 {
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  .option-button {
    padding: 0.75rem 1rem;
    font-size: 0.9rem;
  }

  .option-explanation {
    padding: 0.5rem 0.75rem;
    margin-top: 0.35rem;
  }

  .explanation-content {
    font-size: 0.8rem;
    padding-left: 20px;
  }

  .explanation-content::before {
    font-size: 14px;
  }

  .submit-button, .next-button, .restart-button {
    padding: 0 1rem;
    font-size: 0.9rem;
    height: 38px;
  }

  /* Review section responsive */
  .review-section h4 {
    font-size: 1rem;
  }

  .review-category {
    padding: 0.75rem;
  }

  .review-category h5 {
    font-size: 0.9rem;
  }

  .review-question {
    padding: 0.75rem;
  }

  .review-question-text {
    font-size: 0.85rem;
  }

  .review-question-header {
    margin-bottom: 0.5rem;
  }

  .review-question-number {
    font-size: 0.8rem;
  }

  .review-status {
    font-size: 1rem;
  }

  .expand-icon {
    width: 16px;
    height: 16px;
    font-size: 0.6rem;
  }

  .option-text {
    font-size: 0.85rem;
  }

  .recommendations {
    padding: 0.75rem;
  }

  .recommended-topic {
    font-size: 0.8rem;
  }
}

/* Small mobile screens */
@media (max-width: 480px) {
  .quiz-modal-content {
    max-height: 90vh;
    margin: 0;
    width: 100%;
    border-radius: 0;
  }

  .quiz-header {
    padding: 0.5rem 0.75rem;
    height: 50px;
  }

  .quiz-header h2 {
    font-size: 1rem;
  }

  .quiz-body {
    padding: 0.75rem;
  }

  .quiz-progress {
    padding: 0.4rem 0.75rem;
    height: 35px;
  }

  .question-container h3 {
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
  }

  .option-button {
    padding: 0.6rem 0.75rem;
    font-size: 0.8rem;
    border-radius: 0.375rem;
  }

  .options {
    @apply space-y-2;
  }

  .option-explanation {
    padding: 0.4rem 0.6rem;
    border-radius: 0.25rem;
  }

  .explanation-content {
    font-size: 0.75rem;
    padding-left: 18px;
  }

  .explanation-content::before {
    font-size: 12px;
  }

  .submit-button, .next-button, .restart-button {
    padding: 0 0.75rem;
    font-size: 0.8rem;
    height: 34px;
    border-radius: 0.375rem;
  }

  /* Review section phone size */
  .review-section h4 {
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
  }

  .review-category {
    padding: 0.5rem;
    margin-bottom: 0.75rem;
  }

  .review-question {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
  }
  
  .question-expanded-content {
    margin-top: 0.5rem;
    padding-top: 0.5rem;
  }
  
  .review-option {
    padding: 0.5rem;
    margin-bottom: 0.5rem;
  }
}

/* Fix for desktop when there's enough vertical space */
@media (min-width: 769px) and (min-height: 700px) {
  .quiz-modal-content {
    height: 700px;
  }
}

/* Fix for small height desktop screens */
@media (min-width: 769px) and (max-height: 700px) {
  .quiz-modal-content {
    height: 90vh;
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

.review-header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.expand-icon {
  font-size: 0.75rem;
  color: #888;
  transition: transform 0.2s ease;
}

.review-option {
  @apply mb-3 p-2 rounded-md;
  @apply bg-white dark:bg-neutral-700;
  border: 1px solid #eee;
}

.review-option.selected-option {
  @apply border-blue-500 bg-blue-50 dark:bg-blue-900/20;
}

.review-option.correct-option {
  @apply border-green-500 bg-green-50 dark:bg-green-900/20;
}

.review-option.incorrect-option {
  @apply border-red-500 bg-red-50 dark:bg-red-900/20;
}

.option-text {
  display: flex;
  align-items: center;
  position: relative;
  padding-right: 25px;
}

.option-key {
  font-weight: 600;
  margin-right: 0.5rem;
}

.option-check {
  position: absolute;
  right: 0.5rem;
  font-weight: bold;
}

.option-check.correct {
  color: #10b981;
}

.option-check.incorrect {
  color: #ef4444;
}

.question-expanded-content {
  @apply mt-3 space-y-2;
}

.review-question-header {
  @apply flex justify-between items-center mb-2;
}

.review-question-number {
  @apply font-medium text-neutral-700 dark:text-neutral-300;
  font-size: 0.95rem;
}

.review-header-right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.review-status {
  @apply font-bold text-lg;
  line-height: 1;
}

.review-status.correct {
  @apply text-green-600 dark:text-green-400;
}

.review-status.incorrect {
  @apply text-red-600 dark:text-red-400;
}

.expand-icon {
  font-size: 0.7rem;
  color: #aaa;
  transition: transform 0.2s ease;
  background: #f5f5f5;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

/* Question content styles */
.review-question-content {
  @apply ml-0;
}

.review-question-text {
  @apply text-sm text-neutral-800 dark:text-neutral-200 mb-2;
  font-weight: 500;
  line-height: 1.4;
}

/* Option styles in expanded mode */
.question-expanded-content {
  @apply mt-4 space-y-3;
  border-top: 1px solid #f5f5f5;
  padding-top: 0.75rem;
}

.option-text {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-right: 25px;
  font-size: 0.95rem;
  line-height: 1.4;
}

.option-key {
  font-weight: 600;
  margin-right: 0.5rem;
  color: #666;
}

.option-check {
  position: absolute;
  right: 0.5rem;
  top: 0;
  font-weight: bold;
}

.option-check.correct {
  color: #10b981;
}

.option-check.incorrect {
  color: #ef4444;
}

.explanation-content {
  @apply text-sm text-neutral-700 dark:text-neutral-300;
  line-height: 1.5;
  position: relative;
  padding-left: 24px; /* Space for the icon */
}

.explanation-content::before {
  position: absolute;
  left: 0;
  top: 1px;
  font-size: 16px;
  font-weight: bold;
}

.option-explanation.correct .explanation-content::before {
  content: "✓";
  color: #10b981; /* Green color */
}

.option-explanation.incorrect .explanation-content::before {
  content: "✗";
  color: #ef4444; /* Red color */
}

.option-explanation.neutral .explanation-content::before {
  content: "ℹ";
  color: #6b7280; /* Gray color */
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

/* For mobile screens, adjust the top padding */
@media (max-width: 768px) {
  .quiz-modal {
    padding-top: 60px;
  }
}

@media (max-width: 480px) {
  .quiz-modal {
    padding-top: 50px;
  }
}
</style> 