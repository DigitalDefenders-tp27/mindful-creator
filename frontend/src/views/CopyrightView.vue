<template>
  <div class="copyright-view">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="slogan">
          <div class="title-group">
            <h1>Copyright</h1>
            <h2>Respect for Creators</h2>
          </div>
          <p class="subtitle">Understanding your rights and responsibilities as a creator</p>
        </div>
        <div class="decorative-elements">
          <!-- Top Row Right -->
          <div class="top-row">
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Flower_Orange.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Switch_Red.svg" alt="Flower" class="element hoverable">
            </div>
            <div class="element-wrapper">
              <img src="/src/assets/icons/elements/Wave_Narrow_Pink.svg" alt="Wave" class="element hoverable">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- License Information Cards Section -->
    <div class="license-cards-section">
      <h2 class="section-title">License Information Cards</h2>
      <p class="section-description">Hover to see copyright permissions instantly</p>
      
      <!-- Mobile Modal Overlay -->
      <div v-if="showLicenseModal" class="license-modal-overlay" @click="closeLicenseModal">
        <div class="license-modal-card">
          <div class="modal-icon">{{ activeLicenseCard.icon }}</div>
          <div class="modal-title">{{ activeLicenseCard.title }}</div>
          <div class="modal-subtitle">{{ activeLicenseCard.subtitle }}</div>
          <ul class="modal-details">
            <li v-for="(item, idx) in activeLicenseCard.details" :key="idx" :class="item.type">{{ item.text }}</li>
          </ul>
          <div class="modal-tap-to-close">Tap anywhere to close</div>
        </div>
      </div>

      <div class="license-grid">
        <!-- Use v-for for mobile, static for desktop/tablet -->
        <div v-for="(card, idx) in licenseCards" :key="idx"
          class="license-card"
          @click="openLicenseModal(card)"
          @touchstart="openLicenseModal(card)"
        >
          <div class="card-front">
            <div class="license-icon">{{ card.icon }}</div>
            <div class="license-title">{{ card.title }}</div>
            <div class="license-subtitle">{{ card.subtitle }}</div>
          </div>
          <!-- Hide card-back on mobile, show on desktop/tablet -->
          <div class="card-back">
            <ul class="license-details">
              <li v-for="(item, i) in card.details" :key="i" :class="item.type">{{ item.text }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Copyright Generator Section -->
    <div class="copyright-generator-section">
      <h2 class="section-title">Marking My Content as Mine</h2>
      <p class="section-description">Create custom copyright notices with fonts to protect your contents</p>
      
      <div class="generator-container">
        <div class="preview-section">
          <div class="image-watermark-disclaimer">
            <p><strong>Reminder:</strong> Only apply watermarks to your own original content. Using watermarks on images you don't own is not permissible.</p>
            <p><strong>Legal Notice:</strong> The watermark generator and license cards are designed strictly for legal use. Please ensure you comply with all applicable copyright laws and only use these tools for lawful purposes.</p>
          </div>
          <div class="image-preview">
            <div v-if="!uploadedImage" class="placeholder-upload" @click="triggerFileUpload">
              <div class="upload-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ff6b98" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7"></path>
                  <line x1="16" y1="5" x2="22" y2="5"></line>
                  <line x1="19" y1="2" x2="19" y2="8"></line>
                  <circle cx="9" cy="9" r="2"></circle>
                  <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
                </svg>
              </div>
              <span>Upload my photo</span>
            </div>
            <canvas v-else ref="previewCanvas" class="preview-canvas"></canvas>
            <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" style="display: none;">
          </div>
          <button v-if="uploadedImage" class="action-button secondary-button reset-image-preview-btn" @click="resetImage">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 2v6h6"></path><path d="M3 13a9 9 0 1 0 3-7.7L3 8"></path></svg>
            Reset Image
          </button>
          
          <div class="copyright-preview" :style="{ fontFamily: selectedFont }">
            {{ copyrightText }}
          </div>
          
          <!-- Status Messages -->
          <div v-if="statusMessage || errorMessage" class="status-messages">
            <div v-if="statusMessage" class="status-message" :class="{ 'success': isSuccess }">
              {{ statusMessage }}
            </div>
            <div v-if="errorMessage" class="error-message">
              {{ errorMessage }}
            </div>
          </div>
        </div>
        
        <div class="controls-section">
          <div class="control-step">
            <div class="step-number">1</div>
            <h3 class="step-title">Choose License Type</h3>
            <div class="license-options">
              <button 
                v-for="(license, index) in licenseOptions" 
                :key="index"
                class="license-option" 
                :class="{ active: selectedLicense === license.value }"
                @click="selectLicense(license.value)"
              >
                {{ license.label }}
              </button>
            </div>
          </div>
          
          <div class="control-step">
            <div class="step-number">2</div>
            <h3 class="step-title">Enter Your Information</h3>
            <div class="input-group">
              <label>Your Name on Social Media</label>
              <input type="text" v-model="creatorName" placeholder="Please enter your username...">
            </div>
            <div class="input-group">
              <label>Year</label>
              <input type="text" v-model="copyrightYear" placeholder="Default of 2025">
            </div>
          </div>
          
          <div class="control-step">
            <div class="step-number">3</div>
            <h3 class="step-title">Select Font Style</h3>
            <div class="font-selector">
              <div 
                v-for="(font, index) in fontOptions" 
                :key="index"
                class="font-option"
                :class="{ active: selectedFont === font.value }"
                :style="{ fontFamily: font.value }"
                @click="selectedFont = font.value"
              >
                {{ font.label }}
              </div>
            </div>
            <div class="color-selector">
              <label>Watermark Color</label>
              <div class="color-options">
                <div 
                  v-for="color in colorOptions" 
                  :key="color"
                  class="color-option"
                  :class="{ active: watermarkColor === color }"
                  :style="{ backgroundColor: color }"
                  @click="selectColor(color)"
                ></div>
                <input 
                  type="color" 
                  v-model="watermarkColor" 
                  class="color-picker"
                  @input="handleColorChange"
                >
              </div>
            </div>
          </div>
          
          <div class="control-step" v-if="uploadedImage">
            <div class="step-number">4</div>
            <h3 class="step-title">Customize Watermark</h3>
            <div class="slider-group">
              <label>Opacity: {{ (watermarkOpacity * 100).toFixed(0) }}%</label>
              <input 
                type="range" 
                v-model="watermarkOpacity" 
                min="0.1" 
                max="1" 
                step="0.1" 
                class="slider"
                @input="updateWatermark"
              >
            </div>
            <div class="slider-group">
              <label>Size: {{ watermarkSize }}px</label>
              <input 
                type="range" 
                v-model="watermarkSize" 
                min="12" 
                max="48" 
                step="2" 
                class="slider"
                @input="updateWatermark"
              >
            </div>
            <div class="slider-group">
              <label>Position</label>
              <div class="position-grid">
                <div 
                  v-for="pos in positions" 
                  :key="pos"
                  class="position-option"
                  :class="{ active: watermarkPosition === pos }"
                  @click="selectPosition(pos)"
                ></div>
              </div>
            </div>
          </div>
          
          <div class="generator-actions">
            <div class="action-buttons-group">
              <button 
                v-if="uploadedImage"
                class="action-button" 
                @click="downloadWatermarkedImage" 
                :disabled="isApplyingWatermark"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                {{ isApplyingWatermark ? 'Processing...' : 'Download with Watermark' }}
              </button>
              <button 
                class="action-button" 
                @click="downloadTransparentWatermark"
                :disabled="isCreatingSvg"
              >
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
                {{ isCreatingSvg ? 'Processing...' : 'Download Transparent Watermark' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container" style="max-width: 100%; padding: 0;">
      <!-- Interactive Content Carousel Section -->
      <div class="interactive-content-carousel">
        <div class="carousel-header-panel">
          <h2 class="carousel-main-title">Copyright Tips</h2>
        </div>

        <div class="carousel-container">
          <div class="carousel-wrapper" :style="{ transform: `translateX(-${currentSlideIndex * 100}%)` }">
            <div v-for="(slide, index) in slidesData" :key="index" class="carousel-slide">
              <div class="content-section">
                <h2>{{ slide.title }}</h2>
                <div v-html="slide.content"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="carousel-dots">
          <span
            v-for="(_slide, index) in slidesData"
            :key="`dot-${index}`"
            :class="{ active: index === currentSlideIndex }"
            @click="goToSlide(index)"
            class="dot"
            :aria-label="`Go to slide ${index + 1}`"
          ></span>
        </div>

        <!-- Arrows are now positioned absolutely relative to interactive-content-carousel -->
        <button @click="prevSlide" class="carousel-nav-button prev" aria-label="Previous slide">&lt;</button>
        <button @click="nextSlide" class="carousel-nav-button next" aria-label="Next slide">&gt;</button>
      </div>

      <!-- Disclaimer Section (now a direct child of the full-width container) -->
      <section class="content-section disclaimer">
        <h3>Disclaimer</h3>
        <p>This information is general in nature and should not be taken as legal advice. If you need specific guidance on copyright matters, consult a legal professional with expertise in intellectual property law.</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue';
import { applyWatermark, createSvgWatermark } from '../services/CopyrightService';

// License card data
const licenseOptions = [
  { label: '© All Rights Reserved', value: 'copyright' },
  { label: 'CC BY', value: 'cc-by' },
  { label: 'CC BY-NC', value: 'cc-by-nc' },
  { label: 'CC BY-SA', value: 'cc-by-sa' }
];

// License card modal data for mobile
const licenseCards = [
  {
    icon: '©️',
    title: 'CC BY',
    subtitle: 'Attribution',
    details: [
      { text: 'Commercial use allowed', type: 'allowed' },
      { text: 'Modification allowed', type: 'allowed' },
      { text: 'Free distribution', type: 'allowed' },
      { text: 'Must credit author', type: 'required' }
    ]
  },
  {
    icon: '🚫',
    title: 'CC BY-NC',
    subtitle: 'Non-Commercial',
    details: [
      { text: 'No commercial use', type: 'prohibited' },
      { text: 'Modification allowed', type: 'allowed' },
      { text: 'Educational sharing OK', type: 'allowed' },
      { text: 'Must credit author', type: 'required' }
    ]
  },
  {
    icon: '🔄',
    title: 'CC BY-SA',
    subtitle: 'ShareAlike',
    details: [
      { text: 'Commercial use allowed', type: 'allowed' },
      { text: 'Modification allowed', type: 'allowed' },
      { text: 'Derivatives use same license', type: 'required' },
      { text: 'Must credit author', type: 'required' }
    ]
  },
  {
    icon: '🌐',
    title: 'Public Domain',
    subtitle: 'No Copyright',
    details: [
      { text: 'Completely free to use', type: 'allowed' },
      { text: 'No attribution needed', type: 'allowed' },
      { text: 'Unlimited commercial use', type: 'allowed' },
      { text: 'Copyright expired works', type: 'info' }
    ]
  },
  {
    icon: '🔒',
    title: 'All Rights Reserved',
    subtitle: 'Full Copyright',
    details: [
      { text: 'No unauthorized use', type: 'prohibited' },
      { text: 'No modification or distribution', type: 'prohibited' },
      { text: 'Explicit permission required', type: 'required' },
      { text: 'Contact copyright holder', type: 'info' }
    ]
  },
  {
    icon: '⚖️',
    title: 'Fair Use',
    subtitle: 'Limited Use',
    details: [
      { text: 'Educational purposes', type: 'info' },
      { text: 'News reporting', type: 'info' },
      { text: 'Court evidence', type: 'info' },
      { text: 'Case-by-case determination', type: 'required' }
    ]
  }
];

const showLicenseModal = ref(false);
const activeLicenseCard = ref(null);

function openLicenseModal(card) {
  activeLicenseCard.value = card;
  showLicenseModal.value = true;
}
function closeLicenseModal() {
  showLicenseModal.value = false;
  activeLicenseCard.value = null;
}

// Font options
const fontOptions = [
  { label: 'Arial', value: 'Arial, sans-serif' },
  { label: 'Georgia', value: 'Georgia, serif' },
  { label: 'Courier', value: '"Courier New", monospace' },
  { label: 'Trebuchet', value: '"Trebuchet MS", sans-serif' },
  { label: 'Verdana', value: 'Verdana, sans-serif' },
  { label: 'Impact', value: 'Impact, sans-serif' },
  { label: 'Times', value: '"Times New Roman", serif' },
];

// Watermark positions - 9 positions in a 3x3 grid
const positions = ['top-left', 'top-center', 'top-right', 'middle-left', 'middle-center', 'middle-right', 'bottom-left', 'bottom-center', 'bottom-right'];

// Copyright generator state
const selectedLicense = ref('copyright');
const creatorName = ref('Your Name');
const copyrightYear = ref('2025');
const selectedFont = ref('Arial, sans-serif');
const uploadedImage = ref(null);
const originalImage = ref(null);
const watermarkOpacity = ref(0.7);
const watermarkSize = ref(24);
const watermarkPosition = ref('bottom-right');
const watermarkColor = ref('#FFFFFF');
const fileInput = ref(null);
const previewCanvas = ref(null);

// Add state for status messages and loading indicators
const isApplyingWatermark = ref(false);
const isCreatingSvg = ref(false);
const statusMessage = ref('');
const errorMessage = ref('');
const isSuccess = ref(false);

// Canvas for creating transparent watermark
const transparentCanvas = ref(null);
const transparentCtx = ref(null);

// Add these constants at the top of the script setup section
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
const MAX_IMAGE_DIMENSIONS = {
  width: 4096,
  height: 4096
};
const MIN_IMAGE_DIMENSIONS = {
  width: 100,
  height: 100
};

// Add these validation functions before handleFileUpload
const validateFileSize = (file) => {
  if (file.size > MAX_FILE_SIZE) {
    throw new Error(`File size must be less than ${MAX_FILE_SIZE / (1024 * 1024)}MB`);
  }
};

const validateFileType = (file) => {
  if (!ALLOWED_IMAGE_TYPES.includes(file.type)) {
    throw new Error(`Only ${ALLOWED_IMAGE_TYPES.map(type => type.split('/')[1].toUpperCase()).join(', ')} files are allowed`);
  }
};

const validateImageDimensions = (width, height) => {
  if (width > MAX_IMAGE_DIMENSIONS.width || height > MAX_IMAGE_DIMENSIONS.height) {
    throw new Error(`Image dimensions must not exceed ${MAX_IMAGE_DIMENSIONS.width}x${MAX_IMAGE_DIMENSIONS.height} pixels`);
  }
  if (width < MIN_IMAGE_DIMENSIONS.width || height < MIN_IMAGE_DIMENSIONS.height) {
    throw new Error(`Image dimensions must be at least ${MIN_IMAGE_DIMENSIONS.width}x${MIN_IMAGE_DIMENSIONS.height} pixels`);
  }
};

const validateImageContent = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const arr = new Uint8Array(e.target.result).subarray(0, 4);
      const header = Array.from(arr).map(b => b.toString(16).padStart(2, '0')).join('');
      
      // Check file signatures (magic numbers)
      const signatures = {
        '89504e47': 'image/png',
        'ffd8ffe0': 'image/jpeg',
        'ffd8ffe1': 'image/jpeg',
        '47494638': 'image/gif',
        '52494646': 'image/webp'
      };
      
      const mimeType = signatures[header];
      if (!mimeType || mimeType !== file.type) {
        reject(new Error('Invalid image file or file type mismatch'));
      } else {
        resolve();
      }
    };
    reader.onerror = () => reject(new Error('Error reading file'));
    reader.readAsArrayBuffer(file);
  });
};

