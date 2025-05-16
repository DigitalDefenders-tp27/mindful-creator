<template>
  <div class="creator-wellbeing">
    <!-- Scroll Island -->
    <ScrollIsland title="Creator Wellbeing" ref="scrollIslandRef">
      <div class="island-sections">
        <div class="island-section" @click="scrollToSection('dashboard-section')">
          <h4>Digital Impact Analysis Dashboard</h4>
        </div>
        <div class="island-section" @click="scrollToSection('resource-finder-section')">
          <h4>Wellbeing Resource Finder</h4>
        </div>
        <div class="island-section" @click="scrollToSection('activities-section')">
          <h4>Wellbeing Activities Hub</h4>
        </div>
      </div>
    </ScrollIsland>
    
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
        <div class="decorative-elements">
          <!-- Top Row Right -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Pink_round.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Wide_Red.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Dashboard Section -->
    <section class="dashboard-section">
      <div class="container">
        <h1 class="section-title">Digital Impact Analysis Dashboard</h1>
        <p class="section-subtitle">Explore how your usage patterns affect wellbeing based on real data</p>
        
        <div class="tabs">
          <div v-for="(tab, index) in tabs" :key="index" class="tab" :class="{ active: currentTab === index }"
            @click="switchTab(index)">
            <span v-if="index === 0">
              <span>Screen Time</span>
              <span>& Emotions</span>
            </span>
            <span v-else-if="index === 1">
              <span>Digital Habits</span>
              <span>& Sleep</span>
            </span>
            <span v-else-if="index === 2">
              <span>Engagement</span>
              <span>& Rewards</span>
            </span>
            <span v-else-if="index === 3">
              <span>Distractions</span>
              <span>& Anxiety</span>
            </span>
          </div>
        </div>

        <div class="visualisation-container">
          <div class="chart-area">
            <canvas id="mainChart" style="max-height: 400px; width: 100%;"></canvas>
          </div>
          <div class="insight-area">
            <h3 class="insight-heading">Key Insights</h3>
            <div v-for="(insight, index) in tabs[currentTab].insights" :key="index" class="insight-box">
              {{ insight }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Wellbeing Resource Finder -->
    <section class="resource-finder-section">
      <div class="container">
        <h1 class="section-title">Wellbeing Resource Finder</h1>
        <p class="section-subtitle">Find and navigate yourself to get wellbeing resources easily near you.</p>

        <div class="resource-finder-content">
          <!-- Tabs for resource type -->
          <div class="resource-tabs">
            <div 
              class="resource-tab" 
              :class="{ active: activeTab === 'offline' }"
              @click="switchResourceTab('offline')"
            >Medical Clinic</div>
            <div 
              class="resource-tab resource-tab-online"
              :class="{ active: activeTab === 'online' }"
              @click="switchResourceTab('online')"
            >Online Resources</div>
          </div>
          
          <div class="resource-content" :class="{ 'online-only': activeTab === 'online' }">
            <!-- Google Map display -->
            <div class="map-container" v-if="activeTab === 'offline'">
              <!-- Search bar for address (MOVED INSIDE map-container) -->
              <div class="search-bar" v-if="activeTab === 'offline'">
                <input 
                  id="address-search"
                  v-model="searchAddress" 
                  @keyup.enter="onSearch"
                  
                  class="search-input"
                  :disabled="isSearching"
                />
                <button 
                  @click="onSearch" 
                  class="search-btn"
                  :class="{ 'is-loading': isSearching }"
                  :disabled="isSearching"
                  v-html="searchBtnContent"
                ></button>
              </div>

              <div id="google-map" style="width: 100%; height: 100%; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.08);"></div>
              
              <button class="position-btn" @click="getMyPosition">
                <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M12 2C8.13 2 5 5.13 5 9C5 14.25 12 22 12 22C12 22 19 14.25 19 9C19 5.13 15.87 2 12 2ZM12 11.5C10.62 11.5 9.5 10.38 9.5 9C9.5 7.62 10.62 6.5 12 6.5C13.38 6.5 14.5 7.62 14.5 9C14.5 10.38 13.38 11.5 12 11.5Z" fill="white"/>
                </svg>
                Get My Location
              </button>
            </div>
            
            <!-- Online Resources -->
            <div class="online-resources-container" :class="{ 'full-width': activeTab === 'online' }" v-if="activeTab === 'online'">
              <div class="online-resources-list">
                <div class="online-resource-card">
                  <div class="resource-logo">
                    <img src="@/assets/icons/elements/online-therapy.svg" alt="BetterHelp" class="resource-icon">
                  </div>
                  <div class="resource-info">
                    <h3>BetterHelp</h3>
                    <p>Online counselling and therapy with professional counsellors.</p>
                    <div class="resource-tags">
                      <span class="tag">Online Therapy</span>
                      <span class="tag">Subscription</span>
                    </div>
                    <a href="https://www.betterhelp.com" target="_blank" class="resource-link-btn">Visit Website</a>
                  </div>
                </div>
                
                <div class="online-resource-card">
                  <div class="resource-logo">
                    <img src="@/assets/icons/elements/meditation-app.svg" alt="Headspace" class="resource-icon">
                  </div>
                  <div class="resource-info">
                    <h3>Headspace</h3>
                    <p>Guided meditation and mindfulness exercises for stress reduction.</p>
                    <div class="resource-tags">
                      <span class="tag">Meditation</span>
                      <span class="tag">Freemium</span>
                    </div>
                    <a href="https://www.headspace.com" target="_blank" class="resource-link-btn">Visit Website</a>
                  </div>
                </div>
                
                <div class="online-resource-card">
                  <div class="resource-logo">
                    <img src="@/assets/icons/elements/support-group.svg" alt="Support Group" class="resource-icon">
                  </div>
                  <div class="resource-info">
                    <h3>7 Cups</h3>
                    <p>Free emotional support through online chat with trained listeners.</p>
                    <div class="resource-tags">
                      <span class="tag">Peer Support</span>
                      <span class="tag">Free</span>
                    </div>
                    <a href="https://www.7cups.com" target="_blank" class="resource-link-btn">Visit Website</a>
                  </div>
                </div>
              </div>
            </div>

            <!-- Clinic Details -->
            <div class="resource-details" v-if="selectedClinic && activeTab === 'offline'">
              <div class="resource-info-content">
                <h3 class="resource-name">{{ selectedClinic.name }}</h3>
                <div class="clinic-details-card info-section">
                  <div class="rating">
                    <span class="rating-score">{{ selectedClinic.rating }}</span>
                    <div class="stars" v-html="generateStars(selectedClinic.rating)"></div>
                    <span class="reviews">({{ selectedClinic.reviews }})</span>
                  </div>

                  <div class="resource-location">
                    <img src="@/assets/icons/elements/location.svg" alt="Location" class="location-icon">
                    <span>{{ selectedClinic.address }}</span>
                  </div>

                  <div class="resource-phone" v-if="selectedClinic.phone">
                    <img src="@/assets/icons/elements/phone.svg" alt="Phone" class="phone-icon">
                    <a :href="`tel:${selectedClinic.phone}`">{{ selectedClinic.phone }}</a>
                  </div>

                  <div class="resource-website">
                    <img src="@/assets/icons/elements/globe.svg" alt="Website" class="website-icon">
                    <a :href="selectedClinic.website" target="_blank">Click to visit</a>
                  </div>
                </div> 

                <div class="opening-hours info-section"> 
                  <h4>Opening hours</h4>
                  <div class="hours-grid">
                    <template v-if="selectedClinic && selectedClinic.openingHours && selectedClinic.openingHours.weekday_text && selectedClinic.openingHours.weekday_text.length">
                      <div v-for="line in selectedClinic.openingHours.weekday_text" :key="line" class="hours-line">
                        <span>{{ line }}</span>
                      </div>
                      <div v-if="selectedClinic.openingHours.open_now !== undefined" 
                           :class="['open-status', selectedClinic.openingHours.open_now ? 'open' : 'closed']">
                        {{ selectedClinic.openingHours.open_now ? 'Open now' : 'Closed now' }}
                      </div>
                    </template>
                    <template v-else-if="selectedClinic && selectedClinic.place_id && (!selectedClinic.openingHours || !selectedClinic.openingHours.weekday_text)">
                       <div><span>Opening hours not available.</span></div>
                    </template>
                    <template v-else-if="selectedClinic && !selectedClinic.place_id">
                        <div><span>Select a clinic to see details.</span></div>
                    </template>
                     <template v-else-if="isSearching && !selectedClinic">
                        <div><span>Finding nearby clinics...</span></div>
                    </template>
                    <template v-else>
                       <div><span>Select a clinic from the map.</span></div>
                    </template>
                  </div>
                </div>
              </div>

              <div class="resource-actions">
                <button class="action-btn direction-btn" @click="getDirections">
                  <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2L4.5 9.5H9V16H15V9.5H19.5L12 2Z" fill="white"/>
                  </svg>
                  Get Directions
                </button>
                <button class="action-btn guide-btn" @click="showGuide = true">
                  <svg class="btn-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3ZM7 7H9V9H7V7ZM7 11H9V13H7V11ZM7 15H9V17H7V15ZM17 17H11V15H17V17ZM17 13H11V11H17V13ZM17 9H11V7H17V9Z" fill="white"/>
                  </svg>
                  Get Preparation Guide
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Wellbeing Activities Hub -->
    <section class="activities-section" id="wellbeing-activities">
      <div class="container">
        <h1 class="section-title">Wellbeing Activities Hub</h1>
        <p class="section-subtitle">Release your stress by joining fun activities and making like-minded friends.</p>

        <div class="activities-header">
          <h3 class="recent-title">RECENT CAMPAIGNS...</h3>
          <button @click="openModal" class="view-all-btn">VIEW ALL EVENTS</button>
        </div>

        <div class="activities-grid">
          <a v-for="(activity, index) in featuredActivities" 
             :key="index"
             :href="activity.link"
             target="_blank" 
             class="activity-card-link">
            <div class="activity-card">
              <img :src="getImageUrl(activity.image)" :alt="activity.title" class="activity-img">
              <h3 class="activity-title">{{ activity.title }}</h3>
              <div class="activity-tags">
                <span v-for="(tag, tagIndex) in activity.tags.slice(0, 2)" 
                      :key="tagIndex" 
                      :class="['tag', tag.toLowerCase().replace(' ', '-')]">{{ tag }}</span>
              </div>
              <div class="activity-details">
                <span class="group-size">{{ activity.location }}</span>
                <span class="location">{{ activity.price === 'Free' ? 'Free Event' : activity.price }}</span>
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
          
          <div class="filter-header">
            <h3>Filters</h3>
            <button class="filter-toggle" @click="toggleFilters">
              <span>{{ filtersVisible ? 'Hide Filters' : 'Show Filters' }}</span>
              <span class="toggle-icon">{{ filtersVisible ? '▲' : '▼' }}</span>
            </button>
          </div>
          
          <div class="event-filters" :class="{ 'filters-collapsed': !filtersVisible }">
            <div class="filter-group">
              <label>Location:</label>
              <select v-model="selectedLocation">
                <option>All locations</option>
                <optgroup label="Queensland">
                  <option>Brisbane</option>
                  <option>West End</option>
                </optgroup>
                <optgroup label="New South Wales">
                  <option>Narrabeen</option>
                  <option>Sydney</option>
                </optgroup>
                <optgroup label="Victoria">
                  <option>Flinders Blowhole</option>
                  <option>Geelong</option>
                  <option>Little River</option>
                  <option>Melbourne</option>
                  <option>Torquay Beach</option>
                  <option>Warrnambool</option>
                </optgroup>
              </select>
            </div>
            <div class="filter-group">
              <label>Category:</label>
              <select v-model="selectedCategory">
                <option>All types</option>
                <option>Festival</option>
                <option>Mental Health</option>
                <option>Outdoor Wellness</option>
                <option>physical wellness practice</option>
                <option>Workplace Wellbeing</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Month:</label>
              <select v-model="selectedMonth">
                <option>Any time</option>
                <option>April</option>
                <option>May</option>
                <option>June</option>
                <option>October</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Price:</label>
              <select v-model="selectedPrice">
                <option>Any price</option>
                <option>Free</option>
                <option>Paid</option>
              </select>
            </div>
            <div class="filter-group">
              <label>Sort by:</label>
              <select v-model="sortOption">
                <option value="dateAsc">Date (Earliest first)</option>
                <option value="dateDesc">Date (Latest first)</option>
                <option value="name">Name (A-Z)</option>
                <option value="location">Location (A-Z)</option>
              </select>
            </div>
            <div class="filter-actions">
              <button @click="resetFilters" class="clear-filters-btn">Clear All Filters</button>
            </div>
          </div>

          <div class="events-grid">
            <div v-for="event in sortedFilteredEvents" :key="event.id" class="event-card">
              <div class="event-img-container">
                <img :src="getImageUrl(event.image)" :alt="event.title" class="event-img">
              </div>
              <div class="event-info">
                <h3>{{ event.title }}</h3>
                <div class="event-tags">
                  <span v-for="(tag, index) in event.tags" :key="index" :class="['tag', tag.toLowerCase().replace(' ', '-')]">{{ tag }}</span>
                </div>
                <p class="event-description">{{ event.description }}</p>
                <div class="event-meta">
                  <div><strong>Location:</strong> {{ event.location }}</div>
                  <div v-if="event.address"><strong>Address:</strong> {{ event.address }}</div>
                  <div><strong>Date:</strong> {{ event.date }}</div>
                  <div><strong>Time:</strong> {{ event.time }}</div>
                  <div class="event-link"><strong>Link:</strong> {{ event.link }}</div>
                </div>
                <a :href="event.link"
                  target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
  
  <!-- Preparation Guide Modal - Moved outside main container to prevent stacking context issues -->
  <div v-if="showGuide" class="preparation-guide-wrapper">
    <Modal @close="showGuide = false">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <span>Preparation Guide for Psychological Consultation</span>
          <button @click="showGuide = false" style="background:none;border:none;font-size:1.5rem;line-height:1;color:#e75a97;cursor:pointer;">×</button>
        </div>
      </template>
      <template #body>
        <h4 style="margin-top:0; color:#e75a97;">Before Your Appointment</h4>
        <ul style="margin-bottom:1.2rem;">
          <li>✓ Bring your Medicare card or insurance details.</li>
          <li>✓ Prepare a brief list of your main concerns or goals.</li>
          <li>✓ Arrive 10 minutes early for paperwork and to relax.</li>
        </ul>
        <h4 style="color:#e75a97;">During Your Appointment</h4>
        <ul style="margin-bottom:1.2rem;">
          <li>✓ Be open and honest with your psychologist.</li>
          <li>✓ Share your prepared concerns and ask questions.</li>
          <li>✓ Take notes if you find it helpful.</li>
        </ul>
        <h4 style="color:#e75a97;">After Your Appointment</h4>
        <ul>
          <li>✓ Reflect on the session and any advice given.</li>
          <li>✓ Schedule your next appointment if needed.</li>
          <li>✓ Take care of yourself and reach out if you have questions.</li>
        </ul>
        <p style="margin-top:1.2rem; color:#666;">Wishing you a positive and supportive experience!</p>
      </template>
    </Modal>
  </div>

  <!-- 添加确认对话框 (Restored Confirmation Dialog) -->
  <div v-if="showOnlineConfirm" class="confirmation-dialog-overlay">
    <div class="confirmation-dialog">
      <div class="dialog-header">
        <h2>Switch to Relaxation Page?</h2>
      </div>
      <div class="dialog-content">
        <p>Would you like to explore our relaxation techniques and exercises?</p>
        <p>You can also stay here to check out our online resources.</p>
      </div>
      <div class="dialog-actions">
        <button class="cancel-btn" @click="handleCancel">Stay Here</button>
        <button class="confirm-btn" @click="handleConfirm">Go to Relaxation</button>
      </div>
    </div>
  </div>

  <!-- Online confirmation dialog (Alternative/Original - kept for reference, might be the one intended) -->
  <div v-if="showOnlineConfirm" class="modal-overlay"> <!-- This uses .modal-overlay, might be different style -->
    <div class="modal-content"> <!-- This uses .modal-content -->
      <h3>Switch to Online Resources?</h3>
      <p>Are you sure you want to switch to online resources? This will help you find professional help from the comfort of your home.</p>
      <div class="modal-actions">
        <button class="cancel-btn" @click="handleCancel">Cancel</button> <!-- handleCancel would make them stay on online resources -->
        <button class="confirm-btn" @click="handleConfirm">Continue</button> <!-- handleConfirm would take them to /relaxation -->
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Loader } from '@googlemaps/js-api-loader'
import Chart from 'chart.js/auto'
import Modal from '../components/Modal.vue'
import axios from 'axios'
import ScrollIsland from '@/components/ScrollIsland.vue'

