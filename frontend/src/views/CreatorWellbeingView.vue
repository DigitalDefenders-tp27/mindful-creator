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
    
    <!-- Digital Impact Analysis Dashboard -->
    <section class="dashboard-section">
      <div class="container">
        <h1 class="section-title">Average working time</h1>
        
        <div class="tabs">
          <div class="tab active">Average working time</div>
          <div class="tab">Anxiety correlation</div>
          <div class="tab">...</div>
          <div class="tab">...</div>
        </div>
        
        <div class="dashboard-content">
          <div class="chart-container">
            <h3 class="chart-title">AVERAGE WORKING TIME FOR CONTENT CREATOR</h3>
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
    
    <!-- Wellbeing Resource Finder -->
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
    
    <!-- Wellbeing Activities Hub -->
    <section class="activities-section">
      <div class="container">
        <h1 class="section-title">Wellbeing Activities Hub</h1>
        <p class="section-subtitle">Release your stress by joining fun activities and making like-minded friends.</p>
        
        <div class="activities-header">
          <h3 class="recent-title">RECENT CAMPAIGNS...</h3>
          <button @click="openModal" class="view-all-btn">VIEW ALL EVENTS</button>
        </div>
        
        <div class="activities-grid">
          <a href="https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch" target="_blank" class="activity-card-link">
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
          
          <a href="https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch" target="_blank" class="activity-card-link">
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
          
          <a href="https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch" target="_blank" class="activity-card-link">
            <div class="activity-card">
              <img src="../assets/icons/activitiesImages/workplaceWarrnambool.avif" alt="Business Workshop" class="activity-img">
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
                <option>Brisbane</option>
                <option>Flinders Blowhole</option>
                <option>Geelong</option>
                <option>Little River</option>
                <option>Melbourne</option>
                <option>Narrabeen</option>
                <option>Sydney</option>
                <option>Torquay Beach</option>
                <option>Warrnambool</option>
                <option>West End</option>
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
                </div>
                <a :href="event.link" target="_blank" class="register-btn-link">
                  <button class="register-btn">Register Now</button>
                </a>
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
import { ref, computed } from 'vue';

// Modal window display status
const isModalVisible = ref(false);

// Open modal window
const openModal = () => {
  isModalVisible.value = true;
};

// Close modal window
const closeModal = () => {
  isModalVisible.value = false;
};

// Reset all filters to default values
const resetFilters = () => {
  searchQuery.value = '';
  selectedLocation.value = 'All locations';
  selectedCategory.value = 'All types';
  selectedMonth.value = 'Any time';
  selectedPrice.value = 'Any price';
  sortOption.value = 'dateAsc';
};

// Search and filter related
const searchQuery = ref('');
const selectedLocation = ref('All locations');
const selectedCategory = ref('All types');
const selectedMonth = ref('Any time');
const selectedPrice = ref('Any price');
const sortOption = ref('dateAsc');

// Function to resolve image paths correctly
const getImageUrl = (path) => {
  try {
    return new URL(path, import.meta.url).href;
  } catch (error) {
    // Fallback to original path if URL construction fails
    return path;
  }
};

