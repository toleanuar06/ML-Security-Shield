import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# 1. ЖАҢАРТЫЛҒАН БЕЛГІЛЕРДІ БӨЛІП АЛУ (10 белгі)
def extract_features_v2(url):
    suspicious_words = ['login', 'update', 'secure', 'bank', 'verify', 'account', 'free', 'admin']

    return {
        'url_length': len(url),
        'has_ip': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'count_at': url.count('@'),
        'count_hyphen': url.count('-'),
        'count_digits': sum(c.isdigit() for c in url),
        'is_https': 1 if url.startswith("https://") else 0,

        # ЖАҢАДАН ҚОСЫЛҒАНДАР:
        'count_dots': url.count('.'),
        'has_suspicious_words': 1 if any(word in url.lower() for word in suspicious_words) else 0,
        'count_equals': url.count('='),
        'count_slash': url.count('/')
    }


# 2. КЕҢЕЙТІЛГЕН ДЕРЕКТЕР БАЗАСЫ (Егер дайын CSV файлыңыз болмаса)
mock_data = [
    {"url": "https://www.google.com", "label": 0},
    {"url": "https://github.com/microsoft", "label": 0},
    {"url": "https://kaznu.kz/kz/about", "label": 0},
    {"url": "https://en.wikipedia.org/wiki/Machine_learning", "label": 0},
    {"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "label": 0},
    {"url": "http://192.168.1.55/login-update-secure", "label": 1},
    {"url": "http://secure-paypal-update.com-info.xyz/verify?id=123", "label": 1},
    {"url": "http://free-money-winner.com@login-secure.info", "label": 1},
    {"url": "http://10.0.0.1/malware.exe", "label": 1},
    {"url": "http://apple-support-verify-account.com.login.submit.xyz", "label": 1},  # Көп нүктелі фишинг
    {"url": "https://steam-community-free-knives.ru/login", "label": 1},  # Ойынға қатысты фишинг
    {"url": "http://bank-of-america-urgent-update.net/admin=true", "label": 1}
]

print("1. Деректерді сараптау басталды...")
df = pd.DataFrame(mock_data)

# Барлық сілтемелерді жаңа 10 белгі бойынша сандарға айналдыру
features_df = df['url'].apply(lambda x: pd.Series(extract_features_v2(x)))

X = features_df
y = df['label']

print("2. Күшейтілген Модельді үйрету...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# ЖЕТІЛДІРІЛГЕН БАПТАУЛАР: n_estimators (200 ағаш)
model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

# Дәлдікті тексеру
predictions = model.predict(X_test)
print(f"Модельдің дәлдігі: {accuracy_score(y_test, predictions) * 100}%\n")

# Жаңа модельді сақтау (ескісінің үстінен жазылады)
joblib.dump(model, 'random_forest_model.pkl')
print("✅ Жаңа, күшейтілген модель 'random_forest_model.pkl' болып сақталды!\n")

# --- СЫНАҚ ---
print("--- КҮРДЕЛІ СІЛТЕМЕЛЕРДІ ТЕКСЕРУ ---")
test_urls = [
    "https://web.telegram.org/k/",  # Қауіпсіз
    "http://verify-account-update.xyz/login?user=admin"  # Өте қауіпті фишинг
]

for test_url in test_urls:
    features = pd.DataFrame([extract_features_v2(test_url)])
    risk_prob = model.predict_proba(features)[0][1] * 100
    status = "ҚАУІПТІ 🔴" if risk_prob > 50 else "ҚАУІПСІЗ 🟢"
    print(f"Сілтеме: {test_url}")
    print(f"Нәтиже: {status} (Қауіп: {risk_prob:.1f}%)\n")