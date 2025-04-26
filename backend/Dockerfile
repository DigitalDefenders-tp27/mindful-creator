FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH="/app"
ENV PORT=8000

# Expose the application port
EXPOSE ${PORT}

# Command to run the application
CMD ["python", "run_server.py"] 