// All event data
const allEvents = [
  {
    id: 1,
    title: "Mentally Healthy Workplaces Workshop",
    image: "../assets/icons/activitiesImages/mentalHealthWorkshop.avif",
    tags: ["Sold out", "May", "Workshop", "Free Event"],
    description: "This workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.",
    location: "Brisbane",
    address: "Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000",
    date: "1st May 2025",
    time: "8:00 AM - 12:00 PM",
    link: "https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch",
    category: "Mental Health",
    month: "May",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 4, 1)  // May 1st, 2025
  },
  {
    id: 2,
    title: "Mentally Healthy Workplaces Workshop",
    image: "../assets/icons/activitiesImages/mentalHealthWorkshop.avif",
    tags: ["Nearly full", "June", "Workshop", "Free Event"],
    description: "This workshop is designed to assist managers and supervisors create and sustain a mentally healthy and safe workplace.",
    location: "Brisbane",
    address: "Auditorium, Plaza Level, 111 George Street Brisbane City, QLD 4000",
    date: "June 4th 2025",
    time: "8:00 AM - 12:00 PM",
    link: "https://www.eventbrite.com.au/e/mentally-healthy-workplaces-workshop-tickets-1269860861019?aff=ebdssbdestsearch",
    category: "Mental Health",
    month: "June",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 5, 4)  // June 4th, 2025
  },
  {
    id: 3,
    title: "Workplace Wellbeing - How to Build Confidence and Manage Stress",
    image: "../assets/icons/activitiesImages/workplace.avif",
    tags: ["October", "Workplace Wellbeing Workshop", "$525.44"],
    description: "You'll learn about both positive and negative factors at play in workplace.",
    location: "Sydney",
    date: "October 11st 2025",
    time: "7:30 AM - 11:30 AM",
    link: "https://www.eventbrite.com.au/e/workplace-wellbeing-how-to-build-confidence-and-manage-stress-tickets-886375582227?aff=ebdssbdestsearch",
    category: "Workplace Wellbeing",
    month: "October",
    isPaid: true,
    priceTag: "$525.44",
    sortDate: new Date(2025, 9, 11)  // October 11th, 2025
  },
  {
    id: 4,
    title: "Resilience, Self-Leadership & Wellbeing - Warrnambool Business Workshop",
    image: "../assets/icons/activitiesImages/workplaceWarrnambool.avif",
    tags: ["May", "Workplace Wellbeing Workshop", "$20"],
    description: "Explore Victoria's beautiful national parks with our guided bushwalking groups. Connect with nature and like-minded creators.",
    location: "Warrnambool",
    address: "185 Timor Street Warrnambool, VIC 3280",
    date: "May 28th 2025",
    time: "1:00 PM - 3:00 PM",
    link: "https://www.eventbrite.com.au/e/resilience-self-leadership-wellbeing-warrnambool-business-workshop-tickets-1271353776369?aff=ebdssbdestsearch",
    category: "Workplace Wellbeing",
    month: "May",
    isPaid: true,
    priceTag: "$20",
    sortDate: new Date(2025, 4, 28)  // May 28th, 2025
  },
  {
    id: 5,
    title: "Strategies for Mental Health at Work and Keeping Psychologically Safe.",
    image: "../assets/icons/activitiesImages/workplaceGeelong.avif",
    tags: ["October", "Workplace Wellbeing Workshop", "$108.9"],
    description: "HR professionals, managers, and business leaders, here's practical strategies to foster wellbeing and mental health in your workplace.",
    location: "Geelong",
    address: "60 Moorabool Street Geelong, VIC 3220",
    date: "October 9th 2025",
    time: "9:30 AM - 11:30 AM",
    link: "https://www.eventbrite.com.au/e/strategies-for-mental-health-at-work-and-keeping-psychologically-safe-tickets-1235190400739?aff=ebdssbdestsearch",
    category: "Workplace Wellbeing",
    month: "October",
    isPaid: true,
    priceTag: "$108.9",
    sortDate: new Date(2025, 9, 9)  // October 9th, 2025
  },
  {
    id: 6,
    title: "MeTreat Retreats Women's Wellness Walk",
    image: "../assets/icons/activitiesImages/TorquayWalking.avif",
    tags: ["April", "Outdoor Walking", "Sales Ended"],
    description: "CONNECT, REVIVE & THRIVE AT OUR METREAT WELLNESS WALK!",
    location: "Torquay Beach",
    address: "Torquay Beach Torquay, VIC 3228",
    date: "April 25th 2025",
    time: "11:00 AM - 2:00 AM",
    link: "https://www.eventbrite.com.au/e/metreat-retreats-womens-wellness-walk-tickets-1309257667929?aff=ebdssbdestsearch",
    category: "Outdoor Wellness",
    month: "April",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 3, 25)  // April 25th, 2025
  },
  {
    id: 7,
    title: "Flinders - Cairns Bay - 7KM'S",
    image: "../assets/icons/activitiesImages/flindersWalking.webp",
    tags: ["April", "Outdoor Walking", "Sales Ended"],
    description: "We haven't done this hike for at least 6 months, and we are thrilled to share it with you all. This hike offers breathtaking views across Bass Strait from the dramatic black basalt cliffs, which are impressively high! Our plan is to visit Cairns Bay and then head to Flinders Blowhole and back. The track can be steep in places, so it requires good leg strength and the ability to handle a steep incline. Although the distance is shorter than usual, I guarantee you'll get a solid workout and absolutely love this hike! It will take approximately 2.5 hours to complete. This hike is rated intermediate and is not suitable for beginners. A moderate level of fitness and stamina is required. We maintain a steady pace but do stop occasionally for photos and snacks.",
    location: "Flinders Blowhole",
    address: "Flinders VIC 3929, Australia",
    date: "April 27th 2025",
    time: "9:00 AM - 11:30 AM",
    link: "https://events.humanitix.com/flinders-cairns-bay-7km-s?hxchl=mkt-sch&_gl=1*m8ing0*_gcl_au*NDM5ODA2NTk5LjE3NDU2NzM0OTA.*_ga*MTUwMjgyOTU5Mi4xNzQ1NjczNDkx*_ga_LHKW5FR9N6*MTc0NTY3MzQ5MC4xLjEuMTc0NTY3MzY5NC41MS4wLjA.",
    category: "Outdoor Wellness",
    month: "April",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 3, 27)  // April 27th, 2025
  },
  {
    id: 8,
    title: "Brisbane Wellbeing Day Festival",
    image: "../assets/icons/activitiesImages/BrisbaneFestival.jpeg",
    tags: ["October", "Brisbane Festival", "Sales Ended"],
    description: "Let's Nourish, Nurture and Rejuvenate our wellbeing at the biggest non-profit community festival.",
    location: "West End",
    address: "Opposite 33 Hill End Terrace, West End, 4101, Queensland, Australia",
    date: "October 17th, 2025",
    time: "3:00 PM - 7:00 PM",
    link: "https://www.5waystowellbeing.org.au/connect/brisbane-wellbeing-day-festival/",
    category: "Festival",
    month: "October",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 9, 17)  // October 17th, 2025
  },
  {
    id: 9,
    title: "Wiggle & Mingle: Dog-Friendly Hike & Yoga at You Yangs - Wet Dog Co Community Event",
    image: "../assets/icons/activitiesImages/wiggleHike.webp",
    tags: ["May", "Outdoor Walking", "Free Event"],
    description: "Wiggle & Mingle: Join the Pack at You Yangs! G'day dog lovers! Ready for an adventure that'll have tails wagging? Join us for Wiggle & Mingle - a community event where you and your four-legged mate can stretch your legs, meet new friends, and reconnect with nature in the stunning You Yangs.",
    location: "Little River",
    address: "You Yangs Regional Park, Toynes Rd, Little River VIC 3211, Australia",
    date: "May 3rd, 2025",
    time: "9:00 AM - 12:30 PM",
    link: "https://events.humanitix.com/wiggle-and-mingle-yqu8fv8l?hxchl=mkt-sch&_gl=1*a1o4ay*_gcl_au*NDM5ODA2NTk5LjE3NDU2NzM0OTA.*_ga*MTUwMjgyOTU5Mi4xNzQ1NjczNDkx*_ga_LHKW5FR9N6*MTc0NTY3MzQ5MC4xLjEuMTc0NTY3MzY0MS40MS4wLjA",
    category: "Outdoor Wellness",
    month: "May",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 4, 3)  // May 3rd, 2025
  },
  {
    id: 10,
    title: "Wayapa Wuurrk Mindfulness & Weaving Workshop",
    image: "../assets/icons/activitiesImages/wayapaWorkshop.webp",
    tags: ["June", "physical wellness practice", "Sold out"],
    description: "Join Jodie Dowd, Noongar weaver for a morning of Wayapa Wuurrk First Nations mindfulness practices. During this free and all-inclusive workshop (ages 15+) you will: Be gently guided through the 14 elements of the internationally accredited Wayapa Wuurrk ('Connect to the earth') physical wellness practice. Learn to weave a bracelet or small basket. Share your thoughts on the Wayapa practice during a Yarning Circle. Enjoy light refreshments.",
    location: "Narrabeen",
    address: "1395A Pittwater Rd, Narrabeen NSW 2101, Australia",
    date: "June 21st, 2025",
    time: "10:30 AM - 12:30 PM",
    link: "https://events.humanitix.com/wayapa-wuurrk-mindfulness-and-weaving-workshop?hxchl=mkt-sch&_gl=1*1dty875*_gcl_au*MTU4MDUxODg1My4xNzQxMDQzMDc4*_ga*MTE5MzU5MTc4Ni4xNzMzMjY1MDMw*_ga_LHKW5FR9N6*MTc0MzQ3NzY0Mi42NS4xLjE3NDM0NzgyMjYuNDEuMC4w",
    category: "physical wellness practice",
    month: "June",
    isPaid: false,
    priceTag: "Free",
    sortDate: new Date(2025, 5, 21)  // June 21st, 2025
  }
];

