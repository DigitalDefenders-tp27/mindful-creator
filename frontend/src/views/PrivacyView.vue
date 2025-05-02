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
          <p class="subtitle" style="background: none; border: none;">Try to prevent your privacy follow these privacy setting steps across differenct platforms</p>
        </div>
      </div>
    </section>
    
    <!-- Cross-Platform Privacy Control Guide -->
    <section class="privacy-section">
      <div class="container">
        <h1 class="section-title" style="background: none; border: none;">Platform-Specific Privacy Settings</h1>
        <div class="guide-description" style="background: none; border: none;">
          <p style="background: none !important; border: none !important; margin: 0; padding: 0; box-shadow: none; color: #666;">Detailed step-by-step instructions for managing your digital footprint across major content platforms</p>
        </div>
        
        <!-- Youtube section -->
        <div class="platform-section youtube-section">
          <div class="platform-header" @click="togglePlatform('youtube')" :class="{ 'active': activePlatform === 'youtube' }">
            <img src="../assets/icons/logo/youtube.svg.png" alt="Youtube Logo" class="platform-logo">
            <h2>Youtube <span class="read-time">(Est. 10 min read)</span></h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'youtube' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'youtube'">
            <div class="privacy-settings">
              <!-- REMOVE SIDEBAR START -->
              <!-- <div class="settings-sidebar">
                <div class="sidebar-nav">
                  <div class="nav-group">
                    <div class="nav-item" :class="{ 'active': activeGuide === 'settings' }" @click="switchGuide('settings')">
                      <h3>Privacy setting guides</h3>
                    </div>
                    
                    <div v-if="activeGuide === 'settings'" class="guide-options">
                      <ul>
                        <li :class="{ 'active': activeVersion === 'browser' }" @click="switchVersion('browser')">· Browser version</li>
                        <li :class="{ 'active': activeVersion === 'mobile' }" @click="switchVersion('mobile')">· Mobile version</li>
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
              </div> -->
              <!-- REMOVE SIDEBAR END -->
              
              <div class="settings-content-area">
                <!-- ADD TABS START -->
                <div class="tab-navigation">
                  <button 
                    :class="{ 'active': activeGuide === 'settings' }" 
                    @click="switchGuide('settings')"
                  >
                    Setting Guides
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'tips' }" 
                    @click="switchGuide('tips')"
                  >
                    Privacy Tips
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'boundary' }" 
                    @click="switchGuide('boundary')"
                  >
                    Boundary Tips
                  </button>
              </div>
                <div class="sub-tab-navigation" v-if="activeGuide === 'settings'">
                  <button 
                    :class="{ 'active': activeVersion === 'browser' }" 
                    @click="switchVersion('browser')"
                  >
                    Browser
                  </button>
                  <button 
                    :class="{ 'active': activeVersion === 'mobile' }" 
                    @click="switchVersion('mobile')"
                  >
                    Mobile (iOS)
                  </button>
                </div>
                <!-- ADD TABS END -->

                <!-- Quick View Button -->
                <div class="quick-view">
                   <button @click="showQuickView('youtube')">Quick view</button>
                </div>

                <div class="settings-guide-content" v-if="activeGuide === 'settings'">
              <div class="settings-content">
                    <div v-if="activeVersion === 'browser'">
                      <div class="section-header" @click="toggleYoutubeSection('default')">
                  <h3>How to change your default privacy settings</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeSection === 'default' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeSection === 'default'">
                  <p>If you use Youtube in your browser</p>
                  <span class="update-date">Update to: 04/14/2025</span>
                <div class="settings-steps">
                  <div class="step">
                    <h4>Step 1:</h4>
                    <p>Open YouTube in your web browser and sign in to your account. Look for your profile picture in the top-right corner of the screen and click on it to reveal a dropdown menu.</p>
                    <div class="step-image">
                               <img src="../assets/screenshots/youtube_1.svg" alt="YouTube Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_1.svg')">
                    </div>
                  </div>
                  
                  <div class="step">
                    <h4>Step 2:</h4>
                    <p>In the dropdown menu that appears, click on "Settings." This will take you to the YouTube settings page where you can manage all aspects of your account.</p>
                    <div class="step-image">
                               <img src="../assets/screenshots/youtube_2.svg" alt="YouTube Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_2.svg')">
                    </div>
                  </div>

                  <div class="step">
                            <h4>Step 3:</h4>
                            <p>In the left sidebar, click on "Privacy". This will take you to the privacy settings page where you can control who can see your activity and manage your data.</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_3.svg" alt="YouTube Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_3.svg')">
                            </div>
                </div>
                
                          <div class="step">
                            <h4>Step 4:</h4>
                            <p>Subscriptions Privacy - Keep all my subscriptions private</p>
                            <ul>
                              <li>If enabled (ON): Your channel subscriptions remain private, preventing others from analyzing your interests or industry connections</li>
                              <li>If disabled (OFF): Your subscriptions become public, potentially revealing your content preferences, research patterns, or competitive analysis</li>
                              <li>Recommendation for content creators: Enable (ON) when researching competitors, exploring sensitive topics, or maintaining separation between personal interests and public brand. Disable (OFF) when intentionally showcasing industry support or participating in community building.</li>
                            </ul>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_4.svg" alt="YouTube Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_4.svg')">
                </div>
                            
                            <p>Live Chat Privacy - Turn off Super Chat and Super Stickers celebrations</p>
                            <ul>
                              <li>If enabled (ON): Your financial support remains private with no public celebrations, protecting spending habits and preventing potential targeting based on your support level</li>
                              <li>If disabled (OFF): Your Super Chat and Stickers purchases will be publicly celebrated, making your spending visible to all viewers in the chat</li>
                              <li>Recommendation for content creators: Enable (ON) when observing competitor strategies or supporting channels discreetly. Disable (OFF) when building relationships with other creators or researching audience engagement mechanics for your own streams.</li>
                            </ul>
                          </div>
                        </div>
                      </div>

                      <div class="section-header" @click="toggleYoutubeSection('perVideo')">
                        <h3>Per-Video Privacy Settings</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeSection === 'perVideo' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeSection === 'perVideo'">
                        <div class="settings-steps">
                          <div class="step">
                            <h4>Step 1:</h4>
                            <p>Open YouTube in your web browser and sign in to your account. Click on your profile picture in the top right corner and go to YouTube Studio.</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_5.svg" alt="YouTube Per-Video Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_5.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 2:</h4>
                            <p>Click "Content" in the left sidebar.</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_6.svg" alt="YouTube Per-Video Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_6.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 3:</h4>
                            <p>Find the video you want to adjust and click the dropdown under "Visibility" to choose between Public, Unlisted, or Private:</p>
                            <ul>
                              <li>Public: Anyone can find and view</li>
                              <li>Unlisted: Only people with the link can view</li>
                              <li>Private: Only you and people you choose can view</li>
                            </ul>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_7.svg" alt="YouTube Per-Video Step 3a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_7.svg')">
                            </div>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_8.svg" alt="YouTube Per-Video Step 3b" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_8.svg')">
                            </div>
                            <p>It is also available during you publish your new videos, in "Visibility" step to choose between Public, Unlisted, or Private</p>
                          </div>
                        </div>
                      </div>

                      <div class="section-header" @click="toggleYoutubeSection('playlists')">
                        <h3>Hiding Saved Playlists</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeSection === 'playlists' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeSection === 'playlists'">
                        <div class="settings-steps">
                          <div class="step">
                            <h4>Step 1:</h4>
                            <p>Open YouTube in your web browser and sign in to your account. Click on your profile picture in the top right corner and go to YouTube Studio.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_1.svg" alt="YouTube Playlist Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_1.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 2:</h4>
                            <p>Click "Content" in the left sidebar.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_2.svg" alt="YouTube Playlist Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_2.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 3:</h4>
                            <p>Find the Playlists option and click the "Details" button to change the setting.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_3.svg" alt="YouTube Playlist Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_3.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 4:</h4>
                            <p>Find the "Visibility" dropdown button to choose between Public, Unlisted, or Private.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_4.svg" alt="YouTube Playlist Step 4a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_4.svg')">
                            </div>
                            <p>It is also available during saving videos from others. Below the video, you can click the "Save" button and create a new playlist, and then set "Visibility" between Public, Unlisted, or Private:</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_5.svg" alt="YouTube Playlist Step 4b" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_5.svg')">
                            </div>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_6.svg" alt="YouTube Playlist Step 4c" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_6.svg')">
                            </div>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_playlist_8.svg" alt="YouTube Playlist Step 4e" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_playlist_8.svg')">
                            </div>
                          </div>
                        </div>
                      </div>

                      <div class="section-header" @click="toggleYoutubeSection('comments')">
                        <h3>Comment Privacy Settings</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeSection === 'comments' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeSection === 'comments'">
                        <div class="settings-steps">
                          <div class="step">
                            <h4>Step 1:</h4>
                            <p>Open YouTube in your web browser and sign in to your account. Click on your profile picture in the top right corner and go to YouTube Studio.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_comment_1.svg" alt="YouTube Comment Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_comment_1.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 2:</h4>
                            <p>Click "Settings" in the left sidebar.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_comment_2.svg" alt="YouTube Comment Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_comment_2.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 3:</h4>
                            <p>Find the Community Moderation and click the "Default" button to change the setting.</p>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_comment_3.svg" alt="YouTube Comment Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_comment_3.svg')">
                            </div>
                          </div>
                          <div class="step">
                            <h4>Step 4:</h4>
                            <p>Under "Comments on your channel", adjust "Moderation" dropdown button and change who can comment on your videos.</p>
                            <p>Options include:</p>
                            <ul>
                              <li>Allow all comments</li>
                              <li>Hold potentially inappropriate comments for review</li>
                              <li>Hold a broader range of comments for review</li>
                              <li>Hold all comments</li>
                            </ul>
                            <div class="step-image">
                              <img src="../assets/screenshots/youtube_comment_4.svg" alt="YouTube Comment Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_comment_4.svg')">
                            </div>
                            <p><strong>Privacy recommendation:</strong> Consider holding all comments for review to filter out personal information others might share about you.</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div v-if="activeVersion === 'mobile'">
                      <span class="update-date">Update: 26/04/2025</span>
                      <div class="section-header" @click="toggleYoutubeMobileSection('iosSettings')">
                        <h3>Privacy Settings for YouTube (iOS)</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeMobileSection === 'iosSettings' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeMobileSection === 'iosSettings'">
                        <div class="settings-steps">
                          <div class="step">
                            <h4>Step 1:</h4>
                            <p>Go to your iPhone's Settings app (not the YouTube app).</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_ios_1.svg" alt="iOS Settings Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_ios_1.svg')">
                            </div>
                          </div>
                           <div class="step">
                            <h4>Step 2:</h4>
                            <p>Scroll down and click "Apps" and head to YouTube.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_ios_2.svg" alt="iOS Settings Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_ios_2.svg')">
                            </div>
                          </div>
                           <div class="step">
                            <h4>Step 3:</h4>
                            <p>Click YouTube, and here you can manage iOS-specific permissions:</p>
                            <ul>
                              <li>Microphone - Control if YouTube can use your microphone for recording</li>
                              <li>Camera - Control if YouTube can access your camera for recording</li>
                              <li>Photos - Control if YouTube can access your photo library</li>
                              <li>Background App Refresh - Control if YouTube updates content when not in use</li>
                              <li>Siri & Search - Manage how Siri interacts with YouTube</li>
                            </ul>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_ios_3.svg" alt="iOS Settings Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_ios_3.svg')">
                            </div>
                          </div>
                          <p><strong>Recommendation for content creators:</strong> Limit YouTube's access to only what's necessary. For example, only allow photo access when uploading, not "Always."</p>
                        </div>
                      </div>

                      <div class="section-header" @click="toggleYoutubeMobileSection('videoChannel')">
                        <h3>Per-Video and Channel Privacy</h3>
                        <span class="toggle-icon" :class="{ 'rotated': activeYoutubeMobileSection === 'videoChannel' }">▼</span>
                      </div>
                      <div class="section-content" v-show="activeYoutubeMobileSection === 'videoChannel'">
                        <p><strong>Note:</strong> For most creator controls on iOS, YouTube will redirect you to YouTube Studio or prompt you to download the YouTube Studio app.</p>
                        <div class="settings-steps">
                          <div class="step">
                            <h4>Step 1:</h4>
                            <p>Download the YouTube Studio app from the App Store if you haven't already.</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_video_1.svg" alt="Mobile Video Step 3a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_video_1.svg')">
                            </div>
                          </div>
                           <div class="step">
                            <h4>Step 2:</h4>
                            <p>Sign in and tap on "Content" at the bottom.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_video_2.svg" alt="Mobile Video Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_video_2.svg')">
                            </div>
                          </div>
                           <div class="step">
                            <h4>Step 3:</h4>
                            <p>For per-video privacy:</p>
                            <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_video_3.svg" alt="Mobile Video Step 3a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_video_3.svg')">
                            </div>
                            <ul>
                              <li>Tap on a video</li>
                              <li>Tap "3 dots" icon to edit</li>
                              <li>Tap Visibility to set as Public, Private, or Unlisted</li>
                            </ul>
                             <div class="step-image">
                               <img src="../assets/screenshots/youtube_mobile_video_4.svg" alt="Mobile Video Step 3b" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/youtube_mobile_video_4.svg')">
                            </div>
                          </div>
                          <p><strong>Note:</strong> Many advanced creator settings like comment filtering rules require using the web version of YouTube Studio.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Privacy Tips Content -->
                <div class="privacy-tips-content" v-if="activeGuide === 'tips'">
                  <h3>Privacy Tips</h3>
                  <div class="tip-item">
                    <h4>Two-Factor Authentication</h4>
                    <p>YouTube offers enhanced security through two-factor authentication linked to your Google account. This prevents account takeovers even if someone obtains your password. The "cost" is slightly slower login and needing your phone nearby whenever you sign in to new devices.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Comment Activity Privacy</h4>
                    <p>YouTube makes all your public comments visible through your channel page. To prevent viewers from seeing every comment you've made, go to Settings -> Privacy -> Keep comments private. This helps maintain separation between your creator persona and your viewing habits. The "cost" is reduced community engagement as your audience can't easily see your interactions with other creators.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Incognito Mode</h4>
                    <p>YouTube's Incognito mode prevents your viewing activity from being saved to your history. Access this by clicking your profile picture -> Turn on Incognito. This allows you to research competitors or sensitive topics without affecting your recommendations.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Review Third-Party Access</h4>
                    <p>Manage third-party access by reviewing and removing any apps you don't recognize or no longer use. In that way it prevents unauthorized apps from accessing your YouTube/Google data.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Brand Account Separation</h4>
                    <p>Create a Brand Account by going to Settings -> Create a channel -> follow prompts for "Brand Account." This creates a complete separation between your personal Google account and your creator identity. The "cost" is having to switch between accounts frequently and managing notifications across multiple accounts.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Content ID Protection</h4>
                    <p>Register your channel for Content ID by applying to the YouTube Partner Program. This helps prevent others from reusing your content without permission. The "cost" is meeting eligibility requirements and potentially dealing with false copyright claims against your content.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Regularly Review Your Privacy</h4>
                    <p>Set a calendar reminder to review these privacy settings every 3 months, as YouTube frequently updates its interface and privacy options.</p>
                  </div>
                </div>

                 <!-- Boundary Tips Content -->
                <div class="boundary-tips-content" v-if="activeGuide === 'boundary'">
                  <h3>Boundary Tips</h3>
                  <div class="tip-item">
                    <h4>Comment Filter Customization</h4>
                    <p>YouTube allows custom comment filtering under YouTube Studio -> Settings -> Community Moderation -> Automated filters. Add specific terms, phrases, or questions that frequently cross your boundaries. Comments containing these will be held for review. The "cost" is potentially delayed posting of legitimate comments that happen to contain filtered words.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Schedule-Protected Uploads</h4>
                    <p>Use YouTube's scheduling feature. Pre-record and schedule content to maintain consistent posting during personal time off without revealing your absence.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Limited Location Disclosures</h4>
                    <p>Avoid "checking in" or tagging specific locations when posting about being out of town. Instead, share travel content after returning home. This prevents revealing when your home might be empty. The "cost" is delayed engagement related to your travel experiences and a less real-time connection with your audience.</p>
                  </div>
                   <div class="tip-item">
                    <h4>Membership-Only Content Boundaries</h4>
                    <p>Create a more controlled environment for personal sharing using Channel Memberships accessed through YouTube Studio -> Monetization -> Memberships. This creates a smaller audience for more personal content with supporters who have a financial investment in your success.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Comment Holding Period</h4>
                    <p>Enable Hold all comments for review under YouTube Studio -> Settings -> Community Moderation -> Defaults. This allows you to review all comments before they appear publicly on new uploads, particularly useful for videos covering sensitive topics. The "cost" is delayed community engagement and increased moderation workload.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Professional Email Forwarding</h4>
                    <p>Set up a dedicated creator email with forwarding to your personal address. Use a service like Gmail to create filters that automatically categorize incoming messages (business, fan mail, etc.). This keeps your personal email private while maintaining professional communication. The "cost" is managing multiple email addresses and potentially missing messages if filters are misconfigured.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Collaboration Contract Template</h4>
                    <p>Create a standard collaboration agreement that outlines privacy expectations, content usage rights, and social media tagging policies. Send this document before agreeing to any collaborations. The "cost" is potentially intimidating smaller creators and appearing overly formal in a typically casual space.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Documented Response Templates</h4>
                    <p>Create a document with prepared responses for common boundary-crossing questions. This allows consistent boundary enforcement without emotional exhaustion from repeatedly crafting individual responses. The "cost" is potentially seeming impersonal if templates are used too frequently or without customization.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Selective Personal Sharing</h4>
                    <p>Deliberately choose one or two personal topics you're comfortable discussing (e.g., pets, cooking, music preferences) while keeping other aspects of your life private. This satisfies audience desire for connection while protecting your privacy. The "cost" is potentially seeming one-dimensional or creating the impression you're hiding something.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- TikTok section -->
        <div class="platform-section tiktok-section">
          <div class="platform-header" @click="togglePlatform('tiktok')" :class="{ 'active': activePlatform === 'tiktok' }">
            <img src="../assets/icons/logo/tiktok.png" alt="TikTok Logo" class="platform-logo">
            <h2>Tiktok <span class="read-time">(Est. 7 min read)</span></h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'tiktok' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'tiktok'">
            <div class="privacy-settings">
              <!-- REMOVE SIDEBAR START -->
              <!-- <div class="settings-sidebar">
                <div class="sidebar-nav">
                  <div class="nav-group">
                    <div class="nav-item" :class="{ 'active': activeGuide === 'settings' }" @click="switchGuide('settings')">
                      <h3>Privacy setting guides</h3>
            </div>
                    <div v-if="activeGuide === 'settings'" class="guide-options">
                      <ul>
                        <li :class="{ 'active': activeVersion === 'browser' }" @click="switchVersion('browser')">· Browser version</li>
                        <li :class="{ 'active': activeVersion === 'mobile' }" @click="switchVersion('mobile')">· Mobile version</li>
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
              </div> -->
              <!-- REMOVE SIDEBAR END -->

              <div class="settings-content-area"> 
                <!-- ADD TABS START -->
                 <div class="tab-navigation">
                  <button 
                    :class="{ 'active': activeGuide === 'settings' }" 
                    @click="switchGuide('settings')"
                  >
                    Setting Guides
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'tips' }" 
                    @click="switchGuide('tips')"
                  >
                    Privacy Tips
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'boundary' }" 
                    @click="switchGuide('boundary')"
                  >
                    Boundary Tips
                  </button>
                </div>
                <div class="sub-tab-navigation" v-if="activeGuide === 'settings'">
                  <button 
                    :class="{ 'active': activeVersion === 'browser' }" 
                    @click="switchVersion('browser')"
                  >
                    Browser
                  </button>
                  <button 
                    :class="{ 'active': activeVersion === 'mobile' }" 
                    @click="switchVersion('mobile')"
                  >
                    Mobile (iOS)
                  </button>
                </div>
                <!-- ADD TABS END -->

                <!-- Quick View Button -->
                <div class="quick-view">
                   <button @click="showQuickView('tiktok')">Quick view</button>
                </div>

                <div class="settings-guide-content" v-if="activeGuide === 'settings'">
                   <div class="settings-content"> 
                      <div v-if="activeVersion === 'browser'">
                       <span class="update-date">Update: 26/04/2025</span>
                       
                       <!-- TikTok Section 1: Account Privacy Settings -->
                       <div class="section-header" @click="toggleTiktokSection('account')">
                         <h3>Account Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeTiktokSection === 'account' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeTiktokSection === 'account'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open your web browser and go to TikTok.com. Sign in to your account.</p>
                           </div>
                            <div class="step-image">
                             <img src="../assets/screenshots/tiktok_account_1.svg" alt="TikTok Account Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_account_1.svg')">
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Click on your profile picture in the top right corner.</p>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Select the "Settings" icon near the profile photo.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/tiktok_account_2.svg" alt="TikTok Account Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_account_2.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 4:</h4>
                             <p>Click on "Privacy" in the left sidebar.</p>
                           </div>
                           <div class="step-image">
                             <img src="../assets/screenshots/tiktok_account_3.svg" alt="TikTok Account Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_account_3.svg')">
                           </div>
                           <div class="step">
                             <h4>Step 5:</h4>
                             <p>Here you'll find several important privacy controls:</p>
                             <h5>Private Account</h5>
                              <ul>
                               <li>Toggle the switch to ON to make your account private or OFF to make it public</li>
                               <li>If enabled (ON): Only approved followers can see your content</li>
                               <li>If disabled (OFF): Anyone can view your videos, even without following you</li>
                               <li>Recommendation: Typically keep this OFF if building an audience is your goal, but consider ON during early brand development or if creating content for a limited audience</li>
                             </ul>
                             <h5>Download Your Data</h5>
                             <ul>
                               <li>Click "Download your data" to request an archive of your account information</li>
                               <li>You can choose between requesting TXT format or JSON format</li>
                             </ul>
                           </div>
                         </div>
                       </div>

                       <!-- TikTok Section 2: Per-Video Privacy Settings -->
                       <div class="section-header" @click="toggleTiktokSection('perVideo')">
                         <h3>Per-Video Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeTiktokSection === 'perVideo' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeTiktokSection === 'perVideo'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open your TikTok and sign in to your account. Click on your profile picture in the top right corner.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_1.svg" alt="TikTok Per-Video Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Click "Video" in the middle, which you want to edit the privacy setting.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_2.svg" alt="TikTok Per-Video Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_2.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Select the "3 dots" icon at the top right corner, and then click " Privacy settings".</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_3.svg" alt="TikTok Per-Video Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_3.svg')">
                             </div>
                             
                             <h5>Visibility for per-video:</h5>
                             <p>How to set: Click the dropdown menu next to "Who can watch this video"</p>
                             <p>Options:</p>
                             <ul>
                               <li>Everyone</li>
                               <li>Friends (people you follow who follow you back)</li>
                               <li>No one</li>
                             </ul>
                             <p>Recommendation: Start with "Everyone" to build engagement, but switch to "Friends" if receiving excessive negative comments which you can't handle.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_4.svg" alt="TikTok Per-Video Visibility" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_4.svg')">
                             </div>

                             <h5>Comment, Duet, and Stitch</h5>
                             <p>How to set: Toggle the switch to ON to make it public or OFF to make each private.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_5.svg" alt="TikTok Per-Video Comment/Duet/Stitch Settings" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_5.svg')">
                             </div>
                             <p>Recommendation: For content creator, it's better to "Not allow" others using your content in their videos, set to "OFF" in Duet and Stitch, but can put the comments on to engage audiences.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/tiktok_pervideo_6.svg" alt="TikTok Per-Video Comment/Duet/Stitch Recommendation" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_pervideo_6.svg')">
                             </div>
                           </div>
                         </div>
                       </div>
                       
                       <!-- REMOVE BUTTON FROM HERE -->
                       <!-- <div class="quick-view">
                         <button>Quick view</button>
                       </div> -->
                     </div>
                     <!-- TikTok Mobile Settings (Conditional) -->
                     <div v-if="activeVersion === 'mobile'">
                       <span class="update-date">Update: 26/04/2025</span>
                       <!-- TikTok Mobile Section 1: iOS Settings -->
                       <div class="section-header" @click="toggleTiktokMobileSection('iosSettings')">
                         <h3>Privacy Settings for TikTok (iOS)</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeTiktokMobileSection === 'iosSettings' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeTiktokMobileSection === 'iosSettings'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Go to your iPhone's Settings app (not the TikTok app).</p>
                             <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_ios_1.svg" alt="iOS Settings Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_ios_1.svg')">
                             </div>
                           </div>
                            <div class="step">
                             <h4>Step 2:</h4>
                             <p>Scroll down and click "Apps" and head to TikTok.</p>
                              <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_ios_2.svg" alt="iOS Settings Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_ios_2.svg')">
                             </div>
                           </div>
                            <div class="step">
                             <h4>Step 3:</h4>
                             <p>Click TikTok, and here you can manage iOS-specific permissions:</p>
                             <ul>
                               <li>Microphone - Control if TikTok can use your microphone for recording</li>
                               <li>Camera - Control if TikTok can access your camera for recording</li>
                               <li>Photos - Control if TikTok can access your photo library</li>
                               <li>Background App Refresh - Control if TikTok updates content when not in use</li>
                               <li>Siri & Search - Manage how Siri interacts with TikTok</li>
                             </ul>
                              <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_ios_3.svg" alt="iOS Settings Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_ios_3.svg')">
                             </div>
                           </div>
                           <p><strong>Recommendation for content creators:</strong> Limit TikTok's access to only what's necessary. For example, only allow TikTok to access your camera, microphone, and photos while using the app, not always.</p>
                         </div>
                       </div>
                       <!-- TikTok Mobile Section 2: Basic Privacy Settings -->
                       <div class="section-header" @click="toggleTiktokMobileSection('basic')">
                         <h3>Basic Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeTiktokMobileSection === 'basic' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeTiktokMobileSection === 'basic'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open the TikTok app on your iPhone.</p>
                             <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_basic_1.svg" alt="TikTok Basic Mobile Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_basic_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Tap on "Profile" in the bottom right corner and tap on the three lines (hamburger menu) in the top right corner.</p>
                              <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_basic_2.svg" alt="TikTok Basic Mobile Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_basic_2.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Tap on "Settings and privacy".</p>
                              <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_basic_3.svg" alt="TikTok Basic Mobile Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_basic_3.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 4:</h4>
                             <p>Tap on "Privacy" under the Account section.</p>
                              <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_basic_4.svg" alt="TikTok Basic Mobile Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_basic_4.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 5:</h4>
                             <p>Here you'll find the main privacy controls:</p>
                             <h5>Discoverability:</h5>
                             <p>Suggest your account to others - Controls whether TikTok recommends your account to other users</p>
                             <ul>
                               <li>How to set: Tap this option to manage who can discover your account</li>
                               <li>Recommendation for creators: Enable if you're trying to grow your audience, disable if you prefer a more private presence</li>
                             </ul>
                              <h5>Contact Syncing</h5>
                              <p>Allows TikTok to access your contacts and Facebook connections to find people you may know</p>
                             <ul>
                               <li>How to set: Tap this option to enable/disable syncing</li>
                               <li>Privacy consideration: Disabling this prevents TikTok from accessing your contact list but may limit networking opportunities</li>
                             </ul>
                              <h5>Interactions:</h5>
                             <p>Privacy recommendation for content creators: Review these settings regularly as you grow your account. Early in your TikTok journey, you might want more open settings to encourage growth and engagement. As your following increases, you may want to tighten certain settings to better manage interactions and protect your content.</p>
                           </div>
                         </div>
                       </div>
                       <!-- TikTok Mobile Section 3: Per-Video Privacy Settings -->
                       <div class="section-header" @click="toggleTiktokMobileSection('perVideo')">
                         <h3>Per-Video Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeTiktokMobileSection === 'perVideo' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeTiktokMobileSection === 'perVideo'">
                         <p>When posting a new video, you can set privacy for individual posts:</p>
                         <div class="settings-steps">
                            <div class="step">
                             <h4>Step 1:</h4>
                             <p>After recording and editing your video, before posting, tap "privacy setting to the post".</p>
                             <div class="step-image">
                                <img src="../assets/screenshots/tiktok_mobile_pervideo_1.svg" alt="TikTok Per-Video Mobile Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_pervideo_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Click "More options" to decide which to toggle ON/OFF</p>
                              <!-- Image row for adjacent images -->
                              <div class="step-image-row">
                                <div class="step-image">
                                  <img src="../assets/screenshots/tiktok_mobile_pervideo_2.svg" alt="TikTok Per-Video Mobile Step 2a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_pervideo_2.svg')">
                                </div>
                                 <div class="step-image">
                                  <img src="../assets/screenshots/tiktok_mobile_pervideo_3.svg" alt="TikTok Per-Video Mobile Step 2b" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/tiktok_mobile_pervideo_3.svg')">
                                </div>
                              </div>
                             <p>Recommendation: Consider open "save posts with watermark" and "audience control" if you want to protect your video, or users.</p>
                           </div>
                         </div>
                       </div>
                       <!-- Add other TikTok Mobile sections here -->
                     </div>
                   </div>
                </div>
                
                <div class="privacy-tips-content" v-if="activeGuide === 'tips'">
                   <h3>Privacy Tips - TikTok</h3>
                   <!-- Replacing the placeholder below -->
                   <div class="tip-item">
                     <h4>Two-Factor Authentication</h4>
                     <p>TikTok offers added security through two-factor authentication. Enable this under Settings and privacy -> Security and login -> 2-step verification. This prevents account takeovers even if someone obtains your password. The "cost" is needing your phone nearby whenever you sign in to new devices.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Pro Account Analytics Privacy</h4>
                     <p>TikTok's Pro Account provides valuable analytics but collects additional data. Manage this under Settings and privacy -> Account -> Switch to Pro Account or Manage my account. The analytics help track performance, but increase data collection. The "cost" is sharing more detailed usage patterns with TikTok in exchange for insights.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Comment Filtering Keywords</h4>
                     <p>TikTok allows you to filter specific words from appearing in your comments. Set this up under Settings and privacy -> Safety -> Filter keywords. This helps prevent harassment and unwanted personal questions. The "cost" is potentially filtering legitimate comments that happen to contain filtered words.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Green Screen Effect Privacy</h4>
                     <p>When using TikTok's Green Screen effect with photos from your camera roll, be aware it may reveal metadata or background elements. Review images carefully before using them as backgrounds. The "cost" is spending extra time screening personal photos before using them in content.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Watermarking Strategy</h4>
                     <p>TikTok automatically adds a watermark to your videos. Leave this intact when sharing to other platforms to deter impersonation and unauthorized reuse of your content. The "cost" is somewhat reduced aesthetic quality and making it obvious content originated on TikTok.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Location Tag Management</h4>
                     <p>Disable precise location access in your device settings for TikTok. For location-based content, consider adding location information manually rather than using automatic tagging. The "cost" is losing automatic location suggestions and potentially reaching fewer local viewers.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Drafts Security</h4>
                     <p>TikTok drafts are stored locally on your device and aren't backed up if you delete the app or switch phones. For important content, consider backing up raw footage elsewhere before editing in TikTok. The "cost" is maintaining duplicate storage systems and a more complex workflow.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Profile Information Minimalism</h4>
                     <p>Limit the personal information in your TikTok bio. Use business contact information rather than personal details, and consider using a business name rather than your legal name. The "cost" is potentially reduced personal connection with your audience.</p>
                   </div>
                </div>

                <div class="boundary-tips-content" v-if="activeGuide === 'boundary'">
                  <h3>Boundary Tips - TikTok</h3>
                  <!-- Replacing placeholder below -->
                   <div class="tip-item">
                    <h4>Scheduled Posting Times</h4>
                    <p>Use TikTok's scheduling feature (available for Business accounts) to maintain consistent posting without being constantly available. This creates time boundaries between your creator life and personal time. The "cost" is less flexibility to respond to trending topics in real-time.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Comment Response Protocol</h4>
                    <p>Establish a personal policy for which comments you'll respond to and which you'll ignore. For example, answer content-related questions but not personal questions about relationships or finances. The "cost" is potentially appearing less engaging to some followers who seek personal connections.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Content Pillars Definition</h4>
                    <p>Define 3-5 specific content topics or "pillars" that your account focuses on. Politely decline requests for content that falls outside these areas by referring to your established content focus. The "cost" is potentially missing opportunities to expand your content range based on follower requests.</p>
                  </div>
                   <div class="tip-item">
                    <h4>Creator vs. Viewer Account Separation</h4>
                    <p>Create a separate viewer account for consuming TikTok content that's not connected to your creator identity. This prevents your content recommendations and likes from being visible to followers. The "cost" is managing multiple accounts and remembering to switch between them.</p>
                  </div>
                  <div class="tip-item">
                    <h4>LIVE Boundaries</h4>
                    <p>Before going LIVE, establish clear topics you won't discuss. Practice phrases like "I don't discuss that on my channel" or "I focus on [your content area] here" to redirect intrusive questions. The "cost" is potentially appearing evasive or less authentic to some viewers.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Collaboration Contracts</h4>
                    <p>Create a simple collaboration agreement template that outlines how shared content can be used, tagged, and distributed. Send this before agreeing to collaborations with other creators. The "cost" is adding formality to what might otherwise be casual creative partnerships.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Comment Timeboxing</h4>
                    <p>Set specific times to review and respond to comments rather than doing so continuously throughout the day. This prevents TikTok engagement from consuming your entire schedule. The "cost" is potentially slower response times that might affect algorithm performance.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Duet/Stitch Permissions</h4>
                    <p>Disable Duet and Stitch features for videos containing more personal content or where you don't want your image reused by others. Enable them strategically only for content designed for wider sharing. The "cost" is potentially reduced viral spread and community engagement.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Knowledge-Sharing Boundaries</h4>
                    <p>Decide in advance what aspects of your creative process or business you're willing to share versus what constitutes your "trade secrets." Prepare polite responses for questions that cross this line. The "cost" is potentially appearing less helpful to other aspiring creators in your community.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Instagram section -->
        <div class="platform-section instagram-section">
          <div class="platform-header" @click="togglePlatform('instagram')" :class="{ 'active': activePlatform === 'instagram' }">
            <img src="../assets/icons/logo/insta.png" alt="Instagram Logo" class="platform-logo">
            <h2>Instagram <span class="read-time">(Est. 8 min read)</span></h2>
            <div class="expand-icon">
              <span :class="{ 'rotated': activePlatform === 'instagram' }">▼</span>
            </div>
          </div>
          
          <div class="platform-content" v-show="activePlatform === 'instagram'">
            <!-- Remove Coming Soon -->
            <!-- <div class="coming-soon">
              <p>Privacy settings guide coming soon</p>
            </div> -->
             <div class="privacy-settings"> 
               <!-- REMOVE SIDEBAR START -->
               <!-- <div class="settings-sidebar">
                 <div class="sidebar-nav">
                   <div class="nav-group">
                     <div class="nav-item" :class="{ 'active': activeGuide === 'settings' }" @click="switchGuide('settings')">
                       <h3>Privacy setting guides</h3>
            </div>
                     <div v-if="activeGuide === 'settings'" class="guide-options">
                       <ul>
                         <li :class="{ 'active': activeVersion === 'browser' }" @click="switchVersion('browser')">· Browser version</li>
                         <li :class="{ 'active': activeVersion === 'mobile' }" @click="switchVersion('mobile')">· Mobile version</li>
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
               </div> -->
               <!-- REMOVE SIDEBAR END -->

               <!-- Content Area: Settings Guide / Tips / Boundary -->
              <div class="settings-content-area"> 
                <!-- ADD TABS START -->
                <div class="tab-navigation">
                  <button 
                    :class="{ 'active': activeGuide === 'settings' }" 
                    @click="switchGuide('settings')"
                  >
                    Setting Guides
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'tips' }" 
                    @click="switchGuide('tips')"
                  >
                    Privacy Tips
                  </button>
                  <button 
                    :class="{ 'active': activeGuide === 'boundary' }" 
                    @click="switchGuide('boundary')"
                  >
                    Boundary Tips
                  </button>
                </div>
                <div class="sub-tab-navigation" v-if="activeGuide === 'settings'">
                  <button 
                    :class="{ 'active': activeVersion === 'browser' }" 
                    @click="switchVersion('browser')"
                  >
                    Browser
                  </button>
                  <button 
                    :class="{ 'active': activeVersion === 'mobile' }" 
                    @click="switchVersion('mobile')"
                  >
                    Mobile (iOS)
                  </button>
                </div>
                <!-- ADD TABS END -->
                
                <!-- Quick View Button -->
                <div class="quick-view">
                   <button @click="showQuickView('instagram')">Quick view</button>
                </div>

                 <!-- Settings Guide Content (v-if="activeGuide === 'settings'") -->
                <div class="settings-guide-content" v-if="activeGuide === 'settings'">
                   <div class="settings-content"> 
                      <!-- Browser Settings (Conditional) -->
                     <div v-if="activeVersion === 'browser'">
                       <span class="update-date">Update: 26/04/2025</span>
                       
                       <!-- Instagram Section 1: General Privacy Settings -->
                       <div class="section-header" @click="toggleInstaSection('general')">
                         <h3>General Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeInstaSection === 'general' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeInstaSection === 'general'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open your web browser and go to instagram.com. Sign in to your account.</p>
                             <!-- No image for step 1 -->
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Click on "Menu" in the left sidebar.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_general_1.svg" alt="Instagram General Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_general_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Select the "Settings" icon after clicking the menu.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_general_2.svg" alt="Instagram General Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_general_2.svg')">
                             </div>
                           </div>
                            <div class="step">
                             <h4>Step 4:</h4>
                             <p>Scroll down the settings line and find & click</p>
                             <ul>
                               <li>"Hide story and live" to maintain privacy about your story from some of the people (you can choose the person).</li>
                               <li>"Hide like & share counts" to avoid users seeing the number of likes on posts and reels</li>
                               <li>Set "Restricted accounts" to protect yourself from unwanted interactions without having to block or unfollow people you know.</li>
                               <li>Set "Hidden words" for some unwanted comments and message requests</li>
                               <li>Click on "Privacy Center" to see more privacy settings, like manage your passwords, login preferences and recovery methods etc</li>
                             </ul>
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_general_3.svg" alt="Instagram General Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_general_3.svg')">
                             </div>
                           </div>
                            <p>Recommendation: Review regularly and adjust based on your comfort level with current followers</p>
                         </div>
                       </div>
                       <!-- Instagram Section 2: Per-Video Privacy Settings -->
                       <div class="section-header" @click="toggleInstaSection('perVideo')">
                         <h3>Per-Video Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeInstaSection === 'perVideo' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeInstaSection === 'perVideo'">
                         <div class="settings-steps">
                            <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open your Instagram and sign in to your account. Click on your "profile" in the left sidebar.</p>
                              <!-- No image for step 1 -->
                           </div>
                            <div class="step">
                             <h4>Step 2:</h4>
                             <p>Click "Video" in the middle, which you want to edit the privacy setting.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_pervideo_1.svg" alt="Instagram Per-Video Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_pervideo_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Select the "3 dots" icon at the top right corner.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/insta_pervideo_2.svg" alt="Instagram Per-Video Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_pervideo_2.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 4:</h4>
                             <p>Here you can manage:</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/insta_pervideo_3.svg" alt="Instagram Per-Video Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_pervideo_3.svg')">
                              </div>
                             <h5>Hide Like Count to Others</h5>
                             <p>What it does: This hides the number of likes from other users, though you can still see how many likes your post received. This helps reduce social pressure and comparison.</p>
                             <p>Privacy benefit for creators: This prevents followers from judging your content based on popularity metrics and can help maintain a more authentic engagement environment.</p>
                             
                             <h5>Turn Off Commenting</h5>
                             <p>What it does: This disables the ability for anyone to comment on this specific post.</p>
                             <p>Privacy benefit: This is useful for posts that might attract unwanted comments or when you want to share content without opening it to discussion. You can always turn comments back on later using the same menu.</p>
                              <div class="step-image">
                               <img src="../assets/screenshots/insta_pervideo_3.svg" alt="Instagram Per-Video Step 4" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_pervideo_3.svg')">
                             </div>
                           </div>
                         </div>
                       </div>
                       <!-- Add other Instagram Browser sections here -->
                       
                       <!-- REMOVE BUTTON FROM HERE -->
                       <!-- <div class="quick-view">
                         <button>Quick view</button>
                       </div> -->
                     </div>
                      <!-- Instagram Mobile Settings (Conditional) -->
                     <div v-if="activeVersion === 'mobile'">
                       <span class="update-date">Update: 26/04/2025</span>
                       <!-- Instagram Mobile Section 1: iOS Settings -->
                       <div class="section-header" @click="toggleInstaMobileSection('iosSettings')">
                         <h3>Privacy Settings for Instagram (iOS)</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeInstaMobileSection === 'iosSettings' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeInstaMobileSection === 'iosSettings'">
                         <div class="settings-steps">
                            <div class="step">
                             <h4>Step 1:</h4>
                             <p>Go to your iPhone's Settings app (not the Instagram app).</p>
                             <div class="step-image">
                                <img src="../assets/screenshots/insta_mobile_ios_1.svg" alt="Instagram iOS Settings Step 1" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_ios_1.svg')">
                             </div>
                           </div>
                            <div class="step">
                             <h4>Step 2:</h4>
                             <p>Scroll down and click "Apps" and head to Instagram.</p>
                              <div class="step-image">
                                <img src="../assets/screenshots/insta_mobile_ios_2.svg" alt="Instagram iOS Settings Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_ios_2.svg')">
                             </div>
                           </div>
                            <div class="step">
                             <h4>Step 3:</h4>
                             <p>Click Instagram, and here you can manage iOS-specific permissions:</p>
                             <ul>
                               <li>Microphone - Control if Instagram can use your microphone for recording</li>
                               <li>Camera - Control if Instagram can access your camera for recording</li>
                               <li>Photos - Control if Instagram can access your photo library</li>
                               <li>Background App Refresh - Control if Instagram updates content when not in use</li>
                               <li>Siri & Search - Manage how Siri interacts with Instagram</li>
                             </ul>
                              <div class="step-image">
                                <img src="../assets/screenshots/insta_mobile_ios_3.svg" alt="Instagram iOS Settings Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_ios_3.svg')">
                             </div>
                           </div>
                           <p><strong>Recommendation for content creators:</strong> Limit Instagram's access to only what's necessary. For example, Only allow Instagram to access your camera, microphone, and photos while using the app, not always.</p>
                         </div>
                       </div>
                       <!-- Instagram Mobile Section 2: Basic Privacy Settings -->
                       <div class="section-header" @click="toggleInstaMobileSection('basic')">
                         <h3>Basic Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeInstaMobileSection === 'basic' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeInstaMobileSection === 'basic'">
                         <div class="settings-steps">
                           <div class="step">
                             <h4>Step 1:</h4>
                             <p>Open the Instagram app on your iPhone.</p>
                             <!-- No image for step 1 -->
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Tap on "Profile" in the bottom right corner and tap on the three lines (hamburger menu) in the top right corner.</p>
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_mobile_basic_1.svg" alt="Instagram Basic Mobile Step 2" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_basic_1.svg')">
                             </div>
                           </div>
                           <div class="step">
                             <h4>Step 3:</h4>
                             <p>Here you'll find the privacy controls, tap on each of these options to manage who can interact with you:</p>
                             <!-- MOVE LIST HERE -->
                             <!-- Beautified Privacy Controls List -->
                             <div class="privacy-control-list">
                               <div class="privacy-control-group">
                                 <h5>Comments</h5>
                                 <ul>
                                   <li>Control who can comment on your posts</li>
                                   <li>Filter out offensive comments</li>
                                   <li>Add specific words to hide in comments</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Story and live</h5>
                                  <ul>
                                   <li>Hide stories from specific people</li>
                                   <li>Control who can reply to your stories</li>
                                   <li>Manage close friends list for exclusive content</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Messages</h5>
                                  <ul>
                                   <li>Control who can message you directly</li>
                                   <li>Manage message requests</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Restricted accounts</h5>
                                  <ul>
                                   <li>Add accounts to a restricted list (they won't know they're restricted)</li>
                                   <li>Restricted accounts' comments are only visible to them</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Hidden words</h5>
                                  <ul>
                                   <li>Filter out potentially offensive content in DM requests</li>
                                   <li>Add custom words to filter</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Posts you've liked</h5>
                                 <ul>
                                   <li>Control who can see posts you've liked</li>
                                 </ul>
                               </div>
                             </div>
                             <!-- End Beautified List -->
                             <!-- Image comes AFTER the list -->
                             <div class="step-image">
                               <img src="../assets/screenshots/insta_mobile_basic_2.svg" alt="Instagram Basic Mobile Step 3" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_basic_2.svg')">
                             </div>
                             
                             <!-- REMOVE LIST FROM HERE -->
                             <!-- Beautified Privacy Controls List -->
                             <!-- <div class="privacy-control-list">
                               <div class="privacy-control-group">
                                 <h5>Comments</h5>
                                 <ul>
                                   <li>Control who can comment on your posts</li>
                                   <li>Filter out offensive comments</li>
                                   <li>Add specific words to hide in comments</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Story and live</h5>
                                  <ul>
                                   <li>Hide stories from specific people</li>
                                   <li>Control who can reply to your stories</li>
                                   <li>Manage close friends list for exclusive content</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Messages</h5>
                                  <ul>
                                   <li>Control who can message you directly</li>
                                   <li>Manage message requests</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Restricted accounts</h5>
                                  <ul>
                                   <li>Add accounts to a restricted list (they won't know they're restricted)</li>
                                   <li>Restricted accounts' comments are only visible to them</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Hidden words</h5>
                                  <ul>
                                   <li>Filter out potentially offensive content in DM requests</li>
                                   <li>Add custom words to filter</li>
                                 </ul>
                               </div>

                               <div class="privacy-control-group">
                                 <h5>Posts you've liked</h5>
                                 <ul>
                                   <li>Control who can see posts you've liked</li>
                                 </ul>
                               </div>
                             </div> -->
                             <!-- End Beautified List -->
                           </div>
                         </div>
                       </div>
                        <!-- Instagram Mobile Section 3: Per-Video Privacy Settings -->
                       <div class="section-header" @click="toggleInstaMobileSection('perVideo')">
                         <h3>Per-Video Privacy Settings</h3>
                         <span class="toggle-icon" :class="{ 'rotated': activeInstaMobileSection === 'perVideo' }">▼</span>
                       </div>
                       <div class="section-content" v-show="activeInstaMobileSection === 'perVideo'">
                         <p>When posting new content, you can set privacy for individual posts:</p>
                         <div class="settings-steps">
                            <div class="step">
                             <h4>Step 1:</h4>
                             <p>Begin creating a story, reel, or live.</p>
                                <div class="step-image insta-pervideo-image">
                                  <img src="../assets/screenshots/insta_mobile_pervideo_1.svg" alt="Instagram Per-Video Mobile Step 2a" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_pervideo_1.svg')">
                                </div>
                             <!-- No image for step 1 -->
                           </div>
                           <div class="step">
                             <h4>Step 2:</h4>
                             <p>Before posting, look for the audience selector, for stories and some content, you can select:</p>
                             <ul>
                               <li>Your Story: Visible to all followers (or the public if the account is public)</li>
                               <li>Close Friends: Only visible to your designated close friends list</li>
                               <li>Hide from: Select specific followers to hide this content from</li>
                               <li>Allow sharing to stories: Toggle ON/OFF</li>
                               <li>Allow resharing to messages: Toggle ON/OFF</li>
                             </ul>
                              <div class="step-image-row">
                                 <div class="step-image insta-pervideo-image">
                                  <img src="../assets/screenshots/insta_mobile_pervideo_2.svg" alt="Instagram Per-Video Mobile Step 2b" onerror="this.src='../assets/icons/elements/screenshot-placeholder.svg'" @click="enlargeImage('../assets/screenshots/insta_mobile_pervideo_2.svg')">
                                </div>
                              </div>
                           </div>
                           <p><strong>Recommendation:</strong> Use the Close Friends feature strategically for exclusive content or behind-the-scenes material for dedicated followers.</p>
                         </div>
                       </div>
                       <!-- Add other Instagram Mobile sections here -->
                     </div>
                   </div>
                </div>
                
                <!-- Privacy Tips Content (v-if="activeGuide === 'tips'") -->
                <div class="privacy-tips-content" v-if="activeGuide === 'tips'">
                   <h3>Privacy Tips - Instagram</h3>
                   <!-- Start Replace -->
                    <div class="tip-item">
                     <h4>Two-Factor Authentication</h4>
                     <p>Instagram offers additional security through two-factor authentication. Enable this under Settings and privacy -> Security -> Two-factor authentication. This prevents account takeovers even if someone obtains your password. The "cost" is needing your phone or authentication app whenever you sign in on new devices.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Login Activity Monitoring</h4>
                     <p>Instagram allows you to see where your account is logged in. Check this regularly under Settings and privacy -> Security -> Login activity. This helps identify unauthorized access to your account. The "cost" is taking time to regularly review this information and investigate unfamiliar logins.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Limit Sensitive Content</h4>
                     <p>Instagram can filter potentially sensitive content from your feed. Adjust this under Settings and privacy -> Content preferences -> Sensitive content control. This reduces exposure to potentially triggering material. The "cost" is potentially missing content that may be incorrectly flagged as sensitive.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Profile Information Strategy</h4>
                     <p>Carefully consider what personal information you include in your bio. Use a business email rather than a personal email, and consider whether revealing your location is necessary for your content niche. The "cost" is potentially less relatable or authentic to some followers.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Restrict Instead of Block</h4>
                     <p>For problematic followers, use the "Restrict" feature instead of blocking. Find this by tapping the three dots on their profile and selecting "Restrict." Their comments will only be visible to them, and they won't know they're restricted. The "cost" is maintaining the follower count while limiting actual engagement.</p>
                   </div>
                   <div class="tip-item">
                     <h4>Location Tag Delay</h4>
                     <p>When posting from recognizable locations, delay posting until after you've left the location. This prevents real-time tracking of your whereabouts. The "cost" is less immediacy in your content and potentially reduced engagement from location-based discovery.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Close Friends Strategic Use</h4>
                     <p>Use Instagram's "Close Friends" feature to test content with a trusted audience before posting publicly. Set this up under Settings and privacy -> Privacy -> Close friends. The "cost" is managing an additional content stream and potentially creating a perception of favoritism.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Link Protection</h4>
                     <p>Avoid clicking links in DMs, even from accounts that look familiar. Verify through separate channels before clicking suspicious links to prevent phishing attacks. The "cost" is extra time spent verifying legitimate requests and potentially delayed responses.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Story View Limitations</h4>
                     <p>Before viewing sensitive Stories (competitors, research on controversial topics), switch to a secondary account to prevent revealing your interests. The "cost" is managing multiple accounts and remembering to switch between them.</p>
                   </div>
                    <div class="tip-item">
                     <h4>Download Your Data</h4>
                     <p>Periodically request a download of your Instagram data under Settings and privacy -> Your activity -> Download your information. This helps you understand what information Instagram stores about you. The "cost" is managing the downloaded data files and potentially discovering concerning stored information.</p>
                   </div>
                   <!-- End Replace -->
                </div>

                <!-- Boundary Tips Content (v-if="activeGuide === 'boundary'") -->
                <div class="boundary-tips-content" v-if="activeGuide === 'boundary'">
                  <h3>Boundary Tips - Instagram</h3> 
                  <!-- Replacing placeholder below -->
                  <div class="tip-item">
                    <h4>Comment Filtering System</h4>
                    <p>Create a custom list of keywords to automatically filter from comments under Settings and privacy -> Privacy -> Hidden Words. Include common boundary-crossing terms relevant to your content niche. The "cost" is potentially filtering legitimate comments that happen to contain filtered words.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Strategic Post Timing</h4>
                    <p>Schedule posts for times when you're available to moderate comments for the first hour after posting, when engagement is typically highest. The "cost" is limiting your posting schedule to your availability windows.</p>
                  </div>
                  <div class="tip-item">
                    <h4>DM Auto-Replies</h4>
                    <p>Create template responses for common DM requests that cross your boundaries. This allows consistent boundary enforcement without emotional drain. The "cost" is potentially appearing impersonal to followers seeking connection.</p>
                  </div>
                   <div class="tip-item">
                    <h4>Professional vs. Personal Accounts</h4>
                    <p>Consider creating separate accounts for professional content and personal interactions. Use a Creator or Business account for your public presence. The "cost" is managing multiple accounts and potentially dividing your audience.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Question Sticker Boundaries</h4>
                    <p>When using the Questions sticker in Stories, specify what types of questions you're open to answering. For example: "Ask me about my editing process!" rather than "Ask me anything!" The "cost" is potentially receiving fewer questions overall.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Limited Reply Windows</h4>
                    <p>Establish specific times for replying to comments and DMs, rather than being continuously available. Communicate these windows to your followers. The "cost" is potentially slower response times that might affect algorithm performance.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Collaboration Guidelines Document</h4>
                    <p>Create a simple one-page document outlining your expectations for collaborations, including content usage rights, tagging policies, and communication boundaries. The "cost" is adding formality to creative partnerships and potentially deterring casual collaborations.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Archive Strategically</h4>
                    <p>Regularly review and archive posts that no longer align with your content direction or that attract persistent boundary-crossing comments. The "cost" is reduced content volume which potentially affects your engagement metrics.</p>
                  </div>
                  <div class="tip-item">
                    <h4>Content Pillars Definition</h4>
                    <p>Define 3-5 specific content topics or "pillars" that your account focuses on. Politely decline requests for content that falls outside these areas. The "cost" is potentially missing opportunities to expand your content range based on follower requests.</p>
                  </div>
                   <div class="tip-item">
                    <h4>"Ask Me Anything" Alternatives</h4>
                    <p>Instead of open "Ask Me Anything" sessions, use more focused prompts like "Ask Me About My Workflow" or "Ask Me About My Equipment." The "cost" is receiving fewer questions overall and potentially appearing less open to your audience.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Image Modal -->
    <div v-if="enlargedImageSrc" class="image-modal-overlay">
      <div class="image-modal-content">
        <img :src="enlargedImageSrc" alt="Enlarged Image" @click="closeEnlargedImage">
        <button class="image-modal-close" @click="closeEnlargedImage">Close</button>
      </div>
    </div>

    <!-- Quick View Modal -->
    <div v-if="isQuickViewVisible" class="quick-view-modal" @click="closeQuickView">
      <div class="quick-view-content" @click.stop>
        <div v-html="quickViewContent"></div>
      </div>
    </div>

    <!-- Back to Top Button -->
    <button v-if="showBackToTop" @click="scrollToTop" class="back-to-top-button">
      ↑
    </button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'; // Add onMounted, onUnmounted

