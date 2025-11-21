# Shelf-Eye Agent - Cloud Run Deployment Script (PowerShell)
# This script deploys the Shelf-Eye Agent to Google Cloud Run

$ErrorActionPreference = "Stop"

Write-Host "🚀 Shelf-Eye Agent Deployment Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

# Check if gcloud is installed
if (-not (Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: gcloud CLI is not installed" -ForegroundColor Red
    Write-Host "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
}

# Get project ID
$PROJECT_ID = gcloud config get-value project 2>$null
if (-not $PROJECT_ID) {
    Write-Host "❌ Error: No Google Cloud project set" -ForegroundColor Red
    Write-Host "Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
}

Write-Host "📦 Project ID: $PROJECT_ID" -ForegroundColor Green
$SERVICE_NAME = "shelf-eye"
$REGION = "us-central1"

# Check for GEMINI_API_KEY
if (-not $env:GEMINI_API_KEY) {
    Write-Host "⚠️  Warning: GEMINI_API_KEY not set in environment" -ForegroundColor Yellow
    Write-Host "Set it with: `$env:GEMINI_API_KEY='your-api-key'"
}

# Enable required APIs
Write-Host ""
Write-Host "🔧 Enabling required Google Cloud APIs..." -ForegroundColor Cyan
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Build container image
Write-Host ""
Write-Host "🏗️  Building container image..." -ForegroundColor Cyan
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
Write-Host ""
Write-Host "🚀 Deploying to Cloud Run..." -ForegroundColor Cyan
gcloud run deploy $SERVICE_NAME `
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --memory 1Gi `
  --cpu 1 `
  --timeout 300 `
  --set-env-vars GEMINI_API_KEY=$env:GEMINI_API_KEY

# Get service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'

Write-Host ""
Write-Host "✅ Deployment successful!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "🌐 Service URL: $SERVICE_URL" -ForegroundColor Green
Write-Host "📊 API Docs: $SERVICE_URL/docs" -ForegroundColor Green
Write-Host "🔍 Test Upload: $SERVICE_URL" -ForegroundColor Green
Write-Host ""
Write-Host "Test with curl:" -ForegroundColor Yellow
Write-Host "curl -X POST -F 'file=@your-shelf-image.jpg' $SERVICE_URL/audit"
