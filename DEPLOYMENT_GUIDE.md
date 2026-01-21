# 🚀 DEPLOYMENT GUIDE
# House Price Prediction System

This guide provides step-by-step instructions for deploying your House Price Prediction System to various platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Trained model file (`model/house_price_model.pkl`)
- ✅ All dependencies listed in `requirements.txt`
- ✅ GitHub repository with all project files
- ✅ Tested the application locally
- ✅ Updated `HousePrice_hosted_webGUI_link.txt` with your details

## 🌐 Deployment Options

### Option 1: Render.com (Recommended) ⭐

**Pros**: Free tier, automatic deployments, easy setup, supports Python
**Best For**: Production-ready deployment with minimal hassle

#### Step-by-Step Instructions:

1. **Prepare Your GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: House Price Prediction System"
   git branch -M main
   git remote add origin https://github.com/yourusername/HousePrice_Project_YourName_MatricNo.git
   git push -u origin main
   ```

2. **Sign Up for Render**
   - Go to https://render.com
   - Sign up with GitHub (recommended) or email
   - Verify your email

3. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"
   - Connect your GitHub account (if not already)
   - Select your repository
   - Click "Connect"

4. **Configure Web Service**
   - **Name**: `houseprice-yourname` (must be unique)
   - **Region**: Choose closest to your location
   - **Branch**: `main`
   - **Root Directory**: Leave blank (or specify if different)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`

5. **Environment Variables** (Optional)
   - Click "Advanced"
   - Add environment variables if needed:
     ```
     FLASK_ENV=production
     SECRET_KEY=your-secret-key-here
     ```

6. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes first time)
   - Copy your live URL: `https://houseprice-yourname.onrender.com`

7. **Verify Deployment**
   - Visit your URL
   - Test the prediction form
   - Check health endpoint: `https://your-url.onrender.com/health`

**Important Notes for Render**:
- Free tier may spin down after inactivity (30 seconds to wake up)
- First request after inactivity will be slow
- Deploy from `main` branch for automatic updates

---

### Option 2: PythonAnywhere

**Pros**: Python-focused, good documentation, free tier
**Best For**: Python applications with straightforward setup

#### Step-by-Step Instructions:

1. **Sign Up**
   - Go to https://www.pythonanywhere.com
   - Create a free account
   - Verify email

2. **Upload Your Code**
   
   **Option A: Using Git (Recommended)**
   - Open a Bash console
   - Clone your repository:
     ```bash
     git clone https://github.com/yourusername/HousePrice_Project_YourName_MatricNo.git
     cd HousePrice_Project_YourName_MatricNo
     ```
   
   **Option B: Upload Files**
   - Go to "Files" tab
   - Create directory: `/home/yourusername/houseprice`
   - Upload files manually

3. **Create Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 houseprice-env
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Python version: 3.10
   - Path to Flask app: `/home/yourusername/HousePrice_Project_YourName_MatricNo/app.py`
   - Click through to create

5. **Configure WSGI File**
   - Edit the WSGI configuration file
   - Replace content with:
     ```python
     import sys
     path = '/home/yourusername/HousePrice_Project_YourName_MatricNo'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```

6. **Set Virtual Environment**
   - In "Web" tab, find "Virtualenv" section
   - Enter: `/home/yourusername/.virtualenvs/houseprice-env`

7. **Configure Static Files**
   - URL: `/static/`
   - Directory: `/home/yourusername/HousePrice_Project_YourName_MatricNo/static/`

8. **Reload Web App**
   - Click green "Reload" button
   - Visit: `https://yourusername.pythonanywhere.com`

**Important Notes for PythonAnywhere**:
- Free tier limits: 1 web app, limited CPU time
- Custom domains require paid plan
- Console access is limited on free tier

---

### Option 3: Streamlit Cloud

**Pros**: Perfect for data apps, very easy deployment, free
**Best For**: Quick demos, data science portfolios

**Note**: Requires converting Flask app to Streamlit format

#### Quick Conversion Guide:

1. **Create Streamlit App** (`app_streamlit.py`):
   ```python
   import streamlit as st
   import joblib
   import numpy as np
   
   # Load model
   @st.cache_resource
   def load_model():
       return joblib.load('model/house_price_model.pkl')
   
   package = load_model()
   
   st.title("🏠 House Price Prediction System")
   
   # Input fields
   overall_qual = st.slider("Overall Quality", 1, 10, 5)
   gr_liv_area = st.number_input("Living Area (sq ft)", 500, 5000, 1500)
   # ... add other inputs
   
   if st.button("Predict Price"):
       # Make prediction
       # Display results
   ```

2. **Deploy to Streamlit Cloud**
   - Push to GitHub
   - Go to https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New app"
   - Select repository, branch, and main file
   - Click "Deploy"

---

### Option 4: Vercel

**Pros**: Fast CDN, serverless, GitHub integration
**Best For**: Modern web apps with API routes

#### Requirements:
- Convert to Vercel-compatible format
- Use `vercel.json` configuration
- Serverless function structure

#### Quick Setup:
1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. Deploy: `vercel --prod`

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. Model File Not Found
**Error**: `FileNotFoundError: model/house_price_model.pkl`

**Solutions**:
- Ensure model file is committed to Git
- Check file path is correct
- Verify model file was uploaded
- Git might ignore `.pkl` files - check `.gitignore`