// Track the currently active platform (youtube, tiktok, etc.)
const activePlatform = ref(null);
// Track the currently active guide type within a platform (settings, tips, boundary)
const activeGuide = ref('settings');
// Track the currently active version (browser/mobile) when viewing settings
const activeVersion = ref('browser'); // Default to browser
// Track the currently active subsection within the YouTube BROWSER settings guide
const activeYoutubeSection = ref('default'); // Start with 'default' section open
// Track the currently active subsection within the YouTube MOBILE settings guide
const activeYoutubeMobileSection = ref('iosSettings'); // Start with 'iosSettings' section open
// Track the currently active subsection within the TikTok BROWSER settings guide
const activeTiktokSection = ref('account'); // Default to 'account' settings
// Track the currently active subsection within the TikTok MOBILE settings guide
const activeTiktokMobileSection = ref('iosSettings'); // Default to 'iosSettings'
// Track the currently active subsection within the Instagram BROWSER settings guide
const activeInstaSection = ref('general'); // Default to 'general' settings
// Track the currently active subsection within the Instagram MOBILE settings guide
const activeInstaMobileSection = ref('iosSettings'); // Default to 'iosSettings'

// State for enlarged image modal
const enlargedImageSrc = ref(null);

// State for Quick View modal
const isQuickViewVisible = ref(false);
const quickViewContent = ref(''); // Store summary HTML or text

