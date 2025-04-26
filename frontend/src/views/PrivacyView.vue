<template>
  <div class="privacy-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Privacy Controls</h1>
            <h2>Cross-Platform Privacy Control Guide</h2>
          </div>
          <p class="subtitle">Try to prevent your privacy follow these privacy setting steps across differenct platforms</p>
        </div>
      </div>
    </section>
    
    <!-- Cross-Platform Privacy Control Guide -->
    <section class="privacy-section">
      <div class="container">
        <h1 class="section-title">Cross-Platform Privacy Control Guide</h1>
        <div class="guide-description">
          <p>Try to prevent your privacy follow these privacy setting steps across differenct platforms</p>
        </div>
        
        <!-- Youtube section -->
        <div class="platform-section youtube-section">
          <div class="platform-header" @click="togglePlatform('youtube')" :class="{ 'active': activePlatform === 'youtube' }">
            <img src="../assets/icons/logo/youtube.svg.png" alt="Youtube Logo" class="platform-logo">
            <h2>Youtube</h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'youtube' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'youtube'">
            <div class="privacy-settings">
              <div class="settings-sidebar">
                <div class="sidebar-nav">
                  <div class="nav-group">
                    <div class="nav-item" :class="{ 'active': activeGuide === 'settings' }" @click="switchGuide('settings')">
                      <h3>Privacy setting guides</h3>
                    </div>
                    
                    <div v-if="activeGuide === 'settings'" class="guide-options">
                      <ul>
                        <li class="active">· Browser version</li>
                        <li>· Mobile version</li>
                      </ul>
                    </div>
                  </div>
                  
                  <div class="nav-item" :class="{ 'active': activeGuide === 'tips' }" @click="switchGuide('tips')">
                    <h3>Privacy tips</h3>
                  </div>
                  <div class="nav-item" :class="{ 'active': activeGuide === 'boundary' }" @click="switchGuide('boundary')">
                    <h3>Boundary tips</h3>
                  </div>
                </div>
              </div>
              
              <div class="settings-content">
                <div class="settings-header">
                  <h3>How to change your default privacy settings</h3>
                  <p>If you use Youtube in your browser</p>
                  <span class="update-date">Update to: 04/14/2025</span>
                </div>
                
                <div class="settings-steps">
                  <div class="step">
                    <h4>Step 1:</h4>
                    <p>Open YouTube in your web browser and sign in to your account. Look for your profile picture in the top-right corner of the screen and click on it to reveal a dropdown menu.</p>
                    <div class="step-image">
                      <img src="../assets/screenshots/youtube-step1.png" alt="YouTube Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'">
                    </div>
                  </div>
                  
                  <div class="step">
                    <h4>Step 2:</h4>
                    <p>In the dropdown menu that appears, click on "Settings." This will take you to the YouTube settings page where you can manage all aspects of your account.</p>
                    <div class="step-image">
                      <img src="../assets/screenshots/youtube-step2.png" alt="YouTube Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'">
                    </div>
                  </div>
                </div>
                
                <div class="quick-view">
                  <button>Quick view</button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- TikTok section -->
        <div class="platform-section tiktok-section">
          <div class="platform-header" @click="togglePlatform('tiktok')" :class="{ 'active': activePlatform === 'tiktok' }">
            <img src="../assets/icons/logo/tiktok.png" alt="TikTok Logo" class="platform-logo">
            <h2>Tiktok</h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'tiktok' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'tiktok'">
            <div class="coming-soon">
              <p>Privacy settings guide coming soon</p>
            </div>
          </div>
        </div>
        
        <!-- Instagram section -->
        <div class="platform-section instagram-section">
          <div class="platform-header" @click="togglePlatform('instagram')" :class="{ 'active': activePlatform === 'instagram' }">
            <img src="../assets/icons/logo/insta.png" alt="Instagram Logo" class="platform-logo">
            <h2>Instagram</h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'instagram' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'instagram'">
            <div class="coming-soon">
              <p>Privacy settings guide coming soon</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <div class="footer">
      <p>© 2025 by Inflowence | <router-link to="/privacy" class="footer-link">Privacy Policy</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// 跟踪当前激活的平台
const activePlatform = ref(null);

// 跟踪当前激活的指南类型（设置指南、隐私提示、边界提示）
const activeGuide = ref('settings');

// 切换平台展开/折叠状态
const togglePlatform = (platform) => {
  if (activePlatform.value === platform) {
    activePlatform.value = null;
  } else {
    activePlatform.value = platform;
  }
};

// 切换指南类型
const switchGuide = (guide) => {
  activeGuide.value = guide;
};
</script>

