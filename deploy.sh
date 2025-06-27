#!/bin/bash

# AWS Elastic Beanstalk Deployment Script
# This script helps deploy the tornado prediction app to AWS

echo "🚀 Starting deployment to AWS Elastic Beanstalk..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "📦 Installing EB CLI..."
    pip install awsebcli
fi

# Create deployment package
echo "📦 Creating deployment package..."
zip -r deployment.zip . -x "*.git*" "node_modules/*" "__pycache__/*" "*.pyc" ".env*" "venv/*" "tornado_env_new/*"

# Initialize EB application (if not already done)
echo "🔧 Initializing Elastic Beanstalk application..."
eb init tornado-prediction-app --region us-east-1 --platform "Python 3.11" --interactive

# Deploy to EB
echo "🚀 Deploying to Elastic Beanstalk..."
eb deploy tornado-prediction-env --region us-east-1

echo "✅ Deployment completed!"
echo "🌐 Your app should be available at: http://tornado-prediction-env.us-east-1.elasticbeanstalk.com" 