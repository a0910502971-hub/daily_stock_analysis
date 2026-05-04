iimport yfinance as yf
import datetime
import time
import math
import pandas as pd

# 🔥 成交量熱門股（近市場活躍股，模擬前100池）
stocks = [
    "2330.TW","2317.TW","2454.TW","2303.TW","2337.TW",
    "2313.TW","3037.TW","2408.TW","2882.TW","2881.TW",
    "2891.TW","2887.TW","2883.TW","2603.TW","2609.TW",
    "2002.TW","2006.TW","1301.TW","1303.TW","1216.TW",
    "1101.TW","3034.TW","2357.TW","2382.TW","3017.TW",
    "6415.TW","2379.TW","3661.TW","3443.TW","4958.TW",
    "3036.TW","2367.TW","2489.TW","1802.TW","2404.TW"
]

# 📊 RSI
def calc_rsi(data, period=14):
    delta = data["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# 🔍 分析
def analyze_stock(symbol):
    time.sleep(0.3)

    try:
        data = yf.download(symbol, period="3mo", interval="1d", progress=False)

        if data is None or len(data) < 30:
            return None

        latest = data.iloc[-1]
        close = float(latest["Close"])
        volume = float(latest["Volume"])

        ma5 = float(data["Close"].rolling(5).mean().iloc[-1])
        ma20 = float(data["Close"].rolling(20).mean().iloc[-1])
        ma60 = float(data["Close"].rolling(60).mean().iloc[-1])
        rsi = float(calc_rsi(data).iloc[-1])

        if math.isnan(ma60) or math.isnan(rsi):
            return None

        score = 0

        # 🔥 1. 趨勢（最重要）
        if close > ma5 > ma20 > ma60:
            score += 5

        # 🔥 2. RSI（動能）
        if 55 < rsi < 70:
            score += 3

        # 🔥 3. 成交量（主力）
        if volume > data["Volume"].rolling(5).mean().iloc[-1]:
            score += 3

        # 🔥 4. 突破（職業級）
        recent_high = data["Close"].rolling(20).max().iloc[-2]
        if close > recent_high:
            score += 4

        # 🔥 5. 強勢股
        if close > ma20:
            score += 1

        return {
            "symbol": symbol,
            "price": round(close, 2),
            "rsi": round(rsi, 2),
            "score": score
        }

    except:
        return None

# 🚀 主程式
results = []

for s in stocks:
    r = analyze_stock(s)
    if r:
        results.append(r)

# 🔥 排序
results = sorted(results, key=lambda x: x["score"], reverse=True)

top3 = results[:3]

# 📄 輸出
today = datetime.date.today()

with open(f"pro_top3_{today}.txt", "w", encoding="utf-8") as f:
    f.write("🔥 職業級最強3檔（成交量+動能）\n\n")
    for r in top3:
        f.write(str(r) + "\n")

print("完成🔥")