// State variables
const currentTab = ref(0)
let chartInstance = null
const selectedClinic = ref(null) // Initialize as null
const showGuide = ref(false)
const mapCenter = ref({ lat: -37.8136, lng: 144.9631 }) // Default Melbourne centre coordinates
const userLocation = ref(null)
const displayedClinics = ref([]) // Initialize as empty
const activeTab = ref('offline')
const searchAddress = ref('')
const userIcon = { url: '../assets/icons/elements/user-location.svg', scaledSize: { width: 32, height: 32 } }

// Event related states
const isModalVisible = ref(false)
const searchQuery = ref('')
const selectedLocation = ref('All locations')
const selectedCategory = ref('All types')
const selectedMonth = ref('Any time')
const selectedPrice = ref('Any price')
const sortOption = ref('dateAsc')
const filtersVisible = ref(window.innerWidth > 768) // Collapsed by default on mobile

// Add new ref for online confirmation
const showOnlineConfirm = ref(false)

// Map-related states
const isSearching = ref(false)
const map = ref(null)
const markers = ref([])
const userMarker = ref(null)
const searchMarker = ref(null)
const searchBox = ref(null)

const router = useRouter()

// Add global Google object reference
let googleInstance = null;
let placesService = null; // Added for Places API

// Initialize Google Maps
const initMap = async () => {
  try {
    // If map already exists, clean it first
    if (map.value) {
      map.value = null;
    }
    
    // Clear all markers
    if (markers.value && markers.value.length > 0) {
      markers.value.forEach(marker => marker.setMap(null));
      markers.value = [];
    }

    // Check API key
    if (!import.meta.env.VITE_GOOGLE_MAPS_API_KEY) {
      throw new Error('Google Maps API key is missing');
    }

    // Check map container
    const mapElement = document.getElementById('google-map');
    if (!mapElement) {
      throw new Error('Map container not found');
    }

    // Ensure map container is visible
    if (!mapElement.offsetParent) {
      console.log('Map container is not visible, waiting for it to become visible...');
      await new Promise(resolve => setTimeout(resolve, 500)); // Wait for DOM update
    }

    // Set map container dimensions
    mapElement.style.width = '100%';
    mapElement.style.height = '100%';

    const loader = new Loader({
      apiKey: import.meta.env.VITE_GOOGLE_MAPS_API_KEY,
      version: "weekly",
      libraries: ["places", "maps", "marker"], // Ensure maps and marker libraries are loaded
      language: "en",
      region: "AU"
    });

    // Load Google Maps
    googleInstance = await loader.load();
    const { Map } = await googleInstance.maps.importLibrary("maps");
    // const { AdvancedMarkerElement } = await googleInstance.maps.importLibrary("marker"); // For advanced markers if needed

    // Initialize map
    map.value = new Map(mapElement, {
      center: mapCenter.value, // Use mapCenter ref
      zoom: 13,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      mapId: 'MINDFUL_CREATOR_MAP_ID', // Optional: for cloud-based map styling
      styles: [
        {
          featureType: "poi",
          elementType: "labels",
          stylers: [{ visibility: "off" }]
        },
        { // Hide most business POIs to de-clutter, we will add our own.
          featureType: "poi.business",
          stylers: [{ visibility: "off" }],
        },
      ]
    });
    
    placesService = new googleInstance.maps.places.PlacesService(map.value);
    googleInstance.maps.event.trigger(map.value, 'resize');


    // Initialize Places Autocomplete
    const input = document.querySelector('.search-input'); // Ensure this selector is correct
    if (input) {
      const autocomplete = new googleInstance.maps.places.Autocomplete(input, {
        // bounds for Melbourne area as an example, adjust as needed or remove for broader search
        bounds: new googleInstance.maps.LatLngBounds(
          new googleInstance.maps.LatLng(-38.5, 144.5), 
          new googleInstance.maps.LatLng(-37.5, 145.5)
        ),
        componentRestrictions: { country: 'au' },
        fields: ['geometry', 'name', 'formatted_address', 'place_id'], // Request needed fields
        types: ['address']
      });

      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
          searchAddress.value = place.formatted_address || place.name; // Update search input text
          handlePlaceSelection(place);
        }
      });
    }

    // Initial search for clinics around the map center
    findAndDisplayNearbyClinics(map.value.getCenter());


  } catch (error) {
    console.error("Error initializing map:", error);
    alert(error.message || 'Error loading map. Please refresh the page and try again.');
    isSearching.value = false;
  }
};

