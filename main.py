import requests 
import os 
import colorama 
import console.utils 
from colorama import Fore 
from console.utils import set_title 
import yaml
import time
import json
import sys
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
os.system('cls')
User = str(input(Fore.CYAN+"Username: ")
os.system('cls')
class LutionCounter:
    Purchased = 0
    OutofStock = 0

def getuser(api_key, User):
    
    userapi = f"http://api.lution.ee/auth/me?apikey={api_key}"
    response = requests.get(userapi)
    json_data = response.json()
    set_title(f"MR Lution | User: {User} | Checking Userinfo | Email: {json_data['email']} | Balance: {json_data['balance']}")
    print(Fore.GREEN+"Email: " + json_data['email'])
    print(Fore.GREEN+"Balance: " + str(json_data['balance']))
    input("")
    starting()

def purchasemail(api_key, User):
    mailcode = "HOTMAIL"
    purchase_results = []
    

    def signal_handler(sig, frame):
        print("\nInterrupted! Saving current progress...")
        save_progress()
        sys.exit(0)

    def save_progress():
        with open('progress.json', 'w') as f:
            json.dump(purchase_results, f, indent=2)
        print("Progress saved.")

    def purchase_email():
        url = f"http://api.lution.ee/mail/buy?mailcode={mailcode}&quantity=1&apikey={api_key}"
        while True:
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json().get('Data', {}).get('Emails', [])
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    LutionCounter.OutofStock +=1
                    time.sleep(2)
                    continue
                print(f"HTTP error: {e.response.status_code} - {e.response.reason}")
                return []
            except Exception as e:
                print(f"Error purchasing emails: {e}")
                return []

    def save_to_files(accounts):
        LutionCounter.Purchased +=1
        with open('accs.json', 'w') as json_file:
            json.dump(accounts, json_file, indent=4)
        with open('accs.txt', 'w') as text_file:
            for account in accounts:
                text_file.write(f"{account['Email']}:{account['Password']}:{account['AccessToken']}\n")
        set_title(f"MR Lution | User: {User} | Status: Purchasing | Purchased: {LutionCounter.Purchased} | OutofStock: {LutionCounter.OutofStock}")
        print(Fore.GREEN+f"PURCHASED: {account['Email']}:{account['Password']}")
        
    def purchase_task():
        purchased_accounts = purchase_email()
        if purchased_accounts:
            purchase_results.extend(purchased_accounts)
            save_to_files(purchase_results)

    def main():
        signal.signal(signal.SIGINT, signal_handler)
        total_accounts = int(input(Fore.YELLOW+"[!] Amount of Email: "))
        thread_count = int(input(Fore.LIGHTCYAN_EX+"[!] Threads: "))
        print("")
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            futures = [executor.submit(purchase_task) for _ in range(total_accounts)]
            for future in as_completed(futures):
                future.result()

    main()
        
def recharge_lution(api_key, User):
    amount = int(input("Amount: "))
    set_title(f"MR Lution | User: {User} | Status: Recharging | Amount: ${amount} | User: {User}")
    rechargeapi = f"http://api.lution.ee/payments/?apikey={api_key}"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer http",
        "Content-Type": "application/json"
    }
    data = {
        "amountUSD": amount,
        "network": "LTC",
        "token": "LTC",
        "promo": ""
    }
    
    response = requests.post(rechargeapi, headers=headers, json=data)
    
    if response.ok:
        response_data = response.json()
        print(Fore.YELLOW+"[!] Information")
        ltc_amount = response_data.get("amount", 0)
        usd_amount = response_data.get("amountUSD", 0)
        address = response_data.get("address", "")
        print(Fore.GREEN+f"LTC Amount: {ltc_amount}\nUSD Amount: {usd_amount}\nAddress: {address}\n")
    else:
        print(f"Error: {response.status_code} - {response.text}")
    input("")
    starting()
def quill(api_key, User):
    ins = input(Fore.YELLOW+"[?] Option: ")
    if ins == "1":
        stert()
        getuser(api_key, User)
    elif ins == "2":
        stert()
        purchasemail(api_key, User)
    elif ins == "3":
        stert()
        recharge_lution(api_key, User)
    else:
        stert()
        time.sleep(3)
        print(Fore.RED+"Quitting in 3 seconds .........")
        quit()
def stert():
    os.system('cls')
    set_title(f"MR Lution | User: {User} | Status: Selecting")
    text ="""
    ███▄ ▄███▓ ██▀███      ██▓     █    ██ ▄▄▄█████▓ ██▓ ▒█████   ███▄    █ 
    ▓██▒▀█▀ ██▒▓██ ▒ ██▒   ▓██▒     ██  ▓██▒▓  ██▒ ▓▒▓██▒▒██▒  ██▒ ██ ▀█   █ 
    ▓██    ▓██░▓██ ░▄█ ▒   ▒██░    ▓██  ▒██░▒ ▓██░ ▒░▒██▒▒██░  ██▒▓██  ▀█ ██▒
    ▒██    ▒██ ▒██▀▀█▄     ▒██░    ▓▓█  ░██░░ ▓██▓ ░ ░██░▒██   ██░▓██▒  ▐▌██▒
    ▒██▒   ░██▒░██▓ ▒██▒   ░██████▒▒▒█████▓   ▒██▒ ░ ░██░░ ████▓▒░▒██░   ▓██░
    ░ ▒░   ░  ░░ ▒▓ ░▒▓░   ░ ▒░▓  ░░▒▓▒ ▒ ▒   ▒ ░░   ░▓  ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
    ░  ░      ░  ░▒ ░ ▒░   ░ ░ ▒  ░░░▒░ ░ ░     ░     ▒ ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
    ░      ░     ░░   ░      ░ ░    ░░░ ░ ░   ░       ▒ ░░ ░ ░ ▒     ░   ░ ░ 
    ░      ░            ░  ░   ░               ░      ░ ░           ░ 
                                                                                """
    print(Fore.RED+text)
    print("")
    print("")
    print("")
    print("")
    print("")
api_key = "API"

def starting():
    stert()
    print(Fore.CYAN+"[!] Options: ")
    print("")
    print(Fore.GREEN+"[1] User Information")
    print(Fore.GREEN+"[2] Purchase Email")
    print(Fore.GREEN+"[3] Recharge Lution")
    print(Fore.GREEN+"[4] Exit")
    print("")
    quill(api_key, User)
if __name__ == "__main__":
    starting()
