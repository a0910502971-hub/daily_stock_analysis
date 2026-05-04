import yfinance as yf
import datetime

stocks = ["2330.TW", "2317.TW", "2454.TW"]

def analyze_stock(symbol):
   time.sleep(1)
    data = yf.download(symbol, period="1mo", progress=False, threads=False)
    if data.empty:
    return {
        "symbol": symbol,
        "error": "抓不到資料"
    }

   latest = data.iloc[-1]
close_price = float(latest["Close"])

ma5 = float(data["Close"].rolling(5).mean().iloc[-1])
ma20 = float(data["Close"].rolling(20).mean().iloc[-1])
    decision = "觀望"

  if close_price > ma5 and ma5 > ma20:
    decision = "買入"
elif close_price < ma20:
    decision = "賣出"

    return {
        "symbol": symbol,
        "price": round(latest["Close"], 2),
        "ma5": round(ma5, 2),
        "ma20": round(ma20, 2),
        "decision": decision
    }

results = []

for s in stocks:
    results.append(analyze_stock(s))

today = datetime.date.today()

with open(f"taiwan_report_{today}.txt", "w", encoding="utf-8") as f:
    for r in results:
        f.write(str(r) + "\n")

print("台股分析完成")