// Update updateMarkers function
const updateMarkers = async () => {
  try {
    if (!map.value || !googleInstance) {
      console.warn("Map or googleInstance not ready for updateMarkers");
      return;
    }

    // Clear existing clinic markers (markers ref stores clinic markers)
    if (markers.value && markers.value.length > 0) {
      markers.value.forEach(marker => marker.setMap(null));
      markers.value = []; // Reset the array
    }

    // Add marker for each clinic from displayedClinics
    displayedClinics.value.forEach(clinic => {
      const marker = new googleInstance.maps.Marker({
        position: { lat: clinic.lat, lng: clinic.lng },
        map: map.value,
        title: clinic.name,
        icon: {
          path: googleInstance.maps.SymbolPath.CIRCLE,
          scale: 8, // size
          fillColor: "red", // Red dot for clinics
          fillOpacity: 1,
          strokeWeight: 1,
          strokeColor: "white"
        },
        animation: googleInstance.maps.Animation.DROP
      });

      marker.addListener('click', () => {
        selectClinic(clinic);
      });
      markers.value.push(marker);
    });
  } catch (error) {
    console.error("Error updating markers:", error);
  }
};

// Handle place selection from autocomplete or search
const handlePlaceSelection = async (place) => { // place is PlaceResult or GeocoderResult
  isSearching.value = true;
  if (!place.geometry || !place.geometry.location) {
    alert('Could not find the specified address details. Please try again.');
    isSearching.value = false;
    return;
  }

  const location = place.geometry.location;

  if (searchMarker.value) {
    searchMarker.value.setMap(null);
  }
  searchMarker.value = new googleInstance.maps.Marker({
    position: location,
    map: map.value,
    icon: {
      path: googleInstance.maps.SymbolPath.CIRCLE,
      scale: 8,
      fillColor: "#e75a97", // Pink for searched location
      fillOpacity: 1,
      strokeColor: "#ffffff",
      strokeWeight: 2,
    },
    animation: googleInstance.maps.Animation.DROP
  });

  map.value.setCenter(location);
  map.value.setZoom(14); // Zoom in a bit more
  
  findAndDisplayNearbyClinics(location);
};

// Calculate distance between two points using Haversine formula (No longer used for clinic sorting, but kept for now if needed elsewhere)
// const getDistance = (lat1, lon1, lat2, lon2) => { ... }; // Can be removed if not used

const findAndDisplayNearbyClinics = (location) => {
  if (!placesService || !map.value) {
    console.error('PlacesService or map not initialized.');
    alert('Map service is not ready. Please try searching again.');
    isSearching.value = false;
    return;
  }
  if (!location) {
    console.error('Location not provided for nearby search.');
    alert('A location is required to find nearby clinics.');
    isSearching.value = false;
    return;
  }

  // Store the current clinic details to maintain UI during loading
  const currentClinic = selectedClinic.value;
  
  isSearching.value = true;
  // Don't clear selectedClinic immediately to maintain UI
  // selectedClinic.value = null; // Clear previous selection - REMOVED
  
  // Clear existing clinic markers
  if (markers.value && markers.value.length > 0) {
    markers.value.forEach(marker => marker.setMap(null));
    markers.value = [];
  }
  // Store current clinics before clearing
  const previousClinics = [...displayedClinics.value];
  displayedClinics.value = [];

  const request = {
    location: location,
    radius: 5000, // 5km radius
    keyword: 'psychologist OR "mental health clinic" OR therapy',
    // type: ['health'] // Optional: can make search broader or narrower. Test with keyword first.
  };

  placesService.nearbySearch(request, (results, status) => {
    if (status === googleInstance.maps.places.PlacesServiceStatus.OK && results) {
      displayedClinics.value = results
        .filter(place => place.business_status === 'OPERATIONAL') // Filter for operational places
        .map(place => ({
        id: place.place_id,
        name: place.name,
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
        address: place.vicinity,
        website: place.website || null,
        rating: place.rating || 0,
        reviews: place.user_ratings_total || 0,
        openingHours: place.opening_hours ? { open_now: place.opening_hours.open_now } : null, // Basic info from nearby
        photos: place.photos || null,
        place_id: place.place_id,
      }));

      updateMarkers();

      if (displayedClinics.value.length > 0) {
        selectClinic(displayedClinics.value[0]); // Auto-select the first one
      } else {
        alert('No operational psychology clinics found nearby with the current filters.');
        // Restore previous clinic if no results found
        selectedClinic.value = currentClinic;
      }
    } else if (status === googleInstance.maps.places.PlacesServiceStatus.ZERO_RESULTS) {
      alert('No psychology clinics found nearby.');
      displayedClinics.value = previousClinics; // Restore previous clinics
      updateMarkers();
      selectedClinic.value = currentClinic; // Restore previous selection
    } else {
      alert('Nearby search failed. Status: ' + status);
      console.error('PlacesService.nearbySearch failed with status:', status);
      displayedClinics.value = previousClinics; // Restore previous clinics
      selectedClinic.value = currentClinic; // Restore previous selection
    }
    isSearching.value = false;
  });
};

const selectClinic = (clinic) => {
  if (!clinic) return;
  selectedClinic.value = clinic; // Show basic info immediately
  if (map.value && clinic.lat && clinic.lng) {
    map.value.panTo({ lat: clinic.lat, lng: clinic.lng });
  }

  if (clinic.place_id) {
    fetchClinicDetails(clinic.place_id);
  }
};

const fetchClinicDetails = (placeId) => {
  if (!placesService || !placeId) return;
  isSearching.value = true; // Indicate loading details

  const request = {
    placeId: placeId,
    fields: ['name', 'vicinity', 'formatted_address', 'geometry', 'website', 
             'formatted_phone_number', 'rating', 'user_ratings_total', 
             'opening_hours', 'photos', 'url', 'business_status', 'place_id']
  };

  placesService.getDetails(request, (place, status) => {
    isSearching.value = false;
    if (status === googleInstance.maps.places.PlacesServiceStatus.OK && place) {
      selectedClinic.value = {
        // Spread existing data from nearbySearch first, then override with details
        ...displayedClinics.value.find(c => c.place_id === placeId),
        id: place.place_id,
        name: place.name,
        address: place.formatted_address || place.vicinity,
        lat: place.geometry.location.lat(),
        lng: place.geometry.location.lng(),
        website: place.website || null,
        phone: place.formatted_phone_number || null,
        rating: place.rating || 0,
        reviews: place.user_ratings_total || 0,
        openingHours: place.opening_hours ? {
            weekday_text: place.opening_hours.weekday_text || ["Opening hours not available"],
            open_now: typeof place.opening_hours.isOpen === 'function' ? place.opening_hours.isOpen() : undefined
        } : { weekday_text: ["Opening hours not available"] },
        photos: place.photos || null,
        googleMapsUrl: place.url,
        business_status: place.business_status,
        place_id: place.place_id
      };
    } else {
      console.error('PlacesService.getDetails failed for ' + placeId + '. Status:', status);
      // Optionally, keep the basic info if details fetch fails but clinic was already partially loaded
      if (!selectedClinic.value || selectedClinic.value.place_id !== placeId) {
        // If this is a new selection that failed, clear it or show error
         selectedClinic.value = { ...selectedClinic.value, openingHours: { weekday_text: ["Could not load details."] } };
      }
    }
  });
};


