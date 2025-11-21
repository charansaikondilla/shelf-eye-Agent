# 🧪 Testing the Shelf-Eye Agent

## Quick Test Guide

### 1. Using the Web UI (Easiest)

1. Open your browser to: http://localhost:8080
2. Click "📸 Choose Shelf Photo"
3. Select a shelf image from your device
4. Click "🔍 Analyze Shelf"
5. View the detailed analysis results

---

### 2. Using cURL (Command Line)

**Windows PowerShell:**
```powershell
curl.exe -X POST -F "file=@path\to\your\shelf-image.jpg" http://localhost:8080/audit
```

**Linux/Mac:**
```bash
curl -X POST -F "file=@/path/to/your/shelf-image.jpg" http://localhost:8080/audit
```

---

### 3. Using Python Script

```python
import requests

# Upload and analyze image
with open('shelf-image.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8080/audit', files=files)
    
result = response.json()
print(result['analysis'])
```

---

### 4. Using Postman

1. Open Postman
2. Create new POST request to: `http://localhost:8080/audit`
3. Go to Body tab → select "form-data"
4. Add key: `file` (change type to File)
5. Choose your shelf image
6. Click Send
7. View JSON response

---

## API Endpoints to Test

### Health Check
```bash
curl http://localhost:8080/health
```

### View Reference Standards
```bash
curl http://localhost:8080/standards
```

### Interactive API Documentation
Open in browser: http://localhost:8080/docs

---

## Sample Test Images

For best results, use images that show:
- ✅ Clear view of retail shelf
- ✅ Good lighting
- ✅ Multiple products visible
- ✅ Product labels readable
- ✅ Front-facing perspective

---

## Expected Response Format

```json
{
  "status": "success",
  "timestamp": "2025-11-21T10:30:00",
  "filename": "shelf.jpg",
  "analysis": "Detailed analysis text...",
  "reference_section": "Beverages - Soft Drinks"
}
```

---

## What to Look For in Results

The AI will provide:

1. **Products Detected** - All items identified
2. **Missing Products** - Items that should be there
3. **Misplaced Products** - Wrong positions
4. **Quality Issues** - Label problems, spacing, etc.
5. **Neatness Score** - Overall organization (0-100)
6. **Compliance Score** - Match to standards (0-100)
7. **Recommendations** - Actionable improvements

---

## Troubleshooting Tests

### Image upload fails
- Check file size < 10MB
- Ensure image format is JPG/PNG
- Verify server is running

### No analysis returned
- Check GEMINI_API_KEY is set
- Verify API key is valid
- Check terminal logs for errors

### Slow response
- First request may be slower (model loading)
- Large images take longer to process
- Check your internet connection

---

## Performance Tips

- Use images 1-5MB for best speed
- JPG format is faster than PNG
- Good lighting improves accuracy
- Clear, frontal shots work best

---

## Example Test Scenarios

### Scenario 1: Perfect Shelf
Upload a well-organized shelf → Should get high scores

### Scenario 2: Missing Products
Upload shelf with gaps → Should identify missing items

### Scenario 3: Messy Shelf
Upload disorganized shelf → Should suggest improvements

### Scenario 4: Wrong Positions
Upload shelf with products in wrong spots → Should flag misplacements

---

Happy Testing! 🎉
