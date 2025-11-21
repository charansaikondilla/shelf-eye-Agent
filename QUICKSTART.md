# 🚀 Quick Start Guide - Shelf-Eye Agent

## ✅ Your System is Ready!

The Shelf-Eye Agent is now running at: **http://localhost:8080**

---

## 📖 How to Use - Two Modes

### **Mode 1: Compare with Reference Image** (Recommended for Position Accuracy)

#### Step 1: Upload Reference Image
1. Open http://localhost:8080
2. In the **green section** (Step 1), click "✅ Choose Reference Photo"
3. Select your **correct shelf layout** image (the ideal arrangement)
4. Click "Upload as Reference"
5. Wait for confirmation: ✅ Reference image uploaded successfully!

#### Step 2: Upload Test Image
1. In the **purple section** (Step 2), click "📸 Choose Shelf Photo to Audit"
2. Select the shelf image you want to compare
3. Click "🔍 Analyze & Compare with Reference"
4. View detailed comparison results!

**What You'll Get:**
- ✅ Products in correct positions
- ❌ Products in wrong positions (with exact locations)
- 📋 Missing products
- 🔄 Step-by-step correction instructions
- 📊 Compliance score (0-100)

---

### **Mode 2: Compare with JSON Standards**

If you don't upload a reference image, the system uses `reference_standard.json`

1. Upload any shelf image
2. Click "🔍 Analyze & Compare with Reference"
3. Get analysis based on JSON standards

---

## 🎯 Example Workflow

### Scenario: Beverage Shelf Audit

**Reference Image:** Perfect shelf with products in correct order
- Coca-Cola (Row 1, Left)
- Pepsi (Row 1, Center)
- Sprite (Row 1, Right)

**Test Image:** Current shelf state
- Pepsi (Row 1, Left) ❌ WRONG
- Coca-Cola (Row 1, Center) ❌ WRONG
- Sprite (Row 1, Right) ✅ CORRECT

**Result:** 
```
POSITION MISTAKES:
- Pepsi: Currently at Row 1, Left → Should be Row 1, Center
- Coca-Cola: Currently at Row 1, Center → Should be Row 1, Left

CORRECTION:
1. Swap Pepsi and Coca-Cola positions
```

---

## 🧪 Test the System

### Using cURL:

**Upload Reference:**
```powershell
curl.exe -X POST -F "file=@correct-shelf.jpg" http://localhost:8080/upload-reference
```

**Audit Test Image:**
```powershell
curl.exe -X POST -F "file=@test-shelf.jpg" http://localhost:8080/audit
```

---

## 📸 Tips for Best Results

### For Reference Images:
- ✅ Clear, well-lit photo
- ✅ All products visible and facing forward
- ✅ Straight front view
- ✅ No obstructions

### For Test Images:
- ✅ Same angle as reference
- ✅ Similar lighting conditions
- ✅ Full shelf visible
- ✅ Products readable

---

## 🔧 Current Configuration

**API Key:** Set in `.env` file
**Model:** Google Gemini 2.5 Flash
**Port:** 8080
**Reference Storage:** `reference_images/` folder

---

## 📊 What the AI Analyzes

1. **Product Detection** - All items identified
2. **Position Comparison** - Row and position matching
3. **Order Verification** - Left-to-right, top-to-bottom
4. **Missing Items** - Gaps in expected products
5. **Quality Check** - Facing, spacing, labels
6. **Compliance Score** - Overall accuracy rating
7. **Correction Steps** - Exact fix instructions

---

## ⚡ Quick Commands

**Start Server:**
```powershell
cd "d:\self eye\shelf-eye"
$env:GEMINI_API_KEY="your-key"
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

**Test API:**
```powershell
python test_api.py
```

**View API Docs:**
http://localhost:8080/docs

---

## 🎉 You're All Set!

Just open http://localhost:8080 and start auditing shelves!

**Need Help?** Check TESTING.md for more examples.
