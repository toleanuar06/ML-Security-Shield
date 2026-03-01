import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# 1. Белгілерді (features) шығарып алу функциясы (алдыңғы сабақтан)
def extract_features(url):
    return {
        'url_length': len(url),
        'has_ip': 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0,
        'count_at': url.count('@'),
        'count_hyphen': url.count('-'),
        'count_digits': sum(c.isdigit() for c in url),
        'is_https': 1 if url.startswith("https://") else 0
    }


# 2. Жаттығуға арналған шағын деректер (Mock Data)
# 0 - таза (қауіпсіз), 1 - қауіпті (фишинг/зиянды)
mock_data = [
    {"url": "https://www.google.com", "label": 0},
    {"url": "https://github.com/microsoft", "label": 0},
    {"url": "http://192.168.1.55/login-update", "label": 1},
    {"url": "http://secure-paypal-update.com-info.xyz", "label": 1},
    {"url": "https://kaznu.kz", "label": 0},
    {"url": "http://free-money-winner.com@login-secure.info", "label": 1},
    {"url": "https://www.youtube.com", "label": 0},
    {"url": "http://10.0.0.1/malware.exe", "label": 1}
]

print("1. Деректер дайындалуда...")
df = pd.DataFrame(mock_data)

# Әрбір URL-дан математикалық белгілерді шығарып, жаңа кесте жасаймыз
features_df = df['url'].apply(lambda x: pd.Series(extract_features(x)))

# X - бұл біздің математикалық белгілеріміз (сұрақтар)
# y - бұл олардың нақты статусы (дұрыс жауаптар)
X = features_df
y = df['label']

print("2. Модельді үйрету басталуда...")
# Деректерді үйрету (80%) және тексеру (20%) үшін екіге бөлеміз
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Random Forest алгоритмін іске қосу
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # Модель осы жерде "оқиды"

print("3. Модель сәтті үйретілді!\n")

# Модельдің қаншалықты ақылды екенін тексеру
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Модельдің дәлдігі (Accuracy): {accuracy * 100}%\n")

print("--- ЖАҢА СІЛТЕМЕЛЕРДІ ТЕКСЕРУ (СЫНАҚ) ---")
test_urls = [
    "https://192.168.1.1/web_whw/#/login",  # Таза сайт
    "http://172.16.254.1/admin-panel-login",  # IP арқылы кіретін күдікті сайт
    "http://verify-apple-id-update.com"  # Фишингке ұқсайтын сайт
]

for test_url in test_urls:
    # Жаңа сілтемені сандарға айналдырамыз
    features = pd.DataFrame([extract_features(test_url)])

    # Модельден болжам сұраймыз
    prediction = model.predict(features)[0]
    risk_prob = model.predict_proba(features)[0][1] * 100  # Қауіптілік пайызы

    # Нәтижені шығару
    status = "ҚАУІПТІ 🔴" if prediction == 1 else "ҚАУІПСІЗ 🟢"
    print(f"Сілтеме: {test_url}")
    print(f"Нәтиже: {status} (Қауіптілік деңгейі: {risk_prob:.1f}%)\n")
    # Модельді компьютер жадына файл ретінде сақтау
    joblib.dump(model, 'random_forest_model.pkl')
    print("Модель 'random_forest_model.pkl' файлы ретінде сақталды!")