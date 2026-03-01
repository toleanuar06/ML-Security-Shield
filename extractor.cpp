#include <iostream>
#include <string>
#include <regex>
#include <algorithm>
#include <cctype>

extern "C" {
    __declspec(dllexport) void extract_url_features(const char* url_c, int* results) {
        std::string url(url_c);

        // URL-ды кіші әріптерге айналдыру (сөздерді дұрыс іздеу үшін)
        std::string url_lower = url;
        std::transform(url_lower.begin(), url_lower.end(), url_lower.begin(),
            [](unsigned char c){ return std::tolower(c); });

        // 1. URL ұзындығы
        results[0] = url.length();

        // 2. IP-адрес бар ма?
        std::regex ip_regex(R"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})");
        results[1] = std::regex_search(url, ip_regex) ? 1 : 0;

        // 3. '@' таңбасының саны
        results[2] = std::count(url.begin(), url.end(), '@');

        // 4. '-' таңбасының саны
        results[3] = std::count(url.begin(), url.end(), '-');

        // 5. Сандардың мөлшері
        int count_digits = 0;
        for (char c : url) if (isdigit(c)) count_digits++;
        results[4] = count_digits;

        // 6. 'https://' хаттамасы
        results[5] = (url_lower.find("https://") == 0) ? 1 : 0;

        // 7. Нүктелердің '.' саны (ЖАҢА)
        results[6] = std::count(url.begin(), url.end(), '.');

        // 8. Күдікті сөздердің болуы (ЖАҢА)
        std::string suspicious_words[] = {"login", "update", "secure", "bank", "verify", "account", "free", "admin", "payment", "support"};
        int has_suspicious = 0;
        for (const auto& word : suspicious_words) {
            if (url_lower.find(word) != std::string::npos) {
                has_suspicious = 1;
                break;
            }
        }
        results[7] = has_suspicious;

        // 9. Теңдік '=' белгісінің саны (ЖАҢА)
        results[8] = std::count(url.begin(), url.end(), '=');

        // 10. Қиғаш сызық '/' саны (ЖАҢА)
        results[9] = std::count(url.begin(), url.end(), '/');
    }
}