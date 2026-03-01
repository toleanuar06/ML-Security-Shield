import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import time


# 10 БЕЛГІНІ БӨЛІП АЛУ
def extract_features_v2(url):
    suspicious_words = ['login', 'update', 'secure', 'bank', 'verify', 'account', 'free', 'admin', 'payment', 'support']

    # URL мәтін болмаған жағдайда (бос ұяшықтар қате бермес үшін)
    if not isinstance(url, str):
        return [0] * 10

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


print("1. Датасетті оқу басталды (urldata.csv)...")
try:
    df = pd.read_csv('urldata.csv')
    print(f"✅ Деректер оқылды! Жалпы сілтемелер саны: {len(df)}")
except FileNotFoundError:
    print("ҚАТЕ: 'urldata.csv' файлы табылмады. Файл атын және орнын тексеріңіз.")
    exit()

print("2. Сілтемелерден 10 математикалық белгіні шығарып алудамыз...")
print("⏳ Бұл процесс 2-5 минут алуы мүмкін. Күте тұрыңыз...")

start_time = time.time()
# Әрбір URL-ды сандарға айналдырамыз
features_df = df['url'].apply(lambda x: pd.Series(extract_features_v2(x)))
print(f"✅ Белгілер сәтті шығарылды! (Уақыты: {round(time.time() - start_time, 1)} секунд)")

# Суреттегі датасетте жауаптар 'result' бағанында 0 (таза) және 1 (қауіпті) деп тұр
X = features_df
y = df['result']

print("3. Модельді үйрету басталды...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Күшейтілген алгоритм параметрлері
model = RandomForestClassifier(n_estimators=150, max_depth=20, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

# Нәтижелерді тексеру
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"\n🏆 МОДЕЛЬДІҢ ДӘЛДІГІ: {round(accuracy * 100, 2)}%")

# Модельді сақтау
joblib.dump(model, 'random_forest_model.pkl')
print("✅ Жаңа, өте ақылды модель 'random_forest_model.pkl' болып сақталды!")