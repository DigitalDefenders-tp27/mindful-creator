# Mindful Creator App

A Vue.js application for content creators to manage their content and engage with their audience responsibly.

## Features

- **Ethical Guidelines**: Comprehensive guidelines for responsible content creation
- **Audience Engagement**: Tools for meaningful interaction with your audience
- **Content Management**: Organise and schedule your content ethically
- **Analytics**: Track your impact and audience growth
- **Relaxation Zone**: Activities to help content creators maintain mental wellbeing
- **Critical Response**: Tools to handle feedback and criticism constructively
- **Memory Match Game**: A fun game to take mental breaks using real memes

## Prerequisites

- Node.js (v16 or higher)
- npm (v7 or higher)
- Python 3.9+ (for backend)

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/aseemcodes72/mindful-creator.git
   cd mindful-creator
   ```

2. Install frontend dependencies
   ```bash
   cd frontend
   npm install
   ```

3. Install backend dependencies
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. Start the development servers

   Frontend:
   ```bash
   cd frontend
   npm run dev
   ```

   Backend:
   ```bash
   cd backend
   python run_server.py
   ```

## Project Structure

```
mindful-creator/
├── frontend/                # Frontend code
│   ├── public/              # Static assets
│   │   ├── icons/           # UI icons
│   │   ├── media/           # Media files
│   │   ├── memes/           # Meme images for games
│   │   └── emojis/          # Emotion emojis
│   ├── src/                 # Source files
│   │   ├── assets/          # Images, icons, etc.
│   │   ├── components/      # Vue components
│   │   │   ├── ui/          # UI components
│   │   │   ├── Activities/  # Relaxation activities
│   │   │   └── Games/       # Game components
│   │   ├── content/         # Content files
│   │   ├── lib/             # Utility libraries
│   │   ├── router/          # Vue Router configuration
│   │   ├── stores/          # Pinia stores
│   │   ├── styles/          # Global styles
│   │   ├── views/           # Page components
│   │   ├── App.vue          # Root component
│   │   └── main.js          # Entry point
│   └── vite.config.js       # Vite configuration
├── backend/                 # Backend code
│   ├── app/                 # Main application
│   │   ├── api/             # API endpoints
│   │   ├── routers/         # Route handlers
│   │   └── main.py          # Main application file
│   ├── models/              # Data models
│   ├── scripts/             # Utility scripts
│   ├── requirements.txt     # Python dependencies
│   └── run_server.py        # Server runner
└── README.md                # Project documentation
```

## Key Sections

### Ethical Influencer
Learn about building trust through authenticity and creating content that makes a positive impact.

### Critical Response
Turn feedback into growth and protect yourself from cyberbullying with tools to analyse YouTube comments and develop appropriate responses.

### Relaxation Zone
Peaceful moments for mental reset with various relaxation activities including:
- Breathing exercises
- Guided meditation
- Sensory grounding
- Nature sounds
- Stretching routines
- Colour breathing
- Affirmation reflection
- Journaling

### Memory Match Game
A fun meme-matching game that provides a mental break while using real memes from the Memotion dataset.

## Technologies Used

### Frontend
- **Framework**: Vue.js 3.5
- **State Management**: Pinia 3.0
- **Routing**: Vue Router 4.3
- **UI Components**: 
  - Tailwind CSS 3.4
  - Headless UI
  - Lucide icons
- **Charts & Visualisations**:
  - ApexCharts 4.7
  - Chart.js 4.4
- **Build Tools**: 
  - Vite 6.2
  - PostCSS 8.5
  - Autoprefixer 10.4

### Backend
- **Framework**: FastAPI 0.95
- **Database**: SQLite/PostgreSQL with SQLAlchemy 2.0
- **Authentication**: JWT
- **Data Processing**: 
  - NumPy
  - Pandas 2.1
  - TensorFlow 2.15
  - scikit-learn 1.2
- **Natural Language Processing**:
  - NLTK 3.8
  - Transformers 4.30

## Deployment

This application can be deployed using:
- Railway
- Vercel
- Docker

For Railway deployment:
1. Configure the Railway project with both frontend and backend services
2. Set the appropriate environment variables
3. Ensure the meme dataset is properly configured

## Acknowledgements

- Thanks to all team members
- Special thanks to our tutors and industrial mentors
- Icon and design resources from various sources

---

*This project is designed to support content creators in Australia and worldwide in maintaining ethical practices and emotional wellbeing while engaging with their audience.* 