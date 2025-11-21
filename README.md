# 🛒 Shelf-Eye Agent

AI-Powered Retail Shelf Auditing System using Google Gemini 2.5 Flash

## 🎯 Overview

Shelf-Eye Agent is an automated retail shelf auditing application that:
- ✅ Analyzes shelf photos in real-time
- ✅ Detects missing products
- ✅ Identifies misplaced items
- ✅ Reports quality issues
- ✅ Provides compliance scores
- ✅ Suggests improvements

**Powered by:** Google Gemini 2.5 Flash multimodal AI

---

## 🏗️ Architecture

### Components:
1. **FastAPI Backend** - RESTful API for image processing
2. **Google Gemini API** - AI vision analysis
3. **Web UI** - Simple interface for uploads
4. **Reference Standards** - JSON-based product expectations

### Deployment Options:
- **Local Development** - Run on your machine
- **Google Cloud Run** - Serverless cloud deployment
- **Docker** - Containerized deployment

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.11+
- Gemini API key ([Get one here](https://ai.google.dev/))

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Your API Key

**Option A: Environment Variable**
```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Edit main.py**
Replace the API key in line 24 of `main.py`:
```python
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-api-key-here")
```

### 3. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### 4. Open in Browser

Navigate to: **http://localhost:8080**

Upload a shelf image and get instant analysis!

---

## 📊 API Endpoints

### `GET /`
Web UI for uploading and analyzing shelf images

### `POST /audit`
Upload shelf image for analysis

**Request:**
```bash
curl -X POST -F "file=@shelf-image.jpg" http://localhost:8080/audit
```

**Response:**
```json
{
  "status": "success",
  "timestamp": "2025-11-21T10:30:00",
  "filename": "shelf-image.jpg",
  "analysis": "Detailed analysis report...",
  "reference_section": "Beverages - Soft Drinks"
}
```

### `GET /health`
Health check endpoint

### `GET /standards`
View current reference standards

### `GET /docs`
Interactive API documentation (Swagger UI)

---

## 🌐 Cloud Deployment (Google Cloud Run)

### Prerequisites
- Google Cloud account
- [gcloud CLI installed](https://cloud.google.com/sdk/docs/install)
- Docker (optional, Cloud Build handles this)

### Deployment Steps

1. **Set up Google Cloud project:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

2. **Set API key:**
```powershell
$env:GEMINI_API_KEY="your-api-key"
```

3. **Run deployment script:**
```powershell
# PowerShell
.\deploy.ps1

# Or Bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
- ✅ Enable required APIs
- ✅ Build container image
- ✅ Deploy to Cloud Run
- ✅ Return your public URL

**Your app will be live at:** `https://shelf-eye-xxxxx.run.app`

---

## 🎨 Web Interface Features

The built-in web UI provides:

- **📸 Image Upload** - Drag & drop or click to upload
- **👁️ Preview** - See your image before analysis
- **🔍 Real-time Analysis** - Instant AI processing
- **📊 Detailed Reports** - Comprehensive audit results
- **⏱️ Timestamps** - Track analysis history
- **📱 Mobile-friendly** - Works on phone cameras

---

## 📝 Customizing Reference Standards

Edit `reference_standard.json` to match your store layout:

```json
{
  "store_name": "Your Store Name",
  "shelf_section": "Product Category",
  "expected_products": [
    {
      "name": "Product Name",
      "position": "Row 1, Left",
      "quantity": 12,
      "price": "$2.99"
    }
  ],
  "quality_requirements": [
    "Products must face forward",
    "No expired items"
  ]
}
```

---

## 🧪 Testing

### Test with Sample Image

```bash
curl -X POST \
  -F "file=@test-shelf.jpg" \
  http://localhost:8080/audit
```

### Test with Postman
1. Open Postman
2. POST to `http://localhost:8080/audit`
3. Body → form-data
4. Key: `file`, Type: File
5. Upload shelf image
6. Send

---

## 📋 What the AI Analyzes

The system provides detailed reports on:

### 1. **Products Detected**
- All visible products identified
- Current positions noted

### 2. **Missing Products**
- Items not found on shelf
- Estimated quantities missing

### 3. **Misplaced Products**
- Wrong positions vs. standard
- Correct placement suggestions

### 4. **Quality Issues**
- Wrong-facing products
- Damaged labels
- Spacing problems
- Price tag issues

### 5. **Scores**
- **Neatness Score** (0-100)
- **Compliance Score** (0-100)

### 6. **Recommendations**
- Specific improvement actions
- Priority restocking items
- Reorganization tips

---

## 🛠️ Project Structure

```
shelf-eye/
│
├── main.py                     # FastAPI application
├── reference_standard.json     # Product standards
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── deploy.ps1                  # PowerShell deployment
├── deploy.sh                   # Bash deployment
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## 🔧 Configuration

### Environment Variables

- `GEMINI_API_KEY` - Your Google Gemini API key (required)
- `GOOGLE_CLOUD_PROJECT` - GCP project ID (for Cloud Run)
- `PORT` - Server port (default: 8080)

### API Settings

In `main.py`, you can configure:
- Gemini model version (line 71)
- CORS settings (lines 27-33)
- File size limits
- Timeout values

---

## 📦 Dependencies

- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **google-genai** - Gemini API client
- **python-multipart** - File upload support

---

## 🐛 Troubleshooting

### Issue: "Invalid API key"
**Solution:** Check your `GEMINI_API_KEY` is set correctly

### Issue: "Image analysis fails"
**Solution:** Ensure image is valid (JPG/PNG) and < 10MB

### Issue: "Module not found"
**Solution:** Run `pip install -r requirements.txt`

### Issue: "Port already in use"
**Solution:** Change port: `uvicorn main:app --port 8081`

---

## 🌟 Features

- ✅ Real-time shelf analysis
- ✅ Detailed product detection
- ✅ Missing item alerts
- ✅ Misplacement detection
- ✅ Quality compliance scoring
- ✅ Actionable recommendations
- ✅ Web-based UI
- ✅ RESTful API
- ✅ Cloud-ready
- ✅ Scalable architecture

---

## 🎯 Use Cases

- **Retail Store Audits** - Daily shelf checks
- **Merchandising** - Planogram compliance
- **Inventory Management** - Stock level monitoring
- **Quality Control** - Shelf presentation standards
- **Training** - Staff performance evaluation
- **Remote Monitoring** - Multi-location oversight

---

## 📈 Future Enhancements

- [ ] Multi-shelf batch processing
- [ ] Historical trend analysis
- [ ] Mobile app integration
- [ ] Automated alerts/notifications
- [ ] Database storage for audits
- [ ] Advanced analytics dashboard
- [ ] OCR for price tag verification
- [ ] Integration with POS systems

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Verify your Gemini API key is valid

---

## 📄 License

This project is provided as-is for demonstration purposes.

---

## 🚀 Getting Started Checklist

- [ ] Install Python 3.11+
- [ ] Get Gemini API key
- [ ] Install dependencies
- [ ] Set environment variable
- [ ] Run the application
- [ ] Upload test image
- [ ] View analysis results
- [ ] Customize reference standards
- [ ] (Optional) Deploy to Cloud Run

---

**Built with ❤️ using Google Gemini 2.5 Flash**

---

## 📞 Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --port 8080

# Test API
curl -X POST -F "file=@image.jpg" http://localhost:8080/audit

# Deploy to Cloud Run
.\deploy.ps1  # or ./deploy.sh

# View logs (Cloud Run)
gcloud run logs read shelf-eye --region us-central1

# Update deployment
gcloud run deploy shelf-eye --image gcr.io/PROJECT_ID/shelf-eye
```

---

**Ready to revolutionize your shelf auditing? Let's go! 🎉**