// Filter events based on selected and search conditions
const filteredEvents = computed(() => {
  return allEvents.filter(event => {
    // Check name search
    const matchesSearch = event.title.toLowerCase().includes(searchQuery.value.toLowerCase());
    
    // Check location filter
    const matchesLocation = selectedLocation.value === 'All locations' || 
                           event.location === selectedLocation.value;
    
    // Check category filter
    const matchesCategory = selectedCategory.value === 'All types' || 
                           event.category === selectedCategory.value;
    
    // Check month filter
    const matchesMonth = selectedMonth.value === 'Any time' || 
                        event.month === selectedMonth.value;
    
    // Check price filter
    const matchesPrice = selectedPrice.value === 'Any price' || 
                        (selectedPrice.value === 'Free' && !event.isPaid) || 
                        (selectedPrice.value === 'Paid' && event.isPaid);
    
    // All conditions must match
    return matchesSearch && matchesLocation && matchesCategory && matchesMonth && matchesPrice;
  });
});

// Sort filtered events
const sortedFilteredEvents = computed(() => {
  const events = [...filteredEvents.value];
  
  switch(sortOption.value) {
    case 'dateAsc':
      return events.sort((a, b) => a.sortDate - b.sortDate);
    case 'dateDesc':
      return events.sort((a, b) => b.sortDate - a.sortDate);
    case 'name':
      return events.sort((a, b) => a.title.localeCompare(b.title));
    case 'location':
      return events.sort((a, b) => a.location.localeCompare(b.location));
    default:
      return events;
  }
});
</script>