// Copyright text based on inputs
const copyrightText = computed(() => {
  switch(selectedLicense.value) {
    case 'copyright':
      return `© ${copyrightYear.value} ${creatorName.value}. All rights reserved.`;
    case 'cc-by':
      return `© ${copyrightYear.value} ${creatorName.value}. Licensed under CC BY 4.0`;
    case 'cc-by-nc':
      return `© ${copyrightYear.value} ${creatorName.value}. Licensed under CC BY-NC 4.0`;
    case 'cc-by-sa':
      return `© ${copyrightYear.value} ${creatorName.value}. Licensed under CC BY-SA 4.0`;
    default:
      return `© ${copyrightYear.value} ${creatorName.value}. All rights reserved.`;
  }
});

// Carousel data and logic
const slidesData = ref([
  {
    title: 'Copyright in Australia',
    content: `
      <p>G'day! As a content creator in Australia, it's important to understand that copyright protection is automatic when you create original content. No need to register or apply for it — ripper!</p>
      <p>Copyright in Australia is governed by the Copyright Act 1968, which gives you exclusive rights to:</p>
      <ul class="rights-list">
        <li>Reproduce your work</li>
        <li>Publish your work</li>
        <li>Perform your work in public</li>
        <li>Communicate your work to the public (including online)</li>
        <li>Make adaptations of your work</li>
      </ul>
      <p>For most works, copyright lasts for the life of the creator plus 70 years. Fair dinkum!</p>
    `
  },
  {
    title: 'Fair Dealing Exceptions',
    content: `
      <p>The Copyright Act allows others to use your content without permission in certain circumstances, known as "fair dealing" exceptions:</p>
      <ul class="exception-list">
        <li><strong>Research or study</strong> - Limited use for educational purposes</li>
        <li><strong>Criticism or review</strong> - Commenting on or assessing content</li>
        <li><strong>Parody or satire</strong> - Using content for humour or commentary</li>
        <li><strong>Reporting news</strong> - Using content in news reporting</li>
      </ul>
      <p>These exceptions are a bit different from the American "fair use" doctrine, so don't get them mixed up, mate!</p>
    `
  },
  {
    title: 'Protecting Your Content',
    content: `
      <p>While copyright is automatic, here are some bonza ways to protect your content:</p>
      <ul class="protection-list">
        <li>Include a copyright notice: © [Year] [Your Name]</li>
        <li>Use watermarks on images and videos</li>
        <li>Include terms and conditions on your website or platform</li>
        <li>Monitor for unauthorized use of your content</li>
        <li>Consider Creative Commons licenses if you want to allow certain uses</li>
      </ul>
    `
  },
  {
    title: 'Using Others\' Content',
    content: `
      <p>When using content created by others, remember:</p>
      <ul class="usage-list">
        <li>Always get permission unless a fair dealing exception applies</li>
        <li>Credit the original creator appropriately</li>
        <li>Consider licensing content through stock image/video sites</li>
        <li>Look for Creative Commons licensed material</li>
        <li>Be especially careful with music in your videos</li>
      </ul>
      <p>Getting permission is always better than copping a copyright strike. No dramas!</p>
    `
  },
  {
    title: 'Further Resources',
    content: `
      <p>For more information about copyright in Australia, check out these resources:</p>
      <ul class="resources-list">
        <li><a href="https://www.ipaustralia.gov.au/ip-for-digital-business/develop-ip-strategy/copyright" target="_blank">IP Australia</a></li>
        <li><a href="https://www.artslaw.com.au/information-sheet/copyright/" target="_blank">Arts Law Centre of Australia</a></li>
        <li><a href="https://www.copyright.org.au/" target="_blank">Australian Copyright Council</a></li>
      </ul>
    `
  }
]);

