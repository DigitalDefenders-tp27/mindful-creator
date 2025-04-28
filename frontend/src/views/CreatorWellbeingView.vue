<template>
  <div class="creator-wellbeing">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Creator Wellbeing</h1>
            <h2>Digital Impact Analysis Dashboard</h2>
          </div>
          <p class="subtitle">Explore how your usage patterns affect wellbeing based on real data</p>
        </div>
      </div>
    </section>

    <!-- Dashboard Section -->
    <section class="dashboard-section">
      <div class="tabs">
        <div v-for="(tab, index) in tabs" :key="index" class="tab" :class="{ active: currentTab === index }"
          @click="switchTab(index)">
          {{ tab.name }}
        </div>
      </div>

      <div class="visualisation-container">
        <div class="chart-area">
          <canvas id="mainChart"></canvas>
        </div>
        <div class="insight-area">
          <h3 class="insight-heading">Key Insights</h3>
          <div v-for="(insight, index) in tabs[currentTab].insights" :key="index" class="insight-box">
            {{ insight }}
          </div>
        </div>
      </div>
    </section>

    <!-- 健康资源查找器 / Wellbeing Resource Finder -->
    <section class="resource-finder-section">
      <div class="container">
        <h1 class="section-title">Wellbeing Resource Finder</h1>
        <p class="section-subtitle">Find and navigate yourself to get wellbeing resources easily near you.</p>

        <div class="resource-finder-content">
          <div class="resource-tabs">
            <div class="resource-tab active">Psychologist (Offline Resources)</div>
            <div class="resource-tab">Online Resources</div>
          </div>

          <div class="resource-content">
            <div class="map-container">
              <img src="../assets/icons/elements/map-placeholder.svg" alt="Map" class="map-img">
              <button class="position-btn">
                <img src="../assets/icons/elements/location-pin.svg" alt="Location" class="pin-icon">
                Get My Position
              </button>
            </div>

            <div class="resource-details">
              <h3 class="resource-name">Calm 'n' Caring Psychology Melbourne</h3>
              <div class="rating">
                <span class="rating-score">5.0</span>
                <div class="stars">★★★★★</div>
                <span class="reviews">(5)</span>
              </div>

              <div class="resource-location">
                <img src="../assets/icons/elements/location.svg" alt="Location" class="location-icon">
                <span>101 Collins St, Melbourne VIC 3000</span>
              </div>

              <div class="resource-website">
                <img src="../assets/icons/elements/globe.svg" alt="Website" class="website-icon">
                <a href="https://calmandcaring.com/melbourne" target="_blank">https://calmandcaring.com/melbourne</a>
                <button class="online-switch">Switch to online</button>
              </div>

              <div class="opening-hours">
                <h4>Opening hours</h4>
                <div class="hours-grid">
                  <div class="day">Sunday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">Monday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">Tuesday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">Wednesday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">Thursday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">Friday</div>
                  <div class="hours">Open 24 hours</div>
                  <div class="day">(Good Friday)</div>
                  <div class="hours">Hours might differ</div>
                  <div class="day">Saturday</div>
                  <div class="hours">Hours might differ</div>
                </div>
              </div>

              <div class="resource-actions">
                <button class="action-btn direction-btn">
                  <img src="../assets/icons/elements/direction.svg" alt="Direction" class="btn-icon">
                  Get direction
                </button>
                <button class="action-btn guide-btn">
                  <img src="../assets/icons/elements/guide.svg" alt="Guide" class="btn-icon">
                  Get Preparation Guide
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 健康活动中心 / Wellbeing Activities Hub -->
    <section class="activities-section">
      <div class="container">
        <h1 class="section-title">Wellbeing Activities Hub</h1>
        <p class="section-subtitle">Release your stress by joining fun activities and making like-minded friends.</p>

        <div class="activities-header">
          <h3 class="recent-title">RECENT CAMPAIGNS...</h3>
          <button @click="openModal" class="view-all-btn">VIEW ALL EVENTS</button>
        </div>

        <div class="activities-grid">
          <a href="https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch"
            target="_blank" class="activity-card-link">
            <div class="activity-card">
              <img src="../assets/icons/activitiesImages/TorquayWalking.avif" alt="Wellness Walk" class="activity-img">
              <h3 class="activity-title">MeTreat Retreats Women's Wellness Walk</h3>
              <div class="activity-tags">
                <span class="tag april">April</span>
                <span class="tag outdoor">Outdoor Wellness</span>
              </div>
              <div class="activity-details">
                <span class="group-size">Torquay Beach</span>
                <span class="location">Melbourne</span>
              </div>
            </div>
          </a>

          <a href="https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch"
            target="_blank" class="activity-card-link">
            <div class="activity-card">
              <img src="../assets/icons/activitiesImages/mentalHealthWorkshop.avif" alt="Workshop" class="activity-img">
              <h3 class="activity-title">Mentally Healthy Workplaces Workshop</h3>
              <div class="activity-tags">
                <span class="tag may">May</span>
                <span class="tag mental">Mental Health</span>
              </div>
              <div class="activity-details">
                <span class="group-size">Free Event</span>
                <span class="location">Brisbane</span>
              </div>
            </div>
          </a>

          <a href="https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch"
            target="_blank" class="activity-card-link">
            <div class="activity-card">
              <img src="../assets/icons/activitiesImages/workplaceWarrnambool.avif" alt="Business Workshop"
                class="activity-img">
              <h3 class="activity-title">Resilience, Self-Leadership & Wellbeing - Warrnambool Business Workshop</h3>
              <div class="activity-tags">
                <span class="tag may">May</span>
                <span class="tag workplace">Workplace Wellbeing</span>
              </div>
              <div class="activity-details">
                <span class="group-size">$20</span>
                <span class="location">Warrnambool</span>
              </div>
            </div>
          </a>
        </div>
      </div>
    </section>

    <!-- Activities Details Modal -->
    <div v-if="isModalVisible" class="activities-modal-overlay" @click="closeModal">
      <div class="activities-modal" @click.stop>
        <div class="modal-header">
          <h2>All Wellbeing Events</h2>
          <button class="close-modal-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-content">
          <div class="search-bar">
            <input type="text" v-model="searchQuery" placeholder="Search by name" class="search-input">
          </div>
          <div class="event-filters">
            <div class="filter-group">
              <label>Location:</label>
              <select v-model="selectedLocation">
                <option>All locations</option>
                <option>Melbourne</option>
                <option>Sydney</option>
                <option>Brisbane</option>
                <option>Warrnambool</option>
                <option>Geelong</option>
                <option>Torquay</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Category:</label>
              <select v-model="selectedCategory">
                <option>All types</option>
                <option>Outdoor Wellness</option>
                <option>Mental Health</option>
                <option>Physical Fitness</option>
                <option>Healthy Eating</option>
                <option>Workplace Wellbeing</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Month:</label>
              <select v-model="selectedMonth">
                <option>Any time</option>
                <option>March</option>
                <option>April</option>
                <option>May</option>
                <option>June</option>
                <option>October</option>
              </select>
            </div>
          </div>

          <div class="events-grid">
            <div class="event-card">
              <img src="../assets/icons/activitiesImages/mentalHealthWorkshop.avif" alt="Mental health workshops"
                class="event-img">
              <div class="event-info">
                <h3>Mentally Healthy Workplaces Workshop</h3>
                <div class="event-tags">
                  <span class="tag ticket">Sold out</span>
                  <span class="tag may">May</span>
                  <span class="tag workshop">Workshop</span>
                  <span class="tag free">Free Event</span>
                </div>
                <p class="event-description">This workshop is designed to assist managers and supervisors create and
                  sustain a mentally healthy and safe workplace.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Brisbane</div>
                  <div><strong>Address:</strong> Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000
                  </div>
                  <div><strong>Date:</strong> 1st May 2025</div>
                  <div><strong>Time:</strong> 8:00 AM - 12:00 PM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/mentalHealthWorkshop.avif" alt="Mental health workshops"
                class="event-img">
              <div class="event-info">
                <h3>Mentally Healthy Workplaces Workshop</h3>
                <div class="event-tags">
                  <span class="tag ticket">Nearly full</span>
                  <span class="tag june">June</span>
                  <span class="tag workshop">Workshop</span>
                  <span class="tag free">Free Event</span>
                </div>
                <p class="event-description">This workshop is designed to assist managers and supervisors create and
                  sustain a mentally healthy and safe workplace.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Brisbane</div>
                  <div><strong>Address:</strong> Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000
                  </div>
                  <div><strong>Date:</strong> June 4th 2025</div>
                  <div><strong>Time:</strong> 8:00 AM - 12:00 PM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/workplace.avif" alt="Workplace Wellbeing" class="event-img">
              <div class="event-info">
                <h3>Workplace Wellbeing - How to Build Confidence and Manage Stress</h3>
                <div class="event-tags">
                  <span class="tag october">October</span>
                  <span class="tag workplace">Workplace Wellbeing Workshop</span>
                  <span class="tag charged">$525.44</span>
                </div>
                <p class="event-description">You'll learn about both positive and negative factors at play in workplace.
                </p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Sydney</div>
                  <!-- <div><strong>Group size:</strong> 15-30</div> -->
                  <div><strong>Date:</strong> October 11st 2025</div>
                  <div><strong>Time:</strong> 7:30 AM - 11:30 AM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/workplace-wellbeing-how-to-build-confidence-and-manage-stress-tickets-886375582227?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/workplace-wellbeing-how-to-build-confidence-and-manage-stress-tickets-886375582227?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/workplaceWarrnambool.avif" alt="Workplace Wellbeing"
                class="event-img">
              <div class="event-info">
                <h3>Resilience, Self-Leadership & Wellbeing - Warrnambool Business Workshop</h3>
                <div class="event-tags">
                  <span class="tag may">May</span>
                  <span class="tag workplace">Workplace Wellbeing Workshop</span>
                  <span class="tag charged">$20</span>
                </div>
                <p class="event-description">Explore Victoria's beautiful national parks with our guided bushwalking
                  groups. Connect with nature and like-minded creators.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Warrnambool</div>
                  <div><strong>Address:</strong> 185 Timor Street Warrnambool, VIC 3280</div>
                  <!-- <div><strong>Group size:</strong> 5-15</div> -->
                  <div><strong>Date:</strong> May 28th</div>
                  <div><strong>Time:</strong> 1:00 PM - 3:00 PM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/workplaceGeelong.avif" alt="Workplace Wellbeing"
                class="event-img">
              <div class="event-info">
                <h3>Strategies for Mental Health at Work and Keeping Psychologically Safe.</h3>
                <div class="event-tags">
                  <span class="tag october">October</span>
                  <span class="tag workplace">Workplace Wellbeing Workshop</span>
                  <span class="tag charged">$108.9</span>
                </div>
                <p class="event-description"> HR professionals, managers, and business leaders , here's practical
                  strategies to foster wellbeing and mental health in your workplace.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Geelong</div>
                  <div><strong>Address:</strong> 60 Moorabool Street Geelong, VIC 3220</div>
                  <!-- <div><strong>Group size:</strong> 5-10</div> -->
                  <div><strong>Date:</strong> October 9th 2025</div>
                  <div><strong>Time:</strong> 9:30 AM - 11:30 AM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/strategies-for-mental-health-at-work-and-keeping-psychologically-safe-tickets-1235190400739?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/strategies-for-mental-health-at-work-and-keeping-psychologically-safe-tickets-1235190400739?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/TorquayWalking.avif" alt="Outdoor Walking" class="event-img">
              <div class="event-info">
                <h3>MeTreat Retreats Women's Wellness Walk</h3>
                <div class="event-tags">
                  <span class="tag april">April</span>
                  <span class="tag outdoor">Outdoor Walking</span>
                  <span class="tag end">Sales Ended</span>
                </div>
                <p class="event-description">CONNECT, REVIVE & THRIVE AT OUR METREAT WELLNESS WALK!</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Torquay Beach</div>
                  <div><strong>Address:</strong> Torquay Beach Torquay, VIC 3228</div>
                  <!-- <div><strong>Group size:</strong> 8-12</div> -->
                  <div><strong>Date:</strong> April 25th</div>
                  <div><strong>Time:</strong> 11:00 AM - 2:00 AM</div>
                  <div class="event-link"><strong>Link:</strong>
                    https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch
                  </div>
                </div>
                <a href="https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer">
      <p>© 2025 by Inflowence | <router-link to="/privacy" class="footer-link">隐私政策</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Chart from 'chart.js/auto'