onMounted(() => {
  renderChart()
  
  const handleResize = () => {
    if (window.innerWidth > 768 && !filtersVisible.value) {
      filtersVisible.value = true
    }
  }
  
  window.addEventListener('resize', handleResize)
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    // Potential cleanup for map listeners if any are added directly to googleInstance.maps.event
    if (map.value && googleInstance) {
        // googleInstance.maps.event.clearInstanceListeners(map.value); // Example, be careful
    }
  })
  
  if (activeTab.value === 'offline') {
    nextTick(initMap)
  }
})

// Get user position
const getMyPosition = () => {
  if (navigator.geolocation) {
    // Store the current selected clinic before starting the loading process
    const previousClinic = selectedClinic.value;
    
    isSearching.value = true;
    navigator.geolocation.getCurrentPosition(
      position => {
        userLocation.value = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        }
        mapCenter.value = userLocation.value
        
        if (map.value && googleInstance) {
          map.value.setCenter(userLocation.value)
          map.value.setZoom(14)
          
          if (userMarker.value) {
            userMarker.value.setMap(null)
          }
          
          userMarker.value = new googleInstance.maps.Marker({
            position: userLocation.value,
            map: map.value,
            icon: { // Blue for user location
              path: googleInstance.maps.SymbolPath.CIRCLE,
              scale: 10,
              fillColor: "#4285F4",
              fillOpacity: 1,
              strokeColor: "#FFFFFF",
              strokeWeight: 2
            },
            animation: googleInstance.maps.Animation.DROP,
            title: "Your Location"
          })
          
          findAndDisplayNearbyClinics(userLocation.value);
        } else {
          isSearching.value = false; // Map not ready
          // Restore previous clinic if map is not ready
          selectedClinic.value = previousClinic;
        }
      },
      error => {
        isSearching.value = false;
        console.error('Error getting location:', error)
        alert('Unable to obtain your location. Please check your location permissions settings.')
        // Restore previous clinic on error
        selectedClinic.value = previousClinic;
      }
    )
  } else {
    isSearching.value = false;
    alert('Your browser does not support geolocation.')
  }
}

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
        scales: {
          x: {
            stacked: true,
            title: { display: true, text: 'Daily Screen Time (hours)' }
          },
          y: {
            stacked: true,
            max: 100,
            title: { display: true, text: 'Percentage of Emotional States (%)' }
          }
        }
      }
    })
  }
  else if (currentTab.value === 1) {
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
      options: {
        responsive: true,
        plugins: { title: { display: false } },
        scales: {
          x: {
            title: { display: true, text: 'Daily Screen Time (hours)' }
          },
          y: {
            title: { display: true, text: 'Sleep Problem Score (1 = Best, 5 = Worst)' },
            suggestedMin: 1,
            suggestedMax: 5
          }
        }
      }
    });
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
      options: {
        responsive: true,
        plugins: { title: { display: false } },
        scales: {
          x: {
            title: { display: true, text: 'Daily Usage Time (hours)' }
          },
          y: {
            title: { display: true, text: 'Engagement Score' }
          }
        }
      }
    });
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
      options: {
        responsive: true,
        plugins: { title: { display: false } },
        scales: {
          x: {
            title: { display: true, text: 'Daily Usage Time (hours)' }
          },
          y: {
            title: { display: true, text: 'Average Anxiety Level (1-5)' }
          }
        }
      }
    });
  }
}

// Event modal functions
const openModal = () => {
  isModalVisible.value = true
}

const closeModal = () => {
  isModalVisible.value = false
}

// Reset filters
const resetFilters = () => {
  searchQuery.value = ''
  selectedLocation.value = 'All locations'
  selectedCategory.value = 'All types'
  selectedMonth.value = 'Any time'
  selectedPrice.value = 'Any price'
  sortOption.value = 'dateAsc'
}

// Function to switch resource tab
const switchResourceTab = async (tabName) => {
  activeTab.value = tabName;
  
  // When switching to offline tab
  if (tabName === 'offline') {
    // Set first clinic as default if selectedClinic is null
    if (!selectedClinic.value && displayedClinics.value.length > 0) {
      selectedClinic.value = displayedClinics.value[0];
    }
    
    // Wait for DOM update
    await nextTick();
    
    // Force reinitialize map
    await initMap();
  }
};

const handleCancel = () => {
  showOnlineConfirm.value = false;
  // User chose to stay, so make sure online tab is visually active if it wasn't
  if (activeTab.value !== 'online') {
    activeTab.value = 'online';
    selectedClinic.value = null; // Clear clinic details if switching to online
  }
};

// Function to get directions to selected clinic
const getDirections = () => {
  if (!selectedClinic.value) return;
  
  // Construct Google Maps directions URL
  const destination = encodeURIComponent(selectedClinic.value.address);
  const origin = userLocation.value 
    ? `${userLocation.value.lat},${userLocation.value.lng}`
    : '';
  
  // Open Google Maps in a new tab
  const url = `https://www.google.com/maps/dir/${origin}/${destination}`;
  window.open(url, '_blank');
};

const onOnlineTabClick = () => {
  showOnlineConfirm.value = true;
};

const handleConfirm = () => {
  showOnlineConfirm.value = false;
  router.push('/relaxation'); // Navigate to relaxation page
};

const events = [
  {
    id: 1,
    title: 'Mentally Healthy Workplaces Workshop',
    tags: ['Sold out', 'May', 'Workshop', 'Free Event'],
    description: 'This workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.',
    location: 'Brisbane',
    address: 'Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000',
    date: '1st May 2025',
    time: '8:00 AM - 12:00 PM',
    link: 'https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch',
    image: 'mentalHealthWorkshop.avif',
    price: 'Free'
  },
  {
    id: 2,
    title: 'Mentally Healthy Workplaces Workshop',
    tags: ['Nearly full', 'June', 'Workshop', 'Free Event'],
    description: 'This workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.',
    location: 'Brisbane',
    address: 'Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000',
    date: 'June 4th 2025',
    time: '8:00 AM - 12:00 PM',
    link: 'https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch',
    image: 'mentalHealthWorkshop.avif',
    price: 'Free'
  },
  {
    id: 3,
    title: 'Workplace Wellbeing: How to Build Confidence and Manage Stress',
    tags: ['October', 'Workplace Wellbeing', 'Paid'],
    description: "You'll learn about both positive and negative factors at play in workplace.",
    location: 'Sydney',
    address: '20 Bond Street, Sydney NSW 2000',
    date: 'October 11st 2025',
    time: '7:30 AM - 11:30 AM',
    link: 'https://www.eventbrite.com.au/e/workplace-wellbeing-how-to-build-confidence-and-manage-stress-tickets-886375582227?aff=ebdssbdestsearch',
    image: 'workplace.avif',
    price: 'Paid'
  },
  {
    id: 4,
    title: 'Resilience, Self-Leadership & Wellbeing - Warrnambool Business Workshop',
    tags: ['May', 'Workplace Wellbeing Workshop', '$20'],
    description: 'Explore Victoria\'s beautiful national parks with our guided bushwalking groups. Connect with nature and like-minded creators.',
    location: 'Warrnambool',
    address: '185 Timor Street Warrnambool, VIC 3280',
    date: 'May 28th',
    time: '1:00 PM - 3:00 PM',
    link: 'https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch',
    image: 'workplaceWarrnambool.avif', 
    price: 'Paid'
  },
  {
    id: 5,
    title: 'Strategies for Mental Health at Work and Keeping Psychologically Safe',
    tags: ['October', 'Workplace Wellbeing Workshop', '$108.9'],
    description: 'HR professionals, managers, and business leaders, here\'s practical strategies to foster wellbeing and mental health in your workplace.',
    location: 'Geelong',
    address: '60 Moorabool Street Geelong, VIC 3220',
    date: 'October 9th 2025',
    time: '9:30 AM - 11:30 AM',
    link: 'https://www.eventbrite.com.au/e/strategies-for-mental-health-at-work-and-keeping-psychologically-safe-tickets-1235190400739?aff=ebdssbdestsearch',
    image: 'workplaceGeelong.avif',
    price: 'Paid'
  },
  {
    id: 6,
    title: 'MeTreat Retreats Women\'s Wellness Walk',
    tags: ['April', 'Outdoor Walking', 'Sales Ended'],
    description: 'CONNECT, REVIVE & THRIVE AT OUR METREAT WELLNESS WALK!',
    location: 'Torquay Beach',
    address: 'Torquay Beach Torquay, VIC 3228',
    date: 'April 25th',
    time: '11:00 AM - 2:00 AM',
    link: 'https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch',
    image: 'TorquayWalking.avif',
    price: 'Paid'
  },
  {
    id: 7,
    title: 'Flinders - Cairns Bay - 7KM\'S',
    tags: ['April', 'Outdoor Walking', 'Sales Ended'],
    description: 'We haven\'t done this hike for at least 6 months, and we are thrilled to share it with you all. This hike offers breathtaking views across Bass Strait from the dramatic black basalt cliffs, which are impressively high! Our plan is to visit Cairns Bay and then head to Flinders Blowhole and back.',
    location: 'Flinders Blowhole',
    address: 'Flinders VIC 3929, Australia',
    date: 'April 27th 2025',
    time: '9:00 AM - 11:30 AM',
    link: 'https://events.humanitix.com/flinders-cairns-bay-7km-s',
    image: 'flindersWalking.webp',
    price: 'Free'
  },
  {
    id: 8,
    title: 'Brisbane Wellbeing Day Festival',
    tags: ['October', 'Brisbane Festival', 'Free Event'],
    description: 'Let\'s Nourish, Nurture and Rejuvenate our wellbeing at the biggest non-profit community festival.',
    location: 'West End',
    address: 'Opposite 33 Hill End Terrace, West End, 4101, Queensland, Australia',
    date: 'October 17th 2025',
    time: '3:00 PM - 7:00 PM',
    link: 'https://www.5waystowellbeing.org.au/connect/brisbane-wellbeing-day-festival/',
    image: 'BrisbaneFestival.jpeg',
    price: 'Free'
  },
  {
    id: 9,
    title: 'Wiggle & Mingle: Dog-Friendly Hike & Yoga at You Yangs',
    tags: ['May', 'Outdoor Walking', 'Free Event'],
    description: 'Wiggle & Mingle: Join the Pack at You Yangs! G\'day dog lovers! Ready for an adventure that\'ll have tails wagging? Join us for Wiggle & Mingle - a community event where you and your four-legged mate can stretch your legs, meet new friends, and reconnect with nature in the stunning You Yangs.',
    location: 'Little River',
    address: 'You Yangs Regional Park, Toynes Rd, Little River VIC 3211, Australia',
    date: 'May 3rd 2025',
    time: '9:00 AM - 12:30 PM',
    link: 'https://events.humanitix.com/wiggle-and-mingle-yqu8fv8l',
    image: 'wiggleHike.webp',
    price: 'Free'
  },
  {
    id: 10,
    title: 'Wayapa Wuurrk Mindfulness & Weaving Workshop',
    tags: ['June', 'physical wellness practice', 'Sold out'],
    description: 'Join Jodie Dowd, Noongar weaver for a morning of Wayapa Wuurrk First Nations mindfulness practices. During this free and all-inclusive workshop (ages 15+) you will: Be gently guided through the 14 elements of the internationally accredited Wayapa Wuurrk (\'Connect to the earth\') physical wellness practice.',
    location: 'Narrabeen',
    address: '1395A Pittwater Rd, Narrabeen NSW 2101, Australia',
    date: 'June 21st 2025',
    time: '10:30 AM - 12:30 PM',
    link: 'https://events.humanitix.com/wayapa-wuurrk-mindfulness-and-weaving-workshop',
    image: 'wayapaWorkshop.webp',
    price: 'Free'
  }
]