const currentSlideIndex = ref(0);
const totalSlides = computed(() => slidesData.value.length);
const currentSlideTitle = computed(() => slidesData.value[currentSlideIndex.value].title);

const goToSlide = (index) => {
  currentSlideIndex.value = index;
};

const nextSlide = () => {
  currentSlideIndex.value = (currentSlideIndex.value + 1) % totalSlides.value;
};

const prevSlide = () => {
  currentSlideIndex.value = (currentSlideIndex.value - 1 + totalSlides.value) % totalSlides.value;
};

const handleKeydown = (event) => {
  if (event.key === 'ArrowRight') {
    nextSlide();
  } else if (event.key === 'ArrowLeft') {
    prevSlide();
  }
};

// Initialize transparent canvas & keyboard listeners
onMounted(() => {
  transparentCanvas.value = document.createElement('canvas');
  transparentCtx.value = transparentCanvas.value.getContext('2d');
  window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
});

// Trigger file upload dialog
const triggerFileUpload = () => {
  fileInput.value.click();
};

// Replace the existing handleFileUpload function with this updated version
const handleFileUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  try {
    // Clear previous messages
    errorMessage.value = '';
    statusMessage.value = '';
    isSuccess.value = false;

    // Validate file size
    validateFileSize(file);
    
    // Validate file type
    validateFileType(file);
    
    // Validate image content
    await validateImageContent(file);
    
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        // Validate image dimensions
        validateImageDimensions(img.width, img.height);
        
        // Store original image for processing
        originalImage.value = img;
        uploadedImage.value = true;
        
        // Draw image on canvas with watermark
        nextTick(() => {
          updateWatermark();
        });
        
        statusMessage.value = 'Image uploaded successfully';
        isSuccess.value = true;
      };
      img.onerror = () => {
        throw new Error('Failed to load image');
      };
      img.src = e.target.result;
    };
    reader.onerror = () => {
      throw new Error('Error reading file');
    };
    reader.readAsDataURL(file);
    
  } catch (error) {
    console.error('Error uploading file:', error);
    errorMessage.value = error.message;
    isSuccess.value = false;
    uploadedImage.value = null;
    originalImage.value = null;
    fileInput.value.value = '';
  }
};

