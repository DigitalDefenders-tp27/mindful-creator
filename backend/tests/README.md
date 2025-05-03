# YouTube API Testing

This directory contains tests for the YouTube API and NLP integration. The tests verify:

1. Fetching YouTube comments
2. Analyzing comments with the local NLP model
3. Analyzing comments with OpenRouter
4. Testing the complete API pipeline

## Running the Tests

### Prerequisites

- Make sure your backend server is running (or accessible at the URL specified in `BACKEND_URL` environment variable)
- Ensure you have the required environment variables set:
  - `YOUTUBE_API_KEY`: Your YouTube API key
  - `OPENROUTER_API_KEY`: Your OpenRouter API key
  - `BACKEND_URL` (optional): URL of your backend API (defaults to `http://localhost:8080`)

### Option 1: Simple Script

For a quick test with detailed output, run:

```bash
cd backend
python -m tests.run_analysis_test
```

This script will:
- Fetch comments from a test YouTube video
- Send them to the local NLP model
- Send them to OpenRouter
- Test the complete API endpoint

The script provides detailed logging of each step and its results.

### Option 2: Unit Tests

For more structured testing with assertions:

```bash
cd backend
python -m unittest tests.test_youtube_analysis
```

You can also run individual tests:

```bash
# Test just fetching YouTube comments
python -m unittest tests.test_youtube_analysis.TestYouTubeAnalysis.test_fetch_youtube_comments

# Test just the local NLP model
python -m unittest tests.test_youtube_analysis.TestYouTubeAnalysis.test_local_nlp_model

# Test just OpenRouter analysis
python -m unittest tests.test_youtube_analysis.TestYouTubeAnalysis.test_openrouter_analysis

# Test the complete pipeline
python -m unittest tests.test_youtube_analysis.TestYouTubeAnalysis.test_complete_pipeline
```

### Option 3: Performance Testing

To measure the time taken by each step in the analysis pipeline:

```bash
cd backend
python -m tests.performance_test
```

This script will:
- Fetch 100 comments from a specific YouTube video
- Time each step of the analysis process
- Output detailed timing information for each operation
- Save the results to a JSON file in the `tests/results` directory

The performance test measures:
- Time to fetch YouTube comments
- Time for local NLP model analysis
- Time for OpenRouter analysis
- Time for complete API endpoint call
- Total time for the entire process

## Troubleshooting

If you encounter issues:

1. Check if all required environment variables are set correctly
2. Verify that the backend server is running and accessible
3. Check the logs for detailed error messages
4. Ensure you have all required dependencies installed

## Common Issues

- **YouTube API quota exceeded**: The YouTube API has daily quotas. If exceeded, the tests will fail.
- **OpenRouter API key issues**: Ensure your OpenRouter API key is valid and has sufficient credits.
- **Network issues**: If testing against a remote backend, ensure network connectivity is available.
- **Missing dependencies**: Make sure all required Python packages are installed. 