const currentTab = ref(0)
let chartInstance = null

const tabs = [
  { name: 'Screen Time and Emotional Wellbeing', insights: [
      'Increased screen time is associated with more negative emotions such as anxiety and sadness.',
      'Maintaining lower daily screen time correlates with better emotional wellbeing.',
      'Balanced digital habits foster more positive and neutral emotional states.'
    ]
  },
  { name: 'Digital Habits and Sleep Health', insights: [
      'More than 3 hours of daily social media use is linked with sleep disturbances.',
      'Sleep issues worsen significantly when daily usage exceeds 4 hours.',
      'Reducing evening screen time can improve sleep quality and mental health.'
    ]
  },
  { name: 'Engagement Metrics and Emotional Rewards', insights: [
      'Moderate posting and interaction (likes, comments) are positively linked with emotional wellbeing.',
      'Creators focusing on meaningful community engagement over numbers show better mental health.',
      'Prioritising genuine conversations over chasing virality strengthens long-term creator satisfaction.'
    ]
  },
  { name: 'Managing Digital Distractions and Anxiety', insights: [
      'Higher daily screen time is associated with elevated anxiety levels.',
      'Spending less time on digital activities correlates with lower anxiety scores.',
      'Practising regular tech-free breaks can significantly lower digital stress levels.'
    ]
  }
]

