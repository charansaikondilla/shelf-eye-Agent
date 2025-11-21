from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
import json
import os
from datetime import datetime
from typing import Optional
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Shelf-Eye Agent",
    description="Automated retail shelf auditing using Gemini AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini client
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCDAZDnSemHlED_Ij99DHyKrq6ZPWd7bZw")
client = genai.Client(api_key=GEMINI_API_KEY)

# Backend reference image path
BACKEND_REFERENCE_IMAGE = "backend_reference/correct_shelf.jpg"
BACKEND_REFERENCE_LAYOUT = "backend_reference/layout.json"
STANDARD_PRICES_FILE = "backend_reference/standard_prices.json"

def load_standard_prices():
    """Load standard product prices"""
    if os.path.exists(STANDARD_PRICES_FILE):
        with open(STANDARD_PRICES_FILE, "r") as f:
            return json.load(f)
    return {
        "standard_prices": {
            "Coca-Cola": {"500ml": 2.99, "1L": 3.99, "1.5L": 4.99},
            "Pepsi": {"500ml": 2.99, "1L": 3.99, "1.5L": 4.99},
            "Sprite": {"500ml": 2.79, "1L": 3.79, "1.5L": 4.79},
            "Mountain Dew": {"500ml": 2.99, "1L": 3.99, "1.5L": 4.99},
            "Fanta": {"500ml": 2.79, "1L": 3.79, "1.5L": 4.79},
        },
        "currency": "USD"
    }

def load_backend_reference():
    """Load reference layout from backend storage"""
    if os.path.exists(BACKEND_REFERENCE_LAYOUT):
        with open(BACKEND_REFERENCE_LAYOUT, "r") as f:
            return json.load(f)
    return None

