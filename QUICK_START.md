# ⚡ QUICK START GUIDE
# House Price Prediction System

Get your application up and running in 10 minutes!

## 🎯 Prerequisites

- Python 3.11+ installed
- pip package manager
- Internet connection (for downloading Kaggle dataset)

## 🚀 Quick Setup (5 Steps)

### Step 1: Set Up Project (2 minutes)

```bash
# Navigate to project directory
cd "House Price Prediction System"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Download Dataset (1 minute)

1. Go to: https://www.kaggle.com/c/house-prices-advanced-regression-techniques/data
2. Download `train.csv` (requires Kaggle account - free)
3. Place `train.csv` in the `model/` directory

### Step 3: Train Model (3 minutes)

```bash
# Navigate to model directory
cd model

# Start Jupyter Notebook
jupyter notebook

# In browser:
# - Open model_building.ipynb
# - Click "Kernel" > "Restart & Run All"
# - Wait for completion (~2-3 minutes)
# - Verify house_price_model.pkl is created

# Close Jupyter
# Press Ctrl+C in terminal and type 'y'
```

### Step 4: Run Application (1 minute)

```bash
# Return to project root
cd ..

# Start Flask application
python app.py

# You should see:
# 🏠 HOUSE PRICE PREDICTION SYSTEM
# Starting Flask application...
# Access the app at: http://127.0.0.1:5000
```

### Step 5: Test Application (2 minutes)

1. Open browser: `http://127.0.0.1:5000`
2. Fill in the form with test values:
   - Overall Quality: 7
   - Living Area: 2000
   - Basement Area: 1000
   - Garage Cars: 2
   - Year Built: 2005
   - Neighborhood: NAmes
3. Click "Predict House Price"
4. Verify you get a prediction result!

## ✅ Success Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed without errors
- [ ] Dataset downloaded and placed in model/ directory
- [ ] Model training completed successfully
- [ ] house_price_model.pkl file exists in model/ directory
- [ ] Flask application starts without errors
- [ ] Web interface loads at http://127.0.0.1:5000
- [ ] Test prediction returns results

## 🆘 Quick Troubleshooting

### Problem: pip install fails
**Solution**: 
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: Jupyter not found
**Solution**:
```bash
pip install jupyter notebook
```

### Problem: Model file not found when running app
**Solution**: 
- Make sure you ran the notebook completely
- Check that `model/house_price_model.pkl` exists
- File should be ~10-50 MB in size

### Problem: Port 5000 already in use
**Solution**:
```bash
# Change port in app.py (last line)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Problem: Dataset not found in notebook
**Solution**:
- Verify `train.csv` is in the `model/` directory
- Check the file size (should be ~460 KB)
- Ensure filename is exactly `train.csv` (not Train.csv)

## 📦 What You Should Have

After successful setup:

```
House Price Prediction System/
├── app.py                          ✓
├── requirements.txt                ✓
├── model/
│   ├── train.csv                   ✓ (downloaded)
│   ├── model_building.ipynb        ✓
│   └── house_price_model.pkl       ✓ (generated)
├── static/
│   └── style.css                   ✓
└── templates/
    ├── index.html                  ✓
    └── error.html                  ✓
```

## 🔄 Development Workflow

### Making Changes

1. **Edit Code**: Make your changes in app.py or other files
2. **Restart Server**: Press Ctrl+C, then run `python app.py` again
3. **Test Changes**: Refresh browser and test

### Retraining Model

1. **Edit Notebook**: Modify model_building.ipynb
2. **Run Notebook**: Kernel > Restart & Run All
3. **Restart App**: Stop and start `python app.py`

## 🌐 Next Steps

Once everything works locally:

1. **Test Thoroughly**: Try various input combinations
2. **Prepare for Deployment**: Follow DEPLOYMENT_GUIDE.md
3. **Create GitHub Repo**: Push your code
4. **Deploy**: Choose a platform (Render recommended)
5. **Submit**: Complete HousePrice_hosted_webGUI_link.txt

## 📚 Documentation

- **Full Documentation**: README.md
- **Deployment Guide**: DEPLOYMENT_GUIDE.md
- **API Examples**: See README.md API section

## 💡 Pro Tips

1. **Keep virtual environment activated** while working
2. **Save your work frequently** in Jupyter
3. **Test after every change** to catch issues early
4. **Use Git** to track changes
5. **Deploy early** to allow time for troubleshooting

## 🎓 Common Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install packages
pip install -r requirements.txt

# Run Jupyter
jupyter notebook

# Run Flask app
python app.py

# Check if running
curl http://localhost:5000/health

# Deactivate virtual environment
deactivate
```

## 📞 Need Help?

1. Check error message carefully
2. Review README.md for detailed info
3. Check DEPLOYMENT_GUIDE.md for deployment issues
4. Google the specific error
5. Ask instructor/TA

## 🎉 You're Ready!

If all steps completed successfully:
- ✅ Application is running locally
- ✅ Model is trained and loaded
- ✅ Predictions are working
- ✅ Ready for deployment!

**Next**: Read DEPLOYMENT_GUIDE.md to deploy your application!

---

**Estimated Total Time**: 10 minutes  
**Difficulty Level**: Beginner-friendly  
**Support**: See README.md for contact info

---

**Quick Start Complete! Happy Coding! 🚀**
