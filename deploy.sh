#!/bin/bash

# Shelf-Eye Agent - Cloud Run Deployment Script
# This script deploys the Shelf-Eye Agent to Google Cloud Run

set -e

echo "🚀 Shelf-Eye Agent Deployment Script"
echo "======================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed"
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No Google Cloud project set"
    echo "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo "📦 Project ID: $PROJECT_ID"
SERVICE_NAME="shelf-eye"
REGION="us-central1"

# Enable required APIs
echo ""
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Build container image
echo ""
echo "🏗️  Building container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)')

echo ""
echo "✅ Deployment successful!"
echo "======================================"
echo "🌐 Service URL: $SERVICE_URL"
echo "📊 API Docs: $SERVICE_URL/docs"
echo "🔍 Test Upload: $SERVICE_URL"
echo ""
echo "Test with curl:"
echo "curl -X POST -F 'file=@your-shelf-image.jpg' $SERVICE_URL/audit"