const switchTab = (index) => {
  currentTab.value = index
  renderChart()
}

const renderChart = () => {
  const ctx = document.getElementById('mainChart')
  if (chartInstance) chartInstance.destroy()

  if (currentTab.value === 0) {
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Below 1h', '1-3h', '3-5h'],
        datasets: [
          { label: 'Positive', backgroundColor: '#4bc0c0', data: [20, 30, 10] },
          { label: 'Negative', backgroundColor: '#ff6384', data: [10, 40, 60] },
          { label: 'Neutral', backgroundColor: '#ffcd56', data: [70, 30, 30] },
        ]
      },
      options: {
        responsive: true,
        plugins: { title: { display: false } },
        scales: { x: { stacked: true }, y: { stacked: true, max: 100 } }
      }
    })

  } else if (currentTab.value === 1) {
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['<1h', '1-2h', '2-3h', '3-4h', '4-5h', '>5h'],
        datasets: [{
          label: 'Sleep Problems (1-5)',
          data: [1.5, 2, 2.5, 3.2, 4, 4.5],
          borderColor: '#7e57c2',
          backgroundColor: '#7e57c2',
          fill: false,
          tension: 0.3
        }]
      },
      options: { responsive: true, plugins: { title: { display: false } } }
    })

  } else if (currentTab.value === 2) {
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Below 1h', '1-3h', '3-5h'],
        datasets: [{
          label: 'Engagement',
          data: [20, 50, 30],
          backgroundColor: '#42a5f5'
        }]
      },
      options: { responsive: true, plugins: { title: { display: false } } }
    })

  } else if (currentTab.value === 3) {
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Below 1h', '1-2h', '2-3h', '3-4h', '4-5h', 'Above 5h'],
        datasets: [{
          label: 'Average Anxiety',
          data: [1.2, 2.0, 2.8, 3.5, 4.2, 4.8],
          borderColor: '#66bb6a',
          backgroundColor: '#66bb6a',
          fill: false,
          tension: 0.3
        }]
      },
      options: { responsive: true, plugins: { title: { display: false } } }
    })
  }
}