// Update watermark on canvas
const updateWatermark = () => {
  if (!previewCanvas.value || !originalImage.value) return;
  
  const canvas = previewCanvas.value;
  const ctx = canvas.getContext('2d');
  
  // Set canvas size to match image
  canvas.width = originalImage.value.width;
  canvas.height = originalImage.value.height;
  
  // Draw original image
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(originalImage.value, 0, 0);
  
  // Add watermark text
  ctx.save();
  
  // Set watermark style
  ctx.font = `${watermarkSize.value}px ${selectedFont.value}`;
  ctx.fillStyle = `${watermarkColor.value}${Math.round(watermarkOpacity.value * 255).toString(16).padStart(2, '0')}`;
  ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
  ctx.shadowBlur = 4;
  
  // Calculate text metrics
  const text = copyrightText.value;
  const metrics = ctx.measureText(text);
  const textWidth = metrics.width;
  const textHeight = watermarkSize.value;
  
  // Calculate position based on selected position
  let x, y;
  
  // Get canvas dimensions
  const width = canvas.width;
  const height = canvas.height;
  
  // Determine x position
  if (watermarkPosition.value.includes('left')) {
    x = 20;
  } else if (watermarkPosition.value.includes('right')) {
    x = width - textWidth - 20;
  } else {
    // Center
    x = (width - textWidth) / 2;
  }
  
  // Determine y position
  if (watermarkPosition.value.includes('top')) {
    y = textHeight + 20;
  } else if (watermarkPosition.value.includes('bottom')) {
    y = height - 20;
  } else {
    // Middle
    y = height / 2;
  }
  
  // Draw watermark text
  ctx.fillText(text, x, y);
  ctx.restore();
};

// Create transparent watermark using the API
const createTransparentWatermark = async () => {
  if (!originalImage.value) return null;
  
  try {
    isCreatingSvg.value = true;
    statusMessage.value = 'Creating SVG watermark...';
    isSuccess.value = true;
    errorMessage.value = '';
    
    const svgContent = await createSvgWatermark(
      copyrightText.value,
      originalImage.value.width,
      originalImage.value.height,
      watermarkPosition.value,
      watermarkSize.value,
      watermarkColor.value,
      selectedFont.value
    );
    
    statusMessage.value = 'SVG watermark created successfully!';
    return svgContent;
  } catch (error) {
    console.error('Error creating transparent watermark:', error);
    errorMessage.value = `Error creating watermark: ${error.message}`;
    isSuccess.value = false;
    return null;
  } finally {
    isCreatingSvg.value = false;
  }
};

// Select license function
const selectLicense = (license) => {
  selectedLicense.value = license;
  if (uploadedImage.value) {
    updateWatermark();
  }
};

// Select watermark position
const selectPosition = (position) => {
  watermarkPosition.value = position;
  updateWatermark();
};

