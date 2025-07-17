from flask import Flask, render_template, jsonify, request
import json, pickle
import pandas as pd
import numpy as np 
import traceback
import sys
from utils.transfomers import CustomImputer, CustomPaymentImputer, FeatureGeneration,  FrequencyEncoder
from sklearn import set_config

app = Flask(__name__)


with open('train_model/real-estate-pakistan_model.pkl', 'rb') as f:
    pipeline = pickle.load(f)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
      try:
            # Print received data for debugging
            data = request.json  

            # Set display options for better visualization
            set_config(transform_output='pandas')

            input_data = pd.DataFrame({
                'type': [data['type']],
                'area(sqft)': [float(data['area'])],
                'purpose': [data['purpose']],
                'bedroom': [float(data['bedrooms'])],
                'bath': [float(data['bath'])],
                'initial_amount(Lakhs)': [float(data['initial_amount'])],
                'monthly_installment(Lakhs)': [float(data['monthly_installment'])],
                'remaining_installments': [int(data['remaining_installments'])],
                'location': [data['location']],
                'location_city': [data['location_city']],
                'location_province': [data['location_province']]
            })
            
            # Print the input DataFrame for debugging
            print(f"Input DataFrame:")
            
            # Make prediction with web form data
            raw_prediction = pipeline.predict(input_data)
            print(f"Raw prediction (logged value): {raw_prediction}")

            # Convert from log to original scale and ensure non-negative values

            prediction = np.expm1(raw_prediction)[0] # Ensure non-negative value
            print(f"Final prediction (unlogged): {prediction}")
            
            
            return jsonify({
                'success': True,
                'prediction': float(prediction),  # Ensure it's a proper float, not numpy type
                'prediction_formatted': f'{prediction:.2f} Lakhs',
                'debug': {
                    'input_data': input_data.to_dict(),
                    'logged_prediction': float(raw_prediction),
                    'raw_prediction_before_max': float(prediction),
                }
            })
      except Exception as e:
            # Get detailed exception information for debugging
            exc_type, exc_value, exc_traceback = sys.exc_info()
            error_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
            print(f"ERROR: {str(e)}")
            print("".join(error_details))
            
            return jsonify({
                'success': False, 
                'error': str(e),
                'error_details': "".join(error_details)
            })
      
if __name__ == '__main__':
    app.run(debug=True)