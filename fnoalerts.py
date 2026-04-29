import requests
import datetime
import time

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

def get_fno_movers():
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://www.nseindia.com"
    }
    session.get("https://www.nseindia.com", headers=headers, timeout=10)

    gainers, losers = [], []

    for symbol in FNO_SYMBOLS:
        try:
            url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
            r = session.get(url, headers={**headers, "Accept": "application/json"}, timeout=10)
            data = r.json()
            ltp = data["priceInfo"]["lastPrice"]
            change_pct = data["priceInfo"]["pChange"]
            if 0 < change_pct < 3:
                gainers.append((symbol, ltp, change_pct))
            elif -3 < change_pct < 0:
                losers.append((symbol, ltp, change_pct))
        except:
            continue

    gainers.sort(key=lambda x: x[2], reverse=True)
    losers.sort(key=lambda x: x[2])

    gainers = gainers[:5]
    losers = losers[:5]

    return gainers, losers

def build_message(gainers, losers):
    now = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")
    g_lines = "\n".join([f"  {s}: ₹{l} (+{c:.2f}%)" for s, l, c in gainers]) or "  None"
    l_lines = "\n".join([f"  {s}: ₹{l} ({c:.2f}%)" for s, l, c in losers]) or "  None"
    return (
        f"📊 *FnO Top 5 Movers — {now}*\n"
        f"_(Stocks with 0–3% move only)_\n\n"
        f"✅ *Top 5 Gainers:*\n{g_lines}\n\n"
        f"🔴 *Top 5 Losers:*\n{l_lines}"
    )

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    })

def get_last_update_id():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?limit=1&offset=-1"
    r = requests.get(url)
    data = r.json()
    if data["result"]:
        return data["result"][-1]["update_id"]
    return None

def listen_for_commands():
    """Listen for /fno command for 55 seconds and respond"""
    print("Listening for /fno commands for 55 seconds...")
    seen_ids = set()

    # Get current update_id to ignore old messages
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?limit=5&offset=-5"
    r = requests.get(url)
    data = r.json()
    for item in data.get("result", []):
        seen_ids.add(item["update_id"])

    start = time.time()
    while time.time() - start < 55:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?timeout=10"
            r = requests.get(url, timeout=15)
            updates = r.json().get("result", [])
            for update in updates:
                uid = update["update_id"]
                if uid in seen_ids:
                    continue
                seen_ids.add(uid)
                text = update.get("message", {}).get("text", "")
                chat_id = update.get("message", {}).get("chat", {}).get("id")
                if text.strip().lower() in ["/fno", "/fno@" + BOT_TOKEN.split(":")[0]]:
                    print(f"Got /fno command from {chat_id}")
                    send_telegram("⏳ Fetching FnO data, please wait...")
                    gainers, losers = get_fno_movers()
                    msg = build_message(gainers, losers)
                    send_telegram(msg)
        except:
            pass
        time.sleep(3)

import sys

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "scheduled"

    if mode == "scheduled":
        # Auto alert at 9:25 AM
        if datetime.datetime.today().weekday() < 5:
            gainers, losers = get_fno_movers()
            msg = build_message(gainers, losers)
            send_telegram(msg)
            print("Scheduled alert sent!")
        else:
            print("Weekend — skipping.")

    elif mode == "listen":
        # Listen for /fno commands
        listen_for_commands()