def analyze_reference_image():
    """Analyze the backend reference image and extract product layout"""
    if not os.path.exists(BACKEND_REFERENCE_IMAGE):
        logger.warning("No backend reference image found")
        return None
    
    try:
        with open(BACKEND_REFERENCE_IMAGE, "rb") as f:
            image_bytes = f.read()
        
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")
        
        extract_prompt = """Analyze this REFERENCE shelf image (the CORRECT layout) and list ALL products from LEFT to RIGHT, TOP to BOTTOM.

For each product provide:
- Product name/brand
- Exact position (Row number, Position from left)
- Quantity visible

Be very specific about positions. This is the standard all other shelves will be compared against."""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[extract_prompt, image_part],
        )
        
        layout_data = {
            "timestamp": datetime.now().isoformat(),
            "extracted_layout": response.text
        }
        
        # Save extracted layout
        os.makedirs("backend_reference", exist_ok=True)
        with open(BACKEND_REFERENCE_LAYOUT, "w") as f:
            json.dump(layout_data, f, indent=2)
        
        logger.info("Backend reference layout analyzed and saved")
        return layout_data
        
    except Exception as e:
        logger.error(f"Error analyzing backend reference: {str(e)}")
        return None

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the web UI"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shelf-Eye Agent - Professional Audit</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                padding: 40px;
            }
            h1 {
                color: #333;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .upload-section {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                background: #f8f9ff;
                transition: all 0.3s;
            }
            .upload-section:hover {
                border-color: #764ba2;
                background: #f0f1ff;
            }
            input[type="file"] {
                display: none;
            }
            .upload-label {
                display: inline-block;
                padding: 15px 40px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 50px;
                cursor: pointer;
                font-size: 1.1em;
                font-weight: 600;
                transition: transform 0.3s;
            }
            .upload-label:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
            }
            #preview {
                max-width: 100%;
                max-height: 400px;
                margin: 20px auto;
                display: none;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            #analyzeBtn {
                display: none;
                padding: 15px 50px;
                background: #28a745;
                color: white;
                border: none;
                border-radius: 50px;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                margin: 20px auto;
                transition: all 0.3s;
            }
            #analyzeBtn:hover {
                background: #218838;
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(40, 167, 69, 0.4);
            }
            #loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            #results {
                display: none;
                margin-top: 30px;
            }
            .perfect-banner {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                font-size: 1.8em;
                font-weight: bold;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(40, 167, 69, 0.3);
                animation: slideIn 0.5s ease-out;
            }
            .error-banner {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                font-size: 1.8em;
                font-weight: bold;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(220, 53, 69, 0.3);
                animation: slideIn 0.5s ease-out;
            }
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .report-box {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                white-space: pre-wrap;
                line-height: 1.8;
                font-size: 1.05em;
                font-family: 'Courier New', monospace;
            }
            .report-box span[style*="color: red"] {
                display: block;
                margin: 3px 0;
            }
            .timestamp {
                text-align: center;
                color: #999;
                margin-top: 20px;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛒 Shelf-Eye Agent</h1>
            <p class="subtitle">Professional AI-Powered Shelf Compliance Auditing</p>
            
            <div class="upload-section">
                <p style="color: #667eea; font-weight: 600; margin-bottom: 20px;">Upload shelf image for compliance audit</p>
                <label for="fileInput" class="upload-label">
                    📸 Choose Shelf Photo
                </label>
                <input type="file" id="fileInput" accept="image/*">
                <img id="preview" alt="Preview">
            </div>
            
            <div style="text-align: center;">
                <button id="analyzeBtn">🔍 Analyze Shelf Compliance</button>
            </div>
            
            <div id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 15px; color: #667eea; font-weight: 600;">Analyzing shelf layout with AI...</p>
            </div>
            
            <div id="results"></div>
        </div>

        <script>
            const fileInput = document.getElementById('fileInput');
            const preview = document.getElementById('preview');
            const analyzeBtn = document.getElementById('analyzeBtn');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');

            fileInput.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                        analyzeBtn.style.display = 'block';
                        results.style.display = 'none';
                    }
                    reader.readAsDataURL(file);
                }
            });

            analyzeBtn.addEventListener('click', async function() {
                const file = fileInput.files[0];
                if (!file) return;

                const formData = new FormData();
                formData.append('file', file);

                loading.style.display = 'block';
                results.style.display = 'none';
                analyzeBtn.disabled = true;

                try {
                    const response = await fetch('/audit', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();
                    displayResults(data);
                } catch (error) {
                    results.innerHTML = '<div class="error-banner">❌ Error: ' + error.message + '</div>';
                    results.style.display = 'block';
                } finally {
                    loading.style.display = 'none';
                    analyzeBtn.disabled = false;
                }
            });

            function displayResults(data) {
                let html = '';
                
                if (data.compliance_status === 'perfect') {
                    html += '<div class="perfect-banner">✅ EXEMPLARY COMPLIANCE<br><span style="font-size: 0.6em;">All products are impeccably positioned according to standards</span></div>';
                } else {
                    html += '<div class="error-banner">⚠️ COMPLIANCE ISSUES DETECTED<br><span style="font-size: 0.6em;">Immediate corrective actions required</span></div>';
                }
                
                html += '<h2 style="text-align: center; color: #333; margin-bottom: 20px;">📊 Professional Shelf Audit Report</h2>';
                
                // Convert analysis text to HTML-safe format while preserving HTML tags
                let analysisHtml = data.analysis
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/&lt;span style="color: red; font-weight: bold;"&gt;/g, '<span style="color: red; font-weight: bold;">')
                    .replace(/&lt;span style="color: red;"&gt;/g, '<span style="color: red;">')
                    .replace(/&lt;\/span&gt;/g, '</span>');
                
                html += '<div class="report-box">' + analysisHtml + '</div>';
                html += '<div class="timestamp">⏱️ Audit completed at: ' + new Date().toLocaleString() + '</div>';
                
                results.innerHTML = html;
                results.style.display = 'block';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/audit")
async def audit_shelf(file: UploadFile = File(...)):
    """
    Analyze shelf image against backend reference
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        content = await file.read()
        logger.info(f"Processing image: {file.filename}, size: {len(content)} bytes")
        
        # Load or analyze backend reference
        reference_layout = load_backend_reference()
        if not reference_layout and os.path.exists(BACKEND_REFERENCE_IMAGE):
            reference_layout = analyze_reference_image()
        
        # Create image part
        image_part = types.Part.from_bytes(data=content, mime_type=file.content_type)
        
        if reference_layout:
            # Compare with backend reference
            prompt = f"""You are a professional retail auditor. You have a REFERENCE IMAGE showing the CORRECT shelf layout.

**REFERENCE STANDARD (CORRECT SHELF LAYOUT):**
{reference_layout['extracted_layout']}

**YOUR TASK:**
Compare the uploaded test image with the reference layout above. Analyze PRODUCT POSITIONS and identify what's missing or wrong.

**CRITICAL INSTRUCTIONS:**
1. Look at EMPTY SPACES in the test image - these are where products should be but are MISSING
2. Compare each position in test image with the same position in reference
3. If you see an EMPTY SHELF SPACE, check what product should be there according to the reference
4. Extract price information from BOTH reference and test images for all products
5. For EMPTY SPACES, identify the exact product (including brand, size, variant) that should be there

**IF EVERYTHING MATCHES PERFECTLY:**
State: "✅ COMPLIANCE STATUS: PERFECT - The shelf matches the reference image exactly. No changes needed."
Then list ALL products with their prices:

**📋 ALL PRODUCTS ON SHELF:**
✓ [Product 1]: $[X.XX]
✓ [Product 2]: $[X.XX]
✓ [Product 3]: $[X.XX]
[Continue for all products...]

**IF THERE ARE DIFFERENCES, USE THIS FORMAT:**

═══════════════════════════════════════════════════════════════
📋 PRODUCTS & PRICES OVERVIEW
═══════════════════════════════════════════════════════════════
**ALL PRODUCTS DETECTED IN TEST IMAGE (With Prices):**
[List ALL products you can see in the test image with their visible prices]

✓ [Product Brand, Name, Size]: $[X.XX] - Present on shelf
✓ [Product Brand, Name, Size]: $[X.XX] - Present on shelf
✓ [Product Brand, Name, Size]: $[X.XX] - Present on shelf
[List all visible products...]

**MISSING PRODUCTS (Not visible in test image but present in reference):**
❌ [Product]: $[X.XX] (from reference) - EMPTY SPACE
❌ [Product]: $[X.XX] (from reference) - EMPTY SPACE
[List all missing products...]

═══════════════════════════════════════════════════════════════
📋 EXECUTIVE SUMMARY
═══════════════════════════════════════════════════════════════
• Total Products in Reference: [X]
• Products Found in Test Image: [X]
• Products in Correct Position: [X]
• Missing Products (Empty Spaces): [X]
• Misplaced Products: [X]
• Overall Match: [X]%

═══════════════════════════════════════════════════════════════
🚨 CRITICAL: MISSING PRODUCTS (EMPTY SHELF SPACES)
═══════════════════════════════════════════════════════════════
[Look for EMPTY SPACES or GAPS in the test image]
[Compare with reference to identify what SHOULD be there]
[BE VERY SPECIFIC about which product variant is missing]

For each empty space/missing product, format with HTML red color:
<span style="color: red; font-weight: bold;">🔴 EMPTY SPACE DETECTED - MISSING PRODUCT</span>

<span style="color: red;">❌ MISSING: [Exact Product Name, Brand, Size, Variant from Reference]</span>
   <span style="color: red;">• Expected Position: Row [X], Position [Y] (Shelf [Left/Center/Right])</span>
   <span style="color: red;">• Status: ⚠️ EMPTY SHELF SPACE - NO PRODUCT PRESENT</span>
   <span style="color: red;">• From Reference Image: [Exact product description from reference]</span>
   <span style="color: red;">• Product Price (from reference): $[X.XX]</span>
   <span style="color: red;">• Description: [Detailed description - brand, flavor, size, packaging type]</span>
   <span style="color: red;">• Action Required: IMMEDIATELY stock [Product Name] at this empty position</span>
   <span style="color: red;">• Estimated Quantity Needed: [X] units (based on reference shelf space)</span>
   <span style="color: red;">• Empty Space Details: [Describe the empty area - "visible gap between X and Y products", "entire section vacant", etc.]</span>
   <span style="color: red;">• 🏢 RECOMMENDED SUPPLIER: Contact [Brand Company Name] for immediate restocking</span>
   <span style="color: red;">• 📦 ORDER URGENCY: CRITICAL - Restock within 24 hours</span>

Example for Mountain Dew:
<span style="color: red; font-weight: bold;">🔴 EMPTY SPACE DETECTED - MISSING PRODUCT</span>

<span style="color: red;">❌ MISSING: Mountain Dew Original 500ml Bottle</span>
   <span style="color: red;">• Expected Position: Row 2, Position 3 (Center Shelf)</span>
   <span style="color: red;">• Status: ⚠️ EMPTY SHELF SPACE - NO PRODUCT PRESENT</span>
   <span style="color: red;">• From Reference Image: Mountain Dew Original flavor in 500ml plastic bottle, green label with logo</span>
   <span style="color: red;">• Product Price (from reference): $2.49</span>
   <span style="color: red;">• Description: Mountain Dew citrus-flavored carbonated soft drink, 500ml PET bottle, bright green packaging</span>
   <span style="color: red;">• Action Required: IMMEDIATELY stock Mountain Dew 500ml at Row 2, Position 3</span>
   <span style="color: red;">• Estimated Quantity Needed: 12 units (based on reference shelf space)</span>
   <span style="color: red;">• Empty Space Details: Clear gap visible between Sprite and Pepsi products where Mountain Dew should be displayed</span>
   <span style="color: red;">• 🏢 RECOMMENDED SUPPLIER: PepsiCo Beverages Company - Mountain Dew Division</span>
   <span style="color: red;">• 📦 ORDER URGENCY: CRITICAL - High-demand product, restock immediately</span>

═══════════════════════════════════════════════════════════════
✅ PRODUCTS CORRECTLY POSITIONED (MATCHING REFERENCE)
═══════════════════════════════════════════════════════════════
[Products that appear in SAME position as reference image]

For each matching product:
✓ [Product Name, Brand, Size]
  • Position: Row [X], Position [Y] - MATCHES REFERENCE ✓
  • Product Price (from test image): $[X.XX]
  • Reference Price (from reference image): $[X.XX]
  • Status: CORRECT PLACEMENT ✓
  • Description: [Brief product description]
  • Comparison: Same location as in reference image

═══════════════════════════════════════════════════════════════
⚠️ POSITION ERRORS (WRONG PLACEMENT)
═══════════════════════════════════════════════════════════════
[Products found in DIFFERENT position than reference]

For each misplaced product:
❌ [Product Name, Brand, Size]
   • Current Position in Test Image: Row [X], Position [Y]
   • Expected Position from Reference: Row [X], Position [Y]
   • Issue: Product is in wrong location
   • Product Price (test image): $[X.XX]
   • Reference Price: $[X.XX]
   • Action: Move from current position to correct position

═══════════════════════════════════════════════════════════════
📦 ADDITIONAL OBSERVATIONS
═══════════════════════════════════════════════════════════════

**Empty Shelf Analysis:**
• Total empty spaces detected: [X]
• Shelf occupancy: [X]% (compared to reference)
• Critical gaps: [describe where major gaps are]

**Price Tags Observed:**
[List ALL visible price tags from BOTH images with detailed product information]

**From Reference Image (Correct Shelf):**
• [Product Brand, Name, Size]: $[X.XX]
• [Product Brand, Name, Size]: $[X.XX]
• [Product Brand, Name, Size]: $[X.XX]

**From Test Image (Uploaded Shelf):**
• [Product Brand, Name, Size]: $[X.XX] (or "Not visible - empty space")
• [Product Brand, Name, Size]: $[X.XX] (or "Not visible - empty space")
• [Product Brand, Name, Size]: $[X.XX] (or "Not visible - empty space")

**Price Analysis Notes:**
• For empty spaces, note: "Price not visible - product missing (should be $X.XX based on reference)"
• Compare which prices are visible vs missing due to empty spaces

**Quality Notes:**
• Product facings: [Good/Issues noted]
• Shelf organization: [compared to reference]
• Visual differences from reference: [describe]

═══════════════════════════════════════════════════════════════
📊 COMPLIANCE METRICS
═══════════════════════════════════════════════════════════════
• Position Match Score: [X]/100
• Stock Completeness: [X]/100 (how full vs reference)
• Overall Compliance: [X]/100

═══════════════════════════════════════════════════════════════
🔧 CORRECTIVE ACTIONS REQUIRED
═══════════════════════════════════════════════════════════════

**IMMEDIATE - Stock Missing Items:**
[List all products found in reference but missing in test image]
1. Stock [Product] at Row X, Position Y
2. Stock [Product] at Row X, Position Y
[etc.]

**REPOSITION - Fix Placement Errors:**
[List products in wrong positions]
1. Move [Product] from current position to correct position
[etc.]

**VERIFY:**
After restocking, compare with reference image to ensure match

═══════════════════════════════════════════════════════════════
📝 DETAILED COMPARISON NOTES
═══════════════════════════════════════════════════════════════
Reference Image shows: [describe what's in reference]
Test Image shows: [describe what you see in test]
Key differences: [explain main differences clearly]
Empty spaces in test image: [describe where gaps/empty spots are]

═══════════════════════════════════════════════════════════════

**ANALYSIS GUIDELINES:**
1. **Show ALL Products First:** At the very beginning, list ALL products visible in test image with their prices
2. **Identify Empty Spaces:** Look carefully at test image for GAPS, EMPTY SHELF SPOTS, or MISSING PRODUCTS - mark these in RED
3. **Detailed Product Identification:** When you find an empty space, identify the EXACT product from reference (brand + flavor + size)
4. **Extract ALL Prices:** Read price tags from both reference and test images for every product and display them
5. **For Empty Spaces:** State the product name, description, price, and supplier company - display ALL in RED HTML formatting
6. **Missing = Empty Space:** If reference shows "Mountain Dew 500ml $2.49" but test shows empty space → mark as RED "MISSING: Mountain Dew 500ml, Price: $2.49, Supplier: PepsiCo"
7. **Be Ultra-Specific:** Use exact product details (Mountain Dew Original vs Mountain Dew Code Red, 500ml vs 1L, etc.)
8. **Empty Space Description:** Describe WHERE the empty space is ("gap between Sprite and Pepsi", "entire right section empty", etc.)
9. **Price Information:** Include prices for ALL products - show prices for visible products and reference prices for missing products
10. **Product Details:** For each missing item include: Brand, Product Name, Flavor/Variant, Size, Packaging Type, Price, Supplier Company
11. **Supplier Recommendations:** For missing products, identify the manufacturing company (e.g., "PepsiCo" for Mountain Dew, "Coca-Cola Company" for Coke, etc.)

**HTML FORMATTING RULES:**
- Use <span style="color: red; font-weight: bold;"> for empty space headers
- Use <span style="color: red;"> for ALL missing product details
- This makes empty spaces HIGHLY VISIBLE in red color
- Do NOT use red for correctly positioned products

**IMPORTANT:** 
- START by listing ALL products with prices that you can see in the test image
- Your primary goal is to identify WHAT IS MISSING and display it in RED with full details, prices, and supplier companies
- Look for EMPTY SPACES in test image and identify exact product that should be there from reference
- Extract and display price information for ALL products (both visible and missing)
- Be extremely detailed about missing products (especially Mountain Dew or any missing items)
- Make empty spaces visually obvious with red color HTML formatting
- For each missing product, recommend the supplier company for restocking"""

        else:
            # No reference available
            prompt = f"""Analyze this shelf image and provide a PROFESSIONAL, STRUCTURED audit report.

**FORMAT YOUR REPORT AS FOLLOWS:**

═══════════════════════════════════════════════════════════════
📋 SHELF ANALYSIS SUMMARY
═══════════════════════════════════════════════════════════════
• Total Products Detected: [X]
• Shelf Organization Quality: [Excellent/Good/Fair/Poor]
• Overall Assessment: [Brief summary]

═══════════════════════════════════════════════════════════════
✅ PRODUCTS DETECTED
═══════════════════════════════════════════════════════════════
[List all products found on shelf]

For each product:
✓ [Product Name] [Size]
  • Location: Row [X], Position [Y]
  • Facing: [Forward/Sideways/etc]
  • Condition: [Good/Damaged/etc]

═══════════════════════════════════════════════════════════════
📦 QUALITY & ORGANIZATION FINDINGS
═══════════════════════════════════════════════════════════════
• Overall shelf organization and neatness
• Product facing and alignment
• Spacing between products
• Any damaged or misaligned items
• General shelf appearance

═══════════════════════════════════════════════════════════════
🔧 RECOMMENDATIONS
═══════════════════════════════════════════════════════════════
[Actionable steps to improve shelf organization and presentation]

═══════════════════════════════════════════════════════════════

Use professional retail auditing language throughout.
DO NOT mention prices or pricing - focus only on product placement and organization."""

        # Call Gemini API
        logger.info("Calling Gemini API for analysis...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image_part],
        )
        
        analysis_result = response.text
        logger.info("Analysis completed successfully")
        
        # Determine compliance status
        compliance_status = "perfect" if "EXEMPLARY" in analysis_result.upper() or "PERFECT" in analysis_result.upper() else "issues"
        
        return JSONResponse(content={
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename,
            "analysis": analysis_result,
            "compliance_status": compliance_status,
            "has_reference": reference_layout is not None
        })
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "shelf-eye-agent"}

@app.post("/admin/upload-reference")
async def upload_backend_reference(file: UploadFile = File(...)):
    """
    Admin endpoint to upload backend reference image
    """
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        os.makedirs("backend_reference", exist_ok=True)
        content = await file.read()
        
        with open(BACKEND_REFERENCE_IMAGE, "wb") as f:
            f.write(content)
        
        # Analyze the reference
        layout = analyze_reference_image()
        
        return JSONResponse(content={
            "status": "success",
            "message": "Backend reference image uploaded and analyzed",
            "layout": layout
        })
        
    except Exception as e:
        logger.error(f"Error uploading reference: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