<style scoped>
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

/* Add responsive media queries */
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

/* Responsive layout support */
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

/* Common section styles */
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
  display: none;
}

/* Dashboard section */
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

/* Resource finder section */
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

/* Use this view-all-btn style definition */
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

/* Search bar styles */
.search-bar {
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.8rem 1.2rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  font-size: 1rem;
  outline: none;
  transition: all 0.3s ease;
  background-color: white;
}

.search-input:hover {
  border-color: #d0d0d0;
}

.search-input:focus {
  border-color: #e75a97;
  box-shadow: 0 0 0 2px rgba(231, 90, 151, 0.1);
}

/* Filter styles */
.event-filters {
  display: flex;
  gap: 1.25rem;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
  background-color: #fafafa;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

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
  .event-filters {
    flex-direction: column;
    padding: 1.25rem;
    gap: 1rem;
  }
  
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

/* Tag styles for additional categories */
.tag.physical-wellness-practice {
  background-color: #9C27B0;
}

.tag.festival {
  background-color: #3F51B5;
}

.tag.free-event {
  background-color: #4CAF50;
}

.tag.sold-out {
  background-color: #9E9E9E;
}

.tag.nearly-full {
  background-color: #FF9800;
}

.tag.sales-ended {
  background-color: #9E9E9E;
}

.tag.outdoor-walking {
  background-color: #6c63ff;
}

.tag.brisbane-festival {
  background-color: #673AB7;
}

.tag.workshop {
  background-color: #795548;
}

.tag.workplace-wellbeing-workshop {
  background-color: #607D8B;
}
</style>