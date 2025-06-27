# AWS Deployment Guide

This guide explains how to deploy the Quantum Natural Disaster Prediction System to AWS using Elastic Beanstalk and GitHub Actions.

## Prerequisites

1. **AWS Account**: You need an AWS account with appropriate permissions
2. **AWS CLI**: Install AWS CLI and configure it with your credentials
3. **GitHub Repository**: Your code should be in a GitHub repository

## Setup Steps

### 1. AWS Setup

#### Create IAM User for GitHub Actions
1. Go to AWS IAM Console
2. Create a new user with programmatic access
3. Attach the following policies:
   - `AWSElasticBeanstalkFullAccess`
   - `AWSElasticBeanstalkService`
4. Save the Access Key ID and Secret Access Key

#### Create Elastic Beanstalk Application
1. Go to AWS Elastic Beanstalk Console
2. Create a new application named `tornado-prediction-app`
3. Create a new environment named `tornado-prediction-env`
4. Choose Python 3.11 platform
5. Upload a sample application to initialize the environment

### 2. GitHub Secrets Setup

In your GitHub repository, go to Settings > Secrets and variables > Actions, and add:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### 3. Environment Variables

In AWS Elastic Beanstalk Console:
1. Go to your environment
2. Configuration > Software
3. Add environment variables:
   - `OPENWEATHERMAP_API_KEY`: Your actual API key
   - `FLASK_ENV`: production
   - `FLASK_DEBUG`: false

## Deployment

### Automatic Deployment (GitHub Actions)
Every push to the `main` branch will automatically trigger deployment.

### Manual Deployment
```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

## Application URL

After deployment, your application will be available at:
```
http://tornado-prediction-env.us-east-1.elasticbeanstalk.com
```

## Monitoring

- **AWS Console**: Monitor your application in the Elastic Beanstalk console
- **Logs**: View application logs in the AWS console
- **Health Checks**: The application includes health check endpoints

## Troubleshooting

### Common Issues

1. **Environment Variables**: Make sure your OpenWeatherMap API key is set in AWS
2. **Dependencies**: Check that all requirements are in `requirements.txt`
3. **Port Configuration**: The app runs on port 8000 (configured in Procfile)
4. **Memory Issues**: The t2.micro instance has limited memory, consider upgrading if needed

### Logs
View logs in AWS Elastic Beanstalk Console:
1. Go to your environment
2. Click on "Logs"
3. Request "Last 100 lines" or "Full logs"

## Cost Optimization

- **Free Tier**: AWS offers a free tier for new accounts
- **Instance Type**: Using t2.micro for development (free tier eligible)
- **Auto Scaling**: Configured to scale based on CPU usage
- **Shutdown**: Remember to terminate environments when not in use

## Security

- **HTTPS**: Enable HTTPS in Elastic Beanstalk configuration
- **Security Groups**: Configure security groups to restrict access
- **Environment Variables**: Never commit API keys to the repository
- **IAM Roles**: Use least privilege principle for IAM permissions

## Updates

To update the application:
1. Push changes to the `main` branch
2. GitHub Actions will automatically deploy
3. Monitor the deployment in AWS console

## Support

For issues with:
- **AWS**: Check AWS documentation and support
- **Application**: Check the logs and error messages
- **Deployment**: Verify GitHub Actions workflow 