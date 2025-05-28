FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables for unbuffered Python output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make server.py executable
RUN chmod +x server.py

# Expose port (if needed for health checks)
EXPOSE 8000

# Run the MCP server
CMD ["python3", "-u", "server.py"]
