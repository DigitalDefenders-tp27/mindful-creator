<template>
  <div class="creator-wellbeing">
    <!-- 数字影响分析仪表板 / Digital Impact Analysis Dashboard -->
    <section class="dashboard-section">
      <div class="container">
        <h1 class="section-title">Digital Impact Analysis Dashboard</h1>
        <p class="section-subtitle">Explore how your usage patterns affect wellbeing<br>based on real data</p>
        
        <div class="tabs">
          <div class="tab active">Average working time</div>
          <div class="tab">Anxiety correlation</div>
          <div class="tab">...</div>
          <div class="tab">...</div>
        </div>
        
        <div class="dashboard-content">
          <div class="chart-container">
            <h3 class="chart-title">AVERAGE WORKING TIME FOR<br>CONTENT CREATOR</h3>
            <div class="chart">
              <img src="../assets/icons/elements/chart-placeholder.svg" alt="Chart" class="chart-img">
            </div>
          </div>
          
          <div class="insights-container">
            <h3 class="insights-title">KEY INSIGHT:</h3>
            <div class="insight-card">
              <p>Content creators tend to work 20% longer hours during seasonal campaigns.</p>
            </div>
            <div class="insight-card">
              <p>Weekend work hours have increased by 15% in the last quarter.</p>
            </div>
            <div class="insight-card">
              <p>Taking regular breaks can reduce stress levels by up to 30%.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 健康资源查找器 / Wellbeing Resource Finder -->
    <section class="resource-finder-section">
      <div class="container">
        <h1 class="section-title">Wellbeing Resource Finder</h1>
        <p class="section-subtitle">Find and navigate yourself to get wellbeing<br>resources easily near you.</p>
        
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
        <p class="section-subtitle">Release your stress by joining fun activities and<br>making like-minded friends.</p>
        
        <div class="activities-header">
          <h3 class="recent-title">RECENT CAMPAIGNS...</h3>
          <button @click="showAllEvents" class="view-all-btn">VIEW ALL EVENTS</button>
        </div>
        
        <div class="activities-grid">
          <div class="activity-card">
            <img src="../assets/icons/elements/activity-yoga.svg" alt="Yoga" class="activity-img">
            <h3 class="activity-title">Beach yoga at St Kilda</h3>
            <div class="activity-tags">
              <span class="tag april">April</span>
              <span class="tag outdoor">Outdoor activities</span>
            </div>
            <div class="activity-details">
              <span class="group-size">Group size 10-20</span>
              <span class="location">Melbourne</span>
            </div>
          </div>
          
          <div class="activity-card">
            <img src="../assets/icons/elements/activity-workshop.svg" alt="Workshop" class="activity-img">
            <h3 class="activity-title">Emotional resilience workshops</h3>
            <div class="activity-tags">
              <span class="tag online">Online</span>
              <span class="tag mental">Mental health</span>
            </div>
            <div class="activity-details">
              <span class="group-size">Group size 15-30</span>
              <span class="location">Melbourne</span>
            </div>
          </div>
          
          <div class="activity-card">
            <img src="../assets/icons/elements/activity-bushwalking.svg" alt="Bushwalking" class="activity-img">
            <h3 class="activity-title">Bushwalking in national parks</h3>
            <div class="activity-tags">
              <span class="tag april">April</span>
              <span class="tag outdoor">Outdoor activities</span>
            </div>
            <div class="activity-details">
              <span class="group-size">Group size 5-15</span>
              <span class="location">Melbourne</span>
            </div>
          </div>
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
          <div class="event-filters">
            <div class="filter-group">
              <label>Location:</label>
              <select>
                <option>All locations</option>
                <option>Melbourne</option>
                <option>Sydney</option>
                <option>Brisbane</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Category:</label>
              <select>
                <option>All types</option>
                <option>Outdoor Wellness</option>
                <option>Mental Health</option>
                <option>Physical Fitness</option>
                <option>Healthy Eating</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Month:</label>
              <select>
                <option>Any time</option>
                <option>March</option>
                <option>April</option>
                <option>May</option>
                <option>June</option>
              </select>
            </div>
          </div>
          
          <div class="events-grid">
            <div class="event-card">
              <img src="../assets/icons/activitiesImages/mentalHealthWorkshop.avif" alt="Beach yoga" class="event-img">
              <div class="event-info">
                <h3>Mentally Healthy Workplaces Workshop</h3>
                <div class="event-tags">
                  <span class="tag may">May</span>
                  <span class="tag workshop">Workshop</span>
                  <span class="tag free">Free Event</span>
                </div>
                <p class="event-description">JThis workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Brisbane</div>
                  <div><strong>Address:</strong> Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000</div>
                  <div><strong>Date:</strong> 1st May 2025</div>
                  <div><strong>Time:</strong> 8:00 AM - 12:00 PM</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>

            <div class="event-card">
              <img src="../assets/icons/activitiesImages/mentalHealthWorkshop.avif" alt="Beach yoga" class="event-img">
              <div class="event-info">
                <h3>Mentally Healthy Workplaces Workshop</h3>
                <div class="event-tags">
                  <span class="tag june">June</span>
                  <span class="tag workshop">Workshop</span>
                  <span class="tag free">Free Event</span>
                </div>
                <p class="event-description">JThis workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Brisbane</div>
                  <div><strong>Address:</strong> Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000</div>
                  <div><strong>Date:</strong> 4th June 2025</div>
                  <div><strong>Time:</strong> 8:00 AM - 12:00 PM</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>

            
            <div class="event-card">
              <img src="../assets/icons/elements/activity-workshop.svg" alt="Emotional workshops" class="event-img">
              <div class="event-info">
                <h3>Emotional resilience workshops</h3>
                <div class="event-tags">
                  <span class="tag april">April</span>
                  <span class="tag mental">Mental Health</span>
                  <span class="tag charged">Charged Event</span>
                </div>
                <p class="event-description">Build your emotional resilience toolbox with our expert-led workshops. Learn practical techniques to manage stress and enhance wellbeing.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Melbourne</div>
                  <div><strong>Group size:</strong> 15-30</div>
                  <div><strong>Date:</strong> April 15th & 22nd</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>
            
            <div class="event-card">
              <img src="../assets/icons/elements/activity-bushwalking.svg" alt="Bushwalking" class="event-img">
              <div class="event-info">
                <h3>Bushwalking in national parks</h3>
                <div class="event-tags">
                  <span class="tag april">April</span>
                  <span class="tag outdoor">Outdoor Wellness</span>
                  <span class="tag free">Free Event</span>
                </div>
                <p class="event-description">Explore Victoria's beautiful national parks with our guided bushwalking groups. Connect with nature and like-minded creators.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Melbourne</div>
                  <div><strong>Group size:</strong> 5-15</div>
                  <div><strong>Date:</strong> April 8th & 29th</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>
            
            <div class="event-card">
              <img src="../assets/icons/elements/activity-gym.svg" alt="Gym sessions" class="event-img">
              <div class="event-info">
                <h3>Local gym sessions</h3>
                <div class="event-tags">
                  <span class="tag march">March</span>
                  <span class="tag physical">Physical Fitness</span>
                  <span class="tag charged">Charged Event</span>
                </div>
                <p class="event-description">Join our creator-friendly gym sessions designed specifically for people who spend long hours at desks. Focus on posture, strength and energy.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Sydney</div>
                  <div><strong>Group size:</strong> 5-10</div>
                  <div><strong>Date:</strong> Every Tuesday in March</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>
            
            <div class="event-card">
              <img src="../assets/icons/elements/activity-market.svg" alt="Farmers market" class="event-img">
              <div class="event-info">
                <h3>Farmers' market tours</h3>
                <div class="event-tags">
                  <span class="tag april">April</span>
                  <span class="tag healthy">Healthy Eating</span>
                  <span class="tag charged">Charged Event</span>
                </div>
                <p class="event-description">Discover local produce and learn about sustainable eating with our guided farmers' market tours. Includes cooking demonstrations and tastings.</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> Melbourne</div>
                  <div><strong>Group size:</strong> 8-12</div>
                  <div><strong>Date:</strong> April 1st & 15th</div>
                </div>
                <button class="register-btn">Register Now</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="footer">
      <p>© 2025 by Inflowence</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Modal state management
