# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y libmagic-dev && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y curl
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8008

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run mcp_server.py when the container launches
# CMD ["fastmcp", "run", "testmcp.py:mcp", "--transport", "http", "--port", "8008"]
CMD ["python3", "mcp_server.py"]