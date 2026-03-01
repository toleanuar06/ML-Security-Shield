import pandas as pd
import re


# 1. Деректерді жүктеу функциясы
def load_and_explore_data(filepath):
    print("Деректер оқылуда...")
    try:
        # CSV файлын оқу (бағандары: 'url' және 'label')
        # label: 0 - таза, 1 - қауіпті
        df = pd.read_csv(filepath)
        print("Деректер сәтті жүктелді!\n")

        # Деректердің теңгерімін (балансын) көру
        print("Деректер статистикасы:")
        stats = df['label'].value_counts().rename({0: 'Таза сайттар', 1: 'Қауіпті сайттар'})
        print(stats)
        return df
    except FileNotFoundError:
        print(f"Қате: '{filepath}' файлы табылмады. Оны жүктеп, осы папкаға салу керек.")
        return None


# 2. Машиналық оқытуға арналған белгілерді (features) жасау
# Бұл процесті (Feature Extraction) кейінірек өнімділікті арттыру үшін C++ тілінде жазуға болады
def extract_features(url):
    features = {}

    # URL ұзындығы (фишингтік сайттар көбіне өте ұзын болады)
    features['url_length'] = len(url)

    # URL ішінде IP-адрестің тікелей жазылуын тексеру
    features['has_ip'] = 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0

    # Күдікті таңбаларды санау
    features['count_at'] = url.count('@')  # '@' таңбасы көбіне құпия сөз ұрлау үшін қолданылады
    features['count_hyphen'] = url.count('-')  # Жалған сайттарда дефис көп болады (мысалы, secure-login-paypal.com)
    features['count_digits'] = sum(c.isdigit() for c in url)  # Сандардың мөлшері

    # 'https' қауіпсіздік хаттамасының болуы
    features['is_https'] = 1 if url.startswith("https://") else 0

    return features


if __name__ == "__main__":
    # Егер сізде 'malicious_urls.csv' файлы болса, мына қатарды іске қосамыз:
    # dataset = load_and_explore_data('malicious_urls.csv')

    # Әзірше функцияның қалай жұмыс істейтінін бірнеше мысалмен көрейік:
    sample_urls = [
        "https://www.github.com",  # Таза сайт
        "http://192.168.1.55/update-account-info",  # IP адресі бар күдікті сайт
        "http://free-money-winner.com@login-secure.info"  # '@' және дефисі бар фишинг
    ]

    print("--- URL Белгілерін талдау (Feature Extraction) ---")
    for url in sample_urls:
        print(f"\nСілтеме: {url}")
        print("Модельге жіберілетін деректер:", extract_features(url))