const isModalVisible = ref(false);

// Show all events modal
const showAllEvents = () => {
  isModalVisible.value = true;
  document.body.style.overflow = 'hidden'; // Prevent background scrolling
};

// Close modal
const closeModal = () => {
  isModalVisible.value = false;
  document.body.style.overflow = ''; // Restore scrolling
};
</script>

<style scoped>
.creator-wellbeing {
  background-color: #fffcf5;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(230, 239, 182, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 75% 75%, rgba(230, 239, 182, 0.03) 0%, transparent 50%);
  min-height: 100vh;
  padding-top: 80px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

/* 通用部分样式 / Common section styles */
.section-title, .section-subtitle {
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
  content: '';
  position: absolute;
  bottom: -150px;
  left: 0;
  right: 0;
  height: 300px;
  background: linear-gradient(to bottom, 
    rgba(230, 239, 182, 0) 0%, 
    rgba(230, 239, 182, 0.08) 10%,
    rgba(230, 239, 182, 0.15) 20%,
    rgba(230, 239, 182, 0.25) 30%,
    rgba(230, 239, 182, 0.4) 40%,
    rgba(230, 239, 182, 0.5) 50%, 
    rgba(230, 239, 182, 0.4) 60%,
    rgba(230, 239, 182, 0.25) 70%,
    rgba(230, 239, 182, 0.15) 80%,
    rgba(230, 239, 182, 0.08) 90%,
    rgba(230, 239, 182, 0) 100%);
  pointer-events: none;
  z-index: 0;
}

/* 仪表板部分 / Dashboard section */
.dashboard-section {
  background-color: #fffcf5;
}

.tabs, .resource-tabs, .activities-header, .activities-grid {
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

.chart-container, .resource-content, .activity-card {
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

.resource-location, .resource-website {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.location-icon, .website-icon {
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

.view-all-btn {
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(231, 90, 151, 0.3);
}

.view-all-btn:hover {
  background-color: #d4488b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(231, 90, 151, 0.4);
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
}

.activity-img {
  width: 100%;
  height: 180px;
  object-fit: cover;
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

/* Activities modal styles */
.activities-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  overflow-y: auto;
  padding: 20px;
}

.activities-modal {
  background-color: #fff;
  border-radius: 16px;
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  position: relative;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  font-size: 1.8rem;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.close-modal-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
}

.modal-content {
  padding: 1.5rem;
}

.event-filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  min-width: 180px;
}

.filter-group label {
  font-weight: 500;
  color: #333;
}

.filter-group select {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.events-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.event-card {
  display: flex;
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03);
  border: 1px solid rgba(230, 239, 182, 0.4);
}

.event-img {
  width: 200px;
  height: 100%;
  object-fit: cover;
  background-color: #f5f5f5;
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

.tag.march {
  background-color: #3498db;
}

.tag.charged {
  background-color: #e67e22;
}

.tag.free {
  background-color: #2ecc71;
}

.tag.physical {
  background-color: #9b59b6;
}

.tag.healthy {
  background-color: #27ae60;
}

.event-description {
  margin-bottom: 1rem;
  color: #555;
  line-height: 1.5;
}

.event-meta {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.register-btn {
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.register-btn:hover {
  background-color: #d4488b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(231, 90, 151, 0.3);
}

/* Responsive styles for the modal */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
  }
  
  .event-img {
    width: 100%;
    height: 180px;
  }
  
  .event-meta {
    grid-template-columns: 1fr;
  }
}

/* 页脚 / Footer */
.footer {
  padding: 2rem;
  text-align: center;
  color: #666;
  font-size: 0.9rem;
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
</style> 