// Download watermarked image using the API
const downloadWatermarkedImage = async () => {
  if (!originalImage.value) return;
  
  try {
    isApplyingWatermark.value = true;
    statusMessage.value = 'Applying watermark...';
    isSuccess.value = true;
    errorMessage.value = '';
    
    // Create a temporary canvas for the final image
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    
    // Set canvas size to match original image
    tempCanvas.width = originalImage.value.width;
    tempCanvas.height = originalImage.value.height;
    
    // Draw original image
    tempCtx.drawImage(originalImage.value, 0, 0);
    
    // Add watermark with current settings
    tempCtx.save();
    tempCtx.font = `${watermarkSize.value}px ${selectedFont.value}`;
    tempCtx.fillStyle = `${watermarkColor.value}${Math.round(watermarkOpacity.value * 255).toString(16).padStart(2, '0')}`;
    tempCtx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    tempCtx.shadowBlur = 4;
    
    // Calculate text metrics
    const text = copyrightText.value;
    const metrics = tempCtx.measureText(text);
    const textWidth = metrics.width;
    const textHeight = watermarkSize.value;
    
    // Calculate position
    let x, y;
    const width = tempCanvas.width;
    const height = tempCanvas.height;
    
    if (watermarkPosition.value.includes('left')) {
      x = 20;
    } else if (watermarkPosition.value.includes('right')) {
      x = width - textWidth - 20;
    } else {
      x = (width - textWidth) / 2;
    }
    
    if (watermarkPosition.value.includes('top')) {
      y = textHeight + 20;
    } else if (watermarkPosition.value.includes('bottom')) {
      y = height - 20;
    } else {
      y = height / 2;
    }
    
    // Draw watermark text
    tempCtx.fillText(text, x, y);
    tempCtx.restore();
    
    // Convert to blob and download
    const blob = await new Promise(resolve => tempCanvas.toBlob(resolve, 'image/png'));
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `watermarked-image-${creatorName.value.replace(/\s+/g, '-')}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    statusMessage.value = 'Watermarked image downloaded successfully';
    isSuccess.value = true;
  } catch (error) {
    console.error('Error downloading watermarked image:', error);
    errorMessage.value = `Error: ${error.message}`;
    isSuccess.value = false;
  } finally {
    isApplyingWatermark.value = false;
  }
};

// Download transparent watermark as SVG
const downloadTransparentWatermark = async () => {
  try {
    isCreatingSvg.value = true;
    statusMessage.value = 'Creating SVG watermark...';
    isSuccess.value = true;
    errorMessage.value = '';
    
    // Calculate dimensions - use image dimensions if available, or reasonable defaults
    let width = 800;
    let height = 600;
    
    if (originalImage.value) {
      // Use uploaded image dimensions
      width = originalImage.value.width;
      height = originalImage.value.height;
    } else {
      // No image uploaded, use reasonably sized dimensions for standalone watermark
      width = 1200;
      height = 630; // Good for social media sharing
    }
    
    // Get SVG content from the updated CopyrightService (which now has fallback)
    const svgContent = await createSvgWatermark(
      copyrightText.value,
      width,
      height,
      watermarkPosition.value,
      watermarkSize.value,
      watermarkColor.value,
      selectedFont.value
    );
    
    // Create download link
    const blob = new Blob([svgContent], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `transparent-watermark-${creatorName.value.replace(/\s+/g, '-')}.svg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    statusMessage.value = 'SVG watermark downloaded successfully';
    isSuccess.value = true;
  } catch (error) {
    console.error('Error downloading transparent watermark:', error);
    errorMessage.value = `Error: ${error.message}`;
    isSuccess.value = false;
  } finally {
    isCreatingSvg.value = false;
  }
};

// Reset image
const resetImage = () => {
  uploadedImage.value = null;
  originalImage.value = null;
  fileInput.value.value = '';
  statusMessage.value = 'Image reset';
  isSuccess.value = true;
  errorMessage.value = '';
};

// Add this in the script setup section
const colorOptions = [
  '#FFFFFF', // White
  '#000000', // Black
  '#FF6B98', // Pink
  '#4ECDC4', // Teal
  '#FFD166', // Yellow
  '#06D6A0', // Green
  '#118AB2', // Blue
  '#EF476F', // Red
  '#073B4C', // Dark Blue
];

// Add these new methods in the script setup section
const selectColor = (color) => {
  watermarkColor.value = color;
  updateWatermark();
};

const handleColorChange = (event) => {
  watermarkColor.value = event.target.value;
  updateWatermark();
};

// Add this to your script setup section
const handleCardTouch = (event) => {
  const card = event.currentTarget;
  card.classList.toggle('flipped');
};
</script>

<style scoped>
.copyright-view {
  background: #fffdf4;
  font-family: Avenir, Helvetica, sans-serif;
  text-align: center;
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
  font-size: 6.5rem;
  font-weight: bold;
  position: relative;
  background: linear-gradient(
    to right,
    #d8a1e5 20%,
    #ffb1c5 40%,
    #ffb1c5 60%,
    #d8a1e5 80%
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
  margin-bottom: 1.5rem;
  white-space: nowrap;
  text-align: left;
  padding: 0 0 0.15em;
  transform: translateY(-0.05em);
}

.title-group h1:hover {
  filter: drop-shadow(0 0 2px rgba(216, 161, 229, 0.5));
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
  font-size: 3.8rem;
  font-weight: bold;
  color: #333;
  line-height: 1.2;
  display: block;
  white-space: nowrap;
  text-align: left;
  overflow: visible;
}

.subtitle {
  font-size: 1.8rem;
  color: #666;
  line-height: 1.4;
  margin-top: 2.5rem;
  white-space: normal;
  text-align: left;
  max-width: 100%;
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

/* License Cards Section */
.license-cards-section {
  max-width: 1200px;
  margin: 3rem auto;
  padding: 2rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 0.5rem;
  text-align: center;
}

.section-description {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 3rem;
  text-align: center;
}

.license-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.license-card {
  height: 250px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  position: relative;
  perspective: 1000px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  transform-style: preserve-3d;
}

.license-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: transform 0.6s ease;
}

.card-front {
  background-color: #fff;
  z-index: 2;
}

.card-back {
  background-color: #dbff00;
  transform: rotateY(180deg);
  z-index: 1;
}

.license-card:hover .card-front {
  transform: rotateY(180deg);
}

.license-card:hover .card-back {
  transform: rotateY(0);
}

.license-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.license-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.license-subtitle {
  font-size: 1.2rem;
  color: #666;
}

.license-details {
  list-style: none;
  padding: 0;
  width: 100%;
  text-align: left;
}

.license-details li {
  margin-bottom: 0.8rem;
  font-size: 1rem;
  position: relative;
  padding-left: 1.5rem;
}

.allowed:before {
  content: "✓";
  color: #28a745;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.prohibited:before {
  content: "✗";
  color: #dc3545;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.required:before {
  content: "!";
  color: #fd7e14;
  font-weight: bold;
  position: absolute;
  left: 0;
}

.info:before {
  content: "ℹ";
  color: #007bff;
  font-weight: bold;
  position: absolute;
  left: 0;
}

/* Mobile-friendly styles for license cards */
@media (max-width: 768px) {
  .license-cards-section {
    padding: 1rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .section-description {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }

  .license-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .license-card {
    height: 250px;
    min-height: 250px;
    transform-style: preserve-3d;
    perspective: 1000px;
    touch-action: manipulation;
    -webkit-tap-highlight-color: transparent;
  }

  .card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    transform-style: preserve-3d;
    transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 1.5rem;
  }

  .card-front {
    background-color: #fff;
    z-index: 2;
  }

  .card-back {
    background-color: #dbff00;
    transform: rotateY(180deg);
    z-index: 1;
  }

  /* Touch-based flip */
  .license-card.flipped .card-front {
    transform: rotateY(180deg);
  }

  .license-card.flipped .card-back {
    transform: rotateY(0);
  }

  .license-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
  }

  .license-title {
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
  }

  .license-subtitle {
    font-size: 1.1rem;
  }

  .license-details li {
    font-size: 0.9rem;
    margin-bottom: 0.6rem;
    padding-left: 1.25rem;
  }
}

