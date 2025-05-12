# Mindful Creator App

A Vue.js application for content creators to manage their content and engage with their audience responsibly.

## Available Languages / 可用语言 / उपलब्ध भाषाएँ / கிடைக்கும் மொழிகள்

- [English (Australia) / 英语（澳大利亚）](README-EN-AU.md)
- [中文简体 / Chinese (Simplified)](README-ZH-CN.md)
- [हिन्दी / Hindi](README-HI.md)
- [தமிழ் / Tamil](README-TA.md)

## Memory Match Game

### Overview
The Memory Match game is a fun way to take a mental break. It uses real meme images from the Memotion dataset.

### Setup Instructions

To ensure the Memory Match game displays real meme images:

1. Make sure the `frontend/public/memes` directory exists:
   ```
   mkdir -p frontend/public/memes
   ```

2. Copy meme images from the dataset to the public directory:
   ```
   # Copy 20 meme images from the dataset
   find ./backend/datasets/meme/memotion_dataset_7k/images -type f -name "*.jpg" | head -20 | xargs -I {} cp {} frontend/public/memes/
   ```

3. Alternatively, you can manually copy images to the `frontend/public/memes` directory. The game will look for images with these naming patterns:
   - `image_XXXX.jpg` (from dataset)
   - `meme_XX.jpg` (numbered memes)

4. You can test if images are accessible by opening the test page:
   ```
   http://localhost:5173/test-memes.html
   ```

### Troubleshooting

If memes aren't displaying:
1. Check that images exist in the `frontend/public/memes` directory
2. Make sure the development server is running with `npm run dev` in the frontend directory
3. Try accessing the test page to verify images are loading correctly

### Running the Game Locally

1. **Set up the dataset**
   Make sure the Memotion dataset is downloaded and prepared:
   ```bash
   cd backend
   ./kaggle_memes/setup_meme_game.sh
   ```
   This downloads approximately 7000 real meme images from the Memotion dataset.

2. **Start the backend API**
   ```bash
   cd backend
   python3 run_meme_server.py
   ```
   This will start the FastAPI server on port 8001. The server provides both API endpoints for meme data and direct access to meme images from the dataset.

3. **Start the frontend**
   ```bash
   cd frontend
   npm run dev
   ```

4. **Access the game**
   Open your browser to http://localhost:5173 and navigate to the Games section.

### API Communication
The game uses real memes from the dataset and communicates with the backend via:
- `GET /api/memes/real` - Get a list of real meme images directly from the dataset
- `GET /api/memes` - Fallback API to fetch meme data 
- `GET /api/memes/{image_name}` - Get a specific meme image
- `GET /meme-images/{image_name}` - Direct access to meme images in the dataset

### Deployment
For deployment on Railway:
1. Make sure the dataset is properly set up on the server.
2. Update the `VITE_MEME_API_URL` in the frontend `.env` file to point to your deployed backend URL.
3. Ensure the API server has access to the meme images directory.

