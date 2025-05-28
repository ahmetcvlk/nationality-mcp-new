FROM python:3.11-slim

WORKDIR /app

# Set environment variables for unbuffered Python output
ENV PYTHONUNBUFFERED=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the MCP server
CMD ["python3", "-u", "server.py"]