// Function to get image URL for events
const getImageUrl = (filename) => {
  return new URL(`../assets/icons/activitiesImages/${filename}`, import.meta.url).href
}

// Computed property for filtering and sorting events
const sortedFilteredEvents = computed(() => {
  // First filter events based on search terms and filters
  let filteredEvents = events.filter(event => {
    // Search by title
    if (searchQuery.value && !event.title.toLowerCase().includes(searchQuery.value.toLowerCase())) {
      return false
    }
    
    // Filter by location
    if (selectedLocation.value !== 'All locations' && event.location !== selectedLocation.value) {
      return false
    }
    
    // Filter by category
    if (selectedCategory.value !== 'All types' && 
        !event.tags.some(tag => tag.toLowerCase().includes(selectedCategory.value.toLowerCase()))) {
      return false
    }
    
    // Filter by month
    if (selectedMonth.value !== 'Any time' && 
        !event.tags.some(tag => tag.toLowerCase() === selectedMonth.value.toLowerCase())) {
      return false
    }
    
    // Filter by price
    if (selectedPrice.value === 'Free' && event.price !== 'Free') {
      return false
    }
    
    if (selectedPrice.value === 'Paid' && event.price === 'Free') {
      return false
    }
    
    return true
  })
  
  // Then sort according to the selected sort option
  return filteredEvents.sort((a, b) => {
    switch (sortOption.value) {
      case 'dateAsc':
        return a.date.localeCompare(b.date)
      case 'dateDesc':
        return b.date.localeCompare(a.date)
      case 'name':
        return a.title.localeCompare(b.title)
      case 'location':
        return a.location.localeCompare(b.location)
      default:
        return 0
    }
  })
})

const featuredActivities = computed(() => {
  // Display a mix of activities (one from each month for variety)
  const april = events.find(event => event.tags.some(tag => tag === 'April'))
  const may = events.find(event => event.tags.some(tag => tag === 'May'))
  const june = events.find(event => event.tags.some(tag => tag === 'June' || tag === 'October'))
  
  // Return three featured events (ensure we have 3 even if fewer months are available)
  return [april, may, june].filter(Boolean).slice(0, 3)
})

const tabs = [
  { 
    name: 'Screen Time and Emotional Wellbeing', 
    insights: [
      'Increased screen time is associated with more negative emotions such as anxiety and sadness.',
      'Maintaining lower daily screen time correlates with better emotional wellbeing.',
      'Balanced digital habits foster more positive and neutral emotional states.'
    ]
  },
  {
    name: 'Digital Habits and Sleep Health', 
    insights: [
      'More than 3 hours of daily social media use is linked with sleep disturbances.',
      'Sleep issues worsen significantly when daily usage exceeds 4 hours.',
      'Reducing evening screen time can improve sleep quality and mental health.'
    ]
  },
  {
    name: 'Engagement Metrics and Emotional Rewards', 
    insights: [
      'Moderate posting and interaction (likes, comments) are positively linked with emotional wellbeing.',
      'Creators focusing on meaningful community engagement over numbers show better mental health.',
      'Prioritising genuine conversations over chasing virality strengthens long-term creator satisfaction.'
    ]
  },
  {
    name: 'Managing Digital Distractions and Anxiety', 
    insights: [
      'Higher daily screen time is associated with elevated anxiety levels.',
      'Spending less time on digital activities correlates with lower anxiety scores.',
      'Practising regular tech-free breaks can significantly lower digital stress levels.'
    ]
  }
]

// Update the search button to show loading state
const searchBtnContent = computed(() => {
  if (isSearching.value) {
    return `<svg class="loading-spinner" width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12" stroke="white" stroke-width="2"/>
    </svg>`
  }
  return `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M15.5 14H14.71L14.43 13.73C15.41 12.59 16 11.11 16 9.5C16 5.91 13.09 3 9.5 3C5.91 3 3 5.91 3 9.5C3 13.09 5.91 16 9.5 16C11.11 16 12.59 15.41 13.73 14.43L14 14.71V15.5L19 20.49L20.49 19L15.5 14ZM9.5 14C7.01 14 5 11.99 5 9.5C5 7.01 7.01 5 9.5 5C11.99 5 14 7.01 14 9.5C14 11.99 11.99 14 9.5 14Z" fill="white"/>
  </svg>`
})

// Function to switch to online resources
const switchToOnline = () => {
  activeTab.value = 'online'
}

const submitFeedback = async () => {
  if (rating.value === 0) {
    alert('Please provide a rating before submitting.')
    return
  }

  submitted.value = true

  try {
    await axios.post('http://localhost:8001/api/activities/submit-rating', {
      activity: currentActivity.value,
      rating: rating.value,
      timestamp: new Date().toISOString()
    })
    
    // Increment the total ratings count after successful submission
    totalRatings.value++
    
    console.log('Feedback submitted successfully')
    
    // Close modal after a short delay to show the thank you message
    setTimeout(() => {
      closeModal()
    }, 1500)
  } catch (err) {
    console.error('Failed to submit feedback:', err)
    // Revert submitted state if submission failed
    submitted.value = false
    alert('Failed to submit rating. Please try again.')
  }
}

// Function to scroll to a specific section on the page
const scrollToSection = (sectionId) => {
  // For Wellbeing Activities Hub, use the ID instead of class
  let selector = `.${sectionId}`;
  if (sectionId === 'activities-section') {
    selector = '#wellbeing-activities';
  }
  
  const section = document.querySelector(selector);
  if (section) {
    // Get the navbar height to use as an offset
    const navbarHeight = 100; // Increased to give more space below the navbar
    
    // Calculate the position to scroll to
    const offsetPosition = section.getBoundingClientRect().top + window.pageYOffset - navbarHeight;
    
    // Scroll to the section with the offset
    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    });
    
    // Close the island after navigation
    if (scrollIslandRef.value) {
      scrollIslandRef.value.closeIsland();
    }
  }
};

// Reference to the ScrollIsland component
const scrollIslandRef = ref(null);

// Add toggle filters function
const toggleFilters = () => {
  filtersVisible.value = !filtersVisible.value
}

const onSearch = () => {
  if (!searchAddress.value.trim()) {
    alert('Please enter an address or location to search.');
    return;
  }
  if (!googleInstance || !placesService) { // Check for placesService too
    alert('Map services are not yet loaded. Please wait a moment and try again.');
    isSearching.value = false;
    return;
  }

  isSearching.value = true;
  const geocoder = new googleInstance.maps.Geocoder();
  geocoder.geocode(
    { address: searchAddress.value, componentRestrictions: { country: 'AU' } },
    (results, status) => {
      if (status === googleInstance.maps.GeocoderStatus.OK && results && results[0]) {
        // Update searchAddress input with the geocoded result for consistency
        searchAddress.value = results[0].formatted_address;
        handlePlaceSelection(results[0]); // This will trigger findAndDisplayNearbyClinics
      } else {
        isSearching.value = false;
        alert('Address not found or geocoding failed. Please try a different address or use autocomplete. Status: ' + status);
      }
    }
  );
};

