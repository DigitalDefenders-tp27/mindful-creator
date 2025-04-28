# Mindful Creator Backend

This is an application for analysing YouTube video comments, supporting sentiment analysis and toxicity detection.

## Features

- Fetches comments from YouTube videos (up to 100)
- Analyses comment sentiment (positive, neutral, negative)
- Detects comment toxicity (toxic, severely toxic, obscene, threatening, insulting, identity hate)
- Stores datasets in PostgreSQL for creator wellbeing dashboard
- Provides statistics including counts and percentages for each category

## System Architecture

The system consists of three main parts:

1. **Backend API**: A REST API developed with FastAPI to receive frontend requests, fetch YouTube comments, and interact with the Space API.
2. **Hugging Face Space**: A Space with deployed sentiment analysis and toxicity detection models for processing comment text analysis.
3. **Frontend Application**: A user interface that interacts with the backend API and displays analysis results.
4. **PostgreSQL Database**: Stores comments, sentiments, and creator wellbeing datasets.

## Installation and Setup

### Requirements

- Python 3.8+
- Node.js 14+ (for frontend)
- PostgreSQL 15+

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/mindful-creator.git
cd mindful-creator/backend
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Create a .env file based on .env.example:

```
YOUTUBE_API_KEY=your_youtube_api_key
SPACE_API_URL=https://huggingface.co/spaces/your-username/your-space-name/api/predict/
CORS_ORIGIN=http://localhost:3000
```

### Running the Backend

```bash
python run_server.py
```

The FastAPI service will start at http://localhost:8000.

### Docker Deployment

To run the application using Docker:

```bash
docker build -t mindful-creator-backend .
docker run -p 8000:8000 -e YOUTUBE_API_KEY=your_key -e SPACE_API_URL=your_url mindful-creator-backend
```

### Space API Deployment

1. Create a new Space on Hugging Face.
2. Upload the `spaces/comment_analyzer/app.py` file to that Space.
3. Install necessary dependencies (transformers, torch, gradio, etc.).

### API Documentation

After starting the backend, visit http://localhost:8000/docs to view the API documentation.

## Usage Example

### Analysing YouTube Video Comments

```python
import requests

url = "http://localhost:8000/api/youtube/analyze"
payload = {
    "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
response = requests.post(url, json=payload)
print(response.json())
```

## Testing

To run the tests:

```bash
cd tests
python test_api.py
```

## Environment Variables

- `YOUTUBE_API_KEY`: YouTube Data API key
- `SPACE_API_URL`: Hugging Face Space API URL
- `CORS_ORIGIN`: Allowed cross-origin source (default is http://localhost:3000)
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`: PostgreSQL Database Credentials

---

> Note: Make sure PostgreSQL is running locally when you start the backend.

---



### 1. Database Setup

Setup Instructions:

1. Copy `.env.example` → create a new file `.env`
2. Fill in your DB username, password, and host.

Example:
DB_USERNAME=your_db_username
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mindful_creator
