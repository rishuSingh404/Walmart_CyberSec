import hashlib
import time
import random
import json

def simulate_tx(user_id, action_type, risk_score=None):
timestamp = int(time.time())
session_id = f"session_{random.randint(1000,9999)}"
tx_payload = f"{user_id}-{action_type}-{session_id}-{timestamp}"
tx_hash = hashlib.sha256(tx_payload.encode()).hexdigest()
block_number = random.randint(5000, 9999)

tx = {
    "user_id": user_id,
    "action": action_type,
    "tx_hash": f"0x{tx_hash[:64]}",
    "block_number": block_number,
    "risk_score": risk_score,
    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
}

print("\n📦 Blockchain Log Entry")
print(json.dumps(tx, indent=4))
print("✅ Action written to chain ✅\n")
return tx

simulate_tx("user_01", "login_success")
simulate_tx("user_02", "otp_failed", risk_score="high")
simulate_tx("user_03", "fraud_detected", risk_score="high")
simulate_tx("user_04", "checkout_verified")
