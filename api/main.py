from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# -------------------------------
# Load Model (once at startup)
# -------------------------------
model = joblib.load("models/salary_model_fixed.pkl")

app = FastAPI(title="Salary Prediction API")


def preprocess_input(df):
    df['location_group'] = df['location'].replace({
        'India': 'Low_income',
        'USA': 'High_income',
        'Canada': 'High_income',
        'Australia': 'High_income',
        'Singapore': 'High_income'
    })
    
    df['job_code'] = df['job_title'].astype('category').cat.codes
    df['loc_code'] = df['location_group'].astype('category').cat.codes
    
    df['exp_x_job'] = df['experience_years'] * df['job_code']
    df['exp_x_location'] = df['experience_years'] * df['loc_code']
    df['exp_squared'] = df['experience_years'] ** 2
    
    return df

# -------------------------------
# Request Schema (STRICT)
# -------------------------------
class InputData(BaseModel):
    job_title: str
    experience_years: int
    education_level: str
    skills_count: int
    industry: str
    company_size: str
    location: str
    remote_work: str
    certifications: int


# -------------------------------
# Health Check Endpoint
# -------------------------------
@app.get("/")
def home():
    return {"message": "API is running"}


# -------------------------------
# Prediction Endpoint
# -------------------------------
@app.post("/predict")
def predict(data: InputData):
    try:
        # Convert input to DataFrame
        df = pd.DataFrame([data.model_dump()])

        # Preprocess input
        df = preprocess_input(df)

        # Prediction
        prediction = model.predict(df)[0]

        return {
            "predicted_salary": round(float(prediction), 2)
        }

    except Exception as e:
        return {"error": str(e)}