// Generate stars based on rating
const generateStars = (rating) => {
  if (!rating) return 'No Rating';
  
  // Round to nearest 0.5
  const roundedRating = Math.round(rating * 2) / 2;
  
  // Create stars string
  let starsHTML = '';
  
  // Full stars
  for (let i = 1; i <= 5; i++) {
    if (i <= roundedRating) {
      // Full star
      starsHTML += '<span class="star filled">★</span>';
    } else if (i - 0.5 === roundedRating) {
      // Half star
      starsHTML += '<span class="star half">★</span>';
    } else {
      // Empty star
      starsHTML += '<span class="star empty">☆</span>';
    }
  }
  
  return starsHTML;
};

</script>

<style scoped>
/* Modal z-index overrides to fix layering issues */
:deep(.modal-overlay) {
  z-index: 9999 !important;
}

/* Filter styles */
.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}


.filter-toggle {
  background: #f8f8f8;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  padding: 0.4rem 1rem;
  font-size: 0.9rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
}


.toggle-icon {
  font-size: 0.8rem;
  margin-left: 0.5rem;
}

.event-filters {
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.3s ease, margin 0.3s ease;
  max-height: 800px;
  opacity: 1;
  margin-bottom: 2.5rem;
}


@media (min-width: 769px) {
  
  
}

@media (max-width: 768px) {
}

.preparation-guide-wrapper {
  position: relative;
  z-index: 10000; /* Ensure this is the highest z-index in the application */
}

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


.tab {
  padding: 0.5rem 1.5rem;
  cursor: pointer;
  color: white;
  position: relative;
  background-color: #e75a97;
  border-radius: 20px;
  font-weight: 500;
  margin: 0 0.5rem;
  transition: all 0.3s ease;
  white-space: normal; /* Allow text to wrap */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  text-align: center;
}



/* Responsive adjustments for tabs */
@media (max-width: 768px) {
  
}

@media (max-width: 480px) {
  
}

/* Make resource tabs responsive as well */
@media (max-width: 768px) {
  .resource-tabs {
    gap: 1rem;
    flex-wrap: wrap;
  }
  
  .resource-tab {
    flex: 1;
    min-width: 140px;
    text-align: center;
  }
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
  width: 100%;
  position: relative;
}

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
    #65c9a4 20%,
    #7e78d2 40%,
    #7e78d2 60%,
    #65c9a4 80%
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
  white-space: nowrap;
  text-align: left;
  padding: 0 0 0.2em; /* Add bottom padding */
  transform: translateY(-0.05em); /* Slightly move text up to ensure background covers all letters */
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(101, 201, 164, 0.5));
  transform: none;
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
  white-space: normal; /* Default allow wrapping */
  text-align: left;
  max-width: 100%;
}

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
    white-space: nowrap; /* No wrapping on wide screens */
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
    white-space: nowrap; /* No wrapping on wide screens */
  }
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
  grid-template-columns: repeat(2, 160px);
  gap: 0.5rem;
  align-items: start;
  margin: 0;
  padding: 0;
  grid-column: 5 / 7;
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

/* Enhanced hover effect */
.top-row .element:hover {
  transform: rotate(-15deg) scale(1.1);
}

/* Responsive adjustments */
@media (max-width: 1800px) {
  .decorative-elements {
    width: 840px;
    grid-template-columns: repeat(6, 140px);
    opacity: 0.9;
    transform: translateX(0);
    justify-content: end;
  }
}

@media (max-width: 1536px) {
  .decorative-elements {
    width: 720px;
    grid-template-columns: repeat(6, 120px);
    opacity: 0.8;
    transform: translateX(0);
    justify-content: end;
  }
}

