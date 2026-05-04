import yfinance as yf
import datetime
import time
import math

# 👉 台股清單（你可以自己加）
stocks = ["2330.TW", "2317.TW", "2454.TW"]

def analyze_stock(symbol):
    time.sleep(1)  # 避免被封鎖

    try:
        data = yf.download(
            symbol,
            period="3mo",          # ⭐ 改這個（解決 MA20 問題）
            interval="1d",
            progress=False,
            threads=False
        )

        # ❌ 沒資料
        if data is None or len(data) == 0:
            return {
                "symbol": symbol,
                "error": "抓不到資料"
            }

        latest = data.iloc[-1]
        close_price = float(latest["Close"])

        # 計算均線
        ma5 = float(data["Close"].rolling(5).mean().iloc[-1])
        ma20 = float(data["Close"].rolling(20).mean().iloc[-1])

        # ❌ MA20 還是無法算
        if math.isnan(ma20):
            return {
                "symbol": symbol,
                "error": "資料不足 (MA20)"
            }

        # 決策邏輯
        decision = "觀望"

        if close_price > ma5 and ma5 > ma20:
            decision = "買入 🔥"
        elif close_price < ma20:
            decision = "賣出 ❗"

        return {
            "symbol": symbol,
            "price": round(close_price, 2),
            "ma5": round(ma5, 2),
            "ma20": round(ma20, 2),
            "decision": decision
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e)
        }


# 👉 主程式
results = []

for s in stocks:
    results.append(analyze_stock(s))

# 👉 輸出報告
today = datetime.date.today()

filename = f"taiwan_report_{today}.txt"

with open(filename, "w", encoding="utf-8") as f:
    for r in results:
        f.write(str(r) + "\n")

print("完成，輸出檔案:", filename)
