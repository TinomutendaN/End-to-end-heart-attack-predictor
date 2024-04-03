import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import pickle

# Set page title and background
st.set_page_config(page_title="Heart Attack Prediction", page_icon="💓", layout= "centered")
st.markdown(
    """
    <style>
    .reportview-container {
        background: black );
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load the pre-trained model
@st.cache_data
def load_model():
    with open('savedmodel.sav', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()


# Add a title
st.title("Heart Attack Predictor")

# Add a description
st.write("Enter the following details to predict the likelihood of a heart attack.")

# Create input fields
col1, col2 = st.columns(2)
with col1: 
   age = st.number_input("Age", min_value=1, max_value=100, step=1)
   sex = st.radio("Sex", [1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
   cp = st.selectbox("Chest Pain Type", range(4), format_func=lambda x: ["Typical Angina", "Atypical Angina", "Non-Anginal Pain", "Asymptomatic"][x])
   trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=1, max_value=300, step=1)
   chol = st.number_input("Cholesterol (mg/dL)", min_value=1, max_value=1000, step=1)
   fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
  
with col2:  
   restecg = st.selectbox("Resting Electrocardiographic Results", range(3), format_func=lambda x: ["Normal", "Abnormal", "Probable Ventricular Hypertrophy"][x])
   thalach = st.number_input("Maximum Heart Rate Achieved", min_value=1, max_value=300, step=1)
   exang = st.selectbox("Exercise Induced Angina", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
   oldpeak = st.number_input("ST Depression Induced by Exercise Relative to Rest", min_value=0.0, max_value=10.0, step=0.1)
   slope = st.selectbox("Slope of the Peak Exercise ST Segment", range(3), format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
   ca = st.selectbox("Number of Major Vessels Colored by Fluoroscopy", ["0", "1", "2", "3"])

thal = st.selectbox("Thalassemia", range(4), format_func=lambda x: ["Normal", "Fixed Defect", "Reversible Defect", "Thalassemia"][x])

# Prepare the input data
input_data = pd.DataFrame({
    "age": [age],
    "sex": [sex],
    "cp": [cp],
    "trestbps": [trestbps],
    "chol": [chol],
    "fbs": [fbs],
    "restecg": [restecg],
    "thalach": [thalach],
    "exang": [exang],
    "oldpeak": [oldpeak],
    "slope": [slope],
    "ca": [ca],
    "thal": [thal]
})

# Define the target labels
target_labels = ["No Heart Attack", "Heart Attack"]

# Make the prediction
if st.button("Predict"):
    prediction = model.predict(input_data)
    prediction_label = target_labels[prediction[0]]
    
    # Display the prediction result
    if prediction_label == "Heart Attack":
        st.error("❗ High Risk of Heart Attack")
        
    else:
        st.success("✅ Low Risk of Heart Attack")