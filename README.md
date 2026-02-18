💳 Credit Card Fraud Detection (Django REST + React)

A full-stack machine learning project that detects fraudulent credit card transactions in real time.
The system uses XGBoost optimized with Optuna, handles class imbalance with SMOTE, and exposes predictions through a Django REST Framework API consumed by a React frontend.

🚀 Features

🔍 Fraud detection using trained ML model

⚖️ Handles imbalanced dataset using SMOTE

🤖 Hyperparameter tuning with Optuna

📡 Real-time prediction via REST API

⚛️ React frontend for user interaction

📈 ROC-AUC evaluation and threshold tuning

🧠 Production-ready model serialization with joblib

🏗️ Tech Stack
Backend

Python

Django REST Framework

NumPy, Pandas

scikit-learn

XGBoost

Optuna

imbalanced-learn

Frontend

React

Fetch API

📊 Dataset

Dataset: Credit Card Fraud Detection

Highly imbalanced (fraud ≪ legit)

Features include:

Time

Amount

V1–V28 (PCA components)

Class (target)

🧠 Model Pipeline
1️⃣ Data Preprocessing

Loaded dataset with pandas

Checked missing values

Verified class imbalance

2️⃣ Train/Test Split

Stratified split to preserve fraud ratio

3️⃣ Handling Imbalance

Applied SMOTE on training data

4️⃣ Model Training

Base model: XGBoost

Metric focus: Recall for fraud class

5️⃣ Hyperparameter Optimization

Used Optuna

Tuned:

n_estimators

max_depth

learning_rate

subsample

colsample_bytree

6️⃣ Evaluation

Confusion Matrix

Classification Report

ROC-AUC score

Custom deployment threshold (0.4)

7️⃣ Model Saving
joblib.dump(xgb_best, "model.pkl")

🔌 API Endpoint
POST /predict/

Request Body

{
  "name": "John",
  "time": 12345,
  "amount": 250.75
}


Response

{
  "prediction": 1
}


Interpretation

1 → Fraud 🚨

0 → Legit ✅

⚛️ Frontend Flow

User enters:

Name

Time

Amount

React sends POST request to Django API

Backend returns prediction

UI displays Fraud / Legit status

📂 Project Structure
project/
│
├── backend/
│   ├── model.pkl
│   ├── views.py
│   └── urls.py
│
├── frontend/
│   └── Predict.jsx
│
├── training/
│   └── model_training.py
│
└── README.md

🛠️ Installation
1️⃣ Clone Repository
git clone https://github.com/PraveenAchary/CreditCardFraudDetection.git
cd credit-card-fraud-detection

2️⃣ Backend Setup
cd backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
python manage.py runserver

3️⃣ Frontend Setup
cd frontend
npm install
npm start

📈 Model Performance

Optimized for fraud recall

ROC-AUC evaluated

Threshold tuning for deployment

SMOTE improves minority detection

⚠️ In fraud detection, recall is prioritized over accuracy.

🚨 Known Issues / Improvements

🔧 Feature vector construction in API needs strict ordering

🔧 Input validation can be improved

🔧 Add probability output

🔧 Add Docker support

🔧 Add authentication

🔧 Deploy to cloud (AWS/Render)

🌟 Future Enhancements

Real payment gateway simulation

Model monitoring

Drift detection

Batch prediction endpoint

Explainable AI (SHAP)

Production deployment with Docker

👨‍💻 Author
 Praveen Vishwabramham AChary.

📜 License

This project is open source and available under the MIT License.