/* Small mobile devices */
@media (max-width: 480px) {
  .license-cards-section {
    padding: 0.75rem;
  }

  .section-title {
    font-size: 1.8rem;
  }

  .section-description {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }

  .license-card {
    height: 220px;
    min-height: 220px;
  }

  .card-front, .card-back {
    padding: 1.25rem;
  }

  .license-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
  }

  .license-title {
    font-size: 1.3rem;
  }

  .license-subtitle {
    font-size: 1rem;
  }

  .license-details li {
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
    padding-left: 1.1rem;
  }
}

/* Remove the touch-friendly styles that disabled flip */
@media (hover: none) {
  .license-card {
    transform-style: preserve-3d;
    perspective: 1000px;
  }

  .card-front, .card-back {
    backface-visibility: hidden;
  }
}

/* Copyright Generator Section */
.copyright-generator-section {
  max-width: 1200px;
  margin: 3rem auto;
  box-sizing: border-box;
}

.generator-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  max-width: 1200px;
  margin: 2rem auto 0;
  box-sizing: border-box;
}

.preview-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  border-radius: 12px;
  background-color: #f8f9fa;
  min-height: 400px;
}

.image-watermark-disclaimer {
  width: 100%;
  padding: 0.75rem;
  margin-bottom: 1rem;
  border: 1px dotted #ff6b98;
  border-radius: 6px;
  background-color: rgba(255, 107, 152, 0.05);
  text-align: left;
}

.image-watermark-disclaimer p {
  font-size: 0.85rem;
  color: #555;
  line-height: 1.4;
  margin: 0;
}

.image-watermark-disclaimer p strong {
  color: #333;
}

.image-preview {
  width: 450px;
  height: 300px;
  background-color: #fff;
  border: 2px dashed #ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
  border-radius: 12px;
  overflow: hidden;
}

.placeholder-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  border: 2px dashed #ff6b98;
  border-radius: 12px;
  background-color: rgba(255, 107, 152, 0.05);
  color: #ff6b98;
  cursor: pointer;
  transition: all 0.3s ease;
}

.placeholder-upload:hover {
  background-color: rgba(255, 107, 152, 0.1);
  transform: scale(1.02);
}

