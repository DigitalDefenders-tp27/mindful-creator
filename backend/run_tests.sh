#!/usr/bin/env bash
# Comprehensive backend testing script

set -e
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_FILE="backend_test_${TIMESTAMP}.log"

# Load environment variables if .env exists
if [ -f .env ]; then
  echo "Loading environment variables from .env file"
  export $(grep -v '^#' .env | xargs)
fi

# Default API base URL
API_BASE=${API_BASE:-"https://api.tiezhu.org"}
echo "Using API base URL: ${API_BASE}"

# Function to handle errors
function handle_error {
  echo "ERROR: Test execution failed!"
  echo "Check the log file for details: ${LOG_FILE}"
  exit 1
}

# Set up error handling
trap handle_error ERR

echo "Starting backend testing at $(date)"
echo "Results will be logged to ${LOG_FILE}"

# Run the test suite
python3 tests/test_complete_flow.py "${API_BASE}" | tee "${LOG_FILE}"

# Check the exit status
TEST_STATUS=$?
if [ $TEST_STATUS -eq 0 ]; then
  echo "All tests passed successfully!"
else
  echo "Some tests failed. Check the log for details."
  exit $TEST_STATUS
fi

echo "Testing completed at $(date)" 