import requests
import datetime

BOT_TOKEN = "8613392574:AAF83_86w1TGHdYuZF5ZXjwQPJQD8ss7fCM"
CHAT_ID = "7084342720"

FNO_SYMBOLS = [
    "ETERNAL", "RELIANCE", "BANDHANBNK", "MAZDOCK", "VEDL", "HDFCBANK",
    "SUNPHARMA", "COCHINSHIP", "MARUTI", "M&M", "BSE", "ADANIPOWER",
    "ONGC", "COALINDIA", "SBIN", "ICICIBANK", "BHARTIARTL", "INFY",
    "IDEA", "MCX", "RECLTD", "ITC", "DIXON", "SUZLON", "ADANIENT",
    "TATASTEEL", "AXISBANK", "RBLBANK", "LT", "DRREDDY", "JIOFIN",
    "WAAREEENER", "HCLTECH", "OFSS", "CROMPTON", "SHRIRAMFIN", "TCS",
    "PFC", "TMPV", "INDIGO", "BAJFINANCE", "ADANIGREEN", "VBL",
    "POWERINDIA", "SWIGGY", "ADANIPORTS", "INDUSTOWER", "TECHM", "KAYNES",
    "NATIONALUM", "HINDZINC", "FORCEMOT", "PERSISTENT", "NESTLEIND",
    "BPCL", "BHEL", "INDUSINDBK", "BHARATFORG", "LODHA", "TVSMOTOR",
    "BAJAJ-AUTO", "ADANIENSOL", "SAMMAANCAP", "SAIL", "TATAPOWER",
    "HINDALCO", "ULTRACEMCO", "EICHERMOT", "PAYTM", "BEL", "CANBK",
    "OIL", "TRENT", "NMDC", "HAL", "ABCAPITAL", "WIPRO", "HAVELLS",
    "NHPC", "JSWSTEEL", "GODFRYPHLP", "HINDUNILVR", "ASHOKLEY",
    "UNIONBANK", "NTPC", "BDL", "SONACOMS", "KEI", "POLYCAB",
    "AUROPHARMA", "HDFCLIFE", "NAUKRI", "POWERGRID", "HEROMOTOCO",
    "CDSL", "FEDERALBNK", "TITAN", "COFORGE", "IDFCFIRSTB", "KOTAKBANK",
    "RVNL", "BRITANNIA", "MAXHEALTH", "APOLLOHOSP", "ABB", "MOTHERSON",
    "YESBANK", "INDIANB", "GLENMARK", "POLICYBZR", "LAURUSLABS",
    "JSWENERGY", "PNB", "CGPOWER", "SBICARD", "GODREJPROP", "HYUNDAI",
    "EXIDEIND", "DLF", "GRASIM", "CUMMINSIND", "ASTRAL", "HDFCAMC",
    "MUTHOOTFIN", "BLUESTARCO", "KALYANKJIL", "TATAELXSI", "SBILIFE",
    "BANKBARODA", "AMBER", "HINDPETRO", "KPITTECH", "SUPREMEIND", "IOC",
    "ASIANPAINT", "PETRONET", "JINDALSTEL", "SOLARINDS", "LUPIN", "SRF",
    "DIVISLAB", "BAJAJFINSV", "ANGELONE", "NAM-INDIA", "UNOMINDA",
    "AUBANK", "MOTILALOFS", "JUBLFOOD", "BOSCHLTD", "PNBHOUSING", "IRFC",
    "MANAPPURAM", "IREDA", "CONCOR", "CIPLA", "MPHASIS", "LTM", "PIIND",
    "VOLTAS", "GAIL", "INDHOTEL", "GMRAIRPORT", "PGEL", "CHOLAFIN",
    "DMART", "LTF", "BANKINDIA", "LICHSGFIN", "IEX", "INOXWIND", "LICI",
    "UNITDSPR", "TATACONSUM", "VMM", "DALBHARAT", "PHOENIXLTD", "SIEMENS",
    "TORNTPHARM", "ZYDUSLIFE", "PREMIERENE", "AMBUJACEM", "NBCC", "BIOCON",
    "CAMS", "UPL", "APLAPOLLO", "FORTIS", "OBEROIRLTY", "DELHIVERY",
    "MFSL", "ICICIGI", "TIINDIA", "COLPAL", "NYKAA", "PAGEIND", "KFINTECH",
    "PRESTIGE", "360ONE", "MANKIND", "MARICO", "PIDILITIND", "ICICIPRULI",
    "GODREJCP", "ALKEM", "PATANJALI", "DABUR", "SHREECEM", "BAJAJHLDNG",
    "NUVAMA"
]

def get_quote(symbol, session):
    try:
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com"
        }
        r = session.get(url, headers=headers, timeout=10)
        data = r.json()
        ltp = data["priceInfo"]["lastPrice"]
        change_pct = data["priceInfo"]["pChange"]
        return ltp, change_pct
    except:
        return None, None

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })

def main():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.nseindia.com"
    }
    session.get("https://www.nseindia.com", headers=headers, timeout=10)

    gainers, losers = [], []

    for symbol in FNO_SYMBOLS:
        ltp, change_pct = get_quote(symbol, session)
        if ltp is None:
            continue
        if 0 < change_pct < 3:
            gainers.append((symbol, ltp, change_pct))
        elif -3 < change_pct < 0:
            losers.append((symbol, ltp, change_pct))

    gainers.sort(key=lambda x: x[2], reverse=True)
    losers.sort(key=lambda x: x[2])

    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

    g_lines = "\n".join([f"  {s}: ₹{l} (+{c:.2f}%)" for s, l, c in gainers]) or "  None"
    l_lines = "\n".join([f"  {s}: ₹{l} ({c:.2f}%)" for s, l, c in losers]) or "  None"

    full_msg = (
        f"📊 *FnO Movers — {now}*\n"
        f"_(Stocks with 0–3% move only)_\n\n"
        f"✅ *Gainers ({len(gainers)}):*\n{g_lines}\n\n"
        f"🔴 *Losers ({len(losers)}):*\n{l_lines}"
    )

    if len(full_msg) > 4000:
        send_telegram(f"📊 *FnO Gainers — {now}*\n✅ *({len(gainers)}):*\n{g_lines}")
        send_telegram(f"📊 *FnO Losers — {now}*\n🔴 *({len(losers)}):*\n{l_lines}")
    else:
        send_telegram(full_msg)

    print(f"Done! Gainers: {len(gainers)}, Losers: {len(losers)}")

if __name__ == "__main__":
    if datetime.datetime.today().weekday() < 5:
        main()
    else:
        print("Weekend — skipping.")
