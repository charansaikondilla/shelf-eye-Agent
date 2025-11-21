# 🚀 Google Cloud Run Deployment Guide

## Quick Start - Deploy in 3 Steps

### Step 1: Open Google Cloud Shell
1. Go to: https://console.cloud.google.com/
2. Click the **Cloud Shell** icon (>_) in top-right corner
3. Wait for terminal to load

### Step 2: Clone Your Repository
```bash
git clone https://github.com/charansaikondilla/shelf-eye-Agent.git
cd shelf-eye-Agent
```

### Step 3: Run Deployment Script
```bash
chmod +x deploy-to-cloud-run.sh
./deploy-to-cloud-run.sh
```

**That's it!** Your app will be deployed in 5-10 minutes.

---

## 📋 Deployment Configuration

**Your Settings:**
- **Project ID:** loyal-oath-384919
- **Region:** us-central1 (Iowa, USA)
- **Service Name:** shelf-eye-agent
- **Access:** Public (anyone can access)
- **API Key:** Securely configured as environment variable

---

## 🖥️ Alternative: Deploy from Local Machine (Windows)

If you want to deploy from your Windows machine instead of Cloud Shell:

### Prerequisites
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Open PowerShell as Administrator

### Run Deployment
```powershell
cd "d:\self eye\shelf-eye"
.\deploy-to-cloud-run.ps1
```

---

## 📦 What Gets Deployed

✅ **FastAPI Application** (main.py)
✅ **Docker Container** (built from Dockerfile)
✅ **Environment Variables** (API keys securely set)
✅ **Cloud Storage Bucket** (for reference images)
✅ **Public HTTPS URL** (automatically provisioned)
✅ **Auto-scaling** (handles 0-10 concurrent requests)
✅ **Health Monitoring** (automatic health checks)

---

## 🔍 After Deployment

### Your Service URL
```
https://shelf-eye-agent-xxxxxxxxxx-uc.a.run.app
```
The deployment script will show you the exact URL.

### Upload Reference Image
```bash
# From Cloud Shell or local terminal
curl -X POST https://your-service-url/admin/upload-reference \
  -F 'file=@backend_reference/correct_shelf.jpg'
```

### Access Web Interface
Open in browser: `https://your-service-url`

### Check Health
```bash
curl https://your-service-url/health
```

### View Logs
```bash
gcloud run services logs read shelf-eye-agent \
  --region us-central1 \
  --project loyal-oath-384919
```

Or visit:
https://console.cloud.google.com/run/detail/us-central1/shelf-eye-agent/logs?project=loyal-oath-384919

---

## 🛠️ Manual Deployment Steps (If Script Fails)

### 1. Set Project
```bash
gcloud config set project loyal-oath-384919
```

### 2. Enable APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 3. Build Container
```bash
gcloud builds submit --tag gcr.io/loyal-oath-384919/shelf-eye-agent
```

### 4. Deploy to Cloud Run
```bash
gcloud run deploy shelf-eye-agent \
  --image gcr.io/loyal-oath-384919/shelf-eye-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --set-env-vars GEMINI_API_KEY=AIzaSyCDAZDnSemHlED_Ij99DHyKrq6ZPWd7bZw
```

### 5. Get Service URL
```bash
gcloud run services describe shelf-eye-agent \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

---

## 📊 Cost Estimate

**Google Cloud Run Pricing (Free Tier):**
- First 2 million requests/month: **FREE**
- 180,000 vCPU-seconds/month: **FREE**
- 360,000 GiB-seconds/month: **FREE**

**Your Configuration:**
- Memory: 1GB
- CPU: 1 vCPU
- Expected cost: **$0-5/month** for typical usage

---

## 🔐 Security Features

✅ **HTTPS Only** - Automatic SSL/TLS encryption
✅ **Environment Variables** - API keys never exposed in code
✅ **IAM Controls** - Managed by Google Cloud IAM
✅ **DDoS Protection** - Built-in Google infrastructure
✅ **Auto-patching** - Container runtime auto-updates

---

## 🐛 Troubleshooting

### Error: "Permission denied"
```bash
# Ensure you're authenticated
gcloud auth login

# Set correct project
gcloud config set project loyal-oath-384919
```

### Error: "APIs not enabled"
```bash
# Enable all required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com
```

### Error: "Container build failed"
```bash
# Check Docker syntax
docker build -t test .

# Check logs
gcloud builds list --limit 5
```

### Service not responding
```bash
# Check logs
gcloud run services logs read shelf-eye-agent --region us-central1

# Check service status
gcloud run services describe shelf-eye-agent --region us-central1
```

---

## 🔄 Update Deployment

After making code changes:

```bash
# Commit to GitHub
git add .
git commit -m "Updated features"
git push

# Redeploy
cd shelf-eye-Agent
./deploy-to-cloud-run.sh
```

---

## 📱 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-service-url/health
# Expected: {"status":"healthy","service":"shelf-eye-agent"}
```

### 2. Upload Test Image
```bash
curl -X POST https://your-service-url/audit \
  -F "file=@test_shelf.jpg"
```

### 3. Web Interface
Open browser: `https://your-service-url`

---

## 🎯 Quick Reference Commands

```bash
# View service details
gcloud run services describe shelf-eye-agent --region us-central1

# View logs
gcloud run services logs read shelf-eye-agent --region us-central1

# Update environment variable
gcloud run services update shelf-eye-agent \
  --region us-central1 \
  --update-env-vars NEW_VAR=value

# Delete service
gcloud run services delete shelf-eye-agent --region us-central1

# List all Cloud Run services
gcloud run services list
```

---

## ✅ Deployment Checklist

- [ ] Google Cloud account active
- [ ] Project ID: loyal-oath-384919
- [ ] Cloud Shell or gcloud CLI installed
- [ ] Repository cloned
- [ ] Deployment script executed
- [ ] Service URL received
- [ ] Health check passed
- [ ] Reference image uploaded
- [ ] Web interface accessible
- [ ] Test audit completed

---

**🎉 Ready to Deploy!**

Run this in Google Cloud Shell:
```bash
git clone https://github.com/charansaikondilla/shelf-eye-Agent.git
cd shelf-eye-Agent
chmod +x deploy-to-cloud-run.sh
./deploy-to-cloud-run.sh
```
