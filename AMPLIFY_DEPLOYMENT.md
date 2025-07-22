# AWS Amplify Deployment Guide

This guide will help you deploy your Natural Disaster Prediction application to AWS Amplify.

## 🚀 Quick Start

### 1. Frontend Deployment (AWS Amplify)

The frontend will be deployed to AWS Amplify, which provides:

- Global CDN
- Automatic HTTPS
- CI/CD pipeline
- Preview deployments

### 2. Backend Deployment (Separate)

The FastAPI backend should be deployed separately to:

- AWS Lambda + API Gateway
- AWS ECS/Fargate
- AWS EC2
- Heroku
- Railway
- Render

## 📋 Prerequisites

1. **AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **GitHub Repository**: Push your code to GitHub
3. **AWS Amplify Console**: Access via AWS Console

## 🔧 Frontend Deployment Steps

### Step 1: Push Code to GitHub

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Amplify deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### Step 2: Connect to AWS Amplify

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify)
2. Click **"New app"** → **"Host web app"**
3. Choose **"GitHub"** as your repository source
4. Authorize AWS Amplify to access your GitHub account
5. Select your repository and branch (main)
6. Click **"Next"**

### Step 3: Configure Build Settings

Amplify will automatically detect the `amplify.yml` file. The build configuration:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - echo "Installing frontend dependencies..."
        - cd frontend
        - npm ci
    build:
      commands:
        - echo "Building frontend application..."
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - "**/*"
  cache:
    paths:
      - frontend/node_modules/**/*
```

### Step 4: Set Environment Variables

In the Amplify Console, go to **"Environment variables"** and add:

```
VITE_API_BASE_URL=https://your-backend-url.com
```

**Important**: Replace `your-backend-url.com` with your actual backend URL.

### Step 5: Deploy

1. Click **"Save and deploy"**
2. Amplify will automatically build and deploy your frontend
3. Your app will be available at: `https://main.xxxxxxxxx.amplifyapp.com`

## 🔧 Backend Deployment Options

### Option 1: AWS Lambda + API Gateway (Recommended)

**Pros**: Serverless, auto-scaling, pay-per-use
**Cons**: Cold starts, 15-minute timeout limit

#### Setup Steps:

1. **Install AWS SAM CLI**:

   ```bash
   # macOS
   brew install aws-sam-cli

   # Windows
   # Download from AWS website
   ```

2. **Create SAM template** (`template.yaml`):

   ```yaml
   AWSTemplateFormatVersion: "2010-09-09"
   Transform: AWS::Serverless-2016-10-31

   Resources:
     NaturalDisasterAPI:
       Type: AWS::Serverless::Function
       Properties:
         CodeUri: backend/
         Handler: app.main.handler
         Runtime: python3.10
         Timeout: 900
         MemorySize: 1024
         Environment:
           Variables:
             PYTHONPATH: /var/task
         Events:
           Api:
             Type: Api
             Properties:
               Path: /{proxy+}
               Method: ANY
   ```

3. **Deploy**:
   ```bash
   sam build
   sam deploy --guided
   ```

### Option 2: AWS ECS/Fargate

**Pros**: Full control, no timeout limits
**Cons**: More complex setup, higher costs

### Option 3: Heroku (Easiest)

**Pros**: Simple deployment, good free tier
**Cons**: Limited resources on free tier

#### Setup Steps:

1. **Install Heroku CLI**:

   ```bash
   # macOS
   brew install heroku/brew/heroku
   ```

2. **Create Procfile** in root directory:

   ```
   web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Deploy**:
   ```bash
   heroku create your-app-name
   git add .
   git commit -m "Add Heroku deployment"
   git push heroku main
   ```

### Option 4: Railway

**Pros**: Simple, good free tier, automatic deployments
**Cons**: Limited resources

#### Setup Steps:

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Set build command: `cd backend && pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 🔗 Connecting Frontend to Backend

### 1. Update Environment Variables

Once your backend is deployed, update the Amplify environment variable:

```
VITE_API_BASE_URL=https://your-backend-url.com
```

### 2. Update CORS Settings

In your backend, ensure CORS allows your Amplify domain:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://*.amplifyapp.com",  # Allow all Amplify domains
        "https://*.amplifyapp.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔍 Testing Your Deployment

### 1. Test Frontend

- Visit your Amplify URL
- Test the prediction functionality
- Check browser console for errors

### 2. Test Backend

- Visit `https://your-backend-url.com/docs`
- Test API endpoints
- Check health endpoint: `https://your-backend-url.com/api/health`

### 3. Test Integration

- Make a prediction from the frontend
- Verify it calls the backend correctly
- Check for CORS errors

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**:

   - Ensure backend CORS settings include Amplify domain
   - Check browser console for CORS errors

2. **API Connection Failed**:

   - Verify `VITE_API_BASE_URL` is correct
   - Test backend URL directly
   - Check backend logs

3. **Build Failures**:

   - Check Amplify build logs
   - Verify `amplify.yml` configuration
   - Ensure all dependencies are in `package.json`

4. **Environment Variables**:
   - Verify environment variables are set in Amplify
   - Check variable names (must start with `VITE_`)

## 📊 Monitoring

### Amplify Monitoring:

- Build status and logs
- Performance metrics
- Error tracking

### Backend Monitoring:

- Use your hosting provider's monitoring
- Set up logging and alerts
- Monitor API response times

## 🔄 Continuous Deployment

### Automatic Deployments:

- Push to `main` branch triggers Amplify build
- Preview deployments for pull requests
- Branch-specific environments

### Manual Deployments:

- Trigger builds from Amplify Console
- Rollback to previous versions
- Promote preview deployments

## 💰 Cost Optimization

### Frontend (Amplify):

- Free tier: 1,000 build minutes/month
- Free tier: 15 GB storage
- Free tier: 15 GB data transfer

### Backend:

- **Lambda**: Pay per request (~$0.20 per 1M requests)
- **Heroku**: Free tier available
- **Railway**: Free tier available
- **ECS**: Pay for compute resources

## 🎉 Success!

Once deployed, your application will be available at:

- **Frontend**: `https://your-app.amplifyapp.com`
- **Backend**: `https://your-backend-url.com`
- **API Docs**: `https://your-backend-url.com/docs`

## 📞 Support

- **AWS Amplify**: [Documentation](https://docs.aws.amazon.com/amplify/)
- **AWS Support**: Available with paid plans
- **Community**: Stack Overflow, AWS Forums
