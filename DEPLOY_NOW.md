# 🚀 DEPLOY NOW - Step by Step Instructions

## ✅ Everything is Ready!

Your deployment scripts are now on GitHub and ready to use.

---

## 🎯 OPTION 1: Deploy from Google Cloud Shell (RECOMMENDED)

### Step 1: Open Google Cloud Shell
1. Go to: **https://console.cloud.google.com/**
2. Click the **Cloud Shell icon** (>_) in the top-right corner
3. Wait for the terminal to open (takes ~10 seconds)

### Step 2: Clone and Deploy
Copy and paste these commands **one by one** into Cloud Shell:

```bash
# Clone your repository
git clone https://github.com/charansaikondilla/shelf-eye-Agent.git

# Navigate to project
cd shelf-eye-Agent

# Make script executable
chmod +x deploy-to-cloud-run.sh

# Run deployment
./deploy-to-cloud-run.sh
```

### Step 3: Wait for Deployment
- Build takes: **3-5 minutes**
- Deployment takes: **1-2 minutes**
- Total time: **5-7 minutes**

You'll see progress bars and status messages.

### Step 4: Get Your URL
At the end, you'll see:
```
✓ Service URL: https://shelf-eye-agent-xxxxxxxxxx-uc.a.run.app
```

**That's your live URL!** Copy it and open in browser.

---

## 🎯 OPTION 2: Deploy from Your Windows PC

### Prerequisites
Install Google Cloud SDK:
1. Download: https://cloud.google.com/sdk/docs/install-sdk#windows
2. Run installer
3. Follow setup wizard
4. Restart PowerShell

### Deploy Commands
```powershell
# Open PowerShell as Administrator
cd "d:\self eye\shelf-eye"

# Authenticate with Google Cloud
gcloud auth login

# Run deployment
.\deploy-to-cloud-run.ps1
```

---

## 📋 What Happens During Deployment

```
[1/8] Setting Google Cloud Project...        ✓ Done in 2s
[2/8] Enabling APIs...                        ✓ Done in 15s
[3/8] Verifying Dockerfile...                 ✓ Done in 1s
[4/8] Building Docker container...            ✓ Done in 180s
[5/8] Setting up Cloud Storage...             ✓ Done in 5s
[6/8] Deploying to Cloud Run...               ✓ Done in 30s
[7/8] Retrieving service URL...               ✓ Done in 2s
[8/8] Testing deployment...                   ✓ Done in 3s

╔════════════════════════════════════════════════════════════╗
║                 DEPLOYMENT SUCCESSFUL! 🎉                  ║
╚════════════════════════════════════════════════════════════╝

Your Shelf-Eye Agent is now live at:
https://shelf-eye-agent-xxxxxxxxxx-uc.a.run.app
```

---

## 🔍 After Deployment - Next Steps

### 1. Upload Reference Image
```bash
curl -X POST https://your-service-url/admin/upload-reference \
  -F 'file=@backend_reference/correct_shelf.jpg'
```

Or use the web interface (coming soon with admin panel).

### 2. Test the Web Interface
Open in browser:
```
https://your-service-url
```

You should see the Shelf-Eye Agent upload interface.

### 3. Test an Audit
Upload a test shelf image and click "Analyze"!

---

## 📊 Your Deployment Details

**Configuration:**
- **Project ID:** loyal-oath-384919
- **Region:** us-central1 (Iowa, USA)
- **Service:** shelf-eye-agent
- **Memory:** 1GB RAM
- **CPU:** 1 vCPU
- **Timeout:** 5 minutes
- **Max Instances:** 10 (auto-scales)
- **Access:** Public (anyone can access)

**Your API Key:** Securely stored as environment variable (never exposed)

---

## 🔗 Important URLs

### Service URL
```
https://shelf-eye-agent-[unique-id]-uc.a.run.app
```
(You'll get this after deployment)

### Cloud Console
```
https://console.cloud.google.com/run/detail/us-central1/shelf-eye-agent?project=loyal-oath-384919
```

### Logs
```
https://console.cloud.google.com/run/detail/us-central1/shelf-eye-agent/logs?project=loyal-oath-384919
```

### Metrics
```
https://console.cloud.google.com/run/detail/us-central1/shelf-eye-agent/metrics?project=loyal-oath-384919
```

---

## 🐛 Troubleshooting

### If Deployment Fails

**Error: "APIs not enabled"**
```bash
# Manually enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

**Error: "Permission denied"**
```bash
# Re-authenticate
gcloud auth login

# Set project
gcloud config set project loyal-oath-384919
```

**Error: "Quota exceeded"**
- You may need to enable billing on your Google Cloud project
- Go to: https://console.cloud.google.com/billing
- Link a billing account (Free tier available)

**Service returns 500 error**
```bash
# Check logs
gcloud run services logs read shelf-eye-agent \
  --region us-central1 \
  --limit 50
```

---

## 💰 Cost Information

**Google Cloud Run Free Tier (per month):**
- 2 million requests: **FREE**
- 360,000 GB-seconds: **FREE**
- 180,000 vCPU-seconds: **FREE**

**Your Expected Cost:**
- Development/Testing: **$0/month** (within free tier)
- Light Production: **$0-5/month**
- Heavy Production: **$10-50/month**

---

## 🔄 Update Your Deployment

When you make code changes:

```bash
# In Cloud Shell
cd shelf-eye-Agent

# Pull latest changes
git pull

# Redeploy
./deploy-to-cloud-run.sh
```

---

## ✅ Deployment Checklist

Before deploying, make sure:

- [x] Google Cloud account is active
- [x] Project ID is correct: loyal-oath-384919
- [x] Billing is enabled (can use free tier)
- [x] Code is pushed to GitHub
- [x] Deployment scripts are ready

**You're all set! Ready to deploy? 🚀**

---

## 🎬 Quick Start Command (Copy-Paste This)

```bash
git clone https://github.com/charansaikondilla/shelf-eye-Agent.git && cd shelf-eye-Agent && chmod +x deploy-to-cloud-run.sh && ./deploy-to-cloud-run.sh
```

Copy this single command and paste it into Google Cloud Shell. It will:
1. Clone your repo
2. Navigate to directory
3. Make script executable
4. Deploy everything

**Done in one command!** 🎉

---

## 📞 Need Help?

If deployment fails, check:
1. **Logs:** https://console.cloud.google.com/run/detail/us-central1/shelf-eye-agent/logs?project=loyal-oath-384919
2. **Build History:** https://console.cloud.google.com/cloud-build/builds?project=loyal-oath-384919
3. **Service Status:** https://console.cloud.google.com/run?project=loyal-oath-384919

---

**Ready? Let's deploy! Open Google Cloud Shell and run the commands above.** 🚀
