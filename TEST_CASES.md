# ===============================================
# SAMPLE TEST CASES
# House Price Prediction System
# ===============================================

This file contains sample test cases you can use to verify your application works correctly.

## Test Case 1: Luxury Home

**Input:**
- Overall Quality: 9
- Living Area: 3500 sq ft
- Basement Area: 1800 sq ft
- Garage Cars: 3
- Year Built: 2010
- Neighborhood: NoRidge

**Expected:**
- High price (typically $300,000 - $400,000+)
- Narrow confidence interval (model is confident)

---

## Test Case 2: Average Family Home

**Input:**
- Overall Quality: 6
- Living Area: 1800 sq ft
- Basement Area: 900 sq ft
- Garage Cars: 2
- Year Built: 2000
- Neighborhood: NAmes

**Expected:**
- Mid-range price (typically $150,000 - $220,000)
- Moderate confidence interval

---

## Test Case 3: Starter Home

**Input:**
- Overall Quality: 4
- Living Area: 1000 sq ft
- Basement Area: 0 sq ft
- Garage Cars: 0
- Year Built: 1970
- Neighborhood: OldTown

**Expected:**
- Lower price (typically $80,000 - $130,000)
- May have wider confidence interval

---

## Test Case 4: New Construction

**Input:**
- Overall Quality: 8
- Living Area: 2500 sq ft
- Basement Area: 1200 sq ft
- Garage Cars: 2
- Year Built: 2023
- Neighborhood: CollgCr

**Expected:**
- High-mid range price (typically $250,000 - $320,000)
- Model may be less confident (fewer recent years in training data)

---

## Test Case 5: Large Older Home

**Input:**
- Overall Quality: 5
- Living Area: 3000 sq ft
- Basement Area: 1500 sq ft
- Garage Cars: 2
- Year Built: 1950
- Neighborhood: Edwards

**Expected:**
- Mid-range price despite size (quality and age factors)
- Demonstrates model considers multiple features

---

## Test Case 6: Minimum Values

**Input:**
- Overall Quality: 1
- Living Area: 500 sq ft
- Basement Area: 0 sq ft
- Garage Cars: 0
- Year Built: 1872
- Neighborhood: BrDale

**Expected:**
- Lowest price range
- Tests model's lower boundary handling

---

## Test Case 7: Maximum Values

**Input:**
- Overall Quality: 10
- Living Area: 5000 sq ft
- Basement Area: 3000 sq ft
- Garage Cars: 4
- Year Built: 2020
- Neighborhood: StoneBr

**Expected:**
- Highest price range
- Tests model's upper boundary handling

---

## Edge Cases to Test

### 1. No Basement
- Total Basement Area: 0
- Should work normally (common scenario)

### 2. No Garage
- Garage Cars: 0
- Should work normally (common scenario)

### 3. Very Old House
- Year Built: 1800-1900
- Model should handle gracefully

### 4. Very New House
- Year Built: 2020-2025
- Model may have less confidence (extrapolation)

---

## API Testing with cURL

### Test 1: Valid Prediction Request
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "overall_qual": 7,
    "gr_liv_area": 2000,
    "total_bsmt_sf": 1000,
    "garage_cars": 2,
    "year_built": 2005,
    "neighborhood": "NAmes"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "predicted_price": 215000.00,
  "lower_bound": 195000.00,
  "upper_bound": 235000.00,
  "confidence": 95,
  "model_r2": 0.8756,
  "model_rmse": 28500.50
}
```

### Test 2: Missing Field
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "overall_qual": 7,
    "gr_liv_area": 2000
  }'
```

**Expected Response:**
```json
{
  "success": false,
  "error": "Missing required field: total_bsmt_sf"
}
```

### Test 3: Invalid Value
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "overall_qual": 15,
    "gr_liv_area": 2000,
    "total_bsmt_sf": 1000,
    "garage_cars": 2,
    "year_built": 2005,
    "neighborhood": "NAmes"
  }'