**Fix for Git**:
```bash
# If .pkl files are ignored, remove from .gitignore
# Then force add the model file
git add -f model/house_price_model.pkl
git commit -m "Add model file"
git push
```

#### 2. Dependencies Installation Failed
**Error**: Package installation errors

**Solutions**:
- Check Python version matches (3.10+)
- Ensure `requirements.txt` is correct
- Try pinned versions (included in requirements)
- Check platform compatibility

#### 3. Port Already in Use
**Error**: `Address already in use`

**Solutions**:
```bash
# Linux/Mac
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### 4. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solutions**:
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python path

#### 5. Render Deployment Fails
**Error**: Build or start command failed

**Solutions**:
- Check Render logs for specific error
- Verify `requirements.txt` is in root directory
- Ensure `Procfile` or start command is correct
- Check Python version in `runtime.txt`

#### 6. Application Timeout
**Error**: 503 Service Unavailable

**Solutions**:
- Model loading takes time on free tiers
- Increase timeout in deployment settings
- Optimize model loading (lazy loading)
- Consider paid tier for consistent performance

---

## 📊 Post-Deployment Checklist

After successful deployment:

- ✅ Test all features (prediction form, API endpoints)
- ✅ Verify model loads correctly
- ✅ Test with various input combinations
- ✅ Check error handling
- ✅ Verify responsive design on mobile
- ✅ Test API endpoints with cURL/Postman
- ✅ Update `HousePrice_hosted_webGUI_link.txt` with live URL
- ✅ Take screenshots for submission
- ✅ Share with others for testing
- ✅ Monitor performance and logs

---

## 🧪 Testing Your Deployment

### 1. Manual Testing
Visit your deployed URL and test:
- Home page loads correctly
- Form validation works
- Predictions are accurate
- Error messages display properly
- Mobile responsiveness

### 2. API Testing with cURL

```bash
# Replace YOUR_URL with your deployed URL

# Test health endpoint
curl https://YOUR_URL.onrender.com/health

# Test prediction
curl -X POST https://YOUR_URL.onrender.com/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "overall_qual": 7,
    "gr_liv_area": 2000,
    "total_bsmt_sf": 1000,
    "garage_cars": 2,
    "year_built": 2005,
    "neighborhood": "NAmes"
  }'

# Get neighborhoods
curl https://YOUR_URL.onrender.com/api/neighborhoods

# Get model info
curl https://YOUR_URL.onrender.com/api/model-info
```

### 3. Load Testing (Optional)
```bash
# Install Apache Bench
# Linux: sudo apt-get install apache2-utils
# Mac: brew install ab

# Run load test (100 requests, 10 concurrent)
ab -n 100 -c 10 https://YOUR_URL.onrender.com/
```

---

## 📝 Updating Your Deployment

### For Render (Automatic)
```bash
# Make changes locally
git add .
git commit -m "Update description"
git push origin main
# Render automatically redeploys
```

### For PythonAnywhere (Manual)
```bash
# SSH into console or use web console
cd HousePrice_Project_YourName_MatricNo
git pull origin main
# Click "Reload" in Web tab
```

---

## 💡 Best Practices

1. **Environment Variables**: Never commit secrets
2. **Logging**: Monitor application logs regularly
3. **Version Control**: Tag releases (`git tag v1.0.0`)
4. **Backup**: Keep model files backed up
5. **Documentation**: Update README with live URL
6. **Testing**: Test thoroughly before submission
7. **Monitoring**: Set up uptime monitoring (e.g., UptimeRobot)

---

## 📞 Getting Help

### Resources
- **Render Docs**: https://render.com/docs
- **PythonAnywhere Help**: https://help.pythonanywhere.com
- **Streamlit Docs**: https://docs.streamlit.io
- **Flask Docs**: https://flask.palletsprojects.com

### Community Support
- Stack Overflow (tag: flask, python, deployment)
- GitHub Issues
- Course instructor/TA

---

## 🎯 Submission Requirements

Before submitting, ensure:

1. ✅ Application is live and accessible
2. ✅ `HousePrice_hosted_webGUI_link.txt` is updated with:
   - Your name and matric number
   - ML algorithm used
   - Persistence method
   - Live URL
   - GitHub repository link
3. ✅ GitHub repository is public and well-documented
4. ✅ All files are committed and pushed
5. ✅ README includes deployment instructions
6. ✅ Screenshots are available (optional but recommended)

---

## ⏰ Final Checklist (Before Deadline)

**24 Hours Before Deadline:**
- [ ] Application is deployed and working
- [ ] All tests pass
- [ ] Documentation is complete
- [ ] GitHub repository is public
- [ ] Live URL is accessible
- [ ] Submission file is ready

**2 Hours Before Deadline:**
- [ ] Final deployment test
- [ ] Verify submission files
- [ ] Backup everything
- [ ] Submit to Scorac

**After Submission:**
- [ ] Take a break! 🎉
- [ ] Keep application running until grading is complete
- [ ] Monitor for any issues

---

**Good Luck with Your Deployment! 🚀**

Remember: Deploy early to allow time for troubleshooting!

---

**Last Updated**: January 21, 2026  
**Version**: 1.0  
**Author**: [Your Name]