// State for Back to Top button
const showBackToTop = ref(false);

// Function to toggle platform visibility
const togglePlatform = (platform) => {
  // Store the previous active platform for comparison
  const previousPlatform = activePlatform.value;
  
  // Toggle platform visibility
  if (activePlatform.value === platform) {
    activePlatform.value = null; // Close if already open
  } else {
    activePlatform.value = platform; // Open the new platform
    
    // Reset to the default guide/view when switching platforms
    activeGuide.value = 'settings'; // Default to the settings guide
    activeVersion.value = 'browser'; // Default to browser version
    
    // Reset relevant section states based on the newly selected platform
    if (platform === 'youtube') {
      activeYoutubeSection.value = 'default';
      activeYoutubeMobileSection.value = 'iosSettings';
    } else if (platform === 'tiktok') {
      activeTiktokSection.value = 'account';
      activeTiktokMobileSection.value = 'iosSettings';
    } else if (platform === 'instagram') {
      activeInstaSection.value = 'general';
      activeInstaMobileSection.value = 'iosSettings';
    }
    // Add logic for other platforms here
  }
  
  // Only scroll if opening a new platform
  if (activePlatform.value && previousPlatform !== activePlatform.value) {
    setTimeout(() => {
      // Find the platform section
      const platformSection = document.querySelector(`.${activePlatform.value}-section`);
      if (platformSection) {
        // Scroll to the top of the platform section
        platformSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }, 100);
  }
};

// Function to switch guide type (settings, tips, etc.)
const switchGuide = (guide) => {
  const previousGuide = activeGuide.value;
  activeGuide.value = guide;
  
  // Reset version/sections if switching away from settings guide for the current platform
  if (guide !== 'settings') {
      activeVersion.value = 'browser'; // Default back to browser
      // Reset relevant section states based on the currently active platform
      if (activePlatform.value === 'youtube') {
        activeYoutubeSection.value = 'default';
        activeYoutubeMobileSection.value = 'iosSettings';
      } else if (activePlatform.value === 'tiktok') {
        activeTiktokSection.value = 'account';
        activeTiktokMobileSection.value = 'iosSettings'; // Reset TikTok mobile too
      } else if (activePlatform.value === 'instagram') {
         activeInstaSection.value = 'general';
         activeInstaMobileSection.value = 'iosSettings'; // Reset Instagram mobile too
      }
      // Add resets for other platforms here
  }
  // Ensure correct default section is shown when switching TO settings
  else if (guide === 'settings') {
      activeVersion.value = 'browser'; // Default to browser when settings guide is selected
      // Reset relevant section states based on the currently active platform
      if (activePlatform.value === 'youtube') {
        activeYoutubeSection.value = 'default';
        activeYoutubeMobileSection.value = 'iosSettings';
      } else if (activePlatform.value === 'tiktok') {
        activeTiktokSection.value = 'account';
        activeTiktokMobileSection.value = 'iosSettings'; // Reset TikTok mobile too
      } else if (activePlatform.value === 'instagram') {
         activeInstaSection.value = 'general';
         activeInstaMobileSection.value = 'iosSettings'; // Reset Instagram mobile too
      }
       // Add resets for other platforms here
  }
  
  // Only scroll when switching to a different tab
  if (previousGuide !== guide && activePlatform.value) {
    setTimeout(() => {
      // Find the active tab button and scroll to its position
      const tabButtons = document.querySelectorAll(`.${activePlatform.value}-section .tab-navigation button`);
      for (const button of tabButtons) {
        if (button.classList.contains('active')) {
          // Get the platform section element
          const platformSection = document.querySelector(`.${activePlatform.value}-section`);
          if (platformSection) {
            // Scroll to the top of the platform section with an offset to ensure the tab is visible
            const platformRect = platformSection.getBoundingClientRect();
            const offset = 100; // Offset to ensure the tab is visible in the viewport
            window.scrollTo({
              top: window.scrollY + platformRect.top - offset,
              behavior: 'smooth'
            });
            break;
          }
        }
      }
    }, 100);
  }
};

// Function to switch between Browser and Mobile versions
const switchVersion = (version) => {
  const previousVersion = activeVersion.value;
  activeVersion.value = version;
  
  // Reset active section when switching versions for the current platform
   if (activePlatform.value === 'youtube') {
      if (version === 'browser') {
        activeYoutubeSection.value = 'default';
      } else if (version === 'mobile') {
        activeYoutubeMobileSection.value = 'iosSettings';
      }
   } else if (activePlatform.value === 'tiktok') {
     if (version === 'browser') {
        activeTiktokSection.value = 'account';
     } else if (version === 'mobile') { 
        activeTiktokMobileSection.value = 'iosSettings'; // Set default mobile section
     }
   } else if (activePlatform.value === 'instagram') {
     if (version === 'browser') {
        activeInstaSection.value = 'general';
     } 
      // Add mobile section reset for instagram when implemented
     // else if (version === 'mobile') { ... }
   }
   
   // Only scroll when switching to a different version
   if (previousVersion !== version && activePlatform.value) {
     setTimeout(() => {
       // Find the sub-tab navigation area
       const subTabNav = document.querySelector(`.${activePlatform.value}-section .sub-tab-navigation`);
       if (subTabNav) {
         // Scroll to the sub-tab navigation position
         const offset = 100; // Offset to ensure the tabs are visible at the top of the viewport
         window.scrollTo({
           top: window.scrollY + subTabNav.getBoundingClientRect().top - offset,
           behavior: 'smooth'
         });
       }
     }, 100);
   }
};

// Function to toggle YouTube BROWSER subsections
const toggleYoutubeSection = (section) => {
  const wasInactive = activeYoutubeSection.value !== section;
  activeYoutubeSection.value = activeYoutubeSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeYoutubeSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.youtube-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.youtube-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to toggle YouTube MOBILE subsections
const toggleYoutubeMobileSection = (section) => {
  const wasInactive = activeYoutubeMobileSection.value !== section;
  activeYoutubeMobileSection.value = activeYoutubeMobileSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeYoutubeMobileSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.youtube-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.youtube-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to toggle TikTok BROWSER subsections
const toggleTiktokSection = (section) => {
  const wasInactive = activeTiktokSection.value !== section;
  activeTiktokSection.value = activeTiktokSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeTiktokSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.tiktok-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.tiktok-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to toggle TikTok MOBILE subsections
const toggleTiktokMobileSection = (section) => {
  const wasInactive = activeTiktokMobileSection.value !== section;
  activeTiktokMobileSection.value = activeTiktokMobileSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeTiktokMobileSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.tiktok-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.tiktok-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to toggle Instagram BROWSER subsections
const toggleInstaSection = (section) => {
  const wasInactive = activeInstaSection.value !== section;
  activeInstaSection.value = activeInstaSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeInstaSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.instagram-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.instagram-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to toggle Instagram MOBILE subsections
const toggleInstaMobileSection = (section) => {
  const wasInactive = activeInstaMobileSection.value !== section;
  activeInstaMobileSection.value = activeInstaMobileSection.value === section ? null : section;
  
  // Only scroll if changing from collapsed to expanded state
  if (wasInactive && activeInstaMobileSection.value === section) {
    setTimeout(() => {
      // First scroll to the platform card
      const platformSection = document.querySelector('.instagram-section');
      if (platformSection) {
        // Scroll to platform section with offset
        const offset = 80;
        window.scrollTo({
          top: window.pageYOffset + platformSection.getBoundingClientRect().top - offset,
          behavior: 'smooth'
        });
        
        // Then after a short delay, scroll to the specific section header
        setTimeout(() => {
          const sectionHeaders = document.querySelectorAll('.instagram-section .section-header');
          for (const header of sectionHeaders) {
            if (header.textContent.includes(section)) {
              header.scrollIntoView({ behavior: 'smooth', block: 'start' });
              break;
            }
          }
        }, 300);
      }
    }, 100);
  }
};

// Function to show image in modal
const enlargeImage = (src) => {
  // Check if the src is the placeholder before enlarging
  if (src && !src.includes('screenshot-placeholder.svg')) {
    let resolvedSrc;
    if (import.meta.env.DEV) {
      // In development, resolve relative paths using import.meta.url
      try {
        resolvedSrc = new URL(src, import.meta.url).href;
      } catch (e) {
        console.error(`Error resolving image URL in dev: ${src}`, e);
        resolvedSrc = src; // Fallback for safety, though should normally resolve
      }
    } else {
      // In production, the src passed from the template is already the correct public path
      resolvedSrc = src;
    }
    enlargedImageSrc.value = resolvedSrc;
  }
};

// Function to close image modal
const closeEnlargedImage = () => {
  enlargedImageSrc.value = null;
};

// --- Quick View Modal Functions ---
const showQuickView = (platform) => {
  // Log current state for debugging
  console.log(`Quick View requested for: Platform=${platform}, Guide=${activeGuide.value}, Version=${activeVersion.value}, YTSection=${activeYoutubeSection.value}, YTMobileSection=${activeYoutubeMobileSection.value}`);

  // --- YouTube Summary Logic ---
  if (platform === 'youtube') {
    let summary = ``; // Start with empty summary

    if (activeGuide.value === 'settings') {
      // REMOVED: summary += `<p><strong>Settings Guide:</strong></p>`;
      if (activeVersion.value === 'browser') {
        // REMOVED: summary += `<p><em>Browser Version</em></p>`;
        // Check active BROWSER subsection
        switch (activeYoutubeSection.value) {
          case 'default':
            summary += `
              <h5>Default Privacy Settings</h5>
              <ul>
                <li><strong>Subscriptions:</strong> Keep private via Settings > Privacy (recommended for research).</li>
                <li><strong>Live Chat:</strong> Turn off Super Chat celebrations (Settings > Privacy) for spending privacy.</li>
              </ul>`;
            break;
          case 'perVideo':
            summary += `
              <h5>Per-Video Privacy Settings</h5>
              <ul>
                <li>Set visibility (Public, Unlisted, Private) via YouTube Studio > Content > Visibility dropdown.</li>
              </ul>`;
            break;
          case 'playlists':
            summary += `
              <h5>Hiding Saved Playlists</h5>
              <ul>
                <li>Set visibility (Public, Unlisted, Private) for your playlists via YouTube Studio > Content > Playlists > Details.</li>
                <li>Set visibility when creating new playlists while saving videos.</li>
              </ul>`;
            break;
          case 'comments':
            summary += `
              <h5>Comment Privacy Settings</h5>
              <ul>
                <li>Manage comment moderation levels (Allow all, Hold potentially inappropriate, Hold all, etc.) via YouTube Studio > Settings > Community > Defaults.</li>
                <li>Recommendation: Hold all comments for review to filter personal info.</li>
              </ul>`;
            break;
          default:
            summary += `<p>Expand a browser settings section (e.g., Default Privacy, Per-Video) to see its quick summary.</p>`;
        }
      } else if (activeVersion.value === 'mobile') {
        // REMOVED: summary += `<p><em>Mobile Version (iOS)</em></p>`;
        // Check active MOBILE subsection
        switch (activeYoutubeMobileSection.value) {
          case 'iosSettings':
             summary += `
               <h5>iOS System Settings</h5>
               <ul>
                 <li>Control Mic, Camera, Photos access via iPhone Settings > YouTube.</li>
                 <li>Recommendation: Limit access (e.g., allow photo access only when uploading).</li>
               </ul>`;
            break;
          case 'videoChannel':
             summary += `
               <h5>Per-Video & Channel Privacy (Mobile)</h5>
               <ul>
                 <li>Use YouTube Studio App > Content to set video visibility (Public, Private, Unlisted).</li>
                 <li>Note: Most advanced settings require the web version of YouTube Studio.</li>
               </ul>`;
            break;
          default:
            summary += `<p>Expand a mobile settings section (e.g., iOS Settings, Per-Video) to see its quick summary.</p>`;
        }
      } else {
         summary += `<p>Select Browser or Mobile version.</p>`;
      }
    } else if (activeGuide.value === 'tips') {
      // Keep existing tips summary, but remove the main H4 title
      summary += `
        <h5>Privacy Tips</h5>
        <ul>
          <li>Enable <strong>Two-Factor Authentication</strong> (Google Account).</li>
          <li>Set comments to private (Settings > Privacy) to hide comment history.</li>
          <li>Use <strong>Incognito Mode</strong> for private browsing.</li>
          <li>Review <strong>Third-Party App Access</strong> (Google Account).</li>
          <li>Consider a <strong>Brand Account</strong> for separation.</li>
          <li>Apply for <strong>Content ID</strong> (Partner Program).</li>
          <li>Review settings <strong>every 3 months</strong>.</li>
        </ul>
      `;
    } else if (activeGuide.value === 'boundary') {
      // Keep existing boundary summary, but remove the main H4 title
      summary += `
        <h5>Boundary Tips</h5>
        <ul>
          <li>Use custom <strong>Comment Filters</strong> (Studio > Settings > Community).</li>
          <li><strong>Schedule uploads</strong> for time off.</li>
          <li>Avoid real-time <strong>Location Disclosures</strong>.</li>
          <li>Use <strong>Memberships</strong> for controlled sharing.</li>
          <li><strong>Hold all comments</strong> for sensitive topics (Studio > Settings > Community).</li>
          <li>Use a separate <strong>Professional Email</strong>.</li>
          <li>Have a <strong>Collaboration Contract</strong> template.</li>
          <li>Prepare <strong>Response Templates</strong> for boundary-crossing questions.</li>
          <li>Practice <strong>Selective Personal Sharing</strong>.</li>
        </ul>
      `;
    } else {
       // If no specific guide/section identified, add a placeholder title
       summary = `<h4>Quick Summary</h4><p>Select a guide (Settings, Tips, Boundary) and expand a section to see details.</p>`;
    }
    quickViewContent.value = summary;
  }
  // --- TikTok Summary Logic ---
  else if (platform === 'tiktok') {
    let summary = ``; // Start empty
    if (activeGuide.value === 'settings') {
      if (activeVersion.value === 'browser') {
        switch (activeTiktokSection.value) {
          case 'account':
            summary += `
              <h5>Account Privacy (Browser)</h5>
              <ul>
                <li><strong>Private Account:</strong> Toggle ON/OFF via Settings > Privacy. Keep OFF for growth, consider ON for limited audiences.</li>
                <li><strong>Download Data:</strong> Request TXT/JSON archive via Settings > Privacy > Download your data.</li>
              </ul>`;
            break;
          case 'perVideo':
            summary += `
              <h5>Per-Video Privacy (Browser)</h5>
              <ul>
                <li><strong>Visibility:</strong> Set per video (Everyone, Friends, No one) via Video > 3 dots > Privacy settings.</li>
                <li><strong>Interactions:</strong> Toggle Comment/Duet/Stitch ON/OFF per video via Video > 3 dots > Privacy settings (Recommend OFF for Duet/Stitch).</li>
              </ul>`;
            break;
          default:
            summary += `<p>Expand a TikTok browser settings section (e.g., Account, Per-Video) to see its quick summary.</p>`;
        }
      } else if (activeVersion.value === 'mobile') {
        switch (activeTiktokMobileSection.value) {
          case 'iosSettings':
            summary += `
              <h5>iOS System Settings (TikTok)</h5>
              <ul>
                <li>Control Mic, Camera, Photos access via iPhone Settings > TikTok.</li>
                <li>Recommendation: Limit access (e.g., allow only while using the app).</li>
              </ul>`;
            break;
          case 'basic':
            summary += `
              <h5>Basic Privacy Settings (Mobile)</h5>
              <ul>
                <li><strong>Discoverability:</strong> Manage account suggestions via Profile > Menu > Settings > Privacy.</li>
                <li><strong>Contact Syncing:</strong> Enable/disable via Profile > Menu > Settings > Privacy.</li>
                <li><strong>Interactions:</strong> Review settings for Comments, DMs, Stitch, Duet, etc., under Profile > Menu > Settings > Privacy. Adjust as your account grows.</li>
              </ul>`;
            break;
          case 'perVideo':
            summary += `
              <h5>Per-Video Privacy (Mobile Post)</h5>
              <ul>
                <li>Set audience (Everyone, Friends, Only You) before posting.</li>
                <li>Toggle Allow Comments, Duet, Stitch via More options before posting.</li>
                <li>Consider allowing 'Save posts with watermark' and 'Audience controls'.</li>
              </ul>`;
            break;
          default:
            summary += `<p>Expand a TikTok mobile settings section (e.g., iOS Settings, Basic) to see its quick summary.</p>`;
        }
      } else {
        summary += `<p>Select Browser or Mobile version.</p>`;
      }
    } else if (activeGuide.value === 'tips') {
      summary += `
        <h5>TikTok Privacy Tips</h5>
        <ul>
          <li>Enable <strong>Two-Factor Authentication</strong>.</li>
          <li>Be aware Pro Accounts collect more analytics data.</li>
          <li>Use <strong>Comment Filter Keywords</strong>.</li>
          <li>Review photos before using in <strong>Green Screen</strong> effect.</li>
          <li>Leave <strong>Watermark</strong> on shares to other platforms.</li>
          <li>Disable precise <strong>Location Access</strong> in device settings.</li>
          <li><strong>Drafts</strong> are stored locally; back up raw footage.</li>
          <li>Limit personal info in <strong>Profile Bio</strong>.</li>
        </ul>
      `;
    } else if (activeGuide.value === 'boundary') {
      summary += `
        <h5>TikTok Boundary Tips</h5>
        <ul>
          <li>Use <strong>Scheduled Posting</strong> (Business accounts).</li>
          <li>Establish a <strong>Comment Response Protocol</strong>.</li>
          <li>Define <strong>Content Pillars</strong> to decline off-topic requests.</li>
          <li>Use a separate <strong>Viewer Account</strong>.</li>
          <li>Set boundaries for <strong>LIVE Streams</strong> beforehand.</li>
          <li>Use simple <strong>Collaboration Contracts</strong>.</li>
          <li>Set <strong>Comment Timeboxing</strong> (specific review times).</li>
          <li>Manage <strong>Duet/Stitch Permissions</strong> strategically per video.</li>
          <li>Define <strong>Knowledge-Sharing Boundaries</strong>.</li>
        </ul>
      `;
    } else {
      summary = `<h4>TikTok Quick Summary</h4><p>Select a guide (Settings, Tips, Boundary) and expand a section.</p>`;
    }
    quickViewContent.value = summary;
  }
  // --- Instagram Summary Logic ---
  else if (platform === 'instagram') {
    let summary = ``; // Start empty
    if (activeGuide.value === 'settings') {
      if (activeVersion.value === 'browser') {
         switch (activeInstaSection.value) {
          case 'general':
            summary += `
              <h5>General Privacy (Browser)</h5>
              <ul>
                <li><strong>Hide Story/Live:</strong> Choose specific people to hide from (Menu > Settings > Privacy).</li>
                <li><strong>Hide Likes:</strong> Hide like counts on posts/reels (Menu > Settings > Privacy).</li>
                <li><strong>Restricted Accounts:</strong> Limit interactions without blocking (Menu > Settings > Privacy).</li>
                <li><strong>Hidden Words:</strong> Filter unwanted comments/DMs (Menu > Settings > Privacy).</li>
                <li><strong>Privacy Center:</strong> Manage passwords, logins etc. (Menu > Settings > Privacy).</li>
              </ul>`;
            break;
          case 'perVideo':
            summary += `
              <h5>Per-Post Privacy (Browser)</h5>
              <ul>
                <li><strong>Hide Like Count:</strong> Toggle per post via 3 dots menu.</li>
                <li><strong>Turn Off Commenting:</strong> Disable comments per post via 3 dots menu.</li>
              </ul>`;
            break;
          default:
            summary += `<p>Expand an Instagram browser settings section (e.g., General, Per-Video) to see its quick summary.</p>`;
        }
      } else if (activeVersion.value === 'mobile') {
        switch (activeInstaMobileSection.value) {
           case 'iosSettings':
             summary += `
               <h5>iOS System Settings (Instagram)</h5>
               <ul>
                 <li>Control Mic, Camera, Photos access via iPhone Settings > Instagram.</li>
                 <li>Recommendation: Limit access (e.g., allow only while using the app).</li>
               </ul>`;
            break;
          case 'basic':
            summary += `
              <h5>Basic Privacy Settings (Mobile)</h5>
              <ul>
                <li>Manage Comments, Story/Live visibility, Messages, Restricted Accounts, Hidden Words via Profile > Menu > Settings & Privacy.</li>
              </ul>`;
            break;
          case 'perVideo': // Note: This is mostly for Stories/Reels/Live during creation
            summary += `
              <h5>Per-Content Privacy (Mobile Creation)</h5>
              <ul>
                <li><strong>Stories/Live:</strong> Choose audience (Your Story, Close Friends, Hide From) before posting.</li>
                <li><strong>Stories:</strong> Toggle sharing options before posting.</li>
                <li>Recommendation: Use Close Friends strategically.</li>
              </ul>`;
            break;
          default:
            summary += `<p>Expand an Instagram mobile settings section (e.g., iOS Settings, Basic) to see its quick summary.</p>`;
         }
      } else {
        summary += `<p>Select Browser or Mobile version.</p>`;
      }
    } else if (activeGuide.value === 'tips') {
       summary += `
        <h5>Instagram Privacy Tips</h5>
        <ul>
          <li>Enable <strong>Two-Factor Authentication</strong>.</li>
          <li>Monitor <strong>Login Activity</strong> regularly.</li>
          <li>Adjust <strong>Sensitive Content Control</strong> filters.</li>
          <li>Limit personal info in <strong>Profile Bio</strong>.</li>
          <li>Use <strong>Restrict</strong> instead of Block for problematic followers.</li>
          <li>Delay posting from recognizable <strong>Locations</strong>.</li>
          <li>Use <strong>Close Friends</strong> strategically (e.g., testing content).</li>
          <li>Avoid clicking suspicious links in DMs (<strong>Link Protection</strong>).</li>
          <li>Use secondary account for sensitive <strong>Story Views</strong>.</li>
          <li>Periodically <strong>Download Your Data</strong>.</li>
        </ul>
      `;
    } else if (activeGuide.value === 'boundary') {
      summary += `
        <h5>Instagram Boundary Tips</h5>
        <ul>
          <li>Use custom <strong>Comment Filtering</strong> (Hidden Words).</li>
          <li>Post when available for initial <strong>Moderation</strong>.</li>
          <li>Use <strong>DM Auto-Replies/Templates</strong> for boundary-crossing messages.</li>
          <li>Consider separate <strong>Professional/Personal Accounts</strong>.</li>
          <li>Use focused prompts for <strong>Question Stickers</strong>.</li>
          <li>Set specific <strong>Reply Windows</strong> (don't be available 24/7).</li>
          <li>Use <strong>Collaboration Guidelines</strong> document.</li>
          <li><strong>Archive</strong> posts attracting unwanted attention.</li>
          <li>Define <strong>Content Pillars</strong>.</li>
          <li>Use focused alternatives to "Ask Me Anything".</li>
        </ul>
      `;
    } else {
      summary = `<h4>Instagram Quick Summary</h4><p>Select a guide (Settings, Tips, Boundary) and expand a section.</p>`;
    }
    quickViewContent.value = summary;
  }
  // --- Fallback if platform unknown (should not happen with current buttons) ---
  else {
     quickViewContent.value = `<h4>Quick Summary</h4><p>Summary not available for this platform yet.</p>`;
  }

  isQuickViewVisible.value = true;
};

const closeQuickView = () => {
  isQuickViewVisible.value = false;
  quickViewContent.value = ''; // Clear content when closing
};
// --- End Quick View Modal Functions ---

// --- Back to Top Button Logic ---
const SCROLL_THRESHOLD = 300; // Pixels to scroll before showing button

const handleScroll = () => {
  if (window.pageYOffset > SCROLL_THRESHOLD) {
    showBackToTop.value = true;
  } else {
    showBackToTop.value = false;
  }
};

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
// --- End Back to Top Button Logic ---

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
  font-size: 4rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #3B5998 20%,
    #73A1FB 40%,
    #73A1FB 60%,
    #3B5998 80%
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
  white-space: normal;
  text-align: left;
  overflow: visible;
  padding-bottom: 0.1em;
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(59, 89, 152, 0.5));
  transform: scale(1.02);
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
  white-space: nowrap;
  text-align: left;
  overflow: visible;
}

.subtitle {
  font-size: 1.25rem;
  color: #666;
  line-height: 1.4;
  margin-top: 1.5rem;
  white-space: normal;
  text-align: left;
  max-width: 100%;
  /* Remove any background or border styles */
}

@media (min-width: 768px) {
  .subtitle {
    white-space: nowrap;
  }
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
  font-size: 1.25rem;
  color: #666;
  line-height: 1.4;
  margin-bottom: 2rem;
  /* Remove any background or border styles */
}

/* Platform section styles */
.platform-section {
  margin-bottom: 4rem; 
  background-color: #ffecf2; 
  border-radius: 20px; 
  padding: 3rem; 
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05); 
  max-width: 95%; 
  margin-left: auto;
  margin-right: auto;
}

.platform-header {
  display: flex;
  align-items: center;
  gap: 1.5rem; 
  cursor: pointer;
  position: relative;
  padding: 1rem;
  border-radius: 12px; 
  transition: background-color 0.3s;
  margin-bottom: 0.5rem; 
}

.platform-header:hover {
  background-color: #ffd9e6;
}

.platform-header.active {
  background-color: #ffb6d3; 
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
  width: 60px; 
  height: 60px;
  object-fit: contain;
}

.platform-header h2 {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

/* Style for Read Time */
.read-time {
  font-size: 0.9rem; /* Smaller font size */
  font-weight: 400; /* Lighter weight */
  color: #777; /* Grey color */
  margin-left: 0.5rem; /* Space from platform name */
  white-space: nowrap; /* Prevent wrapping */
}

/* YouTube section special styles */
.youtube-section {
  background-color: #ffecf2;
}

/* TikTok section special styles */
.tiktok-section {
  background-color: #ffecf2; 
}

/* Instagram section special styles */
.instagram-section {
  background-color: #ffecf2; 
}

/* Privacy settings section */
.privacy-settings {
  /* Grid layout removed */
  background-color: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}

.settings-content {
  padding: 2rem;
}

.section-header {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
  margin-bottom: 1rem;
}

.section-header:hover {
  background-color: #f9f9f9;
}

.section-header h3 {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
  color: #333;
}

.toggle-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.toggle-icon.rotated {
  transform: rotate(180deg);
}

.section-content {
  padding-left: 1rem;
  margin-bottom: 1rem;
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
  cursor: pointer;
  transition: opacity 0.2s ease-in-out;
}

.step-image img:hover {
  opacity: 0.85;
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
  }
}

@media (min-width: 1280px) {
  .title-group h1 {
    font-size: 6rem;
  }
  .title-group h2 {
    font-size: 3.75rem;
  }
  .subtitle {
    font-size: 1.875rem;
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
  }
  
  .decorative-elements {
    transform: translateX(0) scale(0.9);
    opacity: 0.5;
    row-gap: 0.5rem;
  }
  
  .title-group h1 {
    @apply text-5xl;
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-4xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-xl;
    white-space: normal;
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
    max-width: 90%;
  }
  
  .title-group h1 {
    @apply text-4xl;
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-3xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-lg;
    white-space: normal;
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

  .title-group h1 {
    @apply text-3xl;
    white-space: nowrap;
  }
  
  .title-group h2 {
    @apply text-2xl;
    white-space: normal;
  }
  
  .subtitle {
    @apply text-base;
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

.step ul {
  list-style-type: disc;
  padding-left: 2rem;
  margin-bottom: 1.5rem;
}

.step li {
  margin-bottom: 0.75rem;
  line-height: 1.5;
  color: #555;
}

/* Style for adjacent images */
.step-image-row {
  display: flex;
  gap: 1rem; /* Adjust gap between images */
  margin-bottom: 1rem; /* Space below the row */
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
}

/* Special styling for Instagram Per-Video section images */
.insta-pervideo-image {
  height: 200px !important; /* Force consistent height for both images */
  max-width: 350px;
  margin: 0 auto; /* Center the images */
}

.insta-pervideo-image img {
  max-height: 100%;
  object-fit: contain;
}

.step-image-row .step-image {
  flex: 1 1 calc(50% - 0.5rem); /* Allow images to take up to half the width, adjusting for gap */
  min-width: 150px; /* Minimum width before wrapping */
  /* Override default step-image height if needed, or ensure aspect ratio is handled */
  height: auto; /* Let height adjust based on width */
}

/* Image Modal Styles */
.image-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.image-modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.image-modal-content img {
  display: block;
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  border-radius: 8px; /* Optional: rounded corners for enlarged image */
}

.image-modal-close {
  position: absolute;
  top: -30px; /* Position above the image */
  right: -10px;
  font-size: 2rem;
  font-weight: bold;
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.image-modal-close:hover {
  color: #ccc;
}

/* Privacy Tips & Boundary Tips Content Styles */
.privacy-tips-content,
.boundary-tips-content {
  padding: 2rem; /* Match settings content padding */
  background-color: #fff; /* White background like settings */
  border-radius: 12px; /* Match settings border radius */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); /* Match settings shadow */
}

.privacy-tips-content h3,
.boundary-tips-content h3 {
  font-size: 1.8rem; /* Slightly larger title */
  font-weight: 600;
  color: #333;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
}

.tip-item {
  margin-bottom: 1.5rem;
}

.tip-item h4 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #e75a97; /* Use accent color for tip titles */
  margin-bottom: 0.5rem;
}

.tip-item p {
  font-size: 1rem;
  line-height: 1.6;
  color: #555;
}

/* Styles for Beautified Privacy Control List (Insta Mobile Step 3) */
.privacy-control-list {
  margin-top: 1.5rem;
  margin-left: 1rem; /* Add left indent */
  padding-left: 1rem; /* Add padding for visual nesting */
  border-left: 2px solid #eee; /* Add a subtle left border */
}

.privacy-control-group {
  /* Remove background/border that makes it look separate */
  /* background-color: #f9f9f9; */ 
  /* border: 1px solid #eee; */
  border: none; /* Remove border */
  background-color: transparent; /* Remove background */
  border-radius: 0; /* Remove border-radius */
  padding: 0 0 1rem 0; /* Adjust padding (remove left/right, keep bottom) */
  margin-bottom: 1rem;
}

.privacy-control-group h5 {
  font-size: 1.1rem; /* Slightly smaller sub-heading */
  font-weight: 600;
  color: #333;
  margin-top: 0;
  margin-bottom: 0.75rem;
  padding-bottom: 0.25rem;
  border-bottom: 1px solid #ddd;
}

.privacy-control-group ul {
  list-style-type: disc; /* Ensure bullets */
  padding-left: 1.5rem; /* Indent list */
  margin-bottom: 0; /* Remove default bottom margin */
}

.privacy-control-group li {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

/* Quick View Modal Styles */
.quick-view-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.quick-view-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  background-color: #fdfcfe;
  border-radius: 12px;
  overflow-y: auto;
  max-height: 80vh; 
  padding: 2rem; 
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease; 
}

.quick-view-content:hover {
  transform: translateY(-5px);
}

/* 删除按钮样式，不再需要 */
/* .quick-view-content button {
  position: absolute;
  top: -30px;
  right: -10px;
  font-size: 2rem;
  font-weight: bold;
  color: white;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.quick-view-content button:hover {
  color: #ccc;
} */

.quick-view-content div {
  color: #444; /* 深色文本 */
  font-size: 1.1rem; /* 基础字体大小 */
  line-height: 1.6; /* 行高 */
}

/* Style the subsection titles (h5) */
.quick-view-content h5 {
  font-size: 1.4rem; /* Larger title font size */
  font-weight: 600; /* Bolder title */
  color: #e75a97; /* Use accent color */
  margin-top: 0; /* Remove default top margin */
  margin-bottom: 1rem; /* Space below title */
  padding-bottom: 0.5rem; /* Space below title underline */
  border-bottom: 2px solid rgba(231, 90, 151, 0.2); /* Subtle underline */
}

/* Style the main placeholder title (h4) */
.quick-view-content h4 {
  font-size: 1.5rem; /* Larger title font size */
  font-weight: 600; /* Bolder title */
  color: #555; /* Slightly muted color */
  margin-top: 0;
  margin-bottom: 1rem;
}

/* Style the placeholder text */
.quick-view-content p {
  margin-bottom: 1rem;
}

/* Style the lists */
.quick-view-content ul {
  list-style: disc; /* Use standard bullets */
  padding-left: 2rem; /* Indent list items */
  margin-bottom: 1rem; /* Space below list */
}

.quick-view-content li {
  margin-bottom: 0.75rem; /* Space between list items */
}

/* Style strong text within list items */
.quick-view-content li strong {
  color: #333; /* Make keywords slightly darker */
}

/* ADD STYLES FOR POSITIONING QUICK VIEW BUTTON */
.settings-content-area {
  position: relative; /* Needed for absolute positioning of child */
  padding-top: 1rem; /* Reduce top padding, tabs provide space */
}

.settings-content-area > .quick-view {
  position: absolute;
  top: 1rem; /* Align with top padding */
  right: 2rem; /* Adjust as needed, matches content padding */
  margin-top: 0; /* Override previous margin */
  z-index: 10; /* Ensure it's above other content and tabs */
}

/* Back to Top Button Styles */
.back-to-top-button {
  position: fixed;
  bottom: 2rem; /* Adjust as needed */
  right: 2rem; /* Adjust as needed */
  background-color: rgba(231, 90, 151, 0.8); /* Accent color with some transparency */
  color: white;
  border: none;
  border-radius: 50%; /* Make it circular */
  width: 50px; /* Fixed width */
  height: 50px; /* Fixed height */
  font-size: 1.5rem; /* Adjust arrow size */
  line-height: 50px; /* Center arrow vertically */
  text-align: center; /* Center arrow horizontally */
  cursor: pointer;
  z-index: 999; /* Below modals but above most content */
  transition: background-color 0.3s, opacity 0.3s;
  opacity: 0.8;
}

.back-to-top-button:hover {
  background-color: rgba(231, 90, 151, 1); /* Solid accent color on hover */
  opacity: 1;
}

/* ADD TAB NAVIGATION STYLES START */
.tab-navigation, .sub-tab-navigation {
  display: flex;
  flex-wrap: wrap; /* Allow wrapping on smaller screens */
  gap: 0.5rem;
  padding: 1rem 2rem 0; /* Add padding top/horizontal */
  border-bottom: 1px solid #eee;
  position: relative; /* To contain absolutely positioned elements like quick view */
  z-index: 5; /* Below quick view button */
}

.sub-tab-navigation {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
  background-color: #f9f9f9; /* Light background for sub-tabs */
  border-bottom: 1px solid #eee; /* Add border back for separation */
}

.tab-navigation button, .sub-tab-navigation button {
  padding: 0.75rem 1.25rem;
  border: none;
  background-color: transparent;
  cursor: pointer;
  font-size: 1.25rem; /* Increased from 1.1rem */
  font-weight: 600; /* Made slightly bolder */
  color: #555;
  border-bottom: 3px solid transparent;
  transition: color 0.3s, border-bottom-color 0.3s;
  margin-bottom: -1px; /* Align bottom border with container border */
  white-space: nowrap; /* Prevent button text wrapping */
}

.tab-navigation button:hover, .sub-tab-navigation button:hover {
  color: #e75a97;
}

.tab-navigation button.active, .sub-tab-navigation button.active {
  color: #e75a97;
  border-bottom-color: #e75a97;
}

.sub-tab-navigation button {
  font-size: 1.15rem; /* Increased from 1rem */
  padding: 0.5rem 1rem;
}
/* ADD TAB NAVIGATION STYLES END */

/* Adjust content area positioning */
.settings-content-area {
  position: relative; 
  padding-top: 1rem; /* Keep minimal top padding */
}

/* Keep quick view button positioning relative to content area */
.settings-content-area > .quick-view {
  position: absolute;
  top: 1rem; 
  right: 2rem; 
  margin-top: 0; 
  z-index: 10; 
}
</style>