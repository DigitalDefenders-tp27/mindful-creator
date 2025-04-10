# Mindful Creator App

A Vue.js application for content creators to manage their content and engage with their audience responsibly.

## Features

- **Ethical Guidelines**: Comprehensive guidelines for responsible content creation
- **Audience Engagement**: Tools for meaningful interaction with your audience
- **Content Management**: Organise and schedule your content ethically
- **Analytics**: Track your impact and audience growth
- **Relaxation Zone**: Activities to help content creators maintain mental wellbeing

## Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher)

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/aseemcodes72/mindful-creator.git
   cd mindful-creator
   ```

2. Install dependencies
   ```bash
   npm install
   ```

3. Start the development server
   ```bash
   npm run dev
   ```

4. Build for production
   ```bash
   npm run build
   ```

## Project Structure

```
mindful-creator/
├── frontend/             # Frontend code
│   ├── public/           # Static assets
│   │   ├── icons/        # UI icons
│   │   ├── images/       # Content images
│   │   └── emojis/       # Emotion emojis
│   │   ├── components/   # Vue components
│   │   │   ├── ui/       # UI components
│   │   │   └── Activities/ # Activity components
│   │   ├── content/      # Content files
│   │   ├── lib/          # Utility libraries
│   │   ├── router/       # Vue Router configuration
│   │   ├── styles/       # Global styles
│   │   ├── views/        # Page components
│   │   ├── App.vue       # Root component
│   │   └── main.js       # Entry point
│   ├── .gitignore        # Git ignore file
│   ├── index.html        # HTML template
│   ├── package.json      # Dependencies and scripts
│   ├── postcss.config.js # PostCSS configuration
│   ├── tailwind.config.js # Tailwind CSS configuration
│   └── vite.config.js    # Vite configuration
└── backend/              # Backend code
    └── [backend structure] # Backend structure to be added
```

## Key Sections

### Ethical Influencer
Learn about building trust through authenticity and creating content that makes a positive impact.

### Critical Response
Turn feedback into growth and protect yourself from cyberbullying.

### Relaxation Zone
Peaceful moments for mental reset with various relaxation activities.

## Technologies Used

- **Frontend**:
  - Vue.js 3
  - Vue Router
  - Tailwind CSS
  - Marked (for Markdown rendering)
  - Vite (for build and development)

- **Design Features**:
  - Responsive Design
  - Animations & Transitions
  - Interactive UI Elements
  - Accessibility Support

## Acknowledgements

- Thanks to all team members
- Special thanks to our tutors and industrial mentors
- Icon and design resources from various sources

---

### Frontend Dependencies
- Vue.js (^3.5.13)
- Vue Router (^4.3.0)
- Tailwind CSS (^3.4.17)
- Vite (^6.2.4)
- PostCSS (^8.5.3)
- Autoprefixer (^10.4.21)
- Axios (^1.6.7)
- Marked (^12.0.0)
- Class Variance Authority (^0.7.1)
- CLSX (^2.1.1)
- Lucide Vue Next (^0.487.0)
- Tailwind Merge (^2.6.0)
- Tailwind CSS Animate (^1.0.7)

### Frontend Dev Dependencies
- @vitejs/plugin-vue (^5.2.3)
- @vue/eslint-config-prettier (^10.2.0)
- ESLint
  - @eslint/js (^9.22.0)
  - eslint-plugin-oxlint (^0.16.0)
  - eslint-plugin-vue (~10.0.0)
- Globals (^16.0.0)
- npm-run-all2 (^7.0.2)
- Oxlint (^0.16.0)
- Prettier (3.5.3)
- Vite Plugin Vue DevTools (^7.7.2) 