.upload-icon {
  margin-bottom: 1rem;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.copyright-preview {
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 6px;
  font-size: 1.2rem;
  width: 100%;
  text-align: center;
}

.controls-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.control-step {
  position: relative;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 12px;
  padding-top: 2.5rem;
}

.step-number {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 36px;
  height: 36px;
  background-color: #ff6b98;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.step-title {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: #333;
}

.license-options {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.license-option {
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.license-option.active {
  background-color: #dbff00;
  border-color: #dbff00;
  font-weight: bold;
}

.input-group {
  margin-bottom: 1rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  text-align: left;
  font-size: 0.9rem;
  color: #666;
}

input[type="text"] {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

.font-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  background-color: white;
}

.generator-actions {
  margin-top: 1rem;
  display: flex;
  justify-content: flex-end;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.download-button {
  background-color: #dbff00;
  color: #333;
}

.download-button:hover {
  background-color: #c8e600;
  transform: translateY(-2px);
}

/* Main content styles */
.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  text-align: left;
}

.content-section {
  margin-bottom: 3rem;
  background-color: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.content-section h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
}

.content-section h2:after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(to right, #FF6B6B, #4ECDC4);
  border-radius: 3px;
}

.content-section p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 1.5rem;
}

.rights-list, 
.exception-list,
.protection-list,
.usage-list,
.resources-list {
  padding-left: 1.5rem;
  margin-bottom: 1.5rem;
}

.rights-list li,
.exception-list li,
.protection-list li,
.usage-list li,
.resources-list li {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #555;
  margin-bottom: 0.75rem;
  position: relative;
  padding-left: 0.5rem;
}

.resources-list a {
  color: #4ECDC4;
  text-decoration: none;
  transition: color 0.2s;
}

.resources-list a:hover {
  color: #FF6B6B;
  text-decoration: underline;
}

.disclaimer {
  background-color: #fff8e8;
  border-left: 4px solid #ffd166;
  max-width: 1200px;
  margin: 3rem auto;
  display: block;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
}

.disclaimer h3 {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 1rem;
}

/* Responsive styles */
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
  .hero-section {
    min-height: 40vh;
    padding: 5rem 0 1rem;
  }
  .hero-content {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }
  .slogan {
    margin-left: 0;
    max-width: 100%;
  }
  .decorative-elements {
    width: 500px;
    grid-template-columns: repeat(5, 100px);
    opacity: 0.6;
  }
  .title-group h1 {
    font-size: 4.5rem;
  }
  .title-group h2 {
    font-size: 2.8rem;
  }
  .subtitle {
    font-size: 1.5rem;
  }
  .generator-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  .preview-section, .controls-section {
    padding: 1.5rem;
  }
  .image-preview {
    width: 100%;
    max-width: 400px;
    height: auto;
    min-height: 250px;
  }
  .preview-canvas {
    max-height: 250px;
  }
}

@media (max-width: 1024px) {
  .hero-section {
    padding: 5rem 0 1rem;
  }
  .title-group h1 {
    font-size: 3.8rem;
  }
  .title-group h2 {
    font-size: 2.2rem;
  }
  .subtitle {
    font-size: 1.25rem;
    margin-top: 1.5rem;
  }
  .decorative-elements {
    width: 400px;
    grid-template-columns: repeat(4, 100px);
    opacity: 0.4;
  }
  .license-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  .section-title {
    font-size: 2rem;
  }
  .section-description {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }
  .carousel-main-title {
    font-size: 1.8rem;
  }
  .carousel-slide .content-section h2 {
    font-size: 1.5rem;
  }
  .carousel-slide .content-section :deep(p),
  .carousel-slide .content-section :deep(li) {
    font-size: 1rem !important;
  }
  .carousel-nav-button {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }
  .carousel-nav-button.prev {
    left: 10px;
  }
  .carousel-nav-button.next {
    right: 10px;
  }
  .carousel-dots .dot {
    width: 10px;
    height: 10px;
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 4rem 0 1rem;
  }
  .hero-content {
    padding: 0 1rem;
    align-items: flex-start;
  }
  .title-group h1 {
    font-size: 3rem;
  }
  .title-group h2 {
    font-size: 1.8rem;
  }
  .subtitle {
    font-size: 1.1rem;
    margin-top: 1rem;
  }
  .decorative-elements {
    display: none;
  }
  .license-grid {
    grid-template-columns: 1fr;
  }
  .license-card {
    height: auto;
    min-height: 180px;
  }
  .card-front, .card-back {
    padding: 1.5rem;
  }
  .generator-container {
    padding: 1.5rem;
  }
  .preview-section {
    min-height: auto;
  }
  .image-preview {
    min-height: 200px;
  }
  .preview-canvas {
    max-height: 200px;
  }
  .control-step {
    padding: 1rem;
    padding-top: 2rem;
  }
  .license-options {
    grid-template-columns: 1fr;
  }
  .font-selector {
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  }
  .action-buttons-group {
    flex-direction: column;
    gap: 0.5rem;
  }
  .action-button {
    width: 100%;
    justify-content: center;
  }
  .interactive-content-carousel {
    padding: 1.5rem;
  }
  .carousel-header-panel,
  .carousel-container,
  .carousel-dots {
    margin-left: 0;
    margin-right: 0;
  }
  .carousel-main-title {
    font-size: 1.6rem;
  }
  .carousel-slide .content-section {
    padding: 1.5rem;
  }
  .carousel-slide .content-section h2 {
    font-size: 1.4rem;
  }
  .carousel-slide .content-section :deep(p),
  .carousel-slide .content-section :deep(li) {
    font-size: 0.95rem !important;
  }
}

@media (max-width: 640px) {
  .decorative-elements {
    opacity: 0.1;
    transform: translateX(0) scale(0.7);
  }
  .hero-section {
    padding: 3rem 0 0.5rem;
  }
  .title-group h1 {
    font-size: 2.5rem;
  }
  .title-group h2 {
    font-size: 1.6rem;
  }
  .subtitle {
    font-size: 1rem;
  }
  .image-preview {
    max-width: 100%;
    min-height: 180px;
  }
  .preview-canvas {
    max-height: 180px;
  }
  .placeholder-upload {
    min-height: 180px;
  }
  .section-title {
    font-size: 1.8rem;
  }
  .section-description {
    font-size: 1rem;
  }
  .carousel-nav-button {
    width: 35px;
    height: 35px;
    font-size: 1.3rem;
  }
  .carousel-main-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 2.5rem 0 0.5rem;
  }
  .title-group h1 {
    font-size: 2rem;
  }
  .title-group h2 {
    font-size: 1.4rem;
  }
  .subtitle {
    font-size: 0.9rem;
  }
  .license-card {
    padding: 0.6rem;
    min-height: 0;
    height: auto;
  }
  .card-front, .card-back {
    padding: 0.8rem;
    justify-content: flex-start;
  }
  .license-icon {
    font-size: 2rem;
    margin-bottom: 0.3rem;
  }
  .license-title {
    font-size: 1.1rem;
    margin-bottom: 0.2rem;
    line-height: 1.2;
  }
  .license-subtitle {
    font-size: 0.8rem;
    margin-bottom: 0.4rem;
    line-height: 1.3;
  }
  .license-details {
    padding: 0;
    margin: 0;
  }
  .license-details li {
    font-size: 0.75rem;
    margin-bottom: 0.25rem;
    padding-left: 1rem;
    line-height: 1.4;
  }
  .generator-container {
    padding: 1rem;
  }
  .preview-section {
    padding: 1rem;
  }
  .image-preview {
    min-height: 150px;
  }
  .preview-canvas {
    max-height: 150px;
  }
  .placeholder-upload {
    min-height: 150px;
  }
  .control-step {
    padding: 1rem;
    padding-top: 1.5rem;
  }
  .step-number {
    width: 30px;
    height: 30px;
    font-size: 0.9rem;
  }
  .step-title {
    font-size: 1.1rem;
  }
  input[type="text"] {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
  .font-selector {
    grid-template-columns: 1fr;
  }
  .font-option {
    padding: 0.6rem;
    font-size: 0.85rem;
  }
  .color-option, .color-picker {
    width: 30px;
    height: 30px;
  }
  .slider-group label, .color-selector label {
    font-size: 0.85rem;
  }
  .position-option {
    width: 30px;
    height: 30px;
  }
  .action-button {
    padding: 0.6rem 1rem;
    font-size: 0.9rem;
  }
  .interactive-content-carousel {
    padding: 1rem;
  }
  .carousel-main-title {
    font-size: 1.4rem;
  }
  .carousel-slide .content-section {
    padding: 1rem;
  }
  .carousel-slide .content-section h2 {
    font-size: 1.3rem;
  }
  .carousel-slide .content-section :deep(p),
  .carousel-slide .content-section :deep(li) {
    font-size: 0.9rem !important;
  }
  .carousel-dots .dot {
    width: 8px;
    height: 8px;
    margin: 0 4px;
  }
}

.preview-canvas {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.font-selector {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 0.75rem;
}

.font-option {
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
  font-size: 0.9rem;
}

.font-option:hover {
  border-color: #c8e600;
  transform: translateY(-2px);
}

.font-option.active {
  background-color: #dbff00;
  border-color: #dbff00;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.slider-group {
  margin-bottom: 1.25rem;
}

.slider-group label {
  display: block;
  margin-bottom: 0.75rem;
  text-align: left;
  font-size: 0.9rem;
  color: #333;
}

.slider {
  -webkit-appearance: none;
  width: 100%;
  height: 6px;
  border-radius: 3px;
  background: #ddd;
  outline: none;
}

.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ff6b98;
  cursor: pointer;
  border: none;
}

.slider::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ff6b98;
  cursor: pointer;
  border: none;
}

.position-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.position-option {
  width: 36px;
  height: 36px;
  border: 2px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.position-option:hover {
  border-color: #ff6b98;
  transform: scale(1.1);
}

.position-option.active {
  background-color: #ff6b98;
  border-color: #ff6b98;
}

.action-buttons-group {
  display: flex;
  flex-wrap: nowrap;
  gap: 0.75rem;
}

.action-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #dbff00;
  color: #333;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-button:hover {
  background-color: #c8e600;
  transform: translateY(-2px);
}

.action-button.secondary-button {
  background-color: #f1f3f5;
  color: #333;
}

.action-button.secondary-button:hover {
  background-color: #e9ecef;
}

