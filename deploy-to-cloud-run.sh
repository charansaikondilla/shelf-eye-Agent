#!/bin/bash

# =============================================================================
# Shelf-Eye Agent - Google Cloud Run Deployment Script
# =============================================================================

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="loyal-oath-384919"
REGION="us-central1"
SERVICE_NAME="shelf-eye-agent"
GEMINI_API_KEY="AIzaSyCDAZDnSemHlED_Ij99DHyKrq6ZPWd7bZw"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Shelf-Eye Agent Cloud Run Deployment              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Set project
echo -e "${YELLOW}[1/8] Setting Google Cloud Project...${NC}"
gcloud config set project ${PROJECT_ID}
echo -e "${GREEN}✓ Project set to: ${PROJECT_ID}${NC}"
echo ""

# Step 2: Enable required APIs
echo -e "${YELLOW}[2/8] Enabling required Google Cloud APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable artifactregistry.googleapis.com
echo -e "${GREEN}✓ APIs enabled successfully${NC}"
echo ""

# Step 3: Verify Dockerfile exists
echo -e "${YELLOW}[3/8] Verifying Dockerfile...${NC}"
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}✗ Error: Dockerfile not found!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dockerfile found${NC}"
echo ""

# Step 4: Build container image
echo -e "${YELLOW}[4/8] Building Docker container...${NC}"
echo -e "${BLUE}This may take 3-5 minutes...${NC}"
gcloud builds submit --tag ${IMAGE_NAME} .
echo -e "${GREEN}✓ Container built successfully${NC}"
echo ""

# Step 5: Create backend_reference directory in Cloud Storage (optional but recommended)
echo -e "${YELLOW}[5/8] Setting up Cloud Storage for reference images...${NC}"
BUCKET_NAME="${PROJECT_ID}-shelf-eye-reference"
if gsutil ls -b gs://${BUCKET_NAME} 2>/dev/null; then
    echo -e "${GREEN}✓ Bucket already exists: ${BUCKET_NAME}${NC}"
else
    gsutil mb -p ${PROJECT_ID} -l ${REGION} gs://${BUCKET_NAME}
    echo -e "${GREEN}✓ Created bucket: ${BUCKET_NAME}${NC}"
fi
echo ""

# Step 6: Deploy to Cloud Run
echo -e "${YELLOW}[6/8] Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME} \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars GEMINI_API_KEY=${GEMINI_API_KEY} \
  --set-env-vars GOOGLE_CLOUD_PROJECT=${PROJECT_ID}

echo -e "${GREEN}✓ Deployment completed${NC}"
echo ""

# Step 7: Get service URL
echo -e "${YELLOW}[7/8] Retrieving service URL...${NC}"
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --format 'value(status.url)')

echo -e "${GREEN}✓ Service URL: ${SERVICE_URL}${NC}"
echo ""

# Step 8: Test deployment
echo -e "${YELLOW}[8/8] Testing deployment...${NC}"
HEALTH_CHECK=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL}/health)

if [ "$HEALTH_CHECK" = "200" ]; then
    echo -e "${GREEN}✓ Health check passed!${NC}"
else
    echo -e "${RED}✗ Health check failed (HTTP ${HEALTH_CHECK})${NC}"
fi
echo ""

# Final summary
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                 DEPLOYMENT SUCCESSFUL! 🎉                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Your Shelf-Eye Agent is now live at:${NC}"
echo -e "${YELLOW}${SERVICE_URL}${NC}"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo -e "1. Upload reference image:"
echo -e "   ${YELLOW}curl -X POST ${SERVICE_URL}/admin/upload-reference \\${NC}"
echo -e "   ${YELLOW}     -F 'file=@/path/to/correct_shelf.jpg'${NC}"
echo ""
echo -e "2. Access the web interface:"
echo -e "   ${YELLOW}${SERVICE_URL}${NC}"
echo ""
echo -e "3. Test the API:"
echo -e "   ${YELLOW}curl ${SERVICE_URL}/health${NC}"
echo ""
echo -e "${GREEN}Logs and monitoring:${NC}"
echo -e "https://console.cloud.google.com/run/detail/${REGION}/${SERVICE_NAME}/logs?project=${PROJECT_ID}"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
