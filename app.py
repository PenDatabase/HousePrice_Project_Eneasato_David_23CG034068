"""
House Price Prediction System - Flask Web Application
Production-grade Flask app for house price predictions using Random Forest model
"""

from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Global variable to store model package
MODEL_PACKAGE = None
MODEL_PATH = 'model/house_price_model.pkl'

def load_model():
    """
    Load the trained model and preprocessing objects
    Returns: Dictionary containing model, scaler, encoder, and metadata
    """
    global MODEL_PACKAGE
    
    if MODEL_PACKAGE is None:
        try:
            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
            
            MODEL_PACKAGE = joblib.load(MODEL_PATH)
            print("✓ Model loaded successfully!")
            print(f"  - Model type: Random Forest Regressor")
            print(f"  - Features: {len(MODEL_PACKAGE['feature_columns'])}")
            print(f"  - Test R² Score: {MODEL_PACKAGE['metrics']['test']['R2']:.4f}")
            
        except Exception as e:
            print(f"ERROR loading model: {e}")
            raise
    
    return MODEL_PACKAGE

def validate_input(data):
    """
    Validate user input data
    
    Args:
        data: Dictionary containing user inputs
    
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        # Check required fields
        required_fields = ['overall_qual', 'gr_liv_area', 'total_bsmt_sf', 
                          'garage_cars', 'year_built', 'neighborhood']
        
        for field in required_fields:
            if field not in data or data[field] == '':
                return False, f"Missing required field: {field}"
        
        # Validate Overall Quality (1-10)
        overall_qual = int(data['overall_qual'])
        if not 1 <= overall_qual <= 10:
            return False, "Overall Quality must be between 1 and 10"
        
        # Validate Living Area (positive number)
        gr_liv_area = float(data['gr_liv_area'])
        if gr_liv_area <= 0:
            return False, "Living Area must be a positive number"
        
        # Validate Basement Area (non-negative)
        total_bsmt_sf = float(data['total_bsmt_sf'])
        if total_bsmt_sf < 0:
            return False, "Basement Area cannot be negative"
        
        # Validate Garage Cars (0-4)
        garage_cars = int(data['garage_cars'])
        if not 0 <= garage_cars <= 4:
            return False, "Garage Cars must be between 0 and 4"
        
        # Validate Year Built (reasonable range)
        year_built = int(data['year_built'])
        current_year = datetime.now().year
        if not 1800 <= year_built <= current_year:
            return False, f"Year Built must be between 1800 and {current_year}"
        
        # Neighborhood validation is handled by the encoder
        
        return True, None
        
    except ValueError as e:
        return False, f"Invalid input format: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def predict_price(overall_qual, gr_liv_area, total_bsmt_sf, 
                 garage_cars, year_built, neighborhood):
    """
    Predict house price using the trained model
    
    Args:
        overall_qual: Overall material and finish quality (1-10)
        gr_liv_area: Above grade living area (sq ft)
        total_bsmt_sf: Total basement area (sq ft)
        garage_cars: Garage size in car capacity (0-4)
        year_built: Original construction year
        neighborhood: Neighborhood name
    
    Returns:
        dict: Prediction result with price and confidence metrics
    """
    try:
        # Load model package
        package = load_model()
        model = package['model']
        scaler = package['scaler']
        encoder = package['label_encoder']
        
        # Encode neighborhood
        try:
            neighborhood_encoded = encoder.transform([neighborhood])[0]
        except ValueError:
            # If neighborhood not in training data, use mode/default
            neighborhood_encoded = 0
            print(f"Warning: Unknown neighborhood '{neighborhood}', using default")
        
        # Create feature array in correct order
        features = np.array([[
            float(overall_qual),
            float(gr_liv_area),
            float(total_bsmt_sf),
            float(garage_cars),
            float(year_built),
            neighborhood_encoded
        ]])
        
        # Scale features
        features_scaled = scaler.transform(features)
        
        # Make prediction
        predicted_price = model.predict(features_scaled)[0]
        
        # Get prediction intervals using individual tree predictions
        tree_predictions = np.array([tree.predict(features_scaled)[0] 
                                    for tree in model.estimators_])
        
        prediction_std = np.std(tree_predictions)
        lower_bound = predicted_price - 1.96 * prediction_std  # 95% CI
        upper_bound = predicted_price + 1.96 * prediction_std
        
        # Ensure non-negative prices
        predicted_price = max(0, predicted_price)
        lower_bound = max(0, lower_bound)
        upper_bound = max(0, upper_bound)
        
        return {
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'lower_bound': round(lower_bound, 2),
            'upper_bound': round(upper_bound, 2),
            'confidence': 95,
            'model_r2': round(package['metrics']['test']['R2'], 4),
            'model_rmse': round(package['metrics']['test']['RMSE'], 2)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Prediction error: {str(e)}"
        }

@app.route('/')
def home():
    """
    Render the home page with input form
    """
    try:
        # Load model to get neighborhood list
        package = load_model()
        neighborhoods = sorted(package['neighborhoods'])
        
        return render_template('index.html', neighborhoods=neighborhoods)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests from the web form
    """
    try:
        # Get form data
        data = {
            'overall_qual': request.form.get('overall_qual'),
            'gr_liv_area': request.form.get('gr_liv_area'),
            'total_bsmt_sf': request.form.get('total_bsmt_sf'),
            'garage_cars': request.form.get('garage_cars'),
            'year_built': request.form.get('year_built'),
            'neighborhood': request.form.get('neighborhood')
        }
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return render_template('index.html', 
                                 error=error_message,
                                 neighborhoods=load_model()['neighborhoods'],
                                 form_data=data)
        
        # Make prediction
        result = predict_price(
            overall_qual=data['overall_qual'],
            gr_liv_area=data['gr_liv_area'],
            total_bsmt_sf=data['total_bsmt_sf'],
            garage_cars=data['garage_cars'],
            year_built=data['year_built'],
            neighborhood=data['neighborhood']
        )
        
        if result['success']:
            return render_template('index.html',
                                 prediction=result,
                                 neighborhoods=load_model()['neighborhoods'],
                                 form_data=data)
        else:
            return render_template('index.html',
                                 error=result['error'],
                                 neighborhoods=load_model()['neighborhoods'],
                                 form_data=data)
    
    except Exception as e:
        return render_template('index.html',
                             error=f"An error occurred: {str(e)}",
                             neighborhoods=load_model()['neighborhoods'])

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """
    API endpoint for predictions (JSON response)
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'error': error_message
            }), 400
        
        # Make prediction
        result = predict_price(
            overall_qual=data['overall_qual'],
            gr_liv_area=data['gr_liv_area'],
            total_bsmt_sf=data['total_bsmt_sf'],
            garage_cars=data['garage_cars'],
            year_built=data['year_built'],
            neighborhood=data['neighborhood']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/neighborhoods', methods=['GET'])
def get_neighborhoods():
    """
    API endpoint to get list of valid neighborhoods
    """
    try:
        package = load_model()
        return jsonify({
            'success': True,
            'neighborhoods': sorted(package['neighborhoods'])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/model-info', methods=['GET'])
def model_info():
    """
    API endpoint to get model information and metrics
    """
    try:
        package = load_model()
        return jsonify({
            'success': True,
            'algorithm': 'Random Forest Regressor',
            'features': package['selected_features'],
            'metrics': {
                'test_r2': package['metrics']['test']['R2'],
                'test_rmse': package['metrics']['test']['RMSE'],
                'test_mae': package['metrics']['test']['MAE'],
                'cv_mean_r2': package['metrics']['cv_mean'],
                'cv_std_r2': package['metrics']['cv_std']
            },
            'persistence_method': 'Joblib'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for deployment monitoring
    """
    try:
        package = load_model()
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'model_loaded': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('error.html', error="Internal server error"), 500

if __name__ == '__main__':
    # Load model at startup
    try:
        load_model()
        print("\n" + "="*50)
        print("🏠 HOUSE PRICE PREDICTION SYSTEM")
        print("="*50)
        print("Starting Flask application...")
        print("Access the app at: http://127.0.0.1:5000")
        print("="*50 + "\n")
        
        # Run Flask app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except Exception as e:
        print(f"\n❌ Failed to start application: {e}")
        print("Please ensure the model file exists at: model/house_price_model.pkl")
        print("Run the model_building.ipynb notebook first to train and save the model.")