.status-messages {
  margin-top: 1rem;
  width: 100%;
}

.status-message {
  padding: 0.75rem;
  border-radius: 6px;
  background-color: #f8f9fa;
  margin-bottom: 0.5rem;
}

.status-message.success {
  background-color: #d1e7dd;
  color: #0f5132;
}

.error-message {
  padding: 0.75rem;
  border-radius: 6px;
  background-color: #f8d7da;
  color: #842029;
  margin-bottom: 0.5rem;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.color-selector {
  margin-top: 1.5rem;
}

.color-selector label {
  display: block;
  margin-bottom: 0.75rem;
  text-align: left;
  font-size: 0.9rem;
  color: #333;
}

.color-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(36px, 1fr));
  gap: 0.75rem;
  align-items: center;
}

.color-option {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.color-option:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.color-option.active {
  border-color: #333;
  transform: scale(1.1);
}

.color-picker {
  width: 36px;
  height: 36px;
  padding: 0;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  -webkit-appearance: none;
  background: none;
}

.color-picker::-webkit-color-swatch-wrapper {
  padding: 0;
}

.color-picker::-webkit-color-swatch {
  border: 2px solid #ddd;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.color-picker::-moz-color-swatch {
  border: 2px solid #ddd;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Styles for the new Interactive Content Carousel */
.interactive-content-carousel {
  max-width: 1200px;
  margin: 3rem auto;
  position: relative;
  background-color: #fff0f5;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  box-sizing: border-box;
}

.carousel-header-panel {
  padding: 0 0 1.5rem 0;
  text-align: center;
  margin-left: 42px;
  margin-right: 42px;
}

.carousel-main-title {
  font-size: 2.2rem;
  font-weight: bold;
  color: #333;
  margin: 0;
}

.carousel-container {
  overflow: hidden;
  border-radius: 0;
  margin: 0;
  margin-left: 42px;
  margin-right: 42px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.carousel-wrapper {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-slide {
  flex: 0 0 100%;
  box-sizing: border-box;
}

.carousel-slide .content-section {
  margin-bottom: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #fff;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.carousel-slide .content-section h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
}

.carousel-slide .content-section h2:after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(to right, #FF6B6B, #4ECDC4);
  border-radius: 3px;
}

.carousel-slide .content-section :deep(p) {
  font-size: 1.1rem !important;
  line-height: 1.8;
  margin-bottom: 1.2rem;
}

.carousel-slide .content-section :deep(li) {
  font-size: 1.1rem !important;
  line-height: 1.8;
  margin-bottom: 0.6rem;
}

.carousel-slide .content-section :deep(ul),
.carousel-slide .content-section :deep(ol) {
  padding-left: 2rem;
  margin-bottom: 1rem;
}

/* Styling for links within the carousel's resources list */
.carousel-slide .content-section :deep(ul.resources-list li a) {
  color: #007bff; /* Standard blue for links */
  text-decoration: underline;
  transition: color 0.2s ease;
}

.carousel-slide .content-section :deep(ul.resources-list li a:hover) {
  color: #0056b3; /* Darker blue on hover */
}

.carousel-slide .content-section :deep(strong) {
  font-weight: 600;
}

.carousel-navigation {
}

.carousel-nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: #ff6b98;
  color: white;
  border: none;
  padding: 0;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.8rem;
  font-weight: bold;
  transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.15);
  z-index: 10;
}

.carousel-nav-button.prev {
  left: 20px;
}

.carousel-nav-button.next {
  right: 20px;
}

.carousel-nav-button:hover {
  background-color: #e0527e;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.carousel-nav-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
  box-shadow: none;
}

.carousel-dots {
  display: flex;
  justify-content: center;
  margin-top: 1.5rem;
  margin-left: 42px;
  margin-right: 42px;
}

.carousel-dots .dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #ddd;
  margin: 0 6px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.carousel-dots .dot:hover {
  background-color: #ccc;
  transform: scale(1.1);
}

.carousel-dots .dot.active {
  background-color: #ff6b98;
  transform: scale(1.25);
}

/* Style for the reset button in preview area */
.reset-image-preview-btn {
  margin-top: 0.25rem;
  margin-bottom: 1rem;
  /* Other styles are inherited from .action-button.secondary-button */
}

/* Add modal styles and adjust mobile card grid */
@media (max-width: 480px) {
  .license-cards-section {
    padding: 0.75rem;
  }
  .section-title {
    font-size: 1.8rem;
  }
  .section-description {
    font-size: 1rem;
    margin-bottom: 1.5rem;
  }
  .license-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .license-card {
    height: 60px;
    min-height: 60px;
    max-height: 60px;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    position: relative;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    cursor: pointer;
    overflow: hidden;
    padding: 0 1.2rem;
    transition: box-shadow 0.2s;
  }
  .license-card:active {
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  }
  .card-front {
    display: flex;
    align-items: center;
    width: 100%;
    height: 100%;
    background: none;
    padding: 0;
    position: static;
    z-index: 1;
  }
  .license-icon {
    font-size: 1.5rem;
    margin-right: 1rem;
  }
  .license-title {
    font-size: 1.1rem;
    font-weight: bold;
    color: #222;
    margin-bottom: 0;
  }
  .license-subtitle {
    display: none;
  }
  .card-back, .license-details {
    display: none !important;
  }
  .license-modal-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.35);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fadeIn 0.2s;
  }
  .license-modal-card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.18);
    padding: 2rem 1.5rem 1.2rem 1.5rem;
    max-width: 90vw;
    width: 340px;
    text-align: center;
    position: relative;
    animation: popIn 0.2s;
  }
  .modal-icon {
    font-size: 2.2rem;
    margin-bottom: 0.5rem;
  }
  .modal-title {
    font-size: 1.3rem;
    font-weight: bold;
    margin-bottom: 0.2rem;
  }
  .modal-subtitle {
    font-size: 1.05rem;
    color: #666;
    margin-bottom: 1.1rem;
  }
  .modal-details {
    list-style: none;
    padding: 0;
    margin-bottom: 1.2rem;
    text-align: left;
  }
  .modal-details li {
    margin-bottom: 0.7rem;
    font-size: 1rem;
    position: relative;
    padding-left: 1.5rem;
  }
  .modal-tap-to-close {
    font-size: 0.95rem;
    color: #888;
    margin-top: 0.5rem;
  }
  @keyframes fadeIn {
    from { opacity: 0; } to { opacity: 1; }
  }
  @keyframes popIn {
    from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; }
  }
}
</style> 