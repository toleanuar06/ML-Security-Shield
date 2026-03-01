from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import re

# Серверді іске қосу
app = FastAPI()

# 450 мың сілтемемен оқытылған ЖАҢА АҚЫЛДЫ МОДЕЛЬДІ жүктеп алу
model = joblib.load('random_forest_model.pkl')


class URLRequest(BaseModel):
    url: str


# Барлық 10 математикалық белгіні Python-ның өзінде лезде бөліп алу
def extract_features_v2(url):
    suspicious_words = ['login', 'update', 'secure', 'bank', 'verify', 'account', 'free', 'admin', 'payment', 'support']
    url_lower = url.lower()

    return {
        'url_length': len(url),
        'has_ip': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'count_at': url.count('@'),
        'count_hyphen': url.count('-'),
        'count_digits': sum(c.isdigit() for c in url),
        'is_https': 1 if url_lower.startswith("https://") else 0,
        'count_dots': url.count('.'),
        'has_suspicious_words': 1 if any(word in url_lower for word in suspicious_words) else 0,
        'count_equals': url.count('='),
        'count_slash': url.count('/')
    }


@app.post("/check-url")
def check_url(request: URLRequest):
    # 1. Сілтемеден белгілерді алу
    features_dict = extract_features_v2(request.url)
    features = pd.DataFrame([features_dict])

    # 2. Модельден қауіптілік пайызын сұрау
    risk_prob = model.predict_proba(features)[0][1] * 100

    # 3. Шешім қабылдау
    if risk_prob <= 30:
        action = "ALLOW"
    elif risk_prob <= 70:
        action = "WARN"
    else:
        action = "BLOCK"

    return {
        "url": request.url,
        "risk_score": round(risk_prob, 2),
        "action": action
    }