from hashlib import sha256
import time
import random
import json
from colorama import Fore, Style, init

init(autoreset=True)

def simulate_flagged_user():
user_id = "user_fraud_99"
action_type = "otp_failed"
session_id = f"session_{random.randint(1000,9999)}"
timestamp = int(time.time())
payload = f"{user_id}-{action_type}-{session_id}-{timestamp}"
tx_hash = sha256(payload.encode()).hexdigest()
block_number = random.randint(9000, 9999)

log = {
    "user_id": user_id,
    "action": action_type,
    "tx_hash": f"0x{tx_hash}",
    "block_number": block_number,
    "risk_score": "high",
    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
}

print(Fore.RED + "\n🚨 BLOCKCHAIN ALERT: High-Risk User Flagged 🚨" + Style.RESET_ALL)
print(json.dumps(log, indent=4))
print(Fore.RED + "✅ Fraud session hash committed to chain\n")
simulate_flagged_user()