<style scoped>
.privacy-view {
  background-color: #fffdf5;
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
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
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

/* Container styles */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

/* Privacy section styles */
.privacy-section {
  padding: 3rem 0;
  position: relative;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  color: #000;
  text-align: center;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.guide-description {
  text-align: center;
  margin-bottom: 3rem;
  padding: 0.5rem 1rem;
  background-color: #f0e6ff;
  border: 1px solid #cbb3ff;
  border-radius: 4px;
  max-width: 800px;
  margin: 0 auto 3rem;
}

.guide-description p {
  font-size: 1.1rem;
  color: #333;
  line-height: 1.6;
}

/* Platform section styles */
.platform-section {
  margin-bottom: 3rem;
  background-color: rgba(235, 250, 180, 0.3);
  border-radius: 16px;
  padding: 2rem;
  overflow: hidden;
}

.platform-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  position: relative;
  padding: 0.5rem;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.platform-header:hover {
  background-color: rgba(235, 250, 180, 0.8);
}

.platform-header.active {
  background-color: rgba(231, 90, 151, 0.1);
}

.expand-icon {
  margin-left: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.expand-icon span {
  font-size: 1rem;
  color: #666;
  transition: transform 0.3s ease;
}

.expand-icon span.rotated {
  transform: rotate(180deg);
}

.platform-content {
  margin-top: 1rem;
  transition: all 0.3s ease-in-out;
  overflow: hidden;
}

.platform-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.platform-header h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

/* YouTube section special styles */
.youtube-section {
  background-color: rgba(235, 250, 180, 0.3);
}

/* TikTok section special styles */
.tiktok-section {
  background-color: rgba(235, 250, 180, 0.3);
}

/* Instagram section special styles */
.instagram-section {
  background-color: rgba(235, 250, 180, 0.3);
}

/* Privacy settings section */
.privacy-settings {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.settings-sidebar {
  padding: 2rem;
  background-color: #f9f9f9;
  border-right: 1px solid #eee;
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.nav-group {
  display: flex;
  flex-direction: column;
}

.nav-item {
  cursor: pointer;
  padding: 0.5rem 0;
  border-left: 3px solid transparent;
  padding-left: 0.5rem;
  transition: all 0.3s;
}

.nav-item:hover {
  border-left-color: #e75a97;
}

.nav-item.active {
  border-left-color: #e75a97;
}

.nav-item h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #555;
  transition: color 0.3s;
  margin: 0;
}

.nav-item:hover h3 {
  color: #e75a97;
}

.nav-item.active h3 {
  color: #e75a97;
}

.guide-options {
  margin-top: 0.5rem;
  margin-left: 1.5rem;
}

.guide-options ul {
  list-style: none;
  padding: 0;
  margin-bottom: 0;
}

.guide-options li {
  padding: 0.5rem 0;
  cursor: pointer;
  font-size: 1.1rem;
  color: #555;
  transition: color 0.3s;
}

.guide-options li:hover {
  color: #e75a97;
}

.guide-options li.active {
  color: #e75a97;
  font-weight: 500;
}

.settings-content {
  padding: 2rem;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-header h3 {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
}

.settings-header p {
  font-size: 1.1rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.update-date {
  font-size: 0.9rem;
  color: #777;
}

.settings-steps {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.step {
  margin-bottom: 1.5rem;
}

.step h4 {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #333;
}

.step p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1rem;
  color: #555;
}

.step-image {
  width: 100%;
  height: 250px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f9f9f9;
}

.step-image img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.quick-view {
  display: flex;
  justify-content: flex-end;
  margin-top: 2rem;
}

.quick-view button {
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
}

.quick-view button:hover {
  background-color: #d4407f;
}

.coming-soon {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.coming-soon p {
  font-size: 1.2rem;
  color: #777;
  font-style: italic;
}

/* Footer */
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

/* Responsive design */
@media (max-width: 1024px) {
  .privacy-settings {
    grid-template-columns: 1fr;
  }
  
  .settings-sidebar {
    border-right: none;
    border-bottom: 1px solid #eee;
    padding-bottom: 1rem;
  }
  
  .sidebar-nav {
    flex-direction: column;
    flex-wrap: nowrap;
    gap: 1.5rem;
  }
  
  .nav-group {
    width: 100%;
  }
  
  .nav-item {
    border-left: none;
    border-bottom: 3px solid transparent;
    padding-left: 0;
    padding-bottom: 0.5rem;
  }
  
  .nav-item:hover, 
  .nav-item.active {
    border-left-color: transparent;
    border-bottom-color: #e75a97;
  }
  
  .guide-options {
    margin-left: 0;
    margin-top: 0.75rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .platform-section {
    padding: 1.5rem;
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
  .title-group h1 {
    font-size: 2.5rem;
    white-space: normal;
  }
  
  .title-group h2 {
    font-size: 1.5rem;
    white-space: normal;
  }
  
  .subtitle {
    font-size: 1rem;
    white-space: normal;
  }
  
  .platform-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
  }
  
  .platform-header h2 {
    font-size: 1.5rem;
  }
  
  .step-image {
    height: 180px;
  }
  
  .expand-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
  }
}
</style>
