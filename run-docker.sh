#!/bin/bash

echo "🚀 Natural Disaster Prediction App - Docker Setup"
echo "=================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully"
else
    echo "❌ Failed to build Docker image"
    exit 1
fi

# Run the container
echo "🚀 Starting the application..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Application started successfully"
    echo ""
    echo "🌐 Your application is now running at:"
    echo "   http://localhost:8080"
    echo ""
    echo "📊 To view logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 To stop the application:"
    echo "   docker-compose down"
    echo ""
    echo "🔄 To restart:"
    echo "   docker-compose restart"
else
    echo "❌ Failed to start the application"
    exit 1
fi 