@media (max-width: 1280px) {
  .decorative-elements {
    width: 600px;
    grid-template-columns: repeat(6, 100px);
    opacity: 0.7;
    transform: translateX(0);
    row-gap: 0.75rem;
  }

  .title-group h2 {
    white-space: normal;
  }
  
  .subtitle {
    white-space: normal; /* For medium screens, allow wrapping */
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
    justify-content: end;
  }
  
  .title-group h1 {
    @apply text-5xl;
  }
  
  .title-group h2 {
    @apply text-4xl;
  }
  
  .subtitle {
    @apply text-xl;
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
  
  .decorative-elements {
    opacity: 0.1;
    transform: translateX(0) scale(0.8);
  }
  
  .title-group h1 {
    @apply text-4xl;
  }
  
  .title-group h2 {
    @apply text-3xl;
  }
  
  .subtitle {
    @apply text-lg;
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

  .decorative-elements {
    opacity: 0;
    transform: translateX(0) scale(0.7);
  }

  .title-group h1 {
    @apply text-3xl;
  }
  
  .title-group h2 {
    @apply text-2xl;
  }
  
  .subtitle {
    @apply text-base;
  }
}

@media (max-width: 480px) {
  .hero-section {
    min-height: 16vh;
    padding: 8rem 0 0.5rem;
  }
  
  .hero-content {
    min-height: 16vh;
  }
  
  .decorative-elements {
    opacity: 0;
    display: none;
  }
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
  white-space: normal;
}

section {
  padding: 3rem 0 5rem;
  position: relative;
  border-bottom: none;
  margin-bottom: 5rem;
}

section:last-child {
  margin-bottom: 3rem;
}

section:not(:last-child)::after {
  display: none;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 1;
}

/* Dashboard section */






@media (max-width: 768px) {
  
}

@media (max-width: 480px) {
  
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

/* Resource finder section */
.resource-finder-section {
  background-color: #fffcf5;
}

/* Apple TV-style Floating Tab Bar */
.resource-tabs {
  display: inline-flex;
  margin-bottom: 2.5rem;
  background-color: rgba(230, 230, 230, 0.8);
  border-radius: 50px;
  padding: 5px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

.resource-tab {
  flex: 1 1 auto;
  padding: 10px 25px;
  font-size: 1.05rem;
  font-weight: 500;
  color: #333;
  text-align: center;
  cursor: pointer;
  background-color: transparent;
  border: none;
  border-radius: 40px;
  transition: all 0.25s ease;
  outline: none;
  white-space: nowrap;
  margin: 0;
  position: relative;
  z-index: 2;
}

.resource-tab.active {
  background-color: #FCE4EC;
  color: #E91E63;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);
  transition: all 0.3s ease; /* Slightly longer transition for smoother effect */
}

/* Hover effect for inactive tabs */
.resource-tab:not(.active):hover {
  background-color: rgba(200, 200, 200, 0.4);
  color: #000;
}

/* Make sure to remove the below styles if they appear elsewhere in the file */
.resource-tab-online {
  /* No separate styling - we're using consistent styling for both tabs */
}

.resource-tab-online.active {
  /* No separate styling - active state should be handled by .resource-tab.active */
}

/* Responsive design for tabs */
@media (max-width: 768px) {
  .resource-tabs {
    max-width: 90%;
  }
  
  .resource-tab {
    padding: 8px 20px;
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .resource-tabs {
    width: 95%;
  }
  
  .resource-tab {
    padding: 8px 15px;
    font-size: 0.95rem;
  }
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
  min-height: 800px; /* Increased from 700px */
  height: 800px; /* Increased from 700px */
  padding: 0;
}

.resource-content.online-only {
  grid-template-columns: 1fr;
  padding: 0;
}

.online-resources-container {
  padding: 2rem;
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.online-resources-container.full-width {
  grid-column: 1 / -1;
  max-width: 800px;
  margin: 0 auto;
}

.map-container {
  position: relative;
  width: 100%;
  height: 100%; 
  border-radius: 16px;
  min-height: 800px; /* Increased from 700px */
}

#google-map {
  width: 100% !important;
  height: 100% !important;
  min-height: 800px; /* Increased from 700px */
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.08);
  position: absolute;
  top: 0;
  left: 0;
}

.resource-details {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 800px; /* Increased from 700px */
  background: #fff;
  overflow-y: auto; /* Kept for very large content */
}

.resource-info-content {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 1rem;
}

.resource-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
  justify-content: center;
  width: 100%;
}

.action-btn {
  flex: 1;
  min-width: 140px;
  max-width: 200px;
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
  height: 48px; /* Increased height */
  white-space: nowrap;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

/* Responsive adjustments for the increased height */
@media (max-width: 768px) {
  .map-container {
    min-height: 400px;
    border-radius: 16px 16px 0 0;
  }

  #google-map {
    min-height: 400px;
    border-radius: 16px 16px 0 0;
  }

  .resource-content {
    min-height: 1000px; /* Increased to account for stacked layout */
    height: auto; /* Allow auto height for stacked layout */
  }
  
  .resource-details {
    min-height: 600px;
  }
  
  .resource-actions {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .action-btn {
    flex: 1 1 auto;
    width: 100%;
  }
}

.resource-name {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: #333;
}

.rating {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.rating-score {
  font-size: 2rem;
  font-weight: 600;
  color: #333;
  line-height: 1;
}

.stars {
  color: #FFB800;
  font-size: 1.2rem;
  letter-spacing: -1px;
  line-height: 1;
  margin-top: 2px;
  display: flex;
  align-items: center;
}

.star {
  display: inline-block;
  margin-right: 1px;
}

.star.filled {
  color: #FFB800; /* Gold color for filled stars */
}

.star.half {
  position: relative;
  background: linear-gradient(90deg, #FFB800 50%, #D1D1D1 50%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}

/* Fallback for browsers that don't support background-clip */
@supports not (background-clip: text) {
  .star.half {
    color: #FFB800;
    position: relative;
    overflow: hidden;
  }
  
  .star.half::after {
    content: '☆';
    position: absolute;
    right: 0;
    top: 0;
    width: 50%;
    color: #D1D1D1;
  }
}

.star.empty {
  color: #D1D1D1; /* Light gray for empty stars */
}

.reviews {
  color: #666;
  font-size: 1.1rem;
  margin-left: 2px;
}

.resource-location {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.location-icon {
  width: 24px;
  height: 24px;
  opacity: 0.7;
}

.resource-phone {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.phone-icon {
  width: 24px;
  height: 24px;
  opacity: 0.7;
}

.resource-website {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  color: #333;
}

.website-icon {
  width: 24px;
  height: 24px;
  opacity: 0.7;
}

.resource-phone a {
  color: #e75a97;
  text-decoration: none;
  font-size: 1.1rem;
}

.resource-phone a:hover {
  text-decoration: underline;
}

.resource-website a {
  color: #e75a97;
  text-decoration: none;
  font-size: 1.1rem;
}

.resource-website a:hover {
  text-decoration: underline;
}

.info-section {
  background: #f8f8f8;
  padding: 1.2rem;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.opening-hours {
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
  background: #f8f8f8;
  padding: 1.5rem;
  border-radius: 12px;
}
.opening-hours h4 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #333;
  font-weight: 600;
}

.hours-grid {
  display: grid;
  gap: 0.75rem;
}

.hours-grid > div {
  display: flex;
  justify-content: space-between;
  padding-bottom: 0.5rem;
  border-bottom: 1px dashed #e0e0e0;
}

.hours-grid > div:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.day {
  color: #333;
  font-weight: 500;
}

.hours {
  color: #666;
  text-align: right;
}

.resource-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.action-btn {
  flex: 1;
  min-width: 140px;
  max-width: 200px;
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
  height: 44px;
  white-space: nowrap;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}


.btn-icon {
  opacity: 0.9;
}

/* 添加响应式布局 */
@media (max-width: 480px) {



  .position-btn {
    width: auto;
    min-width: 160px;
    height: 44px;
  }
}




/* 添加响应式布局 */
@media (max-width: 480px) {


  .position-btn {
    width: auto;
    min-width: 160px;
    height: 44px;
  }
}

/* Activities hub section */
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
  margin-top: 2rem;
}

.activity-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.activity-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.activity-img {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
}

.activity-card:hover .activity-img {
  transform: scale(1.02);
}

.activity-title {
  font-size: 1.5rem;
  font-weight: 600;
  padding: 1rem;
  padding-bottom: 0.5rem;
  padding-right: 1.5rem;
  color: #333;
  margin: 1rem;
  line-height: 1.3;
}

.activity-tags {
  padding: 0 1rem;
  margin-bottom: 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.activity-details {
  padding: 0 1rem 1rem;
  margin-top: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
}

/* 添加响应式布局 */
@media (max-width: 1024px) {
  .activities-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }

  .activity-title {
    font-size: 1.25rem;
  }
}

@media (max-width: 768px) {
  .activities-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .view-all-btn {
    width: 100%;
    text-align: center;
    padding: 0.75rem;
  }

  .activities-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .activity-card {
    max-width: 100%;
  }

  .activity-img {
    aspect-ratio: 16/10;
  }

  .activity-title {
    font-size: 1.25rem;
    margin: 0.75rem;
  }

  .activity-tags {
    padding: 0 0.75rem;
    margin-bottom: 0.75rem;
  }

  .activity-details {
    padding: 0 0.75rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
  }

  .section-subtitle {
    font-size: 1rem;
    margin-bottom: 2rem;
  }

  .recent-title {
    font-size: 1rem;
  }

  .activity-title {
    font-size: 1.1rem;
  }

  .activity-tags {
    gap: 0.25rem;
  }

  .tag {
    padding: 0.15rem 0.5rem;
    font-size: 0.7rem;
  }

  .activity-details {
    font-size: 0.9rem;
  }
}

/* Modal window styles */
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
  z-index: 1000; /* Keep this lower than modal-overlay's z-index */
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
  display: flex;
  flex-direction: column;
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
  border-radius: 16px 16px 0 0;
}

.modal-content {
  padding: 2rem;
  overflow-y: auto;
  flex: 1;
}

/* Event filters responsive improvements */
@media (max-width: 768px) {
  
  .filter-group, 
  .filter-actions {
    width: 100%;
  }
  
  .clear-filters-btn {
    width: 100%;
    margin-top: 0.5rem;
  }
  
  .activities-modal {
    width: 95%;
    max-height: 90vh;
  }
  
  .modal-content {
    padding: 1.5rem;
  }
  
  .modal-header {
    padding: 1.25rem 1.5rem;
  }
  
  .modal-header h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  
  .activities-modal {
    width: 98%;
    max-height: 92vh;
  }
  
  .modal-content {
    padding: 1rem;
  }
  
  .modal-header {
    padding: 1rem;
  }
  
  .modal-header h2 {
    font-size: 1.25rem;
  }
  
  .close-modal-btn {
    font-size: 1.75rem;
  }
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

/* Search bar styles */
.search-bar {
  position: absolute;
  top: 15px;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 60px);
  max-width: 500px;
  z-index: 10;
  background-color: #fff;
  border-radius: 30px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15), 0 0 0 2px rgba(255,255,255,0.7);
  height: 40px;
  display: flex;
  align-items: center;
  padding: 0 3px 0 10px; /* Reduced padding */
}

.search-input {
  flex-grow: 1;
  height: 100%;
  font-size: 0.9rem;
  border: none;
  outline: none;
  background-color: transparent;
  color: #333;
  padding: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0; /* Ensure text fits in container */
}

.search-input::placeholder {
  opacity: 0.75;
  color: #666;
  text-overflow: ellipsis;
}

.search-btn {
  width: 30px;
  height: 30px;
  min-width: 30px;
  background-color: #E91E63;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-left: auto;
}

/* Mobile adjustments */
@media (max-width: 480px) {
  .search-bar {
    width: calc(100% - 20px);
    top: 10px;
    height: 36px;
    padding: 0 2px 0 8px; /* Even smaller padding for mobile */
  }
  
  .search-input {
    font-size: 0.85rem;
  }
  
  .search-btn {
    width: 26px;
    height: 26px;
    min-width: 26px;
  }
}

.search-btn:hover:not(:disabled) {
  background-color: #d81b60; /* Slightly darker pink on hover */
  transform: scale(1.05);
}

.search-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.search-btn.is-loading {
  background-color: #e0e0e0;
  cursor: not-allowed;
}

.search-btn .loader {
  border: 2px solid #f3f3f3;
  border-top: 2px solid #E91E63;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  animation: spin 1s linear infinite;
  margin-right: 5px; /* If you want text next to loader */
}

/* Google Places Autocomplete customization */
:deep(.pac-container) {
  border-radius: 12px;
  margin-top: 8px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

:deep(.pac-item) {
  padding: 8px 12px;
  cursor: pointer;
}

:deep(.pac-item:hover) {
  background-color: #f5f5f5;
}

:deep(.pac-item-selected) {
  background-color: #f0f0f0;
}

/* Filter styles */

.filter-group {
  flex: 1;
  min-width: 180px;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-group label {
  display: block;
  color: #555;
  font-weight: 500;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
  letter-spacing: 0.02em;
}

.filter-group select {
  width: 100%;
  padding: 0.7rem 1rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  outline: none;
  transition: all 0.3s ease;
  background-color: white;
  color: #333;
  font-size: 0.95rem;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.7rem center;
  background-size: 1rem;
  cursor: pointer;
}

.filter-group select:hover {
  border-color: #d0d0d0;
  background-color: #fcfcfc;
}

.filter-group select:focus {
  border-color: #e75a97;
  box-shadow: 0 0 0 2px rgba(231, 90, 151, 0.1);
}

.filter-actions {
  display: flex;
  align-items: flex-end;
  margin-bottom: 0.5rem;
}

.clear-filters-btn {
  white-space: nowrap;
  background-color: white;
  color: #666;
  border: 1px solid #eaeaea;
  padding: 0.7rem 1.25rem;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  height: fit-content;
}

.clear-filters-btn:hover {
  background-color: #f5f5f5;
  border-color: #d0d0d0;
  transform: translateY(-1px);
}

.clear-filters-btn:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  
  .filter-group, 
  .filter-actions {
    width: 100%;
  }
  
  .clear-filters-btn {
    width: 100%;
    margin-top: 0.5rem;
  }
}

/* Event card styles */
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

.event-img-container {
  width: 280px;
  height: 220px;
  overflow: hidden;
}

.event-img {
  width: 100%;
  height: 100%;
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

/* Responsive adjustments */
@media (max-width: 768px) {
  .event-card {
    flex-direction: column;
  }

  .event-img {
    width: 100%;
    height: 200px;
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

/* Hide link tags */
.event-meta div.event-link {
  display: none;
}

/* Add styles for button links */
.register-btn-link {
  text-decoration: none;
  display: inline-block;
}

/* Activity card link styles */
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


.resource-btn:hover {
  background-color: #d4407f;
  transform: translateY(-2px);
}

/* Online resources styles */
.online-resources-container {
  padding: 2rem;
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.online-resources-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 100%;
  padding-bottom: 2rem;
}

.online-resource-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.online-resource-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.resource-logo {
  width: 160px;
  height: 160px;
  min-width: 160px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: 20px;
}

.resource-icon {
  width: 120px;
  height: 120px;
  object-fit: contain;
  display: block;
}

.resource-info {
  flex: 1;
  min-width: 0;
}

.resource-info h3 {
  margin: 0 0 6px;
  font-size: 1.25rem;
  color: #333;
  font-weight: 600;
}

.resource-info p {
  margin: 0 0 12px;
  color: #666;
  font-size: 1rem;
  line-height: 1.5;
}

.resource-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.tag {
  padding: 6px 12px;
  background: #F0F0F0;
  border-radius: 16px;
  font-size: 0.875rem;
  color: #666;
  font-weight: 500;
}

.resource-link-btn {
  display: inline-block;
  padding: 10px 24px;
  background: #e75a97;
  color: white;
  border-radius: 20px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.resource-link-btn:hover {
  background: #d4407f;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .online-resource-card {
    flex-direction: column;
    align-items: flex-start;
    padding: 16px;
  }
  
  .resource-logo {
    margin-right: 0;
    margin-bottom: 1rem;
    width: 120px;
    height: 120px;
    padding: 16px;
  }

  .resource-icon {
    width: 88px;
    height: 88px;
  }
}

/* Add general tag styles */
.tag {
  padding: 0.2rem 0.7rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #222222;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  display: inline-flex;
  align-items: center;
  transition: all 0.2s ease;
  margin-right: 0.5rem;
}

/* Remove dark tag styles */
.tag.may, 
.tag.june, 
.tag.workshop, 
.tag.mental-health, 
.tag.physical-wellness-practice, 
.tag.workplace-wellbeing, 
.tag.workplace-wellbeing-workshop {
  color: #222222;
}

/* Remove light tag styles */
.tag.april, 
.tag.free-event, 
.tag.october, 
.tag.sales-ended, 
.tag.nearly-full {
  color: #222222;
}

.tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.15);
}

/* Modify different tag colours */
.tag.sold-out {
  background-color: #ff5252;
}

.tag.nearly-full {
  background-color: #ff9800;
}

.tag.april {
  background-color: #8bc34a;
}

.tag.may {
  background-color: #2196F3;
}

.tag.june {
  background-color: #9C27B0;
}

.tag.october {
  background-color: #FF9800;
}

.tag.workshop {
  background-color: #795548;
}

.tag.free-event {
  background-color: #4CAF50;
}

.tag.paid {
  background-color: #F44336;
}

.tag.festival {
  background-color: #e91e63;
}

.tag.mental-health {
  background-color: #673ab7;
}

.tag.outdoor-wellness {
  background-color: #009688;
}

.tag.physical-wellness-practice {
  background-color: #3f51b5;
}

.tag.workplace-wellbeing, .tag.workplace-wellbeing-workshop {
  background-color: #607D8B;
}

.tag.sales-ended {
  background-color: #9E9E9E;
}

/* Modify activity tag container styles */
.activity-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
  padding: 0 1rem;
}

/* 添加确认对话框样式 */
.confirmation-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.confirmation-dialog {
  background-color: white;
  border-radius: 16px;
  padding: 2rem;
  width: 90%;
  max-width: 450px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.dialog-header h2 {
  color: #e75a97;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  text-align: center;
}

.dialog-content {
  margin: 1.5rem 0;
  color: #333;
  text-align: center;
}

.dialog-content p {
  margin: 0.8rem 0;
  line-height: 1.5;
  font-size: 1.1rem;
}

.dialog-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.cancel-btn, .confirm-btn {
  padding: 0.75rem 2rem;
  border-radius: 25px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1.1rem;
  min-width: 150px;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
}

.confirm-btn {
  background-color: #e75a97;
  color: white;
  border: none;
}

.cancel-btn:hover,
.confirm-btn:hover {
  transform: translateY(-2px);
}

.confirm-btn:hover {
  background-color: #d4407f;
}

.cancel-btn:hover {
  background-color: #ebebeb;
}

.resource-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #f8f0f4;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
}

.resource-img {
  width: 50px;
  height: 50px;
  object-fit: contain;
}

.position-btn {
  position: absolute;
  bottom: 32px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #e75a97;
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 25px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 5;
  height: 44px;
  white-space: nowrap;
  font-size: 0.95rem;
  line-height: 44px;
  transition: all 0.3s ease;
}

.position-btn:hover {
  background-color: #d4407f;
  transform: translateX(-50%) translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
}

.position-btn:active {
  transform: translateX(-50%) translateY(0);
}

.search-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.search-input:focus {
  outline: none;
  border-color: #e75a97;
  box-shadow: 0 0 0 3px rgba(231, 90, 151, 0.1);
}

.search-btn:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

.search-btn:not(:disabled):hover {
  background: #d4407f;
  transform: translateY(-1px);
}

.search-btn:not(:disabled):active {
  transform: translateY(0);
}

.loading-spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .resource-content {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .map-container {
    min-height: 400px;
    border-radius: 16px 16px 0 0;
  }

  #google-map {
    min-height: 400px;
    border-radius: 16px 16px 0 0;
  }

  .resource-details {
    border-radius: 0 0 16px 16px;
  }

  .resource-name {
    font-size: 1.5rem;
  }

  .rating-score {
    font-size: 1.5rem;
  }

  .resource-location, 
  .resource-website {
    font-size: 1rem;
  }

  .opening-hours {
    margin-top: 1rem;
    margin-bottom: 1rem;
    padding: 1rem;
  }

  .hours-grid {
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .resource-tabs {
    flex-direction: row; /* Keep as row for small screens */
    gap: 0.75rem;
    width: 100%;
    align-items: stretch;
  }

  .resource-tab {
    width: calc(50% - 0.375rem); /* Two tabs per row with gap */
    min-width: unset;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    border-radius: 2rem;
    white-space: normal; /* Allow wrapping in very small screens */
    flex: 1;
  }

  .search-bar {
    flex-direction: column;
    gap: 0.5rem;
  }

  .search-input {
    width: 100%;
  }

  .search-btn {
    width: 100%;
  }

  .map-container {
    min-height: 300px;
  }

  #google-map {
    min-height: 300px;
  }

  .resource-details {
    padding: 1rem;
  }

  .resource-name {
    font-size: 1.25rem;
  }

  .rating-score {
    font-size: 1.25rem;
  }

  .opening-hours h4 {
    font-size: 1rem;
  }

  .hours-grid {
    font-size: 0.9rem;
  }
}

/* Island Sections Styling */
.island-sections {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 4px;
  padding-bottom: 0;
}

.island-section {
  padding: 6px 4px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  cursor: pointer;
  background: none;
  position: relative;
  overflow: hidden;
}

.island-section::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.6);
  transform: scaleX(0);
  transform-origin: right;
  transition: transform 0.3s ease;
}

.island-section:hover::after {
  transform: scaleX(1);
  transform-origin: left;
}

.island-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.island-section:hover {
  transform: translateX(3px);
}

.island-section:active {
  transform: translateX(5px);
}

.island-section h4 {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
  text-align: center;
}

.island-section p {
  font-size: 0.8rem;
  margin: 0;
  opacity: 0.9;
}







@media (max-width: 768px) {
  
}

@media (max-width: 480px) {
  
}








@media (min-width: 769px) {
  
  
}

@media (max-width: 768px) {
}

.hours-grid .hours-line {
  padding: 0.25rem 0;
  font-size: 0.95rem;
  color: #555;
}

.hours-grid .open-status {
  margin-top: 0.5rem;
  font-weight: bold;
  font-size: 0.95rem;
}
.hours-grid .open-status.open {
  color: #4CAF50; /* Green */
}
.hours-grid .open-status.closed {
  color: #F44336; /* Red */
}



.search-bar {
  padding: 1rem;          /* Padding around the input and button - RETAINED */
  margin-bottom: 1.5rem;  /* Space below the search bar - RETAINED */
  position: relative;     /* For positioning the search button absolutely if needed - RETAINED */
}

.search-btn:disabled {
  background: #e0e0e0;
  cursor: not-allowed;
}

.search-btn:not(:disabled):hover {
  background: #d4407f;
  transform: translateY(-1px);
}

.search-btn:not(:disabled):active {
  transform: translateY(0);
}

.search-input::placeholder {
  color: #9e9e9e;
  font-size: 0.9rem;
  opacity: 0.8;
}

.search-input:focus::placeholder {
  opacity: 0.5;
}

/* Mobile-specific search bar */
@media (max-width: 480px) {
  .search-bar {
    width: calc(100% - 20px);
    top: 10px;
    height: 36px;
  }
  
  .search-input {
    font-size: 0.85rem;
    padding-left: 10px;
  }
  
  .search-btn {
    width: 26px;
    height: 26px;
    min-width: 26px;
    margin: 0 5px 0 0;
  }
  
  /* Reduce padding in the map container for mobile */
  .map-container {
    border-radius: 10px;
  }
  
  #google-map {
    border-radius: 10px;
  }
  
  /* Fix resource container padding for mobile */
  .resource-finder-section .container {
    padding: 0 0.5rem;
  }
  
  .resource-content {
    border-radius: 10px;
  }
  
  /* Fix button positioning at bottom */
  .position-btn {
    bottom: 15px;
  }
  
  /* Reduce padding in section titles */
  .section-title {
    margin-bottom: 0.3rem;
  }
  
  .section-subtitle {
    margin-bottom: 1.5rem;
  }
  
  /* Reduce tab margins */
  .resource-tabs {
    margin-bottom: 1.5rem;
  }
}

/* Resource finder section general adjustments */
.resource-finder-section .container {
  padding: 0 1rem;
  max-width: 1150px;
}

/* Resource finder section */
.resource-finder-section {
  padding-top: 2rem;
  padding-bottom: 3rem;
}

@media (max-width: 480px) {
  .resource-finder-section {
    padding-top: 1rem;
    padding-bottom: 2rem;
  }
}
</style>