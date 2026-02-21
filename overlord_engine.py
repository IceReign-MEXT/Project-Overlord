# overlord_engine.py - Project Overlord, The 24/7 Hunter-Killer AI

import os
import time
from dotenv import load_dotenv
from web3 import Web3, Account
from eth_account.signers.local import LocalAccount
import json
import requests

# --- Load Configuration ---
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
HOT_WALLET_PRIVATE_KEY = os.getenv("HOT_WALLET_PRIVATE_KEY")
FORTRESS_WALLET_ADDRESS = os.getenv("FORTRESS_WALLET_ADDRESS")
PHOENIX_BOT_TOKEN = os.getenv("PHOENIX_BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
THIEF_ADDRESS = os.getenv("THIEF_ADDRESS")

# --- Constants & Colors ---
USDT_ADDRESS = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
USDT_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"type":"function"}]')
RED, GREEN, YELLOW, BLUE, NC = '\033[0;31m', '\033[0;32m', '\033[1;33m', '\033[0;94m', '\033[0m'

# --- Alerter Function ---
def send_alert(message):
    try:
        requests.post(f"https://api.telegram.org/bot{PHOENIX_BOT_TOKEN}/sendMessage", json={"chat_id": ADMIN_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception: pass

def run_overlord():
    """The main 24/7 loop for the Overlord Engine."""
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        hot_wallet: LocalAccount = Account.from_key(HOT_WALLET_PRIVATE_KEY)
        usdt_contract = w3.eth.contract(address=USDT_ADDRESS, abi=USDT_ABI)
        send_alert("✅ **Overlord Engine ONLINE.** Eternal vigilance has begun.")
        print(f"{GREEN}OVERLORD ENGINE ONLINE. GUARDING: {YELLOW}{hot_wallet.address}{NC}")
    except Exception as e:
        print(f"{RED}CRITICAL BOOT ERROR: {e}. Check .env file.{NC}")
        send_alert(f"❌ **Overlord Engine BOOT FAILED!**\nError: `{e}`. Check configuration.")
        return

    while True:
        try:
            eth_balance = w3.eth.get_balance(hot_wallet.address)
            usdt_balance = usdt_contract.functions.balanceOf(hot_wallet.address).call()
            gas_price = w3.eth.gas_price
            
            print(f"  {BLUE}STATUS ({time.strftime('%H:%M:%S')}):{NC} ETH: {w3.from_wei(eth_balance, 'ether'):.8f}, USDT: {usdt_balance / 10**6:.2f}")

            # --- OFFENSIVE LOGIC: USDT RESCUE ---
            if usdt_balance > 0:
                gas_estimate = 100000 # High gas limit for USDT transfer
                required_gas = gas_estimate * (gas_price * 3) # Aggressive 3x gas price
                
                # The "$3 up" logic
                if eth_balance >= required_gas and eth_balance > w3.to_wei(0.001, 'ether'): # Min ~$3 gas
                    send_alert(f"🎯 **Target Acquired!**\nDetected `{usdt_balance / 10**6:.2f} USDT` and sufficient gas. LAUNCHING SWEEP.")
                    nonce = w3.eth.get_transaction_count(hot_wallet.address)
                    tx = usdt_contract.functions.transfer(FORTRESS_WALLET_ADDRESS, usdt_balance).build_transaction({
                        'from': hot_wallet.address, 'nonce': nonce, 'gas': gas_estimate, 'gasPrice': int(gas_price * 3), 'chainId': 1,
                    })
                    signed_tx = hot_wallet.sign_transaction(tx)
                    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    send_alert(f"🚀 **USDT SWEEP SENT!** HASH: `{tx_hash.hex()}`. Awaiting confirmation...")
                    
                    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180)
                    if receipt['status'] == 1:
                        send_alert(f"✅ **MISSION SUCCESSFUL!**\n`{usdt_balance / 10**6:.2f} USDT` secured in the Fortress.")
                        eth_balance = w3.eth.get_balance(hot_wallet.address) # Get updated balance

            # --- DEFENSIVE LOGIC: SWEEP ALL REMAINING ETH ---
            eth_tx_cost = 21000 * (gas_price * 1.2) # Normal speed
            if eth_balance > eth_tx_cost:
                amount_to_sweep = eth_balance - eth_tx_cost
                send_alert(f"🧹 **Gas Sweep:** Securing `{w3.from_wei(amount_to_sweep, 'ether'):.8f} ETH` in the Fortress.")
                nonce = w3.eth.get_transaction_count(hot_wallet.address)
                tx = {'nonce': nonce, 'to': FORTRESS_WALLET_ADDRESS, 'value': int(amount_to_sweep), 'gas': 21000, 'gasPrice': int(gas_price * 1.2), 'chainId': 1}
                signed_tx = hot_wallet.sign_transaction(tx)
                w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            # --- COUNTER-OFFENSIVE LOGIC: "REVOKE ENERGY" ---
            if THIEF_ADDRESS and eth_balance > eth_tx_cost:
                send_alert(f"⚡️ **Counter-Offensive:** Frustrating enemy bot at `{THIEF_ADDRESS[:10]}...`")
                nonce = w3.eth.get_transaction_count(hot_wallet.address)
                tx = {'nonce': nonce, 'to': THIEF_ADDRESS, 'value': 0, 'gas': 21000, 'gasPrice': w3.eth.gas_price, 'data': b'AZ_ICEGODS_IS_WATCHING_YOU'.hex(), 'chainId': 1}
                signed_tx = hot_wallet.sign_transaction(tx)
                w3.eth.send_raw_transaction(signed_tx.rawTransaction)

            time.sleep(12) # Hyper-fast loop, checks every 12 seconds
            
        except KeyboardInterrupt: print("\nOverlord shutting down."); break
        except Exception as e: send_alert(f"⚠️ **Engine Alert!** `{e}`."); time.sleep(12)

if __name__ == "__main__": run_overlord()