onMounted(() => {
  renderChart()
})
</script>



<style scoped>
.visualisation-container {
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align top instead of center */
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
  align-items: center; /* Center title and boxes horizontally */
  margin-top: 20px; /* Push a little lower */
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
  width: 100%; /* Full width */
  max-width: 500px; /* Limit width nicely */
  box-shadow: 0px 1px 5px rgba(0, 0, 0, 0.05);
  text-align: center;
}


.tab.active {
  background: #e75a97;
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
}




.chart-wrapper {
  width: 100%;
  max-width: 800px;
  height: 400px;
  margin: 0 auto;
}





.creator-wellbeing {
  padding: 2rem;
}

.tabs {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: #e0e0e0;
  cursor: pointer;
  font-weight: 600;
}

.tab.active {
  background: #e75a97;
  color: white;
}

.chart-area {
  max-width: 800px;
  margin: 0 auto;
}

.insights {
  text-align: center;
  margin-top: 2rem;
}







/* Add hover zoom for charts */
.hover-zoom img {
  transition: transform 0.3s ease;
  cursor: pointer;
}

.hover-zoom img:hover {
  transform: scale(1.05);
}

.creator-wellbeing {
  background-color: #fffcf5;
  background-image:
    radial-gradient(circle at 25% 25%, rgba(230, 239, 182, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(230, 239, 182, 0.03) 0%, transparent 50%);
  min-height: 100vh;
  padding-top: 0;
}

/* Hero Section Styles */
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
  font-size: 5rem;
  font-weight: bold;
  background: linear-gradient(135deg, #6B64F3 0%, #8BDFE7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.4;
  display: block;
  margin-bottom: 0.5rem;
  white-space: nowrap;
  text-align: left;
  overflow: visible;
  padding-right: 1rem;
  padding-bottom: 0.5rem;
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
  white-space: nowrap;
  text-align: left;
  overflow: visible;
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

/* 添加响应式媒体查询 */
@media (max-width: 1800px) {
  .decorative-elements {
    width: 840px;
    grid-template-columns: repeat(6, 140px);
    opacity: 0.9;
    transform: translateX(-1.5rem);
  }
}

@media (max-width: 1536px) {
  .decorative-elements {
    width: 720px;
    grid-template-columns: repeat(6, 120px);
    opacity: 0.8;
    transform: translateX(-1rem);
  }
}

@media (max-width: 1280px) {
  .decorative-elements {
    width: 600px;
    grid-template-columns: repeat(6, 100px);
    opacity: 0.7;
    transform: translateX(-0.5rem);
    row-gap: 0.75rem;
  }

  .title-group h2,
  .subtitle {
    white-space: normal;
  }
}

@media (max-width: 1024px) {
  .decorative-elements {
    transform: translateX(0) scale(0.9);
    opacity: 0.5;
    row-gap: 0.5rem;
  }

  .title-group h1 {
    white-space: normal;
  }
}

@media (max-width: 768px) {
  .decorative-elements {
    opacity: 0.1;
    transform: translateX(0) scale(0.8);
  }

  .hero-content {
    flex-direction: column;
    align-items: flex-start;
    padding-top: 0.75rem;
    min-height: 22vh;
  }

  .hero-section {
    min-height: 22vh;
    padding: 7rem 0 0.5rem;
  }

  .slogan {
    max-width: 90%;
  }

  .title-group h1 {
    font-size: 3.5rem;
  }

  .title-group h2 {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1.125rem;
  }
}

@media (max-width: 640px) {
  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.7);
  }

  .hero-content {
    min-height: 18vh;
    padding-top: 0.25rem;
  }

  .hero-section {
    min-height: 18vh;
    padding: 7.5rem 0 0.5rem;
    margin-bottom: 1rem;
  }

  .title-group h1 {
    font-size: 2.5rem;
  }

  .title-group h2 {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .decorative-elements {
    opacity: 0;
    display: none;
  }

  .hero-content {
    min-height: 16vh;
  }

  .hero-section {
    min-height: 16vh;
    padding: 8rem 0 0.5rem;
  }
}

/* 响应式布局支持 */
@media (max-width: 1200px) {
  .container {
    max-width: 95%;
  }

  .dashboard-content,
  .resource-content {
    flex-direction: column;
  }

  .chart-container,
  .insights-container,
  .map-container,
  .resource-details {
    width: 100%;
    margin-bottom: 2rem;
  }

  .activities-grid {
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .section-subtitle {
    font-size: 1rem;
  }

  .tabs,
  .resource-tabs {
    flex-wrap: wrap;
  }

  .tab,
  .resource-tab {
    margin: 0.25rem;
  }

  .activities-grid {
    grid-template-columns: 1fr;
  }

  .events-grid {
    grid-template-columns: 1fr;
  }

  .activities-header {
    flex-direction: column;
    gap: 1rem;
  }

  .recent-title {
    font-size: 1.2rem;
  }
}

@media (max-width: 640px) {
  .section-title {
    font-size: 1.75rem;
  }

  .chart-title,
  .insights-title,
  .resource-name {
    font-size: 1.25rem;
  }

  .resource-actions {
    flex-direction: column;
    gap: 0.75rem;
  }

  .action-btn {
    width: 100%;
  }

  .event-card {
    flex-direction: column;
  }

  .event-img {
    width: 100%;
    height: 200px;
  }
}

.dashboard-section {
  padding: 5rem 0;
  position: relative;
  margin-bottom: 7rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

/* 通用部分样式 / Common section styles */
.section-title,
.section-subtitle {
  position: relative;
  z-index: 2;
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
}

section {
  padding: 5rem 0;
  position: relative;
  border-bottom: none;
  margin-bottom: 7rem;
}

section:last-child {
  margin-bottom: 3rem;
}

section:not(:last-child)::after {
  display: none;
}

/* 仪表板部分 / Dashboard section */
.dashboard-section {
  background-color: #fffcf5;
}

.tabs,
.resource-tabs,
.activities-header,
.activities-grid {
  position: relative;
  z-index: 2;
}

.tabs {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.tab {
  padding: 0.5rem 1rem;
  cursor: pointer;
  color: #666;
  position: relative;
}

.tab.active {
  color: #e75a97;
  font-weight: 600;
}

.tab.active::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e75a97;
}

.dashboard-content {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 2rem;
}

.chart-container,
.resource-content,
.activity-card {
  position: relative;
  z-index: 2;
  background-color: #fff;
  background-image: linear-gradient(to bottom, #fff, rgba(255, 255, 255, 0.95));
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(230, 239, 182, 0.4);
}

.chart-container {
  padding: 2rem;
}

.chart-title {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
  text-align: center;
  font-weight: 600;
  color: #333;
}

.chart {
  height: 250px;
  position: relative;
}

.chart-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.insights-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.insights-title {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

.insight-card {
  position: relative;
  z-index: 2;
  background-color: #fffaee;
  background-image: linear-gradient(to bottom, #fffaee, rgba(255, 250, 238, 0.95));
  padding: 1.5rem;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(230, 239, 182, 0.4);
}

.insight-card p {
  color: #333;
  line-height: 1.5;
}

/* 资源查找器部分 / Resource finder section */
.resource-finder-section {
  background-color: #fffcf5;
}

.resource-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.resource-tab {
  padding: 0.75rem 1.5rem;
  background-color: #f0f0f0;
  border-radius: 20px;
  cursor: pointer;
  color: #666;
}

.resource-tab.active {
  background-color: #e75a97;
  color: white;
}

.resource-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(230, 239, 182, 0.4);
  position: relative;
  z-index: 2;
}

.map-container {
  position: relative;
  height: 100%;
  min-height: 400px;
}

.map-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.position-btn {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.pin-icon {
  width: 18px;
  height: 18px;
}

.resource-details {
  padding: 2rem;
}

.resource-name {
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.rating-score {
  font-weight: 600;
  color: #333;
}

.stars {
  color: #ffc107;
}

.reviews {
  color: #666;
}

.resource-location,
.resource-website {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.location-icon,
.website-icon {
  width: 18px;
  height: 18px;
}

.online-switch {
  background-color: transparent;
  border: 1px solid #ddd;
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  margin-left: 0.5rem;
  color: #666;
  cursor: pointer;
  font-size: 0.85rem;
}

.opening-hours {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}

.opening-hours h4 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: #333;
}

.hours-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.day {
  color: #333;
  font-weight: 500;
}

.hours {
  color: #666;
}

.resource-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-btn {
  flex: 1;
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.75rem 1rem;
  border-radius: 25px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 500;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* 活动中心部分 / Activities hub section */
.activities-section {
  background-color: #fffcf5;
}

.activities-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.recent-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

/* 统一使用此处的view-all-btn样式定义 */
.view-all-btn {
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.5rem 1.25rem;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.view-all-btn:hover {
  background-color: #d4407f;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.activities-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.activity-card {
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(230, 239, 182, 0.4);
  position: relative;
  z-index: 2;
  transition: all 0.3s ease-in-out;
  cursor: pointer;
}

.activity-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(231, 90, 151, 0.2);
}

.activity-card:hover .activity-title {
  color: #e75a97;
}

.activity-card:hover .activity-img {
  transform: scale(1.05);
}

.activity-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.activity-title {
  font-size: 1.2rem;
  font-weight: 600;
  padding: 1rem;
  padding-bottom: 0.5rem;
  color: #333;
}

.activity-tags {
  padding: 0 1rem;
  margin-bottom: 0.5rem;
  display: flex;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.5rem;
  border-radius: 15px;
  font-size: 0.85rem;
  color: white;
}

.tag.april {
  background-color: #e75a97;
}

.tag.outdoor {
  background-color: #6c63ff;
}

.tag.online {
  background-color: #4CAF50;
}

.tag.mental {
  background-color: #e67e22;
}

.activity-details {
  padding: 0 1rem 1rem;
  display: flex;
  justify-content: space-between;
  color: #666;
  font-size: 0.9rem;
}

/* 页脚 / Footer */
.footer {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
}

.footer-link {
  color: #e75a97;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-link:hover {
  color: #d4407f;
  text-decoration: underline;
}

/* 响应式设计 / Responsive design */
@media (max-width: 1024px) {

  .dashboard-content,
  .resource-content {
    grid-template-columns: 1fr;
  }

  .map-container {
    min-height: 300px;
  }

  .activities-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .tabs {
    flex-wrap: wrap;
  }

  .activities-grid {
    grid-template-columns: 1fr;
  }

  .resource-tabs {
    flex-direction: column;
  }
}

/* 模态窗口样式 */
.activities-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  overflow-y: auto;
  padding: 2rem 0;
}

.activities-modal {
  background-color: #fff;
  border-radius: 16px;
  width: 90%;
  max-width: 1000px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 10;
}

.modal-header h2 {
  font-size: 1.8rem;
  color: #333;
  margin: 0;
}

.close-modal-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #666;
  cursor: pointer;
  transition: color 0.3s;
}

.close-modal-btn:hover {
  color: #e75a97;
}

.modal-content {
  padding: 2rem;
}

/* 搜索栏样式 */
.search-bar {
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 25px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #e75a97;
}

/* 筛选器样式 */
.event-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-group {
  flex: 1;
  min-width: 180px;
}

.filter-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.filter-group select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
  transition: border-color 0.3s;
}

.filter-group select:focus {
  border-color: #e75a97;
}

/* 事件卡片样式 */
.events-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
}

.event-card {
  display: flex;
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  border: 1px solid #eee;
}

.event-img {
  width: 280px;
  height: auto;
  object-fit: cover;
}

.event-info {
  padding: 1.5rem;
  flex: 1;
}

.event-info h3 {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #333;
}

.event-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.tag.ticket {
  background-color: #ff5252;
}

.tag.may {
  background-color: #2196F3;
}

.tag.june {
  background-color: #9C27B0;
}

.tag.workshop {
  background-color: #795548;
}

.tag.free {
  background-color: #4CAF50;
}

.tag.october {
  background-color: #FF9800;
}

.tag.workplace {
  background-color: #607D8B;
}

.tag.charged {
  background-color: #F44336;
}

.tag.end {
  background-color: #9E9E9E;
}

.event-description {
  margin-bottom: 1.5rem;
  color: #666;
  line-height: 1.5;
}

.event-meta {
  margin-bottom: 1.5rem;
}

.event-meta div {
  margin-bottom: 0.5rem;
  color: #333;
}

.register-btn {
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s, transform 0.2s;
}

.register-btn:hover {
  background-color: #d4407f;
  transform: translateY(-2px);
}

/* 响应式调整 */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
  }

  .event-img {
    width: 100%;
    height: 200px;
  }

  .event-filters {
    flex-direction: column;
  }

  .filter-group {
    width: 100%;
  }

  .activities-modal {
    width: 95%;
    max-height: 90vh;
  }

  .modal-content {
    padding: 1.5rem;
  }
}

/* 隐藏链接标签 */
.event-meta div.event-link {
  display: none;
}

/* 为按钮链接添加样式 */
.register-btn-link {
  text-decoration: none;
  display: inline-block;
}

/* 活动卡片链接样式 */
.activity-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  cursor: pointer;
}

.insights-gallery {
  padding: 4rem 2rem;
  text-align: center;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.image-grid img {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.tab.active {
  background: #e75a97;
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
}
</style>
