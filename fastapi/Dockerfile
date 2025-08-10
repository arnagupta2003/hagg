# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables (can be overridden at runtime)
ENV DB_HOST=127.0.0.1
ENV DB_USER=postgres
ENV DB_PASS=postgres
ENV DB_NAME=hagg

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