```

**Expected Response:**
```json
{
  "success": false,
  "error": "Overall Quality must be between 1 and 10"
}
```

### Test 4: Get Neighborhoods
```bash
curl http://localhost:5000/api/neighborhoods
```

**Expected Response:**
```json
{
  "success": true,
  "neighborhoods": ["Blmngtn", "Blueste", "BrDale", ...]
}
```

### Test 5: Health Check
```bash
curl http://localhost:5000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2026-01-21T12:00:00"
}
```

### Test 6: Model Info
```bash
curl http://localhost:5000/api/model-info
```

**Expected Response:**
```json
{
  "success": true,
  "algorithm": "Random Forest Regressor",
  "features": ["OverallQual", "GrLivArea", ...],
  "metrics": {...},
  "persistence_method": "Joblib"
}
```

---

## Validation Testing

### Test Invalid Inputs:

1. **Quality out of range**: overall_qual = 11 or 0
   - Should return validation error

2. **Negative living area**: gr_liv_area = -1000
   - Should return validation error

3. **Negative basement**: total_bsmt_sf = -500
   - Should return validation error

4. **Invalid garage**: garage_cars = 5 or -1
   - Should return validation error

5. **Invalid year**: year_built = 1700 or 3000
   - Should return validation error

6. **Empty neighborhood**: neighborhood = ""
   - Should return validation error

7. **Invalid neighborhood**: neighborhood = "XYZ123"
   - Should handle gracefully (use default)

---

## Performance Testing

### Response Time Expectations:

1. **First Request (Cold Start)**:
   - Local: < 1 second
   - Deployed (Free tier): 5-30 seconds

2. **Subsequent Requests**:
   - Local: < 200ms
   - Deployed: < 500ms

3. **Model Loading**:
   - Should happen once at startup
   - ~1-2 seconds for model load

---

## Browser Testing Checklist

Test on multiple browsers:
- [ ] Chrome/Edge
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers

Test features:
- [ ] Form submission
- [ ] Input validation
- [ ] Error messages display
- [ ] Success messages display
- [ ] Tooltips work
- [ ] Responsive design (resize window)
- [ ] Print layout (Ctrl+P)

---

## Accessibility Testing

- [ ] Tab navigation works
- [ ] Form labels are clear
- [ ] Error messages are descriptive
- [ ] Color contrast is sufficient
- [ ] Works with screen readers (basic)

---

## Security Testing

1. **SQL Injection**: Not applicable (no database)
2. **XSS**: Flask auto-escapes templates
3. **Input validation**: All inputs validated server-side
4. **Rate limiting**: Not implemented (consider for production)

---

## Load Testing (Optional)

```bash
# Using Apache Bench (if installed)
ab -n 100 -c 10 http://localhost:5000/

# Expected: All requests succeed, reasonable response time
```

---

## Common Neighborhoods in Dataset

For testing, these neighborhoods exist in the training data:

- Blmngtn
- Blueste
- BrDale
- BrkSide
- ClearCr
- CollgCr
- Crawfor
- Edwards
- Gilbert
- IDOTRR
- MeadowV
- Mitchel
- NAmes
- NoRidge
- NPkVill
- NridgHt
- NWAmes
- OldTown
- SWISU
- Sawyer
- SawyerW
- Somerst
- StoneBr
- Timber
- Veenker

---

## Troubleshooting Test Failures

### Prediction seems wrong
- Check all input values are correct
- Verify model was trained properly
- Compare with similar test cases
- Remember: predictions are estimates, not exact

### API returns 500 error
- Check server logs for details
- Verify model file exists
- Ensure all dependencies installed
- Check input format matches API spec

### Form validation not working
- Check browser console for JavaScript errors
- Verify input constraints in HTML
- Test with different browsers

---

## Testing Before Submission

**Final Test Checklist:**

1. [ ] All test cases run successfully
2. [ ] Error handling works correctly
3. [ ] API endpoints respond properly
4. [ ] Web interface is user-friendly
5. [ ] Mobile view works well
6. [ ] No console errors in browser
7. [ ] Application logs show no errors
8. [ ] Model predictions are reasonable
9. [ ] Confidence intervals make sense
10. [ ] Documentation is complete

---

## Automated Testing Script (Optional)

Save as `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    print("✓ Health check passed")

def test_predict():
    data = {
        "overall_qual": 7,
        "gr_liv_area": 2000,
        "total_bsmt_sf": 1000,
        "garage_cars": 2,
        "year_built": 2005,
        "neighborhood": "NAmes"
    }
    response = requests.post(f"{BASE_URL}/api/predict", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result['success'] == True
    assert 'predicted_price' in result
    print("✓ Prediction test passed")

def test_neighborhoods():
    response = requests.get(f"{BASE_URL}/api/neighborhoods")
    assert response.status_code == 200
    result = response.json()
    assert result['success'] == True
    assert len(result['neighborhoods']) > 0
    print("✓ Neighborhoods test passed")

if __name__ == "__main__":
    print("Running tests...")
    test_health()
    test_predict()
    test_neighborhoods()
    print("\n✓ All tests passed!")
```

Run: `python test_api.py`

---

**Remember**: Testing is crucial for a production-grade application!

**Test early, test often, test thoroughly!**
