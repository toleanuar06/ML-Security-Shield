chrome.tabs.onUpdated.addListener(async (tabId, changeInfo, tab) => {
    // Сайт жүктеле бастаған кезде ғана іске қосылады
    if (changeInfo.status === 'loading' && tab.url) {

        // Браузердің ішкі сілтемелерін тексермейміз (қате шықпас үшін)
        if (tab.url.startsWith('chrome://') || tab.url.startsWith('chrome-extension://')) return;

        try {
            // Серверге сұраныс жіберу
            let response = await fetch("http://127.0.0.1:8000/check-url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: tab.url })
            });

            let result = await response.json();

            // Егер модель сайтты "Қызыл" (BLOCK) деп тапса:
            if (result.action === "BLOCK") {
                // Бұғаттау парақшасына бағыттау
                let blockUrl = chrome.runtime.getURL("block.html") + "?url=" + encodeURIComponent(tab.url) + "&score=" + result.risk_score;
                chrome.tabs.update(tabId, { url: blockUrl });
            }
            // Ескерту: Сары деңгей болса (WARN), әзірге консольге ғана жазамыз
            else if (result.action === "WARN") {
                console.log("Күдікті сайт табылды: " + tab.url);
            }
        } catch (error) {
            console.error("Python серверімен байланыс жоқ:", error);
        }
    }
});