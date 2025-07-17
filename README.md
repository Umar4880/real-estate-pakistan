# Real Estate Price Prediction in Pakistan 🏠

## 📊 Project Overview
This project performs comprehensive data analysis and machine learning model development to predict real estate prices in Pakistan using data from Zameen.com. The project demonstrates end-to-end data science workflow including data cleaning, exploratory data analysis, feature engineering, and model deployment.

**Author:** Rana Umar  
**Dataset:** [Real Estate Dataset Pakistan](https://www.kaggle.com/datasets/hassaanmustafavi/real-estate-dataset-pakistan)  
**Source:** Zameen.com listings

---

## 📁 Dataset Description
The dataset contains **16 features** describing various aspects of real estate properties:

- `index` - Unique identifier for each property
- `url` - Link to the property listing on Zameen.com
- `type` - Property type (House, Flat, Plot, etc.)
- `purpose` - Purpose of listing (For Sale, For Rent)
- `area` - Property size (Kanal, Marla, Sq. Yd.)
- `bedroom` - Number of bedrooms
- `bath` - Number of bathrooms
- `added` - Days since property was listed
- `price` - Total property price (target variable)
- `initial_amount` - Initial down payment
- `monthly_installment` - Monthly payment amount
- `remaining_installments` - Number of installments left
- `location` - Specific location (e.g., DHA Defence)
- `location_city` - City name
- `location_province` - Province name
- `country` - Country (Pakistan)

---

## 🛠️ Key Steps & Methods

### 1. **Data Preprocessing**
- **Duplicate Removal:** Eliminated duplicate entries
- **Missing Value Imputation:** 
  - Installment columns filled with 0 (no installments)
  - Location province mapped from city data
  - Bedroom/bath values imputed using median by property type and area
- **Type Correction:** Converted categorical columns and standardized data types

### 2. **Data Cleaning & Standardization**
- **Area Normalization:** Converted all area units (Kanal, Marla, Sq. Yd.) to square feet
- **Price Standardization:** Converted all price formats (Arab, Crore, Lakh, Thousand) to Lakhs
- **Data Anomaly Handling:** Removed properties with impossible bedroom/bath combinations for given areas

### 3. **Outlier Detection & Handling**
- **IQR Method:** Used Interquartile Range for outlier detection
- **Domain Knowledge:** Applied real estate expertise to filter unrealistic property combinations
- **Price Outliers:** Removed extreme price outliers for better model performance

### 4. **Exploratory Data Analysis**
- **Univariate Analysis:** Distribution analysis of all features
- **Bivariate Analysis:** Relationship exploration between features and target variable
- **Correlation Analysis:** Feature correlation heatmap generation
- **Visualizations:** Comprehensive plots using seaborn and matplotlib

### 5. **Feature Engineering**
- **New Features Created:**
  - `area_x_bedroom`: Area multiplied by bedroom count
  - `bed_bath_ratio`: Bedroom to bathroom ratio
  - `total_payments`: Sum of initial amount and total installments
- **Feature Scaling:** Applied Quantile Transformer for normal distribution

### 6. **Feature Encoding**
- **Frequency Encoding:** For high-cardinality location features
- **One-Hot Encoding:** For categorical variables (type, purpose, province)
- **Custom Transformers:** Built reusable encoding classes

### 7. **Model Development**
- **Models Tested:** LinearRegression, SVR, XGBRegressor, LGBMRegressor
- **Best Model:** XGBRegressor with optimized hyperparameters
- **Pipeline Creation:** End-to-end ML pipeline with preprocessing and modeling

---

## 📈 Results & Performance

### Model Performance Metrics:
- **R² Score:** ~0.85 (after outlier removal)
- **Mean Absolute Error:** Optimized for practical prediction accuracy
- **Root Mean Squared Error:** Minimized through feature engineering

### Key Insights:
- **Top Price Drivers:** Area, location, and property type are primary price determinants
- **Regional Patterns:** Punjab province shows highest property sales volume
- **Property Types:** Houses and commercial properties command premium prices

---

## 🚀 How to Use

### 1. **Clone the Repository**
```bash
git clone https://github.com/your-username/real-estate-pakistan.git
cd real-estate-pakistan
```

### 2. **Install Dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost lightgbm missingno
```

### 3. **Run the Analysis**
- Open [`real-estate-pakistan.ipynb`](real-estate-pakistan.ipynb) in Jupyter Notebook or VS Code
- Ensure the dataset is in the `Datasets/` folder
- Run all cells to reproduce the complete analysis

### 4. **Use the Trained Model**
```python
import pickle
import pandas as pd

# Load the trained model
with open('train_model/real-estate-pakistan_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Make predictions
sample_data = pd.DataFrame({
    'type': ['House'],
    'area(sqft)': [2250.0],
    'purpose': ['For Sale'],
    'bedroom': [3.0],
    'bath': [3.0],
    'initial_amount(Lakhs)': [0.0],
    'monthly_installment(Lakhs)': [0.0],
    'remaining_installments': [0.0],
    'location': ['DHA Defence'],
    'location_city': ['Lahore'],
    'location_province': ['Punjab']
})

predicted_price = model.predict(sample_data)
print(f"Predicted Price: {predicted_price[0]:.2f} Lakhs")
```

---

## 📂 Project Structure
```
real-estate-pakistan/
├── notebook/
│   └── real-estate-pakistan.ipynb     # Main analysis notebook
├── train_model/
│   └── real-estate-pakistan_model.pkl # Trained model
├── static/
│   ├── real-estate.js                 # Web app JavaScript
│   └── style.css                      # Styling
├── templates/
│   └── index.html                     # Web interface
├── utils/                             # Utility functions
├── app.py                             # Flask web application

```

---

## 🔧 Technical Implementation

### Custom Transformers Built:
- **`CustomImputer`**: Intelligent missing value imputation based on property characteristics
- **`FrequencyEncoder`**: Frequency-based encoding for categorical variables
- **`CustomPaymentImputer`**: Specialized imputation for payment-related features
- **`FeatureGeneration`**: Automated feature engineering transformer

### Pipeline Architecture:
```python
Pipeline([
    ('feature_imputation', ColumnTransformer()),
    ('feature_generation', FeatureGeneration()),
    ('preprocessing', ColumnTransformer()),
    ('regressor', XGBRegressor())
])
```

---

## 💡 Future Enhancements
- **Advanced Models:** Implement ensemble methods and neural networks
- **Real-time Data:** Integration with live property listing APIs
- **Geographic Analysis:** Add latitude/longitude for spatial modeling
- **Market Trends:** Time series analysis for price trend prediction
- **Web Deployment:** Deploy model as REST API using Flask/FastAPI

---

## 📊 Visualizations Included
- Distribution plots for all numeric features
- Correlation heatmaps
- Outlier detection scatter plots
- Property type and location analysis
- Price vs. feature relationship plots
- Before/after preprocessing comparisons

---

## 🏆 Project Highlights
- **Comprehensive EDA:** In-depth analysis of Pakistani real estate market
- **Domain Expertise:** Applied real estate knowledge for data cleaning
- **Production-Ready:** Complete ML pipeline with custom transformers
- **Reproducible:** Well-documented code with clear methodology
- **Scalable:** Modular design for easy extension and deployment

---

## 📝 Dependencies
```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
lightgbm>=3.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
missingno>=0.5.0
```

---

## 📄 License
This project is open source and available under the [MIT License](LICENSE).

---

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📧 Contact
**Rana Umar**  
- GitHub: [@Umar4880](https://github.com/Umar4880)
- Email: ranaumarranaumar705@gmail.com

---

**⭐ If you found this project helpful, please consider giving it a star!**
