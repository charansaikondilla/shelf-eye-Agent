# =============================================================================
# Shelf-Eye Agent - Google Cloud Run Deployment Script (PowerShell)
# =============================================================================

$ErrorActionPreference = "Stop"

# Configuration
$PROJECT_ID = "loyal-oath-384919"
$REGION = "us-central1"
$SERVICE_NAME = "shelf-eye-agent"
$GEMINI_API_KEY = "AIzaSyCDAZDnSemHlED_Ij99DHyKrq6ZPWd7bZw"
$IMAGE_NAME = "gcr.io/$PROJECT_ID/$SERVICE_NAME"

function Write-ColorOutput($ForegroundColor, $Message) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $fc
}

Write-ColorOutput Blue "╔════════════════════════════════════════════════════════════╗"
Write-ColorOutput Blue "║         Shelf-Eye Agent Cloud Run Deployment              ║"
Write-ColorOutput Blue "╚════════════════════════════════════════════════════════════╝"
Write-Output ""

# Step 1: Set project
Write-ColorOutput Yellow "[1/8] Setting Google Cloud Project..."
gcloud config set project $PROJECT_ID
Write-ColorOutput Green "✓ Project set to: $PROJECT_ID"
Write-Output ""

# Step 2: Enable required APIs
Write-ColorOutput Yellow "[2/8] Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com
Write-ColorOutput Green "✓ APIs enabled successfully"
Write-Output ""

# Step 3: Verify Dockerfile exists
Write-ColorOutput Yellow "[3/8] Verifying Dockerfile..."
if (!(Test-Path "Dockerfile")) {
    Write-ColorOutput Red "✗ Error: Dockerfile not found!"
    exit 1
}
Write-ColorOutput Green "✓ Dockerfile found"
Write-Output ""

# Step 4: Build container image
Write-ColorOutput Yellow "[4/8] Building Docker container..."
Write-ColorOutput Blue "This may take 3-5 minutes..."
gcloud builds submit --tag $IMAGE_NAME .
Write-ColorOutput Green "✓ Container built successfully"
Write-Output ""

# Step 5: Create Cloud Storage bucket
Write-ColorOutput Yellow "[5/8] Setting up Cloud Storage for reference images..."
$BUCKET_NAME = "$PROJECT_ID-shelf-eye-reference"
$bucketExists = gsutil ls -b "gs://$BUCKET_NAME" 2>$null
if ($bucketExists) {
    Write-ColorOutput Green "✓ Bucket already exists: $BUCKET_NAME"
} else {
    gsutil mb -p $PROJECT_ID -l $REGION "gs://$BUCKET_NAME"
    Write-ColorOutput Green "✓ Created bucket: $BUCKET_NAME"
}
Write-Output ""

# Step 6: Deploy to Cloud Run
Write-ColorOutput Yellow "[6/8] Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME `
  --image $IMAGE_NAME `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --port 8080 `
  --memory 1Gi `
  --cpu 1 `
  --timeout 300 `
  --max-instances 10 `
  --set-env-vars "GEMINI_API_KEY=$GEMINI_API_KEY" `
  --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

Write-ColorOutput Green "✓ Deployment completed"
Write-Output ""

# Step 7: Get service URL
Write-ColorOutput Yellow "[7/8] Retrieving service URL..."
$SERVICE_URL = gcloud run services describe $SERVICE_NAME `
  --platform managed `
  --region $REGION `
  --format 'value(status.url)'

Write-ColorOutput Green "✓ Service URL: $SERVICE_URL"
Write-Output ""

# Step 8: Test deployment
Write-ColorOutput Yellow "[8/8] Testing deployment..."
try {
    $response = Invoke-WebRequest -Uri "$SERVICE_URL/health" -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-ColorOutput Green "✓ Health check passed!"
    }
} catch {
    Write-ColorOutput Red "✗ Health check failed"
}
Write-Output ""

# Final summary
Write-ColorOutput Blue "╔════════════════════════════════════════════════════════════╗"
Write-ColorOutput Blue "║                 DEPLOYMENT SUCCESSFUL! 🎉                  ║"
Write-ColorOutput Blue "╚════════════════════════════════════════════════════════════╝"
Write-Output ""
Write-ColorOutput Green "Your Shelf-Eye Agent is now live at:"
Write-ColorOutput Yellow $SERVICE_URL
Write-Output ""
Write-ColorOutput Green "Next Steps:"
Write-Output "1. Upload reference image:"
Write-ColorOutput Yellow "   curl -X POST $SERVICE_URL/admin/upload-reference \"
Write-ColorOutput Yellow "     -F 'file=@/path/to/correct_shelf.jpg'"
Write-Output ""
Write-Output "2. Access the web interface:"
Write-ColorOutput Yellow "   $SERVICE_URL"
Write-Output ""
Write-Output "3. Test the API:"
Write-ColorOutput Yellow "   curl $SERVICE_URL/health"
Write-Output ""
Write-ColorOutput Green "Logs and monitoring:"
Write-Output "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/logs?project=$PROJECT_ID"
Write-Output ""
Write-ColorOutput Blue "═══════════════════════════════════════════════════════════"
