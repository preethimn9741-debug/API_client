
import requests
import argparse
import json
import os

# -----------------------------
# Helper: Load Base URL from config.json (optional)
# -----------------------------
CONFIG_FILE = "config.json"

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        BASE_URL = config.get("base_url", "https://open.er-api.com/v6/latest/")
else:
    BASE_URL = "https://open.er-api.com/v6/latest/"

# -----------------------------
# 1. Fetch currency rates from API
# -----------------------------
def get_rates(base="USD"):
    url = f"{BASE_URL}{base}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        
        print("API Error:", e)
        return None

# -----------------------------
# 2. Convert currency
# -----------------------------
def convert(amount, from_curr, to_curr):
    data = get_rates(from_curr)
    if not data:
        return None

    rates = data.get("rates", {})
    rate = rates.get(to_curr)

    if not rate:
        print("Invalid target currency:", to_curr)
        return None

    return amount * rate

# -----------------------------
# 3. CLI (Command Line Interface)
# -----------------------------
parser = argparse.ArgumentParser(description="Currency API Client")

parser.add_argument("command", choices=["rates", "convert"], help="Choose an action")

parser.add_argument("--from", dest="from_curr", help="Base currency (example: USD)")
parser.add_argument("--to", dest="to_curr", help="Target currency (example: INR)")
parser.add_argument("--amount", type=float, help="Amount to convert")

args = parser.parse_args()

# -----------------------------
# 4. Handle Commands                                              
# -----------------------------
if args.command == "rates":
    if not args.from_curr:
        print("Please provide --from currency. Example: USD")
    else:
        print(get_rates(args.from_curr))

elif args.command == "convert":
    if not args.from_curr or not args.to_curr or not args.amount:
        print("Please provide --from, --to, and --amount")
        print("Example: python client.py convert --from USD --to INR --amount 10")
    else:
        result = convert(args.amount, args.from_curr, args.to_curr)
        if result:
            print(f"{args.amount} {args.from_curr} = {result} {args